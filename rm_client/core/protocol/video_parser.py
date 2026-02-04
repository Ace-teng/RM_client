"""
图传 UDP 解析 — 协议层：8 字节包头解析、分片重组，可选 HEVC 解码后写入 DataCenter（§4.2）。

包头：帧编号 2B、当前帧内分片序号 2B、当前帧总字节数 4B（大端），后跟 HEVC 码流。
"""
import logging
import struct
from typing import TYPE_CHECKING, Dict, Optional

if TYPE_CHECKING:
    from rm_client.core.model.datacenter import DataCenter

logger = logging.getLogger(__name__)

HEADER_LEN = 8
_MAX_FRAME_SIZE = 10 * 1024 * 1024
_reassembly_buf: Dict[int, Dict[int, bytes]] = {}
_hevc_codec: Optional[object] = None


def _decode_hevc_to_qimage(hevc_bytes: bytes):
    """若可用 PyAV 则解码 HEVC 为 QImage，否则返回 None。先试容器方式，再试 parse/decode。"""
    global _hevc_codec
    try:
        import io
        import av
        from qtpy.QtGui import QImage
    except ImportError:
        return None
    try:
        # 方式1：当作裸流用容器打开（兼容编码器输出的 Annex B 等）
        buf = io.BytesIO(hevc_bytes)
        try:
            container = av.open(buf, format="hevc")
            for frame in container.decode(video=0):
                arr = frame.to_ndarray(format="rgb24")
                h, w = arr.shape[0], arr.shape[1]
                b = arr.tobytes() if hasattr(arr, "tobytes") else arr.data.tobytes()
                return QImage(b, w, h, w * 3, QImage.Format_RGB888).copy()
        except Exception:
            pass
        # 方式2：CodecContext.parse + decode（复用解码器保留 SPS/PPS）
        if _hevc_codec is None:
            _hevc_codec = av.CodecContext.create("hevc", "r")
        codec = _hevc_codec
        packets = codec.parse(hevc_bytes)
        for pkt in packets:
            for frame in codec.decode(pkt):
                if frame is not None:
                    arr = frame.to_ndarray(format="rgb24")
                    h, w = arr.shape[0], arr.shape[1]
                    b = arr.tobytes() if hasattr(arr, "tobytes") else arr.data.tobytes()
                    return QImage(b, w, h, w * 3, QImage.Format_RGB888).copy()
    except Exception as e:
        logger.debug("HEVC 解码失败: %s", e)
    return None


def on_video_packet(raw: bytes, dc: "DataCenter") -> None:
    """
    通信层回调：解析 8 字节包头，按帧重组；完整帧可选解码后写入 dc.video_frame。
    """
    if len(raw) < HEADER_LEN:
        return
    frame_id, fragment_id, frame_size = struct.unpack(">HHI", raw[:HEADER_LEN])
    payload = raw[HEADER_LEN:]
    if frame_size <= 0 or frame_size > _MAX_FRAME_SIZE:
        return
    if frame_id not in _reassembly_buf:
        _reassembly_buf[frame_id] = {}
    _reassembly_buf[frame_id][fragment_id] = payload
    total = sum(len(p) for p in _reassembly_buf[frame_id].values())
    if total < frame_size:
        return
    parts = [_reassembly_buf[frame_id][i] for i in sorted(_reassembly_buf[frame_id].keys())]
    assembled = b"".join(parts)[:frame_size]
    del _reassembly_buf[frame_id]
    img = _decode_hevc_to_qimage(assembled)
    if img is not None:
        dc.video_frame = img

"""
向本机 3334 端口发送带 8 字节包头的 HEVC 测试流，用于验证客户端图传显示。

先启动客户端：python -m rm_client.main
再在另一终端执行：python scripts/send_test_video_udp.py

依赖：pip install av
"""
import socket
import struct
import sys
import time

try:
    import av
    from fractions import Fraction
    import numpy as np
except ImportError:
    print("请先安装: pip install av")
    sys.exit(1)


def main() -> int:
    host = "127.0.0.1"
    port = 3334
    fps = 10
    duration_sec = 15

    # 用 PyAV 编码几帧 HEVC（简单彩色渐变图）；每帧关键帧便于解码
    width, height = 640, 360
    codec = av.CodecContext.create("hevc", "w")
    codec.width = width
    codec.height = height
    codec.pix_fmt = "yuv420p"
    codec.time_base = Fraction(1, fps)
    try:
        codec.gop_size = 1
    except Exception:
        pass
    try:
        codec.options = {"tune": "zerolatency", "x265-params": "keyint=1"}
    except Exception:
        pass

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    frame_count = 0
    t0 = time.monotonic()
    print("向 %s:%s 发送 HEVC 测试流（约 %s 秒，%s fps）…" % (host, port, duration_sec, fps))

    while (time.monotonic() - t0) < duration_sec:
        # 生成一帧 YUV420P：Y (H*W) + U (H/2*W/2) + V (H/2*W/2)
        y = np.full((height, width), (frame_count * 3) % 256, dtype=np.uint8)
        u = np.full((height // 2, width // 2), 128, dtype=np.uint8)
        v = np.full((height // 2, width // 2), 128, dtype=np.uint8)
        # 拼成连续内存：yuv420p 为 Y 整平面 + U 整平面 + V 整平面
        yuv = np.concatenate([y.ravel(), u.ravel(), v.ravel()]).reshape((height * 3 // 2, width))
        frame = av.VideoFrame.from_ndarray(yuv, format="yuv420p")
        frame.pts = frame_count

        for pkt in codec.encode(frame):
            hevc_bytes = pkt.to_bytes() if hasattr(pkt, "to_bytes") else bytes(pkt)
            if not hevc_bytes:
                continue
            # 8 字节包头：frame_id(2) fragment_id(2) frame_size(4) 大端
            header = struct.pack(">HHI", frame_count & 0xFFFF, 0, len(hevc_bytes))
            sock.sendto(header + hevc_bytes, (host, port))
        frame_count += 1
        time.sleep(1.0 / fps)

    sock.close()
    print("已发送 %s 帧，结束。" % frame_count)
    return 0


if __name__ == "__main__":
    sys.exit(main())

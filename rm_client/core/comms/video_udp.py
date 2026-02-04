"""
图传 UDP 接收 — 通信层，仅收包并回调原始字节（§4.1）。

端口 3334；不解析 8 字节包头与 HEVC，由 protocol 层处理。
"""
import logging
import socket
import threading
from typing import Callable, Optional

logger = logging.getLogger(__name__)


class VideoUDPReceiver:
    """图传 UDP 接收：绑定端口，收包后回调 on_packet_cb(raw_bytes)。"""

    def __init__(
        self,
        port: int,
        on_packet_cb: Optional[Callable[[bytes], None]] = None,
    ) -> None:
        self._port = port
        self._on_packet_cb = on_packet_cb
        self._sock: Optional[socket.socket] = None
        self._thread: Optional[threading.Thread] = None
        self._stop = threading.Event()

    def start(self) -> None:
        if self._sock is not None:
            return
        try:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._sock.bind(("0.0.0.0", self._port))
        except OSError as e:
            logger.warning("图传 UDP 绑定 %s 失败: %s", self._port, e)
            return
        self._stop.clear()
        self._thread = threading.Thread(target=self._recv_loop, daemon=True)
        self._thread.start()
        logger.info("图传 UDP 已监听端口 %s", self._port)

    def _recv_loop(self) -> None:
        while not self._stop.is_set() and self._sock:
            try:
                data, _ = self._sock.recvfrom(65535)
                if data and self._on_packet_cb:
                    self._on_packet_cb(data)
            except (OSError, AttributeError):
                if not self._stop.is_set():
                    logger.debug("图传 UDP recv 异常", exc_info=True)
                break

    def stop(self) -> None:
        self._stop.set()
        if self._sock:
            try:
                self._sock.close()
            except OSError:
                pass
            self._sock = None
        if self._thread:
            self._thread.join(timeout=2.0)
            self._thread = None

"""
RoboMaster 自定义客户端 — 程序入口。

Phase 1：启动 QtPy 主窗口、创建 DataCenter。
Phase 2：MQTT 连接、订阅、接收数据日志打印。
数据流：comms → protocol → DataCenter → service → ui（见总文档 §6）。

本地测试：加 --local 即连本机 MQTT(127.0.0.1:1883)，与 run_local_test.bat 行为一致。
"""
import logging
import sys

from qtpy.QtWidgets import QApplication

from rm_client.config.default import (
    REFEREE_MQTT_CONNECT_TIMEOUT,
    REFEREE_MQTT_HOST,
    REFEREE_MQTT_PORT,
    REFEREE_MQTT_TOPICS,
    VIDEO_UDP_PORT,
)
from rm_client.core.comms.referee_mqtt import RefereeMQTTClient
from rm_client.core.comms.video_udp import VideoUDPReceiver
from rm_client.core.model.datacenter import DataCenter
from rm_client.core.protocol.referee_parser import parse_referee_message
from rm_client.core.protocol.video_parser import on_video_packet
from rm_client.ui.main_window import MainWindow

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)


def main() -> int:
    """创建应用、DataCenter、主窗口、MQTT 客户端并启动事件循环。"""
    # --local：与本机 MQTT 连接(127.0.0.1:1883)，与 run_local_test.bat 一致；从 argv 移除避免 Qt 报错
    if "--local" in sys.argv:
        sys.argv = [a for a in sys.argv if a != "--local"]
        import os
        os.environ["REFEREE_MQTT_HOST"] = "127.0.0.1"
        os.environ["REFEREE_MQTT_PORT"] = "1883"
        # 重新从环境变量读取（config 已 import，需覆盖后再次取值）
        _mqtt_host = os.environ.get("REFEREE_MQTT_HOST", "192.168.12.1")
        _mqtt_port = int(os.environ.get("REFEREE_MQTT_PORT", "3333"))
    else:
        _mqtt_host = REFEREE_MQTT_HOST
        _mqtt_port = REFEREE_MQTT_PORT

    app = QApplication(sys.argv)
    app.setApplicationName("RoboMaster 自定义客户端")
    app.setApplicationDisplayName("RoboMaster 自定义客户端")

    # 单例数据中心（R-ARCH-002 唯一数据源）
    dc = DataCenter()

    window = MainWindow()
    window.show()

    # Phase 2：赛事 MQTT 连接与订阅；Phase 3：comms → protocol → DataCenter
    def on_mqtt_connect() -> None:
        window.set_status_message("就绪 | DataCenter 已创建 | MQTT 已连接")

    def on_mqtt_disconnect() -> None:
        window.set_status_message("就绪 | DataCenter 已创建 | MQTT 未连接")

    def on_mqtt_message(topic: str, payload: bytes) -> None:
        # 通信层只传 (topic, payload)；协议层解析并写入 DataCenter（R-ARCH-003）
        parse_referee_message(topic, payload, dc)
        logging.getLogger("rm_client").debug("MQTT [%s] %d bytes -> protocol", topic, len(payload))

    mqtt_client = RefereeMQTTClient(
        _mqtt_host,
        _mqtt_port,
        REFEREE_MQTT_TOPICS,
        on_connect_cb=on_mqtt_connect,
        on_message_cb=on_mqtt_message,
        on_disconnect_cb=on_mqtt_disconnect,
    )
    window.set_status_message("就绪 | DataCenter 已创建 | MQTT 连接中…")
    mqtt_client.start(connect_timeout=REFEREE_MQTT_CONNECT_TIMEOUT)

    # Phase 4：图传 UDP 接收，协议层解析后写入 DataCenter.video_frame
    def on_video_udp(raw: bytes) -> None:
        on_video_packet(raw, dc)

    video_receiver = VideoUDPReceiver(VIDEO_UDP_PORT, on_packet_cb=on_video_udp)
    video_receiver.start()

    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())

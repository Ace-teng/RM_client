"""
RoboMaster 自定义客户端 — 程序入口。

Phase 1：启动 QtPy 主窗口、创建 DataCenter。
Phase 2：MQTT 连接、订阅、接收数据日志打印。
数据流：comms → protocol → DataCenter → service → ui（见总文档 §6）。

本地测试：加 --local 即连本机 MQTT(127.0.0.1:1883)。
"""
import logging
import time
import os
import sys

# 必须在 import config 之前处理 --local，否则 config 会读到错误的默认值
if "--local" in sys.argv:
    sys.argv = [a for a in sys.argv if a != "--local"]
    os.environ["REFEREE_MQTT_HOST"] = "127.0.0.1"
    os.environ["REFEREE_MQTT_PORT"] = "1883"

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
    _mqtt_host = REFEREE_MQTT_HOST
    _mqtt_port = REFEREE_MQTT_PORT

    app = QApplication(sys.argv)
    app.setApplicationName("RoboMaster 自定义客户端")
    app.setApplicationDisplayName("RoboMaster 自定义客户端")

    # 单例数据中心（R-ARCH-002 唯一数据源）
    dc = DataCenter()

    # Phase 5：注入占位 robot_states，便于态势图展示；协议接入后由 protocol 覆盖
    from rm_client.core.service.demo_data import inject_demo_robot_states
    inject_demo_robot_states()

    window_ref = [None]

    def _update_link_status(**kw) -> None:
        ls = dc.link_status
        ls.update(kw)
        dc.link_status = ls

    def on_mqtt_connect() -> None:
        _update_link_status(mqtt_connected=True)
        if window_ref[0]:
            window_ref[0].set_status_message("就绪 | DataCenter 已创建 | MQTT 已连接")

    def on_mqtt_disconnect() -> None:
        _update_link_status(mqtt_connected=False)
        if window_ref[0]:
            window_ref[0].set_status_message("就绪 | DataCenter 已创建 | MQTT 未连接")

    def on_mqtt_message(topic: str, payload: bytes) -> None:
        _update_link_status(mqtt_last_update=time.time())
        parse_referee_message(topic, payload, dc)
        logging.getLogger("rm_client").debug("MQTT [%s] %d bytes -> protocol", topic, len(payload))

    logging.getLogger("rm_client").info("MQTT 目标: %s:%s", _mqtt_host, _mqtt_port)
    mqtt_client = RefereeMQTTClient(
        _mqtt_host,
        _mqtt_port,
        REFEREE_MQTT_TOPICS,
        on_connect_cb=on_mqtt_connect,
        on_message_cb=on_mqtt_message,
        on_disconnect_cb=on_mqtt_disconnect,
    )
    mqtt_client.start(connect_timeout=REFEREE_MQTT_CONNECT_TIMEOUT)

    # Phase 6：赛事指令发送（需在 mqtt_client 创建后，MainWindow 创建前）
    from rm_client.core.service.command_sender import CommandSender
    command_sender = CommandSender(publish_fn=mqtt_client.publish)

    window = MainWindow(command_sender=command_sender)
    window_ref[0] = window
    # 若 MQTT 在窗口创建前已连接成功，on_connect 时 window 未就绪会漏更新，此处补检
    if mqtt_client.is_connected:
        _update_link_status(mqtt_connected=True)
        window.set_status_message("就绪 | DataCenter 已创建 | MQTT 已连接")
    else:
        window.set_status_message("就绪 | DataCenter 已创建 | MQTT 连接中…")

    # Phase 7：加载插件
    from rm_client.plugins.interface import PluginContext
    from rm_client.plugins.loader import load_plugins
    plugin_ctx = PluginContext(dc=dc, main_window=window, command_sender=command_sender)
    load_plugins(plugin_ctx)

    window.show()

    # Phase 4：图传 UDP 接收，协议层解析后写入 DataCenter.video_frame
    def on_video_udp(raw: bytes) -> None:
        _update_link_status(video_last_update=time.time())
        on_video_packet(raw, dc)

    video_receiver = VideoUDPReceiver(VIDEO_UDP_PORT, on_packet_cb=on_video_udp)
    video_receiver.start()

    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())

"""
赛事引擎 MQTT 客户端 — 通信层，仅收发原始字节流（§4.1）。

职责：连接 192.168.12.1:3333、订阅/发布、输出 (topic, payload) 原始字节。
禁止：协议解析、状态存储、UI 调用。Phase 3 由 protocol 层解析 payload。
"""
import logging
from typing import Callable, List, Optional

import paho.mqtt.client as mqtt

logger = logging.getLogger(__name__)


class RefereeMQTTClient:
    """
    赛事引擎 MQTT 客户端。连接、订阅、收包时仅输出原始字节与 topic，不解析内容。
    """

    def __init__(
        self,
        host: str,
        port: int,
        topics: List[str],
        on_connect_cb: Optional[Callable[[], None]] = None,
        on_message_cb: Optional[Callable[[str, bytes], None]] = None,
        on_disconnect_cb: Optional[Callable[[], None]] = None,
    ) -> None:
        self._host = host
        self._port = port
        self._topics = list(topics)
        self._on_connect_cb = on_connect_cb
        self._on_message_cb = on_message_cb
        self._on_disconnect_cb = on_disconnect_cb
        self._client: Optional[mqtt.Client] = None
        self._connected = False

    def _on_connect(self, client: mqtt.Client, userdata: None, flags: dict, rc: int) -> None:
        if rc != 0:
            logger.warning("MQTT 连接失败 rc=%s", rc)
            return
        self._connected = True
        for t in self._topics:
            client.subscribe(t)
            logger.info("MQTT 已订阅: %s", t)
        if self._on_connect_cb:
            self._on_connect_cb()

    def _on_disconnect(self, client: mqtt.Client, userdata: None, rc: int) -> None:
        self._connected = False
        logger.info("MQTT 已断开 rc=%s", rc)
        if self._on_disconnect_cb:
            self._on_disconnect_cb()

    def _on_message(self, client: mqtt.Client, userdata: None, msg: mqtt.MQTTMessage) -> None:
        topic = msg.topic
        payload = msg.payload
        logger.info("MQTT 收到 [%s] len=%d bytes", topic, len(payload))
        if self._on_message_cb:
            self._on_message_cb(topic, payload)

    def start(self, connect_timeout: int = 10) -> None:
        """连接并启动网络循环（非阻塞，适合与 Qt 共用）。"""
        self._client = mqtt.Client(client_id="rm_client", protocol=mqtt.MQTTv311)
        self._client.on_connect = self._on_connect
        self._client.on_disconnect = self._on_disconnect
        self._client.on_message = self._on_message
        try:
            self._client.connect(self._host, self._port, keepalive=60)
        except Exception as e:
            logger.warning("MQTT connect(%s:%s) 失败: %s", self._host, self._port, e)
            return
        self._client.loop_start()

    def stop(self) -> None:
        """断开并停止网络循环。"""
        if self._client:
            self._client.loop_stop()
            self._client.disconnect()
            self._client = None
        self._connected = False

    @property
    def is_connected(self) -> bool:
        return self._connected

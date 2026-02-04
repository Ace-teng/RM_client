"""
赛事指令发送 — 业务层，调用 protocol 序列化 + comms 发布。

UI 不直接访问 comms，通过本模块发送指令。
"""
import logging
from typing import Callable, Optional

from rm_client.core.protocol.command_serializer import (
    serialize_air_support,
    serialize_ammo_exchange,
    serialize_performance_mode,
)

logger = logging.getLogger(__name__)


class CommandSender:
    """赛事指令发送：序列化后经 publish_fn 发布到 MQTT。"""

    def __init__(self, publish_fn: Callable[[str, bytes], bool]) -> None:
        self._publish = publish_fn

    def send_performance_mode(self, mode_id: int) -> bool:
        """性能体系选择。"""
        topic, payload = serialize_performance_mode(mode_id)
        ok = self._publish(topic, payload)
        if ok:
            logger.info("已发送性能体系 mode_id=%s", mode_id)
        return ok

    def send_ammo_exchange(self) -> bool:
        """兑换发弹量。"""
        topic, payload = serialize_ammo_exchange()
        ok = self._publish(topic, payload)
        if ok:
            logger.info("已发送兑换发弹量")
        return ok

    def send_air_support(self) -> bool:
        """空中支援。"""
        topic, payload = serialize_air_support()
        ok = self._publish(topic, payload)
        if ok:
            logger.info("已发送空中支援")
        return ok

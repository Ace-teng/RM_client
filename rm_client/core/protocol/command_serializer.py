"""
赛事指令序列化 — 协议层，将高层命令转为 (topic, payload) 供 comms 发布。

占位实现：返回简单 payload；正式开发时以《RoboMaster 通信协议》为准替换。
"""
from rm_client.config.default import (
    REFEREE_TOPIC_CMD_AMMO,
    REFEREE_TOPIC_CMD_AIR_SUPPORT,
    REFEREE_TOPIC_CMD_PERFORMANCE,
)


def serialize_performance_mode(mode_id: int) -> tuple[str, bytes]:
    """性能体系选择。mode_id: 1/2/3 等。占位：单字节。"""
    return (REFEREE_TOPIC_CMD_PERFORMANCE, bytes([min(255, max(0, mode_id))]))


def serialize_ammo_exchange() -> tuple[str, bytes]:
    """兑换发弹量。占位：空 payload。"""
    return (REFEREE_TOPIC_CMD_AMMO, b"\x00")


def serialize_air_support() -> tuple[str, bytes]:
    """空中支援。占位：空 payload。"""
    return (REFEREE_TOPIC_CMD_AIR_SUPPORT, b"\x00")

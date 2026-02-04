"""
赛事 MQTT 协议解析 — 协议层，仅做反序列化与写入 DataCenter（§4.2）。

职责：接收 (topic, payload)，按 Topic 选择消息类型、Protobuf 反序列化，写入 DataCenter。
禁止：直接访问 comms、直接操作 UI。数据流 comms → protocol → DataCenter（R-ARCH-003）。
"""
import logging
from typing import TYPE_CHECKING

from rm_client.config.default import REFEREE_TOPIC_GAME_STATUS
from rm_client.core.protocol.generated.referee_pb2 import GameStatus

if TYPE_CHECKING:
    from rm_client.core.model.datacenter import DataCenter

logger = logging.getLogger(__name__)


def _topic_matches_game_status(topic: str) -> bool:
    t = topic.strip().rstrip("/")
    return t == REFEREE_TOPIC_GAME_STATUS or t.endswith("/" + REFEREE_TOPIC_GAME_STATUS)


def parse_referee_message(topic: str, payload: bytes, dc: "DataCenter") -> None:
    """
    根据 topic 解析 payload 并写入 DataCenter。
    当前仅支持 REFEREE_TOPIC_GAME_STATUS → GameStatus → dc.game_state。
    """
    if not payload:
        return
    if _topic_matches_game_status(topic):
        try:
            msg = GameStatus()
            msg.MergeFromString(payload)
            dc.game_state = msg
            logger.debug(
                "解析 GameStatus: game_phase=%s remaining_time_sec=%s",
                msg.game_phase,
                msg.remaining_time_sec,
            )
        except Exception as e:
            logger.warning("解析 GameStatus 失败 [%s] len=%d: %s", topic, len(payload), e)

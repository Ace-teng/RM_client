"""
战术分析服务 — 基于 DataCenter 数据计算操作建议，写入 dc.tactical_advice。

仅使用官方协议数据。逻辑为占位实现，接入真实协议后按字段调整。
见 docs/战术分析功能设计.md。配置来自 config.default。
"""
from dataclasses import dataclass
from typing import Any, Optional

from rm_client.config.default import (
    TACTICAL_BUYBACK_ECONOMY_THRESHOLD,
    TACTICAL_HP_DIFF_THRESHOLD,
    TACTICAL_MY_TEAM,
)
from rm_client.core.model.datacenter import DataCenter


@dataclass
class TacticalAdvice:
    hp_suggestion: Optional[str] = None  # "追击" | "撤退" | "谨慎"
    hp_diff: Optional[int] = None       # 我方 - 对方 总血量差
    hp_ours: int = 0
    hp_enemy: int = 0
    enemy_behind: bool = False
    economy_hint: str = ""
    buyback_alert: bool = False


def update_tactical_advice(dc: DataCenter) -> None:
    """从 DataCenter 读取数据，计算建议并写回 dc.tactical_advice。"""
    advice = TacticalAdvice()
    states = dc.robot_states

    # 按阵营汇总血量
    ours, enemy = 0, 0
    for rid, info in states.items():
        if not isinstance(info, dict):
            continue
        hp = info.get("hp", 0) or 0
        team = (info.get("team") or "").lower()
        if team == TACTICAL_MY_TEAM:
            ours += int(hp)
        else:
            enemy += int(hp)

    advice.hp_ours = ours
    advice.hp_enemy = enemy
    advice.hp_diff = ours - enemy

    # 追击/撤退建议
    if advice.hp_diff is not None:
        if advice.hp_diff >= TACTICAL_HP_DIFF_THRESHOLD:
            advice.hp_suggestion = "追击"
        elif advice.hp_diff <= -TACTICAL_HP_DIFF_THRESHOLD:
            advice.hp_suggestion = "撤退"
        else:
            advice.hp_suggestion = "谨慎"

    # 经济与买活（占位：game_state 中若有 economy 等字段则解析）
    gs = dc.game_state
    if gs is not None:
        enemy_economy = _get_enemy_economy(gs)
        if enemy_economy is not None:
            if enemy_economy >= TACTICAL_BUYBACK_ECONOMY_THRESHOLD:
                advice.buyback_alert = True
                advice.economy_hint = "对方经济充足，可能买活"
            elif enemy_economy >= 500:
                advice.economy_hint = "对方可能频繁补弹"
            else:
                advice.economy_hint = "对方经济紧张"

    # 背后敌人：需位置与朝向，暂不实现
    advice.enemy_behind = False

    dc.tactical_advice = advice


def _get_enemy_economy(gs: Any) -> Optional[int]:
    """从 game_state 中解析对方经济（占位）。TACTICAL_MY_TEAM=blue 时取 red，否则取 blue。"""
    if gs is None:
        return None
    if TACTICAL_MY_TEAM == "blue":
        return getattr(gs, "red_economy", None) or getattr(gs, "enemy_economy", None)
    return getattr(gs, "blue_economy", None) or getattr(gs, "enemy_economy", None)

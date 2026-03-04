"""
Phase 5 占位数据 — 向 DataCenter 写入 demo robot_states，便于态势图展示。

操作手调研（§0.6、操作.md）：注入 operator_display_state 占位数据，供角色视图与 HUD 展示；
协议接入后由 protocol 层写入真实数据，本模块可停用或仅用于离线演示。
"""
from types import SimpleNamespace

from rm_client.core.model.datacenter import DataCenter
from rm_client.core.model.operator_state import OperatorDisplayState


def inject_demo_robot_states() -> None:
    """写入占位 robot_states，格式：{robot_id: {x, y, hp, team}}，x/y 为 0～1 归一化坐标。"""
    dc = DataCenter()
    dc.robot_states = {
        "red_1": {"x": 0.25, "y": 0.5, "hp": 600, "team": "red"},
        "red_2": {"x": 0.35, "y": 0.35, "hp": 600, "team": "red"},
        "blue_1": {"x": 0.75, "y": 0.5, "hp": 600, "team": "blue"},
        "blue_2": {"x": 0.65, "y": 0.65, "hp": 450, "team": "blue"},
    }
    # 占位 game_state 含 red_economy，用于战术分析买活预警演示（TACTICAL_MY_TEAM=blue 时读 red）
    if dc.game_state is None:
        dc.game_state = SimpleNamespace(red_economy=1100, blue_economy=800)


def inject_operator_display_state() -> None:
    """注入操作手调研展示用占位数据（可靠功能 + 兵种特殊）。协议接入后由 protocol 覆盖。"""
    dc = DataCenter()
    state = OperatorDisplayState(
        aim_status="targeting",
        capacitor_pct=0.85,
        energy_limit=100.0,
        energy_current=72.0,
        hp_self=600,
        hp_enemy=480,
        ammo_count=45,
        ammo_limit=50,
        heat_current=120,
        heat_limit=360,
        buff_remaining_sec=25.0,
        buff_gain="攻击增益",
        enemy_respawn_sec=12.5,
        buyback_cost=800,
        vehicle_online=True,
        referee_online=True,
        level_self=2,
        level_enemy=2,
        performance_self=1,
        performance_enemy=2,
        sentry_target="3号",
        sentry_state="moving",
        sentry_goal="前哨站",
        outpost_hp_self=1200,
        outpost_hp_enemy=800,
        base_hp_self=5000,
        base_hp_enemy=4500,
        outpost_rebuild_count=1,
        base_armor_open=False,
        chassis_state="normal",
        hit_feedback=False,
        remote_control_ok=True,
        match_time_sec=328.0,
        infantry_pitch_deg=-5.2,
        infantry_yaw_deg=12.0,
        aim_target_distance=8.5,
        big_symbol_remain_sec=45.0,
        big_symbol_count=2,
        small_symbol_remain_sec=120.0,
        infantry_jump_target="二级台阶",
        infantry_state_machine="正常",
        fly_slope_line_on=True,
        aim_boxes_px=[(280, 140, 360, 220)],
    )
    dc.operator_display_state = state

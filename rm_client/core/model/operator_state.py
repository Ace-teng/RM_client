"""
操作手调研展示状态 — 占位数据结构（§0.6、操作.md）。

无协议时由 demo_data 注入；协议接入后由 protocol 层写入同名字段。
供 UI 图传绘制、侧边栏、悬浮窗按角色读取。
"""
from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class OperatorDisplayState:
    """操作手调研可靠功能 + 兵种特殊 — 占位字段，协议接入后由 protocol 覆盖。"""

    # ---------- 通用（操作.md 1.通用功能） ----------
    # 1. 自瞄状态：offline | notarget | targeting
    aim_status: str = "notarget"
    # 2. 超级电容（0~1）
    capacitor_pct: float = 1.0
    # 3. 官方总能量限制
    energy_limit: float = 100.0
    energy_current: float = 80.0
    # 4. 血量
    hp_self: int = 600
    hp_enemy: int = 600
    # 5. 发弹量
    ammo_count: int = 50
    ammo_limit: int = 50
    # 6. 热量
    heat_current: int = 0
    heat_limit: int = 360
    # 7. buff 剩余时间(s)、增益描述
    buff_remaining_sec: float = 0.0
    buff_gain: str = ""
    # 8. 对方复活时间(s)、买活金额
    enemy_respawn_sec: float = 0.0
    buyback_cost: int = 0
    # 9. 电机/裁判系统在线
    vehicle_online: bool = True
    referee_online: bool = True
    # 10. 己方基地扣血提示
    base_hit_self: bool = False
    # 11. 对方基地受击反馈
    base_hit_enemy: bool = False
    # 12. 等级与性能体系（己/敌）
    level_self: int = 1
    level_enemy: int = 1
    performance_self: int = 1
    performance_enemy: int = 1
    # 13. 哨兵：当前目标、选择状态、目的位置
    sentry_target: str = ""
    sentry_state: str = "idle"
    sentry_goal: str = ""
    # 14. 前哨站/基地血量、前哨站重建次数
    outpost_hp_self: int = 1500
    outpost_hp_enemy: int = 1500
    base_hp_self: int = 5000
    base_hp_enemy: int = 5000
    outpost_rebuild_count: int = 0
    # 15. 基地底装甲是否打开
    base_armor_open: bool = False
    # 16. 准心（自定义）：类型与偏移等，由 UI 配置
    crosshair_type: str = "cross"  # cross | T_shape
    # 17. 底盘姿态：unlocked | locked | low | high
    chassis_state: str = "normal"
    # 18. 受击提示
    hit_feedback: bool = False
    # 19. 遥控器状态（丢控与否）
    remote_control_ok: bool = True
    # 20. 比赛时间(s)
    match_time_sec: float = 0.0

    # ---------- 兵种特殊 ----------
    # 飞机被标记进度（己/敌 0~1）
    aircraft_marked_self: float = 0.0
    aircraft_marked_enemy: float = 0.0
    # 工程机械臂姿态
    engineer_arm_pose: str = ""
    # 步兵跳跃目标
    infantry_jump_target: str = ""
    # 步兵 pitch/yaw 角度(°)
    infantry_pitch_deg: float = 0.0
    infantry_yaw_deg: float = 0.0
    # 自瞄目标距离(m)
    aim_target_distance: float = 0.0
    # 飞镖发射提示
    dart_launch_self: bool = False
    dart_launch_enemy: bool = False
    # 大小符：剩余时间(s)、大符次数
    big_symbol_remain_sec: float = 0.0
    big_symbol_count: int = 0
    small_symbol_remain_sec: float = 0.0
    # 步兵状态机：翻倒自起、跳跃 on/off
    infantry_state_machine: str = ""
    # 飞坡对准线开关
    fly_slope_line_on: bool = True
    # 自瞄框（像素矩形，图传坐标系）：[(x1,y1,x2,y2), ...]
    aim_boxes_px: List[Tuple[float, float, float, float]] = field(default_factory=list)


# 角色枚举，用于视图切换
OPERATOR_ROLES = ("hero", "engineer", "infantry1", "infantry2", "gimbal")
OPERATOR_ROLE_LABELS = {
    "hero": "英雄",
    "engineer": "工程",
    "infantry1": "步兵1",
    "infantry2": "步兵2",
    "gimbal": "云台手",
}

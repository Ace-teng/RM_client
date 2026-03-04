# rm_client/ui/hud/hud_overlay.py
"""HUD 主叠加层 - 放置所有 HUD 组件。"""
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QWidget

from .health_bar import HealthBar
from .capacitor_bar import CapacitorBar
from .aim_status import AimStatus, AimState
from .match_timer import MatchTimer
from .crosshair import Crosshair
from .chassis_status import ChassisStatus, ChassisMode
from .sentry_info import SentryInfo
from .infantry.jump_target import JumpTarget
from .infantry.gimbal_angles import GimbalAngles


class HUDOverlay(QWidget):
    """HUD 主叠加层 - 放置所有 HUD 组件"""

    def __init__(self, robot_type: str = "infantry1", parent=None):
        super().__init__(parent)
        self.robot_type = robot_type
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self._setup_components()
        self._layout_components()

    def _setup_components(self) -> None:
        """创建所有组件"""
        self.ally_health = HealthBar(is_enemy=False, parent=self)
        self.enemy_health = HealthBar(is_enemy=True, parent=self)
        self.capacitor = CapacitorBar(parent=self)
        self.aim_status = AimStatus(parent=self)
        self.match_timer = MatchTimer(parent=self)
        self.crosshair = Crosshair(parent=self)
        self.chassis_status = ChassisStatus(parent=self)
        self.sentry_info = SentryInfo(parent=self)

        if self.robot_type in ("infantry1", "infantry2"):
            self.jump_target = JumpTarget(parent=self)
            self.gimbal_angles = GimbalAngles(parent=self)
            self.crosshair.set_ramp_guide(True)
        else:
            self.jump_target = None
            self.gimbal_angles = None

    def _layout_components(self) -> None:
        """修复重叠后的布局：左上/右上垂直排列，间距≥35px。"""
        w = self.width()
        h = self.height()
        cx = w // 2
        cy = h // 2
        if w < 100 or h < 100:
            return

        # ========== 左上角（垂直排列，不重叠） ==========
        y_offset = 20
        self.ally_health.move(20, y_offset)
        y_offset += 55  # 血量条高度 + 间距

        self.capacitor.move(20, y_offset)
        y_offset += 40  # 电容条高度 + 间距

        self.aim_status.move(20, y_offset)

        # ========== 顶部中央 ==========
        self.match_timer.move(cx - 50, 16)

        # ========== 右上角（垂直排列，不重叠） ==========
        y_offset_r = 20
        self.enemy_health.move(w - 200, y_offset_r)
        y_offset_r += 55

        if hasattr(self, "ammo_count") and self.ammo_count is not None:
            self.ammo_count.move(w - 120, y_offset_r)
            y_offset_r += 35

        y_offset_r += 35  # 与上一行间距
        if self.gimbal_angles is not None:
            self.gimbal_angles.move(w - 160, y_offset_r)

        # ========== 中央 ==========
        self.crosshair.move(cx - 40, cy - 40)

        # ========== 左下角 ==========
        if hasattr(self, "minimap") and self.minimap is not None:
            self.minimap.move(20, h - 180)

        self.chassis_status.move(200, h - 60)

        if self.jump_target is not None:
            self.jump_target.move(200, h - 100)

        # ========== 右侧边栏（中部） ==========
        self.sentry_info.move(w - 160, cy - 60)

        # ========== 右下角（调试面板，若存在） ==========
        if hasattr(self, "debug_panel") and self.debug_panel is not None:
            self.debug_panel.move(w - 220, h - 250)
        if hasattr(self, "plugin_panel") and self.plugin_panel is not None:
            self.plugin_panel.move(w - 220, h - 120)

        # ========== 底部中央 ==========
        if hasattr(self, "heat_limit") and self.heat_limit is not None:
            self.heat_limit.move(cx - 100, h - 50)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self._layout_components()

    # ===== 数据更新接口 =====

    def update_ally_health(self, current: int, max_val: int) -> None:
        self.ally_health.update_health(current, max_val)

    def update_enemy_health(self, current: int, max_val: int) -> None:
        self.enemy_health.update_health(current, max_val)

    def update_capacitor(self, current: float, max_val: float) -> None:
        self.capacitor.update_capacitor(current, max_val)

    def update_aim(self, state: str, distance: float | None = None) -> None:
        state_map = {
            "offline": AimState.OFFLINE,
            "online": AimState.ONLINE,
            "locked": AimState.LOCKED,
        }
        self.aim_status.update_state(
            state_map.get(state, AimState.ONLINE), distance
        )

    def update_match_time(self, seconds: int) -> None:
        self.match_timer.update_time(seconds)

    def update_chassis(self, mode: str) -> None:
        mode_map = {
            "unlocked": ChassisMode.UNLOCKED,
            "locked": ChassisMode.LOCKED,
            "low": ChassisMode.LOW,
            "high": ChassisMode.HIGH,
        }
        self.chassis_status.update_mode(
            mode_map.get(mode, ChassisMode.UNLOCKED)
        )

    def update_sentry(self, target: str, state: str, destination: str) -> None:
        self.sentry_info.update_info(target, state, destination)

    def update_gimbal_angles(self, pitch: float, yaw: float) -> None:
        if self.gimbal_angles is not None:
            self.gimbal_angles.update_angles(pitch, yaw)

    def update_jump_target(self, target: str) -> None:
        if self.jump_target is not None:
            self.jump_target.update_target(target)

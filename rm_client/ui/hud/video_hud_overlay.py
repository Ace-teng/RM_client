"""
图传 HUD 叠加层 — 用 QPainter 在图传上直接绘制，是界面上实际看到的 HUD。

注意：hud_overlay.py 里是控件版 HUD（HealthBar/CapacitorBar 等），覆盖在 centralWidget 上；
本文件 VideoHudOverlay 是图传区域内的绘制层，布局改这里才会生效。

左上角：己方血量 → 电容条 → 自瞄状态（垂直排列，间距≥35px）
右上角：敌方血量 → 能量 → 发弹量（垂直排列）
中央：比赛时间、目标距离、准心。底部：热量条、技能栏、信息面板。
"""
from qtpy.QtCore import Qt, QTimer, QRect
from qtpy.QtGui import QColor, QPainter, QPen, QBrush, QFont
from qtpy.QtWidgets import QWidget

NEON_CYAN = QColor(0, 229, 255)
NEON_GREEN = QColor(34, 197, 94)
NEON_RED = QColor(239, 68, 68)
NEON_ORANGE = QColor(255, 170, 0)
TEXT_LIGHT = QColor(229, 231, 235)
HUD_LINE_COLOR = QColor(200, 220, 255)

# 左上角垂直排列，间距≥35px，避免重叠
M = 20
TOP_LEFT = (M, 20)           # 第1行：己方血量
TOP_LEFT_2 = (M, 75)         # 第2行：电容条（20+55）
TOP_LEFT_3 = (M, 115)        # 第3行：自瞄状态（75+40）

# 右上角垂直排列
RIGHT_Y1 = 20                # 敌方血量
RIGHT_Y2 = 75                # 能量 / 发弹量
RIGHT_Y3 = 110

BOTTOM_RIGHT_2 = (200, 80)   # 热量条 right 200, bottom 80


class VideoHudOverlay(QWidget):
    """覆盖在图传上的 HUD：贴边布局，中央仅准心。"""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.update)
        self._timer.start(100)

    def paintEvent(self, event) -> None:
        from rm_client.core.model.datacenter import DataCenter

        super().paintEvent(event)
        dc = DataCenter()
        state = dc.operator_display_state
        role = dc.current_operator_role
        if state is None:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()
        if w < 10 or h < 10:
            return

        # 顶部一行（与 LAYOUT.md 严格一致）
        self._draw_player_health(painter, state, w, h)       # top-left 己方血量
        self._draw_capacitor_bar_top(painter, state, w, h)   # top-left-2 电容条
        self._draw_aim_status(painter, state, w, h)          # top-left-3 自瞄状态
        self._draw_match_timer(painter, state, w, h)          # top-center 比赛时间
        self._draw_energy_limit(painter, state, w, h)        # top-right-2 能量限制
        self._draw_enemy_hp(painter, state, w, h)            # top-right 对方血量
        self._draw_ammo(painter, state, w, h)                # top-right-3 发弹量
        # 顶部居中：锁定时目标距离
        self._draw_target_info_top(painter, state, w, h)
        # 准心（中央）
        self._draw_crosshair(painter, state, role, w, h)
        if role in ("infantry1", "infantry2") and state.fly_slope_line_on:
            self._draw_fly_slope_lines(painter, w, h)
        # 底部
        self._draw_heat_bar(painter, state, w, h)            # bottom-right-2 热量条
        self._draw_skill_bar(painter, state, w, h)           # bottom-center 技能栏
        self._draw_info_panel(painter, state, w, h)          # bottom-right 信息面板

    def _draw_player_health(self, p: QPainter, state, w: int, h: int) -> None:
        """左上 .position-top-left：己方血量"""
        x, y = TOP_LEFT[0], TOP_LEFT[1]
        p.setPen(TEXT_LIGHT)
        font = QFont()
        font.setPointSize(11)
        font.setBold(True)
        p.setFont(font)
        p.drawText(x, y + 14, f"HP {state.hp_self}")
        bar_w, bar_h = 100, 6
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(QColor(40, 40, 40)))
        p.drawRoundedRect(x, y + 18, bar_w, bar_h, 3, 3)
        fill = max(0, min(1.0, state.hp_self / 600.0)) * bar_w
        if fill > 0:
            p.setBrush(QBrush(NEON_GREEN))
            p.drawRoundedRect(x, y + 18, int(fill), bar_h, 3, 3)

    def _draw_capacitor_bar_top(self, p: QPainter, state, w: int, h: int) -> None:
        """左上第二行 .position-top-left-2：电容条"""
        x, y = TOP_LEFT_2[0], TOP_LEFT_2[1]
        bar_w, bar_h = 180, 8
        p.setPen(QPen(QColor(51, 65, 85), 1))
        p.setBrush(QBrush(QColor(30, 41, 59)))
        p.drawRoundedRect(x, y, bar_w, bar_h, 3, 3)
        fill_w = max(0, int(bar_w * state.capacitor_pct))
        if fill_w > 0:
            p.setBrush(QBrush(NEON_CYAN))
            p.setPen(Qt.NoPen)
            p.drawRoundedRect(x, y, fill_w, bar_h, 3, 3)
        p.setPen(TEXT_LIGHT)
        font = QFont()
        font.setPointSize(9)
        p.setFont(font)
        p.drawText(x, y + bar_h + 12, f"电容 {int(state.capacitor_pct * 100)}%")

    def _draw_aim_status(self, p: QPainter, state, w: int, h: int) -> None:
        """左 .position-top-left-3：自瞄状态 (left 220)"""
        x, y = TOP_LEFT_3[0], TOP_LEFT_3[1]
        status = state.aim_status
        text = {"offline": "自瞄 离线", "notarget": "自瞄 未锁", "targeting": "自瞄 锁定"}.get(status, status)
        color = NEON_RED if status == "offline" else NEON_GREEN if status == "targeting" else NEON_CYAN
        p.setPen(color)
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        p.setFont(font)
        p.drawText(x, y + 14, text)

    def _draw_match_timer(self, p: QPainter, state, w: int, h: int) -> None:
        """顶部居中 .position-top-center：比赛时间"""
        time_s = int(state.match_time_sec) if state.match_time_sec else 0
        mm, ss = time_s // 60, time_s % 60
        text = f"{mm}:{ss:02d}"
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        p.setFont(font)
        p.setPen(NEON_CYAN)
        rect = p.boundingRect(QRect(0, 0, w, 24), Qt.AlignCenter, text)
        p.drawText((w - rect.width()) // 2, 16 + 14, text)

    def _draw_energy_limit(self, p: QPainter, state, w: int, h: int) -> None:
        """右上第2行：能量限制，与敌方血量垂直错开"""
        x = w - 220 - 80
        y = RIGHT_Y2
        text = f"能量 {int(state.energy_current)}/{int(state.energy_limit)}"
        font = QFont()
        font.setPointSize(10)
        p.setFont(font)
        p.setPen(TEXT_LIGHT)
        p.drawText(x, y + 14, text)

    def _draw_enemy_hp(self, p: QPainter, state, w: int, h: int) -> None:
        """右上第1行：对方血量"""
        text = f"敌 HP {state.hp_enemy}"
        font = QFont()
        font.setPointSize(11)
        font.setBold(True)
        p.setFont(font)
        p.setPen(NEON_RED)
        tw = p.fontMetrics().horizontalAdvance(text)
        p.drawText(w - M - tw, RIGHT_Y1 + 14, text)

    def _draw_ammo(self, p: QPainter, state, w: int, h: int) -> None:
        """右上第3行：发弹量，在能量下方"""
        text = f"弹 {state.ammo_count}/{state.ammo_limit}"
        font = QFont()
        font.setPointSize(10)
        p.setFont(font)
        p.setPen(TEXT_LIGHT)
        tw = p.fontMetrics().horizontalAdvance(text)
        p.drawText(w - M - tw, RIGHT_Y3 + 14, text)

    def _draw_target_info_top(self, p: QPainter, state, w: int, h: int) -> None:
        """顶部居中：目标距离（仅锁定时），在比赛时间下方"""
        if state.aim_status != "targeting":
            return
        dist = state.aim_target_distance or 0
        text = f"TARGET {dist:.1f}m"
        font = QFont()
        font.setPointSize(9)
        font.setBold(True)
        p.setFont(font)
        p.setPen(NEON_CYAN)
        rect = p.boundingRect(QRect(0, 0, w, 20), Qt.AlignCenter, text)
        p.drawText((w - rect.width()) // 2, 50, text)

    def _draw_heat_bar(self, p: QPainter, state, w: int, h: int) -> None:
        """底部偏右：热量条，文字在条上方不重叠"""
        bar_w, bar_h = 160, 8
        # 与技能条同一底边：条底 h-M，条顶 h-M-bar_h
        bar_y = h - M - bar_h
        text_y = bar_y - 8  # 文字在条上方 8px
        x = w - 200 - bar_w
        p.setPen(TEXT_LIGHT)
        font = QFont()
        font.setPointSize(9)
        p.setFont(font)
        p.drawText(x, text_y, f"热量 {state.heat_current}/{state.heat_limit}")
        p.setPen(QPen(QColor(51, 65, 85), 1))
        p.setBrush(QBrush(QColor(30, 41, 59)))
        p.drawRoundedRect(x, bar_y, bar_w, bar_h, 3, 3)
        heat_pct = state.heat_limit and (state.heat_current / state.heat_limit) or 0
        fill_w = max(0, min(1.0, heat_pct)) * bar_w
        if fill_w > 0:
            p.setBrush(QBrush(NEON_ORANGE))
            p.setPen(Qt.NoPen)
            p.drawRoundedRect(x, bar_y, int(fill_w), bar_h, 3, 3)

    def _draw_skill_bar(self, p: QPainter, state, w: int, h: int) -> None:
        """底部居中：技能栏，文字在条上方不重叠"""
        bar_h, bar_w = 10, 220
        cx = w // 2
        bar_y = h - M - bar_h
        text_y = bar_y - 6  # 文字在条上方
        x = cx - bar_w // 2
        p.setPen(TEXT_LIGHT)
        font = QFont()
        font.setPointSize(9)
        p.setFont(font)
        p.drawText(cx - 30, text_y, f"技能 CAP {int(state.capacitor_pct * 100)}%")
        p.setPen(QPen(QColor(51, 65, 85), 1))
        p.setBrush(QBrush(QColor(30, 41, 59)))
        p.drawRoundedRect(x, bar_y, bar_w, bar_h, 3, 3)
        fill_w = max(0, int(bar_w * state.capacitor_pct))
        if fill_w > 0:
            p.setBrush(QBrush(NEON_CYAN))
            p.setPen(Qt.NoPen)
            p.drawRoundedRect(x, bar_y, fill_w, bar_h, 3, 3)

    def _draw_info_panel(self, p: QPainter, state, w: int, h: int) -> None:
        """右下 .position-bottom-right：信息面板"""
        time_s = int(state.match_time_sec) if state.match_time_sec else 0
        mm, ss = time_s // 60, time_s % 60
        font = QFont()
        font.setPointSize(10)
        p.setFont(font)
        p.setPen(TEXT_LIGHT)
        line1 = f"TIME {mm:02d}:{ss:02d}"
        line2 = f"HP {state.hp_self}/{state.hp_enemy}"
        tw = max(p.fontMetrics().horizontalAdvance(line1), p.fontMetrics().horizontalAdvance(line2))
        x = w - M - tw
        y = h - M - 28
        p.drawText(x, y, line1)
        p.drawText(x, y + 16, line2)

    def _draw_crosshair(self, p: QPainter, state, role: str, w: int, h: int) -> None:
        """准心：青/白细线，主屏中央无紫色框。"""
        cx, cy = w // 2, h // 2
        p.setPen(QPen(HUD_LINE_COLOR, 1))
        p.setBrush(Qt.NoBrush)
        if role in ("infantry1", "infantry2"):
            # 扌型
            p.drawLine(cx, cy - 22, cx, cy + 22)
            p.drawLine(cx - 18, cy - 22, cx + 18, cy - 22)
            # 参考图：分段圆（8 段，每段 36° 弧，间隔 9°）
            r = 28
            for i in range(8):
                start = i * 45 * 16
                span = 36 * 16
                p.drawArc(cx - r, cy - r, r * 2, r * 2, start, span)
        else:
            p.drawLine(cx - 18, cy, cx + 18, cy)
            p.drawLine(cx, cy - 18, cx, cy + 18)
            r = 24
            for i in range(8):
                start = i * 45 * 16
                span = 36 * 16
                p.drawArc(cx - r, cy - r, r * 2, r * 2, start, span)

    def _draw_fly_slope_lines(self, p: QPainter, w: int, h: int) -> None:
        cx, cy = w // 2, h // 2
        p.setPen(QPen(HUD_LINE_COLOR, 1))
        p.drawLine(cx - 40, cy - 28, cx - 40, cy + 28)
        p.drawLine(cx + 40, cy - 28, cx + 40, cy + 28)

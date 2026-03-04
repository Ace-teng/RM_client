"""
态势图 / 小地图 — Phase 5，只读 DataCenter.robot_states 绘制场地与机器人位置。

见总文档 §5.1、§7 Phase 5。
"""
from qtpy.QtCore import Qt, QTimer
from qtpy.QtGui import QColor, QPainter, QPen
from qtpy.QtWidgets import QFrame, QSizePolicy, QVBoxLayout, QWidget


class MapWidget(QFrame):
    """小地图：画矩形场地 + 己方/对方机器人点位，数据来自 DataCenter.robot_states。"""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setMinimumSize(200, 120)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        from rm_client.ui.styles import STYLE_PANEL
        self.setStyleSheet(STYLE_PANEL + " background: #1a1a1a;")
        self._robot_states: dict = {}

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._refresh_and_repaint)
        self._timer.start(300)

    def _refresh_and_repaint(self) -> None:
        from rm_client.core.model.datacenter import DataCenter

        dc = DataCenter()
        # 步兵视图时，小地图在左侧面板中已经展示；右侧的 MapWidget 可以选择隐藏以降低信息密度。
        role = getattr(dc, "current_operator_role", "hero")
        # 这里不直接 setVisible，以避免影响左侧嵌入的实例；由父容器控制可见性。
        self._robot_states = dc.robot_states
        self.update()

    def paintEvent(self, event) -> None:
        super().paintEvent(event)
        w, h = self.width(), self.height()
        if w < 10 or h < 10:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 场地边框（留边距）
        margin = 8
        cx, cy = margin, margin
        cw, ch = w - 2 * margin, h - 2 * margin
        painter.setPen(QPen(QColor(0, 229, 255), 1))
        painter.drawRect(cx, cy, cw, ch)
        painter.setPen(QColor(0, 229, 255))
        painter.drawText(cx + 4, cy + 14, "MINI-MAP")

        # 机器人点位：x/y 为 0～1 归一化，映射到场地内
        for rid, state in self._robot_states.items():
            if not isinstance(state, dict):
                continue
            x = state.get("x", 0.5)
            y = state.get("y", 0.5)
            team = state.get("team", "red")
            px = int(cx + x * cw)
            py = int(cy + y * ch)
            color = QColor(220, 60, 60) if team == "red" else QColor(60, 100, 220)
            painter.setBrush(color)
            painter.setPen(QPen(color.darker(120), 1))
            painter.drawEllipse(px - 4, py - 4, 8, 8)

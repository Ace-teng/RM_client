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
        self.setFrameStyle(QFrame.StyledPanel)
        self.setStyleSheet("background: #2d2d2d;")
        self._robot_states: dict = {}

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._refresh_and_repaint)
        self._timer.start(300)

    def _refresh_and_repaint(self) -> None:
        from rm_client.core.model.datacenter import DataCenter

        self._robot_states = DataCenter().robot_states
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
        painter.setPen(QPen(QColor(80, 80, 80), 1))
        painter.drawRect(cx, cy, cw, ch)
        painter.drawText(cx + 4, cy + 14, "态势图")

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

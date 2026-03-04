# rm_client/ui/hud/crosshair.py
"""准心组件 - '扌'型。"""
from qtpy.QtCore import Qt
from qtpy.QtGui import QPainter, QPen, QColor
from qtpy.QtWidgets import QWidget


class Crosshair(QWidget):
    """准心组件 - '扌'型"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(80, 80)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.color = QColor("#00FF00")
        self.show_ramp_guide = False

    def set_color(self, color: str) -> None:
        self.color = QColor(color)
        self.update()

    def set_ramp_guide(self, show: bool) -> None:
        self.show_ramp_guide = show
        self.update()

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        pen = QPen(self.color)
        pen.setWidth(2)
        painter.setPen(pen)

        cx, cy = 40, 40

        # "扌"型准心 - 横线
        painter.drawLine(10, cy, 30, cy)
        painter.drawLine(50, cy, 70, cy)
        # 竖线
        painter.drawLine(cx, 10, cx, 30)
        painter.drawLine(cx, 50, cx, 70)
        # "扌"特征短横
        painter.drawLine(22, 32, 30, 32)
        painter.drawLine(22, 48, 30, 48)
        # 中心点
        painter.setBrush(self.color)
        painter.drawEllipse(cx - 3, cy - 3, 6, 6)

        # 飞坡线
        if self.show_ramp_guide:
            pen.setWidth(2)
            painter.setPen(pen)
            painter.save()
            painter.translate(cx - 35, cy)
            painter.rotate(15)
            painter.drawLine(-20, 0, 0, 0)
            painter.restore()
            painter.save()
            painter.translate(cx + 35, cy)
            painter.rotate(-15)
            painter.drawLine(0, 0, 20, 0)
            painter.restore()

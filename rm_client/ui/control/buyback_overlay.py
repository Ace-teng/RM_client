"""
买活预警叠加层 — 屏幕中央醒目提醒「对方可能买活」。

覆盖在图传区域中央。仅当战术分析判定为「具体事件」时显示：
即比赛进行中（game_phase > 0）且对方经济 ≥ 买活阈值时 tactical_advice.buyback_alert 为 True，
一打开或占位数据不会触发。
"""
from qtpy.QtCore import Qt, QTimer
from qtpy.QtGui import QFont
from qtpy.QtWidgets import QLabel, QWidget

from rm_client.core.model.datacenter import DataCenter


class BuybackOverlay(QLabel):
    """半透明背景 + 大字号警示文字，居中显示。"""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet(
            "background-color: rgba(26, 26, 26, 0.95); color: #fef3c7; "
            "border: 1px solid #f97316; border-radius: 8px; padding: 10px 24px;"
        )
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.setFont(font)
        self.setText("⚠  注意：对方可能买活")
        self.setMinimumWidth(280)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.hide()

        self._dc = DataCenter()
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._refresh)
        self._timer.start(400)

    def _refresh(self) -> None:
        advice = self._dc.tactical_advice
        if advice is not None and advice.buyback_alert:
            self.show()
        else:
            self.hide()

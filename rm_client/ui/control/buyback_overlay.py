"""
买活预警叠加层 — 屏幕中央醒目提醒「对方可能买活」。

覆盖在图传区域中央，仅当 dc.tactical_advice.buyback_alert 为 True 时显示。
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
            "background-color: rgba(180, 0, 0, 0.85); color: white; "
            "border: 3px solid white; border-radius: 8px; padding: 12px;"
        )
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        self.setFont(font)
        self.setText("⚠ 注意：对方可能买活")
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

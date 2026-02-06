"""
战术建议面板 — 显示追击/撤退、血量差、经济提示。

从 DataCenter 读取 tactical_advice，由 TacticalAdvisor 定时更新。
"""
from qtpy.QtCore import QTimer
from qtpy.QtWidgets import QFrame, QLabel, QVBoxLayout, QWidget

from rm_client.core.model.datacenter import DataCenter
from rm_client.core.service.tactical_advisor import update_tactical_advice


class TacticalPanel(QFrame):
    """战术建议：追击/撤退、血量差、经济提示。"""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFrameStyle(QFrame.StyledPanel)
        layout = QVBoxLayout(self)
        layout.setSpacing(4)
        title = QLabel("战术建议")
        title.setStyleSheet("font-weight: bold; font-size: 12px;")
        layout.addWidget(title)
        self._hp_label = QLabel("—")
        self._hp_label.setWordWrap(True)
        layout.addWidget(self._hp_label)
        self._economy_label = QLabel("")
        self._economy_label.setWordWrap(True)
        self._economy_label.setStyleSheet("color: #666; font-size: 11px;")
        layout.addWidget(self._economy_label)
        layout.addStretch()

        self._dc = DataCenter()
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._refresh)
        self._timer.start(500)

    def _refresh(self) -> None:
        update_tactical_advice(self._dc)
        advice = self._dc.tactical_advice
        if advice is None:
            self._hp_label.setStyleSheet("")
            self._hp_label.setText("—")
            self._economy_label.setText("")
            return
        hp_text = f"血量 我方 {advice.hp_ours} vs 对方 {advice.hp_enemy}"
        if advice.hp_diff is not None:
            sign = "+" if advice.hp_diff >= 0 else ""
            hp_text += f"（差{sign}{advice.hp_diff}）"
        if advice.hp_suggestion:
            hp_text += f"\n建议：{advice.hp_suggestion}"
            color = "#0a0" if advice.hp_suggestion == "追击" else "#a00" if advice.hp_suggestion == "撤退" else "#aa0"
            self._hp_label.setStyleSheet(f"font-weight: bold; color: {color};")
        else:
            self._hp_label.setStyleSheet("")
        self._hp_label.setText(hp_text)
        self._economy_label.setText(advice.economy_hint or "")

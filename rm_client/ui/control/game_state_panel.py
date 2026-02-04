"""
右侧控制面板 — 赛事状态与血量展示（Phase 4）。

只读 DataCenter.game_state，展示 game_phase、remaining_time_sec；预留血量/经济等占位。
见总文档 §5.1、§7 Phase 4。
"""
from qtpy.QtCore import QTimer
from qtpy.QtWidgets import QFormLayout, QFrame, QLabel, QVBoxLayout, QWidget


class GameStatePanel(QFrame):
    """右侧状态面板：从 DataCenter 只读 game_state，定时刷新显示。"""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setMaximumWidth(320)
        self.setFrameStyle(QFrame.StyledPanel)
        layout = QVBoxLayout(self)
        layout.setSpacing(8)

        title = QLabel("赛事状态")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)

        form = QFormLayout()
        self._phase_label = QLabel("—")
        self._time_label = QLabel("—")
        self._hp_placeholder = QLabel("—")
        form.addRow("阶段 (phase):", self._phase_label)
        form.addRow("剩余时间 (s):", self._time_label)
        form.addRow("血量 (待协议):", self._hp_placeholder)
        layout.addLayout(form)

        layout.addStretch()

        self._refresh_timer = QTimer(self)
        self._refresh_timer.timeout.connect(self._refresh_from_dc)
        self._refresh_timer.start(500)

    def _refresh_from_dc(self) -> None:
        from rm_client.core.model.datacenter import DataCenter

        dc = DataCenter()
        gs = dc.game_state
        if gs is None:
            self._phase_label.setText("—")
            self._time_label.setText("—")
            self._hp_placeholder.setText("—")
            return
        self._phase_label.setText(str(getattr(gs, "game_phase", "?")))
        self._time_label.setText(str(getattr(gs, "remaining_time_sec", "?")))
        self._hp_placeholder.setText("(协议接入后显示)")

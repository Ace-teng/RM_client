"""
右侧控制面板 — 赛事状态与血量展示（Phase 4）。

只读 DataCenter.game_state，展示 game_phase、remaining_time_sec；预留血量/经济等占位。
见总文档 §5.1、§7 Phase 4。
"""
from qtpy.QtCore import QTimer
from qtpy.QtWidgets import QFrame, QLabel, QVBoxLayout, QWidget

from rm_client.ui.control.field_row import FieldRow


class GameStatePanel(QFrame):
    """右侧状态面板：参考图圆角边框行。"""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setMaximumWidth(320)
        from rm_client.ui.styles import STYLE_PANEL, STYLE_PANEL_TITLE
        self.setStyleSheet(STYLE_PANEL)
        layout = QVBoxLayout(self)
        layout.setSpacing(6)

        title = QLabel("MATCH STATUS")
        title.setStyleSheet(STYLE_PANEL_TITLE)
        layout.addWidget(title)

        self._row_phase = FieldRow("阶段 (phase):")
        self._row_time = FieldRow("剩余时间 (s):")
        self._row_hp = FieldRow("血量 (待协议):")
        layout.addWidget(self._row_phase)
        layout.addWidget(self._row_time)
        layout.addWidget(self._row_hp)

        layout.addStretch()

        self._refresh_timer = QTimer(self)
        self._refresh_timer.timeout.connect(self._refresh_from_dc)
        self._refresh_timer.start(500)

    def _refresh_from_dc(self) -> None:
        from rm_client.core.model.datacenter import DataCenter

        dc = DataCenter()
        gs = dc.game_state
        if gs is None:
            self._row_phase.set_value("—")
            self._row_time.set_value("—")
            self._row_hp.set_value("—")
            return
        self._row_phase.set_value(str(getattr(gs, "game_phase", "?")))
        self._row_time.set_value(str(getattr(gs, "remaining_time_sec", "?")))
        self._row_hp.set_value("(协议接入后显示)")

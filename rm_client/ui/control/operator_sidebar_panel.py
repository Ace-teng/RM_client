"""
操作手侧边栏 — 等级与性能体系、哨兵状态（§0.7、操作.md 英雄 1.12、1.13）。

数据来自 DataCenter.operator_display_state（占位由 demo 注入，协议接入后由 protocol 覆盖）。
"""
from qtpy.QtCore import QTimer
from qtpy.QtWidgets import QFrame, QLabel, QVBoxLayout, QWidget

from rm_client.ui.control.field_row import FieldRow


class OperatorSidebarPanel(QFrame):
    """侧边栏：参考图圆角边框行，等级与性能、哨兵状态。英雄视图时显示。"""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setMaximumWidth(320)
        layout = QVBoxLayout(self)
        layout.setSpacing(6)

        from rm_client.ui.styles import STYLE_PANEL, STYLE_PANEL_TITLE
        self.setStyleSheet(STYLE_PANEL)
        title = QLabel("LEVEL & PERFORMANCE")
        title.setStyleSheet(STYLE_PANEL_TITLE)
        layout.addWidget(title)
        self._row_level_self = FieldRow("己方等级:")
        self._row_level_enemy = FieldRow("对方等级:")
        self._row_perf_self = FieldRow("己方性能体系:")
        self._row_perf_enemy = FieldRow("对方性能体系:")
        layout.addWidget(self._row_level_self)
        layout.addWidget(self._row_level_enemy)
        layout.addWidget(self._row_perf_self)
        layout.addWidget(self._row_perf_enemy)

        title2 = QLabel("SENTRY STATUS")
        title2.setStyleSheet(STYLE_PANEL_TITLE)
        layout.addWidget(title2)
        self._row_sentry_target = FieldRow("当前目标:")
        self._row_sentry_state = FieldRow("状态:")
        self._row_sentry_goal = FieldRow("目的位置:")
        layout.addWidget(self._row_sentry_target)
        layout.addWidget(self._row_sentry_state)
        layout.addWidget(self._row_sentry_goal)

        layout.addStretch()

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._refresh)
        self._timer.start(400)

    def _refresh(self) -> None:
        from rm_client.core.model.datacenter import DataCenter

        # 仅英雄视图显示侧边栏（等级与哨兵）
        role = DataCenter().current_operator_role
        self.setVisible(role == "hero")
        self._refresh_content()

    def _refresh_content(self) -> None:
        from rm_client.core.model.datacenter import DataCenter

        dc = DataCenter()
        state = dc.operator_display_state
        if state is None:
            self._row_level_self.set_value("—")
            self._row_level_enemy.set_value("—")
            self._row_perf_self.set_value("—")
            self._row_perf_enemy.set_value("—")
            self._row_sentry_target.set_value("—")
            self._row_sentry_state.set_value("—")
            self._row_sentry_goal.set_value("—")
            return
        self._row_level_self.set_value(str(state.level_self))
        self._row_level_enemy.set_value(str(state.level_enemy))
        self._row_perf_self.set_value(str(state.performance_self))
        self._row_perf_enemy.set_value(str(state.performance_enemy))
        self._row_sentry_target.set_value(state.sentry_target or "—")
        self._row_sentry_state.set_value(state.sentry_state or "—")
        self._row_sentry_goal.set_value(state.sentry_goal or "—")

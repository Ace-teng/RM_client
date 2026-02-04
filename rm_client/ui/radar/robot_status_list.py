"""
机器人关键状态列表 — Phase 5，只读 DataCenter.robot_states 展示 ID、血量、阵营。

见总文档 §5.1、§7 Phase 5。
"""
from qtpy.QtCore import QTimer
from qtpy.QtWidgets import QFrame, QLabel, QVBoxLayout, QWidget


class RobotStatusList(QFrame):
    """关键状态：列出 robot_states 中的 ID、血量、阵营。"""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFrameStyle(QFrame.StyledPanel)
        layout = QVBoxLayout(self)
        layout.setSpacing(4)
        title = QLabel("机器人状态")
        title.setStyleSheet("font-weight: bold; font-size: 12px;")
        layout.addWidget(title)
        self._content = QLabel("—")
        self._content.setWordWrap(True)
        self._content.setStyleSheet("font-size: 11px; color: #ccc;")
        layout.addWidget(self._content)
        layout.addStretch()

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._refresh_from_dc)
        self._timer.start(400)

    def _refresh_from_dc(self) -> None:
        from rm_client.core.model.datacenter import DataCenter

        rs = DataCenter().robot_states
        if not rs:
            self._content.setText("—")
            return
        lines = []
        for rid, state in sorted(rs.items()):
            if not isinstance(state, dict):
                continue
            hp = state.get("hp", "?")
            team = state.get("team", "?")
            lines.append("%s %s HP:%s" % (rid, team, hp))
        self._content.setText("\n".join(lines) if lines else "—")

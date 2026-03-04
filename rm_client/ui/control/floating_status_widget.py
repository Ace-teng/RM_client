"""
悬浮窗 — 基地底装甲、遥控器状态（§0.7、操作.md 英雄 1.15、1.19）。

可关闭/折叠，数据来自 DataCenter.operator_display_state。
"""
from qtpy.QtCore import Qt, QTimer
from qtpy.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget


class FloatingStatusWidget(QFrame):
    """悬浮小窗：基地底装甲是否打开、遥控器状态。"""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        from rm_client.ui.styles import STYLE_FLOATING
        self.setStyleSheet(STYLE_FLOATING)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        header = QHBoxLayout()
        title = QLabel("GIMBAL / STATUS")
        title.setStyleSheet("font-weight: bold; font-size: 11px; color: #a855f7;")
        header.addWidget(title)
        self._close_btn = QPushButton("×")
        self._close_btn.setFixedSize(20, 20)
        self._close_btn.setStyleSheet("font-size: 14px;")
        self._close_btn.clicked.connect(self.hide)
        header.addWidget(self._close_btn)
        layout.addLayout(header)
        self._armor_label = QLabel("基地底装甲: —")
        self._armor_label.setStyleSheet("font-size: 11px;")
        layout.addWidget(self._armor_label)
        self._remote_label = QLabel("遥控器: —")
        self._remote_label.setStyleSheet("font-size: 11px;")
        layout.addWidget(self._remote_label)

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._refresh)
        self._timer.start(500)

    def _refresh(self) -> None:
        from rm_client.core.model.datacenter import DataCenter

        state = DataCenter().operator_display_state
        if state is None:
            self._armor_label.setText("基地底装甲: —")
            self._remote_label.setText("遥控器: —")
            return
        self._armor_label.setText("基地底装甲: 已打开" if state.base_armor_open else "基地底装甲: 关闭")
        self._remote_label.setText("遥控器: 正常" if state.remote_control_ok else "遥控器: 丢控")

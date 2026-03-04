"""
步兵视图顶栏 — 参考图：左侧 ROBOMASTER INFANTRY 1、中间 FPV、右侧 70% 30% 16:9，全部高对比度白/青。
"""
from qtpy.QtCore import QTimer
from qtpy.QtWidgets import QFrame, QHBoxLayout, QLabel, QWidget

from rm_client.ui.styles import NEON_CYAN, TEXT_WHITE


class InfantryTopBar(QFrame):
    """顶栏：与参考图一致，文字均使用白色/霓虹青保证可读。"""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFixedHeight(36)
        self.setStyleSheet(
            "background-color: #1a1a1a; border-bottom: 1px solid #334155;"
        )
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 6, 12, 6)
        self._title = QLabel("ROBOMASTER INFANTRY 1")
        self._title.setStyleSheet(f"color: {NEON_CYAN}; font-weight: bold; font-size: 13px;")
        self._center = QLabel("FPV")
        self._center.setStyleSheet(f"color: {TEXT_WHITE}; font-size: 12px; font-weight: bold;")
        self._right = QLabel("70%  30%  16:9")
        self._right.setStyleSheet(f"color: {TEXT_WHITE}; font-size: 11px;")
        layout.addWidget(self._title)
        layout.addStretch()
        layout.addWidget(self._center)
        layout.addStretch()
        layout.addWidget(self._right)
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_visibility)
        self._timer.start(300)

    def _update_visibility(self) -> None:
        from rm_client.core.model.datacenter import DataCenter
        role = DataCenter().current_operator_role
        self.setVisible(role in ("infantry1", "infantry2"))
        if role == "infantry2":
            self._title.setText("ROBOMASTER INFANTRY 2")
        else:
            self._title.setText("ROBOMASTER INFANTRY 1")

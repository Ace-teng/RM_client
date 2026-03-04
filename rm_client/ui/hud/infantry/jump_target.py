# rm_client/ui/hud/infantry/jump_target.py
"""跳跃目标设定。"""
from qtpy.QtWidgets import QFrame, QHBoxLayout, QLabel


class JumpTarget(QFrame):
    """跳跃目标设定"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.setStyleSheet("""
            QFrame {
                background-color: transparent;
                border: 1px solid rgba(255, 255, 255, 0.25);
                border-radius: 4px;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(8)

        label = QLabel("跳跃目标")
        label.setStyleSheet(
            "color: rgba(255,255,255,0.6); font-size: 10px; background: transparent;"
        )
        layout.addWidget(label)

        self.target_label = QLabel("-")
        self.target_label.setStyleSheet("""
            color: #00AAFF;
            font-size: 12px;
            font-weight: bold;
            background: transparent;
        """)
        layout.addWidget(self.target_label)

    def update_target(self, target: str) -> None:
        """更新跳跃目标"""
        self.target_label.setText(target if target else "-")
        self.setVisible(bool(target))

# rm_client/ui/hud/sentry_info.py
"""哨兵信息面板。"""
from qtpy.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel


class SentryInfo(QFrame):
    """哨兵信息面板"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.setFixedWidth(140)
        self.setStyleSheet("""
            QFrame {
                background-color: rgba(0, 0, 0, 0.6);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 4px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(6)

        title = QLabel("🤖 哨兵")
        title.setStyleSheet("""
            color: #FFFFFF;
            font-size: 12px;
            font-weight: bold;
            background: transparent;
            border-bottom: 1px solid rgba(255,255,255,0.2);
            padding-bottom: 4px;
        """)
        layout.addWidget(title)

        self.target_row = self._create_row("目标", "#FFAA00")
        layout.addLayout(self.target_row["layout"])

        self.state_row = self._create_row("状态", "#00AAFF")
        layout.addLayout(self.state_row["layout"])

        self.dest_row = self._create_row("前往", "#00FF00")
        layout.addLayout(self.dest_row["layout"])

    def _create_row(self, label: str, value_color: str) -> dict:
        layout = QHBoxLayout()
        layout.setSpacing(8)

        label_widget = QLabel(label)
        label_widget.setStyleSheet(
            "color: rgba(255,255,255,0.6); font-size: 12px; background: transparent;"
        )
        layout.addWidget(label_widget)
        layout.addStretch()

        value_widget = QLabel("-")
        value_widget.setStyleSheet(
            f"color: {value_color}; font-size: 12px; background: transparent;"
        )
        layout.addWidget(value_widget)
        return {"layout": layout, "value": value_widget}

    def update_info(self, target: str, state: str, destination: str) -> None:
        """更新哨兵信息"""
        self.target_row["value"].setText(target or "无")
        self.state_row["value"].setText(state or "-")
        self.dest_row["value"].setText(destination or "-")

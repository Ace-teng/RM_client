# rm_client/ui/hud/health_bar.py
"""血量条组件。"""
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QWidget, QProgressBar, QLabel, QVBoxLayout


class HealthBar(QWidget):
    """血量条组件"""

    def __init__(self, is_enemy: bool = False, parent=None):
        super().__init__(parent)
        self.is_enemy = is_enemy
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        self.type_label = QLabel()
        self.type_label.setStyleSheet("""
            color: rgba(255, 255, 255, 0.6);
            font-size: 10px;
        """)
        layout.addWidget(self.type_label)

        self.bar = QProgressBar()
        self.bar.setFixedSize(180, 20)
        self.bar.setTextVisible(False)
        self.bar.setStyleSheet(self._get_bar_style())
        layout.addWidget(self.bar)

        self.value_label = QLabel("500/500")
        self.value_label.setStyleSheet("""
            color: #FFFFFF;
            font-size: 14px;
            font-weight: bold;
            font-family: 'Consolas', monospace;
        """)
        layout.addWidget(self.value_label)

    def _get_bar_style(self) -> str:
        if self.is_enemy:
            chunk_color = "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #AA0000, stop:1 #FF3333)"
        else:
            chunk_color = "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00AA00, stop:1 #00FF00)"
        return f"""
            QProgressBar {{
                background-color: rgba(0, 0, 0, 0.5);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 2px;
            }}
            QProgressBar::chunk {{
                background: {chunk_color};
                border-radius: 1px;
            }}
        """

    def update_health(self, current: int, max_health: int) -> None:
        """更新血量"""
        self.bar.setMaximum(max_health)
        self.bar.setValue(current)
        self.value_label.setText(f"{current}/{max_health}")

        percentage = (current / max_health) if max_health > 0 else 0
        if percentage < 0.15:
            self.value_label.setStyleSheet(
                "color: #FF3333; font-size: 14px; font-weight: bold; font-family: 'Consolas', monospace;"
            )
        elif percentage < 0.3:
            self.value_label.setStyleSheet(
                "color: #FFAA00; font-size: 14px; font-weight: bold; font-family: 'Consolas', monospace;"
            )
        else:
            self.value_label.setStyleSheet(
                "color: #FFFFFF; font-size: 14px; font-weight: bold; font-family: 'Consolas', monospace;"
            )

    def set_robot_type(self, robot_type: str) -> None:
        """设置机器人类型"""
        self.type_label.setText(robot_type.upper())

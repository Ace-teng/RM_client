# rm_client/ui/hud/chassis_status.py
"""底盘状态指示。"""
from enum import Enum
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QFrame, QHBoxLayout, QLabel


class ChassisMode(Enum):
    UNLOCKED = "unlocked"
    LOCKED = "locked"
    LOW = "low"
    HIGH = "high"


class ChassisStatus(QFrame):
    """底盘状态指示"""

    MODE_CONFIG = {
        ChassisMode.UNLOCKED: {"text": "UNLOCKED", "icon": "🔓", "color": "#00FF00"},
        ChassisMode.LOCKED: {"text": "LOCKED", "icon": "🔒", "color": "#FF3333"},
        ChassisMode.LOW: {"text": "LOW", "icon": "⬇", "color": "#FFFFFF"},
        ChassisMode.HIGH: {"text": "HIGH", "icon": "⬆", "color": "#FFAA00"},
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.setStyleSheet("""
            QFrame {
                background-color: rgba(0, 0, 0, 0.6);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 4px;
                padding: 8px;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(8)

        self.icon_label = QLabel("🔓")
        self.icon_label.setStyleSheet("font-size: 14px; background: transparent;")
        layout.addWidget(self.icon_label)

        self.status_label = QLabel("UNLOCKED")
        self.status_label.setStyleSheet("""
            color: #00FF00;
            font-size: 14px;
            font-weight: bold;
            font-family: 'Consolas', monospace;
            background: transparent;
        """)
        layout.addWidget(self.status_label)

    def update_mode(self, mode: ChassisMode) -> None:
        """更新底盘状态"""
        config = self.MODE_CONFIG.get(mode, self.MODE_CONFIG[ChassisMode.UNLOCKED])
        self.icon_label.setText(config["icon"])
        self.status_label.setText(config["text"])
        self.status_label.setStyleSheet(f"""
            color: {config["color"]};
            font-size: 14px;
            font-weight: bold;
            font-family: 'Consolas', monospace;
            background: transparent;
        """)

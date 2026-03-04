# rm_client/ui/hud/aim_status.py
"""自瞄状态指示器。"""
from enum import Enum
from qtpy.QtCore import QTimer
from qtpy.QtWidgets import QWidget, QLabel, QHBoxLayout


class AimState(Enum):
    OFFLINE = "offline"
    ONLINE = "online"   # NOTARGET
    LOCKED = "locked"


class AimStatus(QWidget):
    """自瞄状态指示器"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._state = AimState.ONLINE
        self._blink_on = True
        self._setup_ui()
        self._setup_blink_timer()

    def _setup_ui(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self.indicator = QLabel("●")
        self.indicator.setFixedWidth(16)
        self.indicator.setStyleSheet("font-size: 12px; color: #00FF00;")
        layout.addWidget(self.indicator)

        self.status_label = QLabel("NOTARGET")
        self.status_label.setStyleSheet("""
            color: #00FF00;
            font-size: 14px;
            font-weight: bold;
            font-family: 'Consolas', monospace;
        """)
        layout.addWidget(self.status_label)

        self.distance_label = QLabel("")
        self.distance_label.setStyleSheet("""
            color: #00AAFF;
            font-size: 12px;
            font-family: 'Consolas', monospace;
        """)
        layout.addWidget(self.distance_label)

    def _setup_blink_timer(self) -> None:
        self.blink_timer = QTimer(self)
        self.blink_timer.timeout.connect(self._toggle_blink)

    def _toggle_blink(self) -> None:
        self._blink_on = not self._blink_on
        if self._state == AimState.LOCKED:
            alpha = 255 if self._blink_on else 100
            self.indicator.setStyleSheet(f"font-size: 12px; color: rgba(255, 51, 51, {alpha});")

    def update_state(self, state: AimState, distance: float | None = None) -> None:
        """更新自瞄状态"""
        self._state = state

        if state == AimState.OFFLINE:
            self.indicator.setStyleSheet("font-size: 12px; color: #666666;")
            self.status_label.setText("OFFLINE")
            self.status_label.setStyleSheet(
                "color: #666666; font-size: 14px; font-weight: bold; font-family: 'Consolas', monospace;"
            )
            self.distance_label.setText("")
            self.blink_timer.stop()

        elif state == AimState.ONLINE:
            self.indicator.setStyleSheet("font-size: 12px; color: #00FF00;")
            self.status_label.setText("NOTARGET")
            self.status_label.setStyleSheet(
                "color: #00FF00; font-size: 14px; font-weight: bold; font-family: 'Consolas', monospace;"
            )
            self.distance_label.setText("")
            self.blink_timer.stop()

        elif state == AimState.LOCKED:
            self.indicator.setStyleSheet("font-size: 12px; color: #FF3333;")
            self.status_label.setText("LOCKED")
            self.status_label.setStyleSheet(
                "color: #FF3333; font-size: 14px; font-weight: bold; font-family: 'Consolas', monospace;"
            )
            self.blink_timer.start(250)
            if distance is not None:
                self.distance_label.setText(f"{distance:.1f}m")

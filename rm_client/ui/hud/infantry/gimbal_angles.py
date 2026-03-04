# rm_client/ui/hud/infantry/gimbal_angles.py
"""Pitch/Yaw 角度显示。"""
from qtpy.QtWidgets import QWidget, QLabel, QHBoxLayout


class GimbalAngles(QWidget):
    """Pitch/Yaw 角度显示"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        self.pitch_label = self._create_angle_label("P")
        layout.addWidget(self.pitch_label)

        self.yaw_label = self._create_angle_label("Y")
        layout.addWidget(self.yaw_label)

    def _create_angle_label(self, prefix: str) -> QLabel:
        label = QLabel(f"{prefix}: 0.0°")
        label.setStyleSheet("""
            color: #00FF00;
            font-size: 14px;
            font-family: 'Consolas', monospace;
            background: transparent;
        """)
        return label

    def _get_color(self, angle: float, threshold: float) -> str:
        abs_angle = abs(angle)
        if abs_angle > threshold:
            return "#FF3333"
        if abs_angle > threshold * 0.7:
            return "#FFAA00"
        return "#00FF00"

    def update_angles(self, pitch: float, yaw: float) -> None:
        """更新角度"""
        pitch_color = self._get_color(pitch, 30)
        yaw_color = self._get_color(yaw, 90)

        sign_p = "+" if pitch > 0 else ""
        sign_y = "+" if yaw > 0 else ""

        self.pitch_label.setText(f"P: {sign_p}{pitch:.1f}°")
        self.pitch_label.setStyleSheet(
            f"color: {pitch_color}; font-size: 14px; font-family: 'Consolas', monospace; background: transparent;"
        )

        self.yaw_label.setText(f"Y: {sign_y}{yaw:.1f}°")
        self.yaw_label.setStyleSheet(
            f"color: {yaw_color}; font-size: 14px; font-family: 'Consolas', monospace; background: transparent;"
        )

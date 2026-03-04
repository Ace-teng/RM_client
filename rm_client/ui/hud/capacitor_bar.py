# rm_client/ui/hud/capacitor_bar.py
"""超级电容条组件。"""
from qtpy.QtWidgets import QWidget, QProgressBar, QLabel, QHBoxLayout


class CapacitorBar(QWidget):
    """超级电容条组件"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self.bar = QProgressBar()
        self.bar.setFixedSize(300, 12)
        self.bar.setTextVisible(False)
        self.bar.setStyleSheet("""
            QProgressBar {
                background-color: rgba(0, 0, 0, 0.5);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 2px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00AA00, stop:1 #00FF00);
                border-radius: 1px;
            }
        """)
        layout.addWidget(self.bar)

        self.value_label = QLabel("100%")
        self.value_label.setFixedWidth(45)
        self.value_label.setStyleSheet("""
            color: #FFFFFF;
            font-size: 12px;
            font-family: 'Consolas', monospace;
        """)
        layout.addWidget(self.value_label)

    def update_capacitor(self, current: float, max_value: float) -> None:
        """更新电容值"""
        percentage = int((current / max_value) * 100) if max_value > 0 else 0
        self.bar.setMaximum(100)
        self.bar.setValue(percentage)
        self.value_label.setText(f"{percentage}%")

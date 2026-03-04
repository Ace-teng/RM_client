# rm_client/ui/hud/base_widget.py
"""HUD 组件基类与通用面板、标签。"""
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QWidget, QLabel, QFrame


class HUDWidget(QWidget):
    """HUD 组件基类：透明背景、不拦截鼠标。"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(Qt.FramelessWindowHint)

    def set_position(self, x: int, y: int) -> None:
        """设置组件位置"""
        self.move(x, y)


class HUDPanel(QFrame):
    """带背景的 HUD 面板。"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("hud-panel")
        self.setStyleSheet("""
            QFrame#hud-panel {
                background-color: rgba(0, 0, 0, 0.6);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 4px;
            }
        """)


class HUDLabel(QLabel):
    """HUD 文字标签。"""

    def __init__(self, text: str = "", parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QLabel {
                color: #FFFFFF;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 14px;
                background: transparent;
            }
        """)

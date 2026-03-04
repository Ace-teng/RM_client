# rm_client/ui/styles/colors.py
# HUD 颜色常量，使用 QtPy 以兼容 PyQt5/6、PySide2/6

from qtpy.QtGui import QColor


class HUDColors:
    """HUD 颜色常量"""

    # 主题色
    PRIMARY = QColor("#00FF00")   # 主要信息 - 绿色
    WARNING = QColor("#FFAA00")   # 警告 - 橙色
    DANGER = QColor("#FF3333")    # 危险 - 红色
    INFO = QColor("#00AAFF")      # 信息 - 蓝色
    PURPLE = QColor("#AA55FF")    # 自瞄框 - 紫色

    # 背景色
    BG_DARK = QColor(0, 0, 0, 153)        # rgba(0,0,0,0.6)
    BG_LIGHT = QColor(255, 255, 255, 26)  # rgba(255,255,255,0.1)
    BORDER = QColor(255, 255, 255, 51)    # rgba(255,255,255,0.2)

    # 文字色
    TEXT_PRIMARY = QColor("#FFFFFF")
    TEXT_SECONDARY = QColor(255, 255, 255, 179)  # rgba(255,255,255,0.7)
    TEXT_MUTED = QColor(255, 255, 255, 102)     # rgba(255,255,255,0.4)

    @staticmethod
    def to_stylesheet(color: QColor) -> str:
        """转换为 QSS/CSS 格式"""
        return f"rgba({color.red()}, {color.green()}, {color.blue()}, {color.alpha()})"

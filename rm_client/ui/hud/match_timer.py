# rm_client/ui/hud/match_timer.py
"""比赛时间显示。"""
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QLabel


class MatchTimer(QLabel):
    """比赛时间显示"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self._update_style("normal")
        self.setText("7:00")

    def _update_style(self, state: str) -> None:
        base_style = """
            font-size: 28px;
            font-weight: bold;
            font-family: 'Consolas', monospace;
            background: transparent;
        """
        if state == "danger":
            self.setStyleSheet(base_style + " color: #FF3333;")
        elif state == "warning":
            self.setStyleSheet(base_style + " color: #FFAA00;")
        else:
            self.setStyleSheet(base_style + " color: #FFFFFF;")

    def update_time(self, seconds: int) -> None:
        """更新时间"""
        minutes = seconds // 60
        secs = seconds % 60
        self.setText(f"{minutes}:{secs:02d}")

        if seconds < 30:
            self._update_style("danger")
        elif seconds < 60:
            self._update_style("warning")
        else:
            self._update_style("normal")

"""
单行字段 — 参考图：圆角矩形、浅青 1px 边框、深色底，左标签右值。
"""
from qtpy.QtWidgets import QFrame, QHBoxLayout, QLabel, QWidget

from rm_client.ui.styles import STYLE_FIELD_ROW


class FieldRow(QFrame):
    """一行：左侧标签、右侧取值，整体为圆角边框块。"""

    def __init__(self, label: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setStyleSheet(STYLE_FIELD_ROW)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(12)
        self._label = QLabel(label)
        self._value = QLabel("—")
        self._value.setStyleSheet("font-weight: bold;")
        layout.addWidget(self._label)
        layout.addStretch()
        layout.addWidget(self._value)

    def set_value(self, text: str) -> None:
        self._value.setText(text)

    def set_value_style(self, style: str) -> None:
        self._value.setStyleSheet(style)

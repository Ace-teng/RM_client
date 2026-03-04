"""
右侧信息面板（精简）— 修改3：无滚动条，仅 3–5 项核心数据，紧凑排版。
"""
import time
from typing import Tuple

from qtpy.QtCore import QTimer
from qtpy.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from rm_client.ui.styles import (
    STYLE_BTN,
    STYLE_INFO_ITEM,
    STYLE_RIGHT_INFO_PANEL,
    STYLE_VALUE_BAD,
    STYLE_VALUE_OK,
    TEXT_WHITE,
)


def _info_row(icon: str, label: str, parent: QWidget) -> Tuple[QFrame, QLabel]:
    """一行：小图标 + 标签 + 值，padding 4px 0，gap 6px。"""
    row = QFrame(parent)
    row.setStyleSheet(STYLE_INFO_ITEM)
    layout = QHBoxLayout(row)
    layout.setContentsMargins(0, 4, 0, 4)
    layout.setSpacing(6)
    icon_lbl = QLabel(icon)
    icon_lbl.setStyleSheet(f"color: {TEXT_WHITE}; font-size: 12px; min-width: 18px;")
    layout.addWidget(icon_lbl)
    layout.addWidget(QLabel(label))
    val = QLabel("—")
    val.setStyleSheet("font-weight: bold; font-size: 12px;")
    layout.addStretch()
    layout.addWidget(val)
    return row, val


class RightInfoPanel(QFrame):
    """右侧精简面板：仅 5 项 — 连接 | 阶段 | 剩余时间 | 血量/关键 | 复制诊断。无滚动条。"""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setStyleSheet(STYLE_RIGHT_INFO_PANEL)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(2)

        self._row_conn, self._val_conn = _info_row("●", "连接", self)
        self._row_phase, self._val_phase = _info_row("◷", "阶段", self)
        self._row_time, self._val_time = _info_row("⏱", "剩余(s)", self)
        self._row_hp, self._val_hp = _info_row("❤", "血量", self)
        layout.addWidget(self._row_conn)
        layout.addWidget(self._row_phase)
        layout.addWidget(self._row_time)
        layout.addWidget(self._row_hp)

        copy_btn = QPushButton("复制诊断")
        copy_btn.setStyleSheet(STYLE_BTN)
        copy_btn.setMaximumWidth(120)
        copy_btn.clicked.connect(self._copy_diagnostic)
        layout.addWidget(copy_btn)

        layout.addStretch()

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._refresh)
        self._timer.start(500)

    @staticmethod
    def _format_ago(ts: float | None) -> str:
        if ts is None or ts <= 0:
            return "—"
        d = time.time() - ts
        if d < 1:
            return "刚刚"
        if d < 60:
            return f"{int(d)}s前"
        return f"{int(d // 60)}m前"

    def _refresh(self) -> None:
        from rm_client.core.model.datacenter import DataCenter

        dc = DataCenter()
        ls = dc.link_status
        gs = dc.game_state

        mqtt = ls.get("mqtt_connected", False)
        self._val_conn.setText("已连接" if mqtt else "未连接")
        self._val_conn.setStyleSheet(STYLE_VALUE_OK if mqtt else STYLE_VALUE_BAD)
        self._val_phase.setText(str(getattr(gs, "game_phase", "?")) if gs else "—")
        self._val_time.setText(str(getattr(gs, "remaining_time_sec", "?")) if gs else "—")
        op = dc.operator_display_state
        hp_text = f"{op.hp_self}/{op.hp_enemy}" if op else "—"
        self._val_hp.setText(hp_text)

    def _copy_diagnostic(self) -> None:
        from rm_client.core.model.datacenter import DataCenter

        dc = DataCenter()
        ls = dc.link_status
        lines = [
            "=== 客户端诊断 ===",
            f"MQTT: {'已连接' if ls.get('mqtt_connected') else '未连接'}",
            f"MQTT数据: {self._format_ago(ls.get('mqtt_last_update'))}",
            f"图传: {self._format_ago(ls.get('video_last_update'))}",
        ]
        QApplication.clipboard().setText("\n".join(lines))

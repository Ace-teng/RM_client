"""
步兵视图左侧面板 — 严格按参考图：AUTO-AIM STATUS / SUPER CAPACITOR / TOTAL ENERGY / YAW / MINI-MAP / TARGET SCAN。
"""
from qtpy.QtCore import QTimer
from qtpy.QtGui import QPainter, QPen, QColor
from qtpy.QtWidgets import (
    QCheckBox,
    QFrame,
    QLabel,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from rm_client.ui.styles import NEON_CYAN, NEON_GREEN, STYLE_PANEL, STYLE_PANEL_TITLE, TEXT_WHITE


class _AimStatusIcon(QFrame):
    """参考图：圆形靶心小图标。"""
    def paintEvent(self, event):
        super().paintEvent(event)
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        cx, cy = self.width() // 2, self.height() // 2
        r = min(cx, cy) - 2
        p.setPen(QPen(QColor(0, 229, 255), 1))
        p.setBrush(QColor(0, 0, 0, 0))
        p.drawEllipse(cx - r, cy - r, r * 2, r * 2)
        p.drawLine(cx - r, cy, cx + r, cy)
        p.drawLine(cx, cy - r, cx, cy + r)


class InfantryLeftPanel(QFrame):
    """
    参考图左侧竖条：
    - AUTO-AIM STATUS（图标 + LOCKED 蓝字）
    - SUPER CAPACITOR（绿条 88%）
    - TOTAL ENERGY（548V）
    - YAW（142.6°）
    - MINI-MAP（嵌入 MapWidget）
    - TARGET SCAN（标题+关闭X、ENEMY #01 #02 #03、Objective 勾选）
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFixedWidth(220)
        self.setStyleSheet(STYLE_PANEL)
        layout = QVBoxLayout(self)
        layout.setSpacing(8)

        # ——— AUTO-AIM STATUS ———
        title_aim = QLabel("AUTO-AIM STATUS")
        title_aim.setStyleSheet(STYLE_PANEL_TITLE)
        layout.addWidget(title_aim)
        aim_row = QFrame()
        aim_row.setStyleSheet("background: transparent;")
        from qtpy.QtWidgets import QHBoxLayout
        arl = QHBoxLayout(aim_row)
        arl.setContentsMargins(0, 0, 0, 0)
        self._aim_icon = _AimStatusIcon()
        self._aim_icon.setFixedSize(28, 28)
        self._aim_icon.setStyleSheet("background: #1e293b; border-radius: 14px;")
        arl.addWidget(self._aim_icon)
        self._aim_label = QLabel("LOCKED")
        self._aim_label.setStyleSheet(f"color: {NEON_CYAN}; font-weight: bold; font-size: 12px;")
        arl.addWidget(self._aim_label)
        arl.addStretch()
        layout.addWidget(aim_row)

        # ——— SUPER CAPACITOR ———
        cap_title = QLabel("SUPER CAPACITOR")
        cap_title.setStyleSheet(f"color: {TEXT_WHITE}; font-size: 11px;")
        layout.addWidget(cap_title)
        self._cap_bar = QProgressBar()
        self._cap_bar.setRange(0, 100)
        self._cap_bar.setValue(88)
        self._cap_bar.setStyleSheet(f"""
            QProgressBar {{
                background: #1e293b;
                border: 1px solid {NEON_CYAN};
                border-radius: 4px;
                height: 10px;
            }}
            QProgressBar::chunk {{
                background: {NEON_GREEN};
                border-radius: 3px;
            }}
        """)
        self._cap_bar.setTextVisible(True)
        self._cap_bar.setFormat("%p%")
        layout.addWidget(self._cap_bar)

        # ——— TOTAL ENERGY ———
        energy_title = QLabel("TOTAL ENERGY")
        energy_title.setStyleSheet(f"color: {TEXT_WHITE}; font-size: 11px;")
        layout.addWidget(energy_title)
        self._energy_label = QLabel("548V")
        self._energy_label.setStyleSheet(f"color: {NEON_CYAN}; font-size: 13px; font-weight: bold;")
        layout.addWidget(self._energy_label)

        # ——— YAW ———
        yaw_title = QLabel("YAW")
        yaw_title.setStyleSheet(f"color: {TEXT_WHITE}; font-size: 11px;")
        layout.addWidget(yaw_title)
        self._yaw_label = QLabel("142.6°")
        self._yaw_label.setStyleSheet(f"color: {TEXT_WHITE}; font-size: 12px;")
        layout.addWidget(self._yaw_label)

        # ——— MINI-MAP ———
        title_map = QLabel("MINI-MAP")
        title_map.setStyleSheet(STYLE_PANEL_TITLE)
        layout.addWidget(title_map)
        from rm_client.ui.radar.map_widget import MapWidget
        self._minimap = MapWidget(self)
        self._minimap.setMinimumHeight(140)
        layout.addWidget(self._minimap)

        # ——— TARGET SCAN（参考图：标题行带 X 关闭、列表、Objective 勾选）———
        scan_header = QFrame()
        scan_header.setStyleSheet("background: transparent;")
        shl = QHBoxLayout(scan_header)
        shl.setContentsMargins(0, 0, 0, 0)
        title_scan = QLabel("TARGET SCAN")
        title_scan.setStyleSheet(STYLE_PANEL_TITLE)
        shl.addWidget(title_scan)
        shl.addStretch()
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(22, 22)
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background: #1e293b;
                color: {TEXT_WHITE};
                border: 1px solid {NEON_CYAN};
                border-radius: 4px;
                font-size: 12px;
            }}
            QPushButton:hover {{ border-color: #ef4444; }}
        """)
        close_btn.setToolTip("关闭目标扫描")
        shl.addWidget(close_btn)
        layout.addWidget(scan_header)

        self._target_list = QLabel("ENEMY #01 —\nENEMY #02 —\nENEMY #03  HP: 64%")
        self._target_list.setStyleSheet(f"color: {TEXT_WHITE}; font-size: 10px;")
        self._target_list.setWordWrap(True)
        layout.addWidget(self._target_list)

        self._obj_check = QCheckBox("Objective")
        self._obj_check.setStyleSheet(f"color: {TEXT_WHITE}; font-size: 11px;")
        self._obj_check.setChecked(False)
        layout.addWidget(self._obj_check)

        layout.addStretch()

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._refresh)
        self._timer.start(400)

    def _refresh(self) -> None:
        from rm_client.core.model.datacenter import DataCenter
        from rm_client.ui.styles import NEON_RED

        dc = DataCenter()
        role = dc.current_operator_role
        self.setVisible(role in ("infantry1", "infantry2"))
        state = dc.operator_display_state
        if state is None:
            return
        self._cap_bar.setValue(int(state.capacitor_pct * 100))
        self._energy_label.setText(f"{int(state.energy_current)}V")
        self._yaw_label.setText(f"{state.infantry_yaw_deg:.1f}°")
        status = state.aim_status
        if status == "targeting":
            self._aim_label.setText("LOCKED")
            self._aim_label.setStyleSheet(f"color: {NEON_CYAN}; font-weight: bold; font-size: 12px;")
        elif status == "notarget":
            self._aim_label.setText("NOT LOCKED")
            self._aim_label.setStyleSheet(f"color: {NEON_CYAN}; font-weight: bold; font-size: 12px;")
        else:
            self._aim_label.setText("OFFLINE")
            self._aim_label.setStyleSheet(f"color: {NEON_RED}; font-weight: bold; font-size: 12px;")

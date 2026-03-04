"""
步兵视图右侧面板 — 严格按参考图：仅 4 块 — SYSTEM STATUS / SCORES / MODULE HEALTH / CHAT LOG。
"""
from qtpy.QtCore import QTimer
from qtpy.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from rm_client.ui.styles import (
    BLUE_TEAM,
    NEON_CYAN,
    NEON_GREEN,
    NEON_RED,
    STYLE_PANEL,
    STYLE_PANEL_TITLE,
    TEXT_WHITE,
)


class InfantryRightPanel(QFrame):
    """
    参考图右侧：SYSTEM STATUS（Battery/CPU/Ammo/Latency）、
    SCORES（Team A / Team B）、MODULE HEALTH（三条绿条）、CHAT LOG（空）。
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFixedWidth(260)
        self.setStyleSheet(STYLE_PANEL)
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        # ——— SYSTEM STATUS ———
        title1 = QLabel("SYSTEM STATUS")
        title1.setStyleSheet(STYLE_PANEL_TITLE)
        layout.addWidget(title1)
        self._lbl_battery = QLabel("BATTERY: 74% [64V]")
        self._lbl_cpu = QLabel("CPU TEMP: 48°C")
        self._lbl_ammo = QLabel("AMMO: 124/320")
        self._lbl_latency = QLabel("LATENCY: 14ms")
        for w in (self._lbl_battery, self._lbl_cpu, self._lbl_ammo, self._lbl_latency):
            w.setStyleSheet(f"color: {TEXT_WHITE}; font-size: 11px;")
        layout.addWidget(self._lbl_battery)
        layout.addWidget(self._lbl_cpu)
        layout.addWidget(self._lbl_ammo)
        layout.addWidget(self._lbl_latency)

        # ——— SCORES ———
        title2 = QLabel("SCORES")
        title2.setStyleSheet(STYLE_PANEL_TITLE)
        layout.addWidget(title2)
        scores_row = QFrame()
        scores_row.setStyleSheet("background: transparent;")
        sl = QVBoxLayout(scores_row)
        sl.setSpacing(4)
        self._lbl_team_a = QLabel("TEAM A: 520")
        self._lbl_team_a.setStyleSheet(f"color: {BLUE_TEAM}; font-weight: bold; font-size: 12px;")
        self._lbl_team_b = QLabel("TEAM B: 485")
        self._lbl_team_b.setStyleSheet(f"color: {NEON_RED}; font-weight: bold; font-size: 12px;")
        sl.addWidget(self._lbl_team_a)
        sl.addWidget(self._lbl_team_b)
        layout.addWidget(scores_row)

        # ——— MODULE HEALTH ———
        title3 = QLabel("MODULE HEALTH")
        title3.setStyleSheet(STYLE_PANEL_TITLE)
        layout.addWidget(title3)
        self._bar_gimbal = QProgressBar()
        self._bar_chassis = QProgressBar()
        self._bar_turret = QProgressBar()
        _bar_style = f"""
            QProgressBar {{
                background: #1e293b;
                border: 1px solid {NEON_CYAN};
                border-radius: 3px;
                height: 10px;
                text-align: center;
            }}
            QProgressBar::chunk {{
                background: {NEON_GREEN};
                border-radius: 2px;
            }}
        """
        for bar, label_text, val in [
            (self._bar_gimbal, "Gimbal", 100),
            (self._bar_chassis, "Chassis", 92),
            (self._bar_turret, "Turret", 95),
        ]:
            bar.setRange(0, 100)
            bar.setValue(val)
            bar.setStyleSheet(_bar_style)
            bar.setTextVisible(True)
            bar.setFormat("%p%")
            lbl = QLabel(f"{label_text}:")
            lbl.setStyleSheet(f"color: {TEXT_WHITE}; font-size: 11px; min-width: 60px;")
            row = QFrame()
            row.setStyleSheet("background: transparent;")
            rl = QHBoxLayout(row)
            rl.setContentsMargins(0, 2, 0, 2)
            rl.addWidget(lbl)
            rl.addWidget(bar, 1)
            layout.addWidget(row)

        # ——— CHAT LOG ———
        title4 = QLabel("CHAT LOG")
        title4.setStyleSheet(STYLE_PANEL_TITLE)
        layout.addWidget(title4)
        self._chat = QTextEdit()
        self._chat.setReadOnly(True)
        self._chat.setPlaceholderText("(empty)")
        self._chat.setMaximumHeight(120)
        self._chat.setStyleSheet(f"""
            QTextEdit {{
                background: #0f172a;
                border: 1px solid {NEON_CYAN};
                border-radius: 4px;
                color: {TEXT_WHITE};
                font-size: 11px;
            }}
        """)
        layout.addWidget(self._chat)

        layout.addStretch()

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._refresh)
        self._timer.start(400)

    def _refresh(self) -> None:
        from rm_client.core.model.datacenter import DataCenter

        dc = DataCenter()
        role = dc.current_operator_role
        self.setVisible(role in ("infantry1", "infantry2"))
        state = dc.operator_display_state
        if state is None:
            return
        cap_pct = int(state.capacitor_pct * 100)
        self._lbl_battery.setText(f"BATTERY: {cap_pct}% [{int(state.energy_current)}V]")
        self._lbl_ammo.setText(f"AMMO: {state.ammo_count}/{state.ammo_limit}")
        # 分数、延迟等占位
        gs = dc.game_state
        if gs and hasattr(gs, "red_score") and hasattr(gs, "blue_score"):
            self._lbl_team_a.setText(f"TEAM A: {getattr(gs, 'blue_score', 520)}")
            self._lbl_team_b.setText(f"TEAM B: {getattr(gs, 'red_score', 485)}")

"""
原有全局 UI 样式（保留兼容）。
"""
# 色值：背景
BG_DARK = "#0d0d0d"
BG_PANEL = "#1a1a1a"
BG_PANEL_ALT = "#252525"
BG_FIELD = "#1e293b"
# 色值：强调与状态
NEON_CYAN = "#00e5ff"
NEON_PURPLE = "#a855f7"
NEON_GREEN = "#22c55e"
NEON_RED = "#ef4444"
NEON_ORANGE = "#f97316"
BLUE_TEAM = "#3b82f6"
# 色值：文字
TEXT_WHITE = "#ffffff"
TEXT_PRIMARY = "#e5e5e5"
TEXT_MUTED = "#94a3b8"
BORDER_SUBTLE = "#334155"

STYLE_PANEL = f"""
    QFrame {{
        background-color: {BG_PANEL};
        border: 1px solid {BORDER_SUBTLE};
        border-left: 3px solid {NEON_CYAN};
        border-radius: 6px;
        padding: 8px;
    }}
    QLabel {{
        color: {TEXT_WHITE};
        font-size: 12px;
    }}
"""

STYLE_PANEL_TITLE = f"""
    font-weight: bold;
    font-size: 11px;
    color: {NEON_CYAN};
    letter-spacing: 0.5px;
    border-bottom: 1px solid {NEON_CYAN};
    padding-bottom: 4px;
    margin-bottom: 6px;
"""

STYLE_FIELD_ROW = f"""
    QFrame {{
        background-color: {BG_FIELD};
        border: 1px solid {NEON_CYAN};
        border-radius: 4px;
        padding: 6px 10px;
        min-height: 24px;
    }}
    QLabel {{
        color: {TEXT_WHITE};
        font-size: 11px;
    }}
"""

STYLE_VALUE_OK = f"color: {NEON_GREEN}; font-weight: bold;"
STYLE_VALUE_BAD = f"color: {NEON_RED}; font-weight: bold;"

STYLE_BTN = f"""
    QPushButton {{
        background-color: {BG_PANEL_ALT};
        color: {TEXT_WHITE};
        border: 1px solid {NEON_CYAN};
        border-radius: 4px;
        padding: 6px 12px;
        font-size: 11px;
    }}
    QPushButton:hover {{
        background-color: #2d2d2d;
        border-color: {NEON_GREEN};
    }}
    QPushButton:pressed {{
        background-color: #333;
    }}
"""

STYLE_MAIN = f"""
    QMainWindow {{
        background-color: {BG_DARK};
    }}
    QWidget {{
        background-color: transparent;
    }}
    QScrollArea {{
        background-color: {BG_DARK};
        border: none;
    }}
    QStatusBar {{
        background-color: {BG_PANEL};
        color: {TEXT_WHITE};
        border-top: 1px solid {BORDER_SUBTLE};
        font-size: 11px;
    }}
"""

STYLE_PLACEHOLDER_NO_SIGNAL = "color: #64748b; font-size: 28px; font-weight: bold;"

STYLE_FLOATING = """
    background-color: rgba(26, 26, 26, 0.92);
    border: none;
    outline: none;
    border-radius: 6px;
    padding: 8px;
"""

STYLE_RIGHT_INFO_PANEL = f"""
    QFrame {{
        background-color: {BG_DARK};
        border: none;
        padding: 12px;
    }}
    QLabel {{
        color: {TEXT_WHITE};
        font-size: 12px;
        line-height: 1.4;
    }}
"""

STYLE_INFO_ITEM = f"""
    QFrame {{
        background: transparent;
        padding: 4px 0;
        min-height: 1px;
    }}
    QLabel {{
        color: {TEXT_WHITE};
        font-size: 12px;
    }}
"""


def apply_app_style(app) -> None:
    """对 QApplication 应用全局深色主题。"""
    app.setStyleSheet(STYLE_MAIN)

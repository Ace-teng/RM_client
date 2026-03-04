"""
UI 样式包：原有 QSS 常量 + HUD 重构用 QSS/颜色。

- 原有导入保持不变：from rm_client.ui.styles import STYLE_PANEL, apply_app_style 等
- HUD 重构：from rm_client.ui.styles import HUDColors；QSS 见 hud_style.qss
"""
from ._legacy import *  # noqa: F401, F403
from .colors import HUDColors

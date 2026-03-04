"""
操作角色选择器 — 英雄/步兵切换（unit-toggle），专业游戏 HUD 样式。
深色模式下白字可读，选中态金底边。写入 DataCenter.current_operator_role。
"""
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QComboBox, QFrame, QHBoxLayout, QLabel, QWidget

from rm_client.core.model.operator_state import OPERATOR_ROLE_LABELS, OPERATOR_ROLES

# 专业 HUD 单位切换样式：白字、半透明深底、金底边选中
_STYLE_UNIT_TOGGLE = """
    QComboBox {
        color: #FFFFFF;
        background: rgba(0, 0, 0, 0.45);
        padding: 8px 16px;
        border-radius: 6px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-bottom: 2px solid #FFD700;
        font-size: 12px;
        min-height: 28px;
    }
    QComboBox:hover {
        background: rgba(0, 0, 0, 0.55);
        border: 1px solid rgba(255, 255, 255, 0.25);
        border-bottom: 2px solid #FFD700;
    }
    QComboBox::drop-down {
        border: none;
        padding-right: 10px;
        background: transparent;
    }
    QComboBox::down-arrow {
        image: none;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 6px solid #FFFFFF;
        margin-right: 4px;
        width: 0;
        height: 0;
    }
    QComboBox QAbstractItemView {
        color: #FFFFFF;
        background: rgba(0, 0, 0, 0.9);
        selection-background-color: rgba(255, 255, 255, 0.2);
        selection-color: #FFFFFF;
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 4px;
    }
"""


class OperatorRoleSelector(QFrame):
    """英雄/步兵等单位切换：HUD 风格，深色下白字可见，选中金底边。"""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setMaximumWidth(320)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 4, 0, 4)
        lbl = QLabel("角色:")
        lbl.setStyleSheet(
            "color: #FFFFFF; font-size: 12px; font-weight: bold; "
            "background: transparent;"
        )
        layout.addWidget(lbl)
        self._combo = QComboBox()
        self._combo.setStyleSheet(_STYLE_UNIT_TOGGLE)
        for r in OPERATOR_ROLES:
            self._combo.addItem(OPERATOR_ROLE_LABELS.get(r, r), r)
        self._combo.setCurrentIndex(0)
        self._combo.currentIndexChanged.connect(self._on_role_changed)
        layout.addWidget(self._combo, 1)
        self._on_role_changed()

    def _on_role_changed(self) -> None:
        from rm_client.core.model.datacenter import DataCenter

        idx = self._combo.currentIndex()
        role = self._combo.itemData(idx) if idx >= 0 else "hero"
        DataCenter().current_operator_role = role

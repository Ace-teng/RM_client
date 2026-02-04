"""
赛事指令控制面板 — Phase 6，按钮触发指令下发。

通过 on_command 回调通知上层，不直接访问 comms。
"""
from typing import Callable, Optional

from qtpy.QtWidgets import QFrame, QGridLayout, QLabel, QMessageBox, QPushButton, QVBoxLayout, QWidget


class CommandPanel(QFrame):
    """赛事指令：性能体系、兑换发弹量、空中支援。点击后通过回调发送。"""

    def __init__(
        self,
        on_performance_mode: Optional[Callable[[int], bool]] = None,
        on_ammo_exchange: Optional[Callable[[], bool]] = None,
        on_air_support: Optional[Callable[[], bool]] = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setFrameStyle(QFrame.StyledPanel)
        self._on_perf = on_performance_mode
        self._on_ammo = on_ammo_exchange
        self._on_air = on_air_support

        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        title = QLabel("赛事指令")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)

        grid = QGridLayout()
        for i, mode_id in enumerate([1, 2, 3]):
            btn = QPushButton("性能体系 %s" % mode_id)
            btn.clicked.connect(lambda checked=False, m=mode_id: self._do_performance(m))
            grid.addWidget(btn, 0, i)
        layout.addLayout(grid)

        btn_ammo = QPushButton("兑换发弹量")
        btn_ammo.clicked.connect(self._do_ammo)
        layout.addWidget(btn_ammo)

        btn_air = QPushButton("空中支援")
        btn_air.clicked.connect(self._do_air)
        layout.addWidget(btn_air)

        layout.addStretch()

    def _do_performance(self, mode_id: int) -> None:
        if self._on_perf:
            ok = self._on_perf(mode_id)
            if not ok:
                QMessageBox.warning(self, "发送失败", "MQTT 未连接，请先连接赛事引擎。")

    def _do_ammo(self) -> None:
        if self._on_ammo:
            ok = self._on_ammo()
            if not ok:
                QMessageBox.warning(self, "发送失败", "MQTT 未连接，请先连接赛事引擎。")

    def _do_air(self) -> None:
        if self._on_air:
            ok = self._on_air()
            if not ok:
                QMessageBox.warning(self, "发送失败", "MQTT 未连接，请先连接赛事引擎。")

"""
主窗口 — 严格按参考图布局：角色切换后左侧/顶部/右侧内容与底部状态栏均随角色变化。
"""
from qtpy.QtCore import Qt, QTimer, Signal
from qtpy.QtGui import QImage, QPixmap
from qtpy.QtWidgets import (
    QFrame,
    QLabel,
    QMainWindow,
    QSplitter,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from rm_client.ui.control.infantry_right_panel import InfantryRightPanel
from rm_client.ui.control.infantry_top_bar import InfantryTopBar
from rm_client.ui.control.operator_role_selector import OperatorRoleSelector
from rm_client.ui.control.right_info_panel import RightInfoPanel
from rm_client.ui.video_area import VideoArea
from rm_client.ui.hud.hud_overlay import HUDOverlay


class MainWindow(QMainWindow):
    """
    主窗口：图传居中；左侧仅步兵显示；右侧按角色切换 — 英雄为完整面板，步兵为参考图四块（SYSTEM STATUS / SCORES / MODULE HEALTH / CHAT LOG）。
    """
    _status_signal = Signal(str)
    _video_frame_signal = Signal(object)

    def __init__(
        self,
        command_sender=None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._command_sender = command_sender
        self.setWindowTitle("RoboMaster 自定义客户端")
        self.setMinimumSize(960, 540)
        self.resize(1280, 720)
        from rm_client.ui.styles import BG_DARK
        self.setStyleSheet(f"QMainWindow {{ background-color: {BG_DARK}; }}")

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(4, 4, 4, 4)
        main_layout.setSpacing(0)

        # 顶栏：仅步兵显示，参考图 "ROBOMASTER INFANTRY 1 | FPV | 70% 30% 16:9"
        from rm_client.ui.control.infantry_left_panel import InfantryLeftPanel
        self._infantry_top_bar = InfantryTopBar(self)
        self._infantry_top_bar.hide()
        main_layout.addWidget(self._infantry_top_bar)

        splitter = QSplitter(Qt.Horizontal)
        self._infantry_left_panel = InfantryLeftPanel(self)
        self._infantry_left_panel.hide()
        splitter.addWidget(self._infantry_left_panel)

        self._video_area = VideoArea()
        splitter.addWidget(self._video_area)

        # 右侧：按角色切换 — 英雄=完整面板，步兵=参考图四块
        self._right_stacked = QStackedWidget()

        # 英雄页：精简右侧信息面板（修改3）— 仅 5 项核心数据，无滚动条
        hero_page = QWidget()
        hero_layout = QVBoxLayout(hero_page)
        hero_layout.setContentsMargins(0, 0, 0, 0)
        hero_layout.addWidget(RightInfoPanel(self))
        from rm_client.ui.styles import STYLE_PANEL, STYLE_PANEL_TITLE, TEXT_WHITE
        self._plugin_frame = QFrame()
        self._plugin_frame.setStyleSheet(STYLE_PANEL)
        self._plugin_layout = QVBoxLayout(self._plugin_frame)
        self._plugin_layout.setContentsMargins(8, 6, 8, 6)
        plugin_label = QLabel("PLUGINS")
        plugin_label.setStyleSheet(STYLE_PANEL_TITLE)
        self._plugin_layout.addWidget(plugin_label)
        self._plugin_layout.addStretch()
        hero_layout.addWidget(self._plugin_frame)
        hero_page.setMaximumWidth(280)
        hero_page.setStyleSheet(f"background-color: {BG_DARK}; padding: 0;")
        self._right_stacked.addWidget(hero_page)

        # 步兵页：角色选择 + 参考图右侧四块（InfantryRightPanel）
        infantry_page = QWidget()
        infantry_layout = QVBoxLayout(infantry_page)
        infantry_layout.setContentsMargins(0, 0, 0, 0)
        self._infantry_right = InfantryRightPanel(self)
        infantry_layout.addWidget(self._infantry_right)
        infantry_layout.addStretch()
        infantry_page.setMaximumWidth(280)
        infantry_page.setStyleSheet(f"background-color: {BG_DARK};")
        self._right_stacked.addWidget(infantry_page)

        # 右侧整体：无滚动条（overflow hidden），角色选择 + 精简内容
        right_wrapper = QWidget()
        right_wrapper.setStyleSheet(
            f"background-color: {BG_DARK}; padding: 12px; font-size: 12px;"
        )
        right_layout = QVBoxLayout(right_wrapper)
        right_layout.setContentsMargins(12, 12, 12, 12)
        right_layout.setSpacing(6)
        right_layout.addWidget(OperatorRoleSelector(self))
        right_layout.addWidget(self._right_stacked, 1)
        right_wrapper.setMaximumWidth(320)
        splitter.addWidget(right_wrapper)

        main_layout.addWidget(splitter)

        self._status_signal.connect(self.statusBar().showMessage)
        self._video_frame_signal.connect(self._on_video_frame)
        self.set_status_message("就绪 | DataCenter 已创建 | MQTT 连接中…")

        # HUD 叠加层：只覆盖图传区域，不盖住右侧栏，避免右上角黑框/重叠
        self._hud_overlay = HUDOverlay(robot_type="infantry1", parent=self._video_area)
        self._hud_overlay.setGeometry(self._video_area.rect())
        self._hud_overlay.raise_()

        from rm_client.core.model.datacenter import DataCenter
        dc = DataCenter()
        dc.subscribe(self._on_dc_update)

        # 定时按角色刷新：顶栏/左侧/右侧堆叠页/底部状态栏
        self._layout_timer = QTimer(self)
        self._layout_timer.timeout.connect(self._sync_layout_to_role)
        self._layout_timer.start(200)

    def _sync_layout_to_role(self) -> None:
        from rm_client.core.model.datacenter import DataCenter
        from datetime import datetime

        dc = DataCenter()
        role = dc.current_operator_role
        is_infantry = role in ("infantry1", "infantry2")

        self._infantry_top_bar.setVisible(is_infantry)
        self._infantry_left_panel.setVisible(is_infantry)
        if is_infantry:
            self._right_stacked.setCurrentIndex(1)
            clock = datetime.now().strftime("%H:%M:%S")
            self.statusBar().showMessage(
                f"SYSTEM ACTIVE | ROBOMASTER INFANTRY-1 | CLOCK: {clock} | V1.4.2 | PING: 14ms | SIGNAL: EXCELLENT"
            )
        else:
            self._right_stacked.setCurrentIndex(0)

    def _on_video_frame(self, frame: object) -> None:
        pi = self._video_area.pixmap_item
        ph = self._video_area.placeholder_text
        if frame is not None and isinstance(frame, QImage):
            pi.setPixmap(QPixmap.fromImage(frame))
            pi.setVisible(True)
            ph.setVisible(False)
        else:
            pi.setVisible(False)
            ph.setVisible(True)

    def _on_dc_update(self, key: str, value: object) -> None:
        if key == "game_state" and value is not None:
            try:
                text = "game_phase=%s remaining_time_sec=%s" % (
                    getattr(value, "game_phase", "?"),
                    getattr(value, "remaining_time_sec", "?"),
                )
                self._status_signal.emit(text)
            except Exception:
                pass
        elif key == "video_frame":
            self._video_frame_signal.emit(value)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        if hasattr(self, "_hud_overlay") and self._hud_overlay is not None:
            self._hud_overlay.setGeometry(self._video_area.rect())

    def set_status_message(self, msg: str) -> None:
        self.statusBar().showMessage(msg)

    def add_plugin_widget(self, widget: QWidget, title: str = "") -> None:
        idx = self._plugin_layout.count() - 1
        if idx < 0:
            idx = 0
        if title:
            lbl = QLabel(title)
            from rm_client.ui.styles import TEXT_WHITE
            lbl.setStyleSheet(f"font-size: 11px; color: {TEXT_WHITE};")
            self._plugin_layout.insertWidget(idx, lbl)
            idx += 1
        self._plugin_layout.insertWidget(idx, widget)

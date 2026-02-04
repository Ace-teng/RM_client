"""
主窗口 — QtPy QMainWindow。

Phase 1：中心图传区、右侧控制面板。Phase 4/5/6：图传、态势、指令。Phase 7：插件区域。
见总文档 §5.1、§5.1.4、§7 Phase 4–7。
"""
from qtpy.QtCore import Qt, Signal
from qtpy.QtGui import QImage, QPixmap
from qtpy.QtWidgets import (
    QFrame,
    QGraphicsPixmapItem,
    QGraphicsScene,
    QGraphicsTextItem,
    QGraphicsView,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QScrollArea,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from rm_client.ui.control.command_panel import CommandPanel
from rm_client.ui.control.game_state_panel import GameStatePanel
from rm_client.ui.radar.map_widget import MapWidget
from rm_client.ui.radar.robot_status_list import RobotStatusList


class MainWindow(QMainWindow):
    """
    主窗口：中心图传区、右侧状态/态势/指令面板。
    只读 DataCenter；指令通过 command_sender 回调发送（§4.5）。
    """
    _status_signal = Signal(str)
    _video_frame_signal = Signal(object)  # QImage | None，从非 UI 线程安全更新图传

    def __init__(
        self,
        command_sender=None,  # CommandSender 实例，用于 Phase 6 指令下发
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._command_sender = command_sender
        self.setWindowTitle("RoboMaster 自定义客户端")
        self.setMinimumSize(960, 540)
        self.resize(1280, 720)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)
        layout.setContentsMargins(4, 4, 4, 4)

        splitter = QSplitter(Qt.Horizontal)

        # 中心：图传显示（Phase 4）
        self._graphics_view = QGraphicsView()
        self._graphics_view.setStyleSheet("background: #1a1a1a;")
        self._graphics_view.setMinimumWidth(640)
        self._scene = QGraphicsScene(0, 0, 640, 360)
        self._graphics_view.setScene(self._scene)
        self._pixmap_item = QGraphicsPixmapItem()
        self._scene.addItem(self._pixmap_item)
        self._placeholder_text = QGraphicsTextItem("图传未连接")
        self._placeholder_text.setDefaultTextColor(Qt.gray)
        self._placeholder_text.setPos(260, 165)
        self._scene.addItem(self._placeholder_text)
        splitter.addWidget(self._graphics_view)

        # 右侧：赛事状态 + 态势图 + 机器人状态 + 赛事指令（Phase 4/5/6）
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.addWidget(GameStatePanel(self))
        right_layout.addWidget(MapWidget(self))
        right_layout.addWidget(RobotStatusList(self))
        cs = self._command_sender
        right_layout.addWidget(
            CommandPanel(
                on_performance_mode=cs.send_performance_mode if cs else None,
                on_ammo_exchange=cs.send_ammo_exchange if cs else None,
                on_air_support=cs.send_air_support if cs else None,
            )
        )
        # Phase 7：插件区域，插件通过 ctx.add_widget 添加控件
        self._plugin_frame = QFrame()
        self._plugin_frame.setFrameStyle(QFrame.StyledPanel)
        self._plugin_layout = QVBoxLayout(self._plugin_frame)
        self._plugin_layout.setContentsMargins(4, 4, 4, 4)
        plugin_label = QLabel("插件")
        plugin_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        self._plugin_layout.addWidget(plugin_label)
        self._plugin_layout.addStretch()
        right_layout.addWidget(self._plugin_frame)
        right_panel.setMaximumWidth(320)
        scroll = QScrollArea()
        scroll.setWidget(right_panel)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        splitter.addWidget(scroll)

        layout.addWidget(splitter)

        self._status_signal.connect(self.statusBar().showMessage)
        self._video_frame_signal.connect(self._on_video_frame)
        self.set_status_message("就绪 | DataCenter 已创建")

        from rm_client.core.model.datacenter import DataCenter
        dc = DataCenter()
        dc.subscribe(self._on_dc_update)

    def _on_video_frame(self, frame: object) -> None:
        """在 UI 线程更新图传画面。frame 为 QImage 或 None。"""
        if frame is not None and isinstance(frame, QImage):
            self._pixmap_item.setPixmap(QPixmap.fromImage(frame))
            self._pixmap_item.setVisible(True)
            self._placeholder_text.setVisible(False)
        else:
            self._pixmap_item.setVisible(False)
            self._placeholder_text.setVisible(True)

    def _on_dc_update(self, key: str, value: object) -> None:
        """DataCenter 通知，通过 signal 转到 UI 线程。"""
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

    def set_status_message(self, msg: str) -> None:
        """供 main 或事件回调更新状态栏。"""
        self.statusBar().showMessage(msg)

    def add_plugin_widget(self, widget: QWidget, title: str = "") -> None:
        """Phase 7：插件调用，将控件加入插件区域。"""
        # 在 addStretch 前插入，保证新控件在「插件」标题下方
        idx = self._plugin_layout.count() - 1
        if idx < 0:
            idx = 0
        if title:
            lbl = QLabel(title)
            lbl.setStyleSheet("font-size: 11px; color: #888;")
            self._plugin_layout.insertWidget(idx, lbl)
            idx += 1
        self._plugin_layout.insertWidget(idx, widget)

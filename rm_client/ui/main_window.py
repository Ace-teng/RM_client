"""
主窗口 — QtPy QMainWindow。

Phase 1：中心图传区、右侧控制面板。Phase 4：图传区显示 DataCenter.video_frame，右侧为状态/血量面板。
见总文档 §5.1、§5.1.4、§7 Phase 4。
"""
from qtpy.QtCore import Qt, Signal
from qtpy.QtGui import QImage, QPixmap
from qtpy.QtWidgets import (
    QGraphicsPixmapItem,
    QGraphicsScene,
    QGraphicsTextItem,
    QGraphicsView,
    QHBoxLayout,
    QMainWindow,
    QSplitter,
    QWidget,
)

from rm_client.ui.control.game_state_panel import GameStatePanel


class MainWindow(QMainWindow):
    """
    主窗口：中心图传区（QGraphicsView）、右侧状态/血量面板。
    只读 DataCenter，不解析协议、不含业务算法（§4.5）。
    """
    _status_signal = Signal(str)
    _video_frame_signal = Signal(object)  # QImage | None，从非 UI 线程安全更新图传

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
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

        # 右侧：状态/血量面板（Phase 4）
        self._game_state_panel = GameStatePanel(self)
        splitter.addWidget(self._game_state_panel)

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

"""
图传显示区域 — 含 QGraphicsView 与买活预警叠加层。
"""
from qtpy.QtWidgets import QFrame, QGraphicsScene, QGraphicsView, QGraphicsPixmapItem, QGraphicsTextItem, QVBoxLayout, QWidget

from qtpy.QtCore import Qt
from qtpy.QtGui import QImage, QPixmap

from rm_client.ui.control.buyback_overlay import BuybackOverlay


class VideoArea(QFrame):
    """图传区 + 中央买活预警叠加。"""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setMinimumWidth(640)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self._graphics_view = QGraphicsView()
        self._graphics_view.setStyleSheet("background: #1a1a1a;")
        self._scene = QGraphicsScene(0, 0, 640, 360)
        self._graphics_view.setScene(self._scene)
        self._pixmap_item = QGraphicsPixmapItem()
        self._scene.addItem(self._pixmap_item)
        self._placeholder_text = QGraphicsTextItem("图传未连接")
        self._placeholder_text.setDefaultTextColor(Qt.gray)
        self._placeholder_text.setPos(260, 165)
        self._scene.addItem(self._placeholder_text)
        layout.addWidget(self._graphics_view)

        self._overlay = BuybackOverlay(self)
        self._overlay.setFixedSize(320, 56)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        w, h = self.width(), self.height()
        ow, oh = self._overlay.width(), self._overlay.height()
        self._overlay.move((w - ow) // 2, (h - oh) // 2)

    @property
    def graphics_view(self):
        return self._graphics_view

    @property
    def scene(self):
        return self._scene

    @property
    def pixmap_item(self):
        return self._pixmap_item

    @property
    def placeholder_text(self):
        return self._placeholder_text

"""
图传显示区域 — 含 QGraphicsView、买活预警叠加层、操作手 HUD、左下角固定小地图（修改4）。
"""
from qtpy.QtWidgets import QFrame, QGraphicsScene, QGraphicsView, QGraphicsPixmapItem, QGraphicsTextItem, QVBoxLayout, QWidget

from qtpy.QtCore import Qt
from qtpy.QtGui import QImage, QPixmap

from rm_client.ui.control.buyback_overlay import BuybackOverlay
from rm_client.ui.hud.video_hud_overlay import VideoHudOverlay
from rm_client.ui.radar.map_widget import MapWidget

# 修改4：小地图固定左下角，弱化黑框
STYLE_MINIMAP_CONTAINER = """
    QFrame {
        background-color: rgba(0, 0, 0, 0.25);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 8px;
    }
"""


class VideoArea(QFrame):
    """图传区 + 中央买活预警叠加 + 操作手 HUD + 左下角固定小地图。"""

    # 左下角小地图固定边距与尺寸
    _MINIMAP_MARGIN = 20
    _MINIMAP_SIZE = 160

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setMinimumWidth(640)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self._graphics_view = QGraphicsView()
        self._graphics_view.setStyleSheet("background: #0d0d0d; border: 1px solid #334155;")
        self._scene = QGraphicsScene(0, 0, 640, 360)
        self._graphics_view.setScene(self._scene)
        self._pixmap_item = QGraphicsPixmapItem()
        self._scene.addItem(self._pixmap_item)
        self._placeholder_text = QGraphicsTextItem("NO SIGNAL")
        self._placeholder_text.setDefaultTextColor(Qt.gray)
        from qtpy.QtGui import QFont
        font = QFont()
        font.setPointSize(24)
        font.setBold(True)
        self._placeholder_text.setFont(font)
        self._placeholder_text.setPos(220, 158)
        self._scene.addItem(self._placeholder_text)
        layout.addWidget(self._graphics_view)

        self._overlay = BuybackOverlay(self)
        self._overlay.setFixedSize(320, 56)

        self._hud_overlay = VideoHudOverlay(self)
        self._hud_overlay.raise_()

        # 修改4：小地图固定到左下角
        self._minimap = MapWidget(self)
        self._minimap.setFixedSize(self._MINIMAP_SIZE, self._MINIMAP_SIZE)
        self._minimap.setStyleSheet(STYLE_MINIMAP_CONTAINER)
        self._minimap.raise_()

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        w, h = self.width(), self.height()
        ow, oh = self._overlay.width(), self._overlay.height()
        self._overlay.move((w - ow) // 2, (h - oh) // 2)
        self._hud_overlay.setGeometry(0, 0, w, h)
        self._hud_overlay.raise_()
        # 小地图：左下角固定 left 20, bottom 20, 160x160
        mx, my = self._MINIMAP_MARGIN, h - self._MINIMAP_MARGIN - self._MINIMAP_SIZE
        self._minimap.setGeometry(mx, my, self._MINIMAP_SIZE, self._MINIMAP_SIZE)
        self._minimap.raise_()

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

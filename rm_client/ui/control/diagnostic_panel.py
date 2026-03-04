"""
右侧控制面板 — 链路诊断（§5.1.3）。

只读 DataCenter.link_status，展示 MQTT 连接状态、数据更新时间、一键复制诊断信息。
"""
import time

from qtpy.QtCore import QTimer
from qtpy.QtWidgets import (
    QApplication,
    QFrame,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from rm_client.ui.control.field_row import FieldRow


class DiagnosticPanel(QFrame):
    """右侧诊断面板：参考图圆角边框行，左标签右值。"""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setMaximumWidth(320)
        from rm_client.ui.styles import STYLE_PANEL, STYLE_PANEL_TITLE, STYLE_BTN, STYLE_VALUE_OK, STYLE_VALUE_BAD
        self.setStyleSheet(STYLE_PANEL)
        layout = QVBoxLayout(self)
        layout.setSpacing(6)

        title = QLabel("LINK DIAGNOSIS")
        title.setStyleSheet(STYLE_PANEL_TITLE)
        layout.addWidget(title)

        self._row_mqtt = FieldRow("MQTT 连接:")
        self._row_mqtt_data = FieldRow("MQTT 数据:")
        self._row_video = FieldRow("图传数据:")
        layout.addWidget(self._row_mqtt)
        layout.addWidget(self._row_mqtt_data)
        layout.addWidget(self._row_video)

        copy_btn = QPushButton("复制诊断信息")
        copy_btn.setStyleSheet(STYLE_BTN)
        copy_btn.clicked.connect(self._copy_diagnostic)
        layout.addWidget(copy_btn)

        layout.addStretch()

        self._refresh_timer = QTimer(self)
        self._refresh_timer.timeout.connect(self._refresh_from_dc)
        self._refresh_timer.start(500)

    @staticmethod
    def _format_ago(ts: float | None) -> str:
        """将时间戳格式化为「X 秒前」或「从未」。"""
        if ts is None or ts <= 0:
            return "从未"
        diff = time.time() - ts
        if diff < 1:
            return "刚刚"
        if diff < 60:
            return f"{int(diff)} 秒前"
        return f"{int(diff // 60)} 分前"

    def _refresh_from_dc(self) -> None:
        from rm_client.core.model.datacenter import DataCenter
        from rm_client.ui.styles import STYLE_VALUE_OK, STYLE_VALUE_BAD

        dc = DataCenter()
        ls = dc.link_status

        mqtt_conn = ls.get("mqtt_connected", False)
        self._row_mqtt.set_value("已连接" if mqtt_conn else "未连接")
        self._row_mqtt.set_value_style(STYLE_VALUE_OK if mqtt_conn else STYLE_VALUE_BAD)
        self._row_mqtt_data.set_value(self._format_ago(ls.get("mqtt_last_update")))
        self._row_video.set_value(self._format_ago(ls.get("video_last_update")))

    def _copy_diagnostic(self) -> None:
        from rm_client.core.model.datacenter import DataCenter

        dc = DataCenter()
        ls = dc.link_status
        lines = [
            "=== RoboMaster 客户端 链路诊断 ===",
            f"MQTT 连接: {'已连接' if ls.get('mqtt_connected') else '未连接'}",
            f"MQTT 数据: {self._format_ago(ls.get('mqtt_last_update'))}",
            f"图传数据: {self._format_ago(ls.get('video_last_update'))}",
        ]
        text = "\n".join(lines)
        QApplication.clipboard().setText(text)

"""
右侧控制面板 — 链路诊断（§5.1.3）。

只读 DataCenter.link_status，展示 MQTT 连接状态、数据更新时间、一键复制诊断信息。
"""
import time

from qtpy.QtCore import QTimer
from qtpy.QtWidgets import (
    QApplication,
    QFormLayout,
    QFrame,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class DiagnosticPanel(QFrame):
    """右侧诊断面板：链路状态、最近更新时间、一键复制。"""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setMaximumWidth(320)
        self.setFrameStyle(QFrame.StyledPanel)
        layout = QVBoxLayout(self)
        layout.setSpacing(8)

        title = QLabel("链路诊断")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)

        form = QFormLayout()
        self._mqtt_status_label = QLabel("—")
        self._mqtt_update_label = QLabel("—")
        self._video_update_label = QLabel("—")
        form.addRow("MQTT 连接:", self._mqtt_status_label)
        form.addRow("MQTT 数据:", self._mqtt_update_label)
        form.addRow("图传数据:", self._video_update_label)
        layout.addLayout(form)

        copy_btn = QPushButton("复制诊断信息")
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

        dc = DataCenter()
        ls = dc.link_status

        mqtt_conn = ls.get("mqtt_connected", False)
        self._mqtt_status_label.setText("已连接" if mqtt_conn else "未连接")
        self._mqtt_update_label.setText(self._format_ago(ls.get("mqtt_last_update")))
        self._video_update_label.setText(self._format_ago(ls.get("video_last_update")))

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

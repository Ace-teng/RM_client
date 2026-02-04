"""
示例插件 — Phase 7 交接示例，展示如何通过插件扩展客户端。

新增功能优先以插件实现，不修改主程序（§4.6）。
"""
from qtpy.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget

from rm_client.plugins.interface import PluginBase, PluginContext


class ExamplePlugin(PluginBase):
    name = "示例插件"
    version = "1.0.0"

    def register(self, ctx: PluginContext) -> None:
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(4)
        layout.addWidget(QLabel("示例插件已加载"))
        btn = QPushButton("点击刷新状态")
        btn.clicked.connect(lambda: self._on_click(ctx))
        layout.addWidget(btn)
        ctx.add_widget(panel, title=self.name)

    def _on_click(self, ctx: PluginContext) -> None:
        gs = ctx.dc.game_state
        phase = getattr(gs, "game_phase", "?") if gs else "?"
        ctx.set_status("示例插件：game_phase=%s" % phase)


PLUGIN = ExamplePlugin()

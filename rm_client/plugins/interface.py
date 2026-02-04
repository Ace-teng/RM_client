"""
插件接口 — Phase 7，§4.6。

插件需实现 register(ctx)，通过 ctx 获取 DataCenter、添加 UI 等。
"""
from dataclasses import dataclass
from typing import Any, Callable, Optional


@dataclass
class PluginContext:
    """插件注册时获得的上下文，只读访问核心对象。"""

    dc: Any  # DataCenter 单例，只读
    main_window: Any  # MainWindow 实例，用于 set_status_message 等
    command_sender: Optional[Any]  # CommandSender，可为 None

    def add_widget(self, widget: Any, title: str = "") -> None:
        """将插件控件添加到主窗口插件区域。由 MainWindow 实现。"""
        if hasattr(self.main_window, "add_plugin_widget"):
            self.main_window.add_plugin_widget(widget, title)

    def set_status(self, msg: str) -> None:
        """设置主窗口状态栏文案。"""
        if hasattr(self.main_window, "set_status_message"):
            self.main_window.set_status_message(msg)


class PluginBase:
    """插件基类，子类实现 register。"""

    name: str = "未命名插件"
    version: str = "0.0.0"

    def register(self, ctx: PluginContext) -> None:
        """插件加载时调用。ctx 提供 dc、main_window、command_sender、add_widget 等。"""
        raise NotImplementedError

    def unregister(self) -> None:
        """插件卸载时调用（可选，用于释放资源）。"""
        pass

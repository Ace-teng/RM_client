"""
插件加载器 — Phase 7，动态发现并加载 plugins 目录下的插件。

约定：plugins 子目录或 plugin_*.py 模块中定义 PLUGIN 属性（PluginBase 实例）。
"""
import importlib
import logging
import pkgutil
from pathlib import Path
from typing import List

from rm_client.plugins.interface import PluginBase, PluginContext

logger = logging.getLogger(__name__)


def _discover_plugin_modules() -> List[str]:
    """发现可加载的插件模块名。"""
    plugins_pkg = __name__.rsplit(".", 1)[0]  # rm_client.plugins
    plugin_names: List[str] = []
    try:
        pkg = importlib.import_module(plugins_pkg)
        pkg_path = getattr(pkg, "__path__", None)
        if not pkg_path:
            return plugin_names
        for importer, modname, ispkg in pkgutil.iter_modules(pkg_path):
            if modname.startswith("_"):
                continue
            if ispkg or modname.startswith("plugin_"):
                full = f"{plugins_pkg}.{modname}"
                plugin_names.append(full)
    except Exception as e:
        logger.warning("插件发现失败: %s", e)
    return plugin_names


def load_plugins(ctx: PluginContext) -> List[PluginBase]:
    """加载所有插件并调用 register。返回成功注册的插件列表。"""
    loaded: List[PluginBase] = []
    for modname in _discover_plugin_modules():
        try:
            mod = importlib.import_module(modname)
            plugin = getattr(mod, "PLUGIN", None)
            if plugin is None or not isinstance(plugin, PluginBase):
                logger.debug("跳过 %s：无 PLUGIN 或非 PluginBase", modname)
                continue
            plugin.register(ctx)
            loaded.append(plugin)
            logger.info("插件已加载: %s %s", plugin.name, plugin.version)
        except Exception as e:
            logger.warning("插件加载失败 %s: %s", modname, e)
    return loaded

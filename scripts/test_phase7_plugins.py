"""
Phase 7 插件机制测试 — 不启动 GUI，仅验证插件发现与加载。

在项目根目录执行：
    python scripts/test_phase7_plugins.py
"""
import sys
from pathlib import Path

_root = Path(__file__).resolve().parents[1]
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

# 必须在任何插件加载前创建 QApplication（插件会创建 QWidget）
from qtpy.QtWidgets import QApplication
_app = QApplication.instance() or QApplication(sys.argv)


def main() -> int:
    from rm_client.core.model.datacenter import DataCenter
    from rm_client.plugins.interface import PluginContext
    from rm_client.plugins.loader import load_plugins

    dc = DataCenter()

    class MockWindow:
        widgets = []

        def add_plugin_widget(self, widget, title=""):
            self.widgets.append((title, widget))

        def set_status_message(self, msg):
            print("[MockWindow] status:", msg)

    ctx = PluginContext(dc=dc, main_window=MockWindow(), command_sender=None)
    loaded = load_plugins(ctx)
    print("[1/2] 插件加载数量: %d" % len(loaded))
    for p in loaded:
        print("     - %s %s" % (p.name, p.version))
    print("[2/2] MockWindow 接收的控件数: %d" % len(ctx.main_window.widgets))
    if loaded and ctx.main_window.widgets:
        print("Phase 7 插件机制测试通过。")
        return 0
    print("Phase 7 测试失败：未加载到示例插件。")
    return 1


if __name__ == "__main__":
    sys.exit(main())

"""
Phase 3 测试：仅验证「协议解析 + 写入 DataCenter」，不启动 MQTT、不启动 GUI。

任意目录下执行（无需虚拟环境）：python scripts/test_phase3_parse_only.py
或先 cd 到项目根再执行上述命令。
"""
import os
import sys

# 项目根 = 本脚本所在目录的上一级；加入 sys.path 以便 import rm_client（不依赖当前工作目录和虚拟环境）
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from rm_client.core.model.datacenter import DataCenter
from rm_client.core.protocol.referee_parser import parse_referee_message


def main() -> int:
    dc = DataCenter()

    # 1. 空 payload 不写
    parse_referee_message("game/status", b"", dc)
    assert dc.game_state is None, "空 payload 不应写入 game_state"
    print("[1/4] 空 payload 不写入: OK")

    # 2. 合法 GameStatus：game_phase=1, remaining_time_sec=120
    #    wire: tag 0x08 (field 1 varint) value 1; tag 0x10 (field 2 varint) value 120
    payload = bytes([0x08, 0x01, 0x10, 0x78])
    parse_referee_message("game/status", payload, dc)
    assert dc.game_state is not None
    assert dc.game_state.game_phase == 1
    assert dc.game_state.remaining_time_sec == 120
    print("[2/4] game/status 解析并写入 DataCenter: OK (phase=1, time=120)")

    # 3. 其它 topic 不解析为 GameStatus（game_state 保持上一次）
    parse_referee_message("other/topic", payload, dc)
    assert dc.game_state is not None and dc.game_state.game_phase == 1
    print("[3/4] 其它 topic 不覆盖: OK")

    # 4. 再次用 game/status 更新
    payload2 = bytes([0x08, 0x02, 0x10, 0x3C])  # phase=2, time=60
    parse_referee_message("game/status", payload2, dc)
    assert dc.game_state.game_phase == 2 and dc.game_state.remaining_time_sec == 60
    print("[4/4] 再次更新 game_state: OK")

    print("\nPhase 3 解析与 DataCenter 写入测试全部通过。")
    return 0


if __name__ == "__main__":
    sys.exit(main())

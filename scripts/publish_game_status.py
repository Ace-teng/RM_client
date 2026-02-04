"""
向本机 MQTT broker 发布一条 GameStatus，用于配合客户端做 Phase 3 端到端测试。

先启动客户端（run_local_test.bat 或 REFEREE_MQTT_HOST=127.0.0.1 python -m rm_client.main），
再在本机另一终端执行（任意目录、无需虚拟环境）：python scripts/publish_game_status.py

可选环境变量：
  MQTT_HOST  默认 127.0.0.1
  MQTT_PORT  默认 1883
  TOPIC      默认 game/status
"""
import os
import sys

# 项目根加入 sys.path，便于任意目录下 import rm_client
_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _root not in sys.path:
    sys.path.insert(0, _root)

import paho.mqtt.client as mqtt

from rm_client.core.protocol.generated.referee_pb2 import GameStatus


def main() -> int:
    host = os.environ.get("MQTT_HOST", "127.0.0.1")
    port = int(os.environ.get("MQTT_PORT", "1883"))
    topic = os.environ.get("TOPIC", "game/status")

    msg = GameStatus()
    msg.game_phase = 2
    msg.remaining_time_sec = 300
    payload = msg.SerializeToString()

    client = mqtt.Client(client_id="phase3_publisher", protocol=mqtt.MQTTv311)
    try:
        client.connect(host, port, keepalive=60)
    except Exception as e:
        print("连接 MQTT 失败:", e)
        print("请先在本机启动 broker（例如 mosquitto），并确认端口", port)
        return 1
    client.publish(topic, payload, qos=0)
    client.disconnect()
    print("已向 %s:%s [%s] 发布 GameStatus(phase=2, remaining_time_sec=300)" % (host, port, topic))
    return 0


if __name__ == "__main__":
    sys.exit(main())

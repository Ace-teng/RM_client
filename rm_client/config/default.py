"""
默认配置 — 赛事引擎与 MQTT（见总文档 §1.5）。

开发环境：用环境变量指向本机 broker 即可自测（见 README「开发环境自测 MQTT」）。
赛场：不设环境变量即用默认 192.168.12.1:3333。
"""
import os

# 赛事引擎 MQTT：默认赛场地址；环境变量覆盖后可在本机用自建 broker 测试
REFEREE_MQTT_HOST = os.environ.get("REFEREE_MQTT_HOST", "192.168.12.1")
REFEREE_MQTT_PORT = int(os.environ.get("REFEREE_MQTT_PORT", "3333"))

# 订阅 Topic 列表（对应指令/消息名，以赛事通信协议为准；此处为占位）
REFEREE_MQTT_TOPICS = [
    "#",  # 占位：订阅所有；正式开发时改为具体 topic 列表
]

# Phase 3 协议层：GameStatus 消息对应 Topic（占位，以赛事通信协议为准）
REFEREE_TOPIC_GAME_STATUS = os.environ.get("REFEREE_TOPIC_GAME_STATUS", "game/status")

# 连接超时（秒）
REFEREE_MQTT_CONNECT_TIMEOUT = 10

# 图传 UDP（§1.5）：端口 3334，8 字节包头
VIDEO_UDP_PORT = int(os.environ.get("VIDEO_UDP_PORT", "3334"))

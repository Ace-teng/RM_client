# 测试命令汇总

本文档汇总项目根目录下常用的测试命令与预期结果。在项目根目录执行以下命令（无需虚拟环境，任意目录执行脚本时脚本会自动把项目根加入路径）。

---

## 一、环境准备

```bash
pip install -r requirements.txt
```

可选（图传解码）：`pip install av`

---

## 二、Phase 3：协议解析 + DataCenter（不启动 GUI）

```bash
python scripts/test_phase3_parse_only.py
```

**预期**：依次输出 `[1/4]`～`[4/4]` 的 OK，最后一行「Phase 3 解析与 DataCenter 写入测试全部通过。」，退出码 0。

---

## 三、启动客户端

**赛场 / 默认（连 192.168.12.1:3333）**

```bash
python -m rm_client.main
```

**本地测试（连本机 MQTT 127.0.0.1:1883，与 run_local_test.bat 一致）**

```bash
python -m rm_client.main --local
```

或用批处理（Windows）：

```bash
run.bat              # 默认赛场 MQTT
run_local_test.bat   # 本机 127.0.0.1:1883
```

**预期**：弹出主窗口；中心图传区显示「图传未连接」，右侧为赛事状态面板。使用 `--local` 且本机有 MQTT broker 时，状态栏显示「MQTT 已连接」。

---

## 四、MQTT 端到端（发布 GameStatus）

1. 本机先启动 MQTT broker（如 mosquitto，端口 1883）。
2. 启动客户端（二选一）：
   - `python -m rm_client.main --local`
   - 或 `run_local_test.bat`
3. 另开终端，在项目根执行：

```bash
python scripts/publish_game_status.py
```

**预期**：客户端右侧「赛事状态」中阶段=2、剩余时间(s)=300；状态栏显示 `game_phase=2 remaining_time_sec=300`。

可选环境变量：`MQTT_HOST`、`MQTT_PORT`、`TOPIC`（默认 127.0.0.1、1883、game/status）。

---

## 五、图传测试（HEVC → 3334）

1. 先启动客户端（任选一种方式，如 `python -m rm_client.main --local`）。
2. 另开终端，在项目根执行：

```bash
python scripts/send_test_video_udp.py
```

**依赖**：`pip install av`

**预期**：脚本输出「向 127.0.0.1:3334 发送 HEVC 测试流…」，约 15 秒后「已发送 xxx 帧，结束。」；客户端中心图传区出现动态画面（灰度渐变）。

---

## 六、命令速查

| 用途           | 命令 |
|----------------|------|
| 装依赖         | `pip install -r requirements.txt` |
| 图传解码依赖   | `pip install av` |
| Phase 3 解析测试 | `python scripts/test_phase3_parse_only.py` |
| 启动客户端（赛场） | `python -m rm_client.main` |
| 启动客户端（本机 MQTT） | `python -m rm_client.main --local` |
| 发布一条 GameStatus | `python scripts/publish_game_status.py` |
| 发送 HEVC 测试流 | `python scripts/send_test_video_udp.py` |

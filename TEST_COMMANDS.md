# 测试命令汇总

本文档汇总项目根目录下常用的测试命令与预期结果。在项目根目录执行以下命令（无需虚拟环境，任意目录执行脚本时脚本会自动把项目根加入路径）。


powershell ：  mosquitto -p 1883

mosquitto_pub -h 127.0.0.1 -p 1883 -t "test/topic" -m "hello"

python -m rm_client.main --local
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

**本地测试（连本机 MQTT 127.0.0.1:1883）**

先启动 mosquitto：`mosquitto -p 1883`，再执行：

```bash
run_local_test.bat   # 推荐：在 Python 启动前设置环境变量
```

或：

```bash
python -m rm_client.main --local
```

启动时控制台会输出 `MQTT 目标: 127.0.0.1:1883`，可确认连接地址。若显示「MQTT 连接中」不变成「已连接」，检查：1）mosquitto 是否在运行；2）`netstat -ano | findstr 1883` 是否有监听。

**预期**：弹出主窗口；中心图传区显示「图传未连接」，右侧为赛事状态 + 态势图 + 机器人状态 + 赛事指令 + 插件区域（Phase 5/6/7）。示例插件会在「插件」区域显示；使用 `--local` 且本机有 MQTT broker 时，状态栏显示「MQTT 已连接」；点击「性能体系 1/2/3」「兑换发弹量」「空中支援」可发送指令（MQTT 未连接时弹窗提示）。

---

## 四、Phase 7：插件机制（不启动 GUI）

```bash
python scripts/test_phase7_plugins.py
```

**预期**：输出插件加载数量 ≥1、MockWindow 接收的控件数 ≥1，最后「Phase 7 插件机制测试通过。」，退出码 0。

---

## 五、MQTT 端到端（发布 GameStatus）

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

## 六、图传测试（HEVC → 3334）

1. 先启动客户端（任选一种方式，如 `python -m rm_client.main --local`）。
2. 另开终端，在项目根执行：

```bash
python scripts/send_test_video_udp.py
```

**依赖**：`pip install av`

**预期**：脚本输出「向 127.0.0.1:3334 发送 HEVC 测试流…」，约 15 秒后「已发送 xxx 帧，结束。」；客户端中心图传区出现动态画面（灰度渐变）。

---

## 七、命令速查

| 用途           | 命令 |
|----------------|------|
| 装依赖         | `pip install -r requirements.txt` |
| 图传解码依赖   | `pip install av` |
| Phase 3 解析测试 | `python scripts/test_phase3_parse_only.py` |
| Phase 7 插件测试 | `python scripts/test_phase7_plugins.py` |
| 启动客户端（赛场） | `python -m rm_client.main` |
| 启动客户端（本机 MQTT） | `python -m rm_client.main --local` |
| 发布一条 GameStatus | `python scripts/publish_game_status.py` |
| 发送 HEVC 测试流 | `python scripts/send_test_video_udp.py` |

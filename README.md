# RoboMaster 自定义客户端 / Custom Client

**GitHub：** [https://github.com/Ace-teng/RM_client](https://github.com/Ace-teng/RM_client)

RoboMaster 赛事队伍自制的**多设备战术信息中枢**，用于接收赛事引擎赛事数据与机器人图传、发送赛事指令，并支持雷达/车端等局域网设备接入与战术可视化。**界面与交互采用 QtPy 开发**，队伍长期基础设施，非一次性工具。

---

## 功能概述

| 能力 | 说明 | 状态 |
|------|------|------|
| 赛事数据接入 | 赛事引擎 MQTT（Protobuf）+ 图传 UDP（HEVC），向赛事引擎发送指令 | ✅ Phase 2–6 |
| 图传显示 | HEVC 解码与渲染、图传区为中心 | ✅ Phase 4 |
| 态势与状态 | 地图、机器人位置、血量/时间、赛事指令 | ✅ Phase 4–6 |
| 插件机制 | 插件加载、示例插件、新功能优先以插件实现 | ✅ Phase 7 |
| 战术分析 | 追击/撤退建议、买活预警、经济提示 | ✅ 已实现 |
| HUD 透视框 | 多目标框、标签、超时隐藏、断流自动消失 | 待实现 |
| 标定 | 标定页面（ArUco 引导、状态四态） | 待实现 |
| 雷达与设备间 | 雷达站、自定义控制器等 LAN 接入 | 待实现 |
| 诊断与联调 | 连接状态、丢包/超时计数、一键复制诊断 | 待实现 |

**系统定位：** 分布式实时通信 + 可视化；开发进度与规划见 [docs/开发进度与规划.md](docs/开发进度与规划.md)。

---

## 技术栈与规范

- **界面：** **QtPy**（QMainWindow / QGraphicsView，可切换 PyQt5/6、PySide2/6）；禁止表现层混用其他 GUI 库
- **语言：** Python 3.10+
- **通信：** MQTT（192.168.12.1:3333）、UDP 图传（3334）、Protobuf v3、局域网 UDP/TCP
- **架构：** 六层（通信 → 协议 → 数据 → 业务 → 表现 → 插件）、单一数据源（DataCenter）、单向数据流、事件总线解耦

基本功能与验收点见总文档 **§0.2 基本功能总览**；最终产品形态见 **§0.3**；规定要求与功能完整、可维护性自检见 **§12**。

---

## 项目结构

```
项目根目录/
├── rm_client/
│   ├── main.py
│   ├── core/       # comms, protocol, model, service, bus, pose, time_sync
│   ├── ui/         # hud, radar, control
│   ├── plugins/    # loader, interface, example
│   ├── proto/
│   └── config/
├── docs/           # CustomClient_Architecture.md, 开发进度与规划.md
├── scripts/        # test_phase3_parse_only, test_phase7_plugins, publish_game_status, send_test_video_udp
├── run.bat / run_local_test.bat
└── TEST_COMMANDS.md
```

---

## 快速开始

```bash
# 克隆
git clone https://github.com/Ace-teng/RM_client.git
cd RM_client

# 依赖（Python 3.10+）
pip install -r requirements.txt

# 运行（赛场模式，连 192.168.12.1:3333）
python -m rm_client.main

# 本地测试（连本机 MQTT 127.0.0.1:1883，需先启动 mosquitto -p 1883）
python -m rm_client.main --local
```

**说明：** 请在**仓库根目录**（与 `rm_client`、`docs` 同级）执行；**必须用 `python -m rm_client.main`**，否则会报 `No module named 'rm_client'`。

**Qt 绑定：** QtPy 需配合一个 Qt 绑定使用。`requirements.txt` 默认含 PyQt6；若只有 Qt5，可改为 `pip install QtPy PyQt5`。

**图传解码（可选）：** `pip install av` 用于 HEVC 解码。不安装则图传区显示「图传未连接」。

---

## 开发环境自测 MQTT

本机无赛事引擎时，可起本地 MQTT broker 验证连接与收发。赛场环境下不设环境变量即使用 192.168.12.1:3333。

**1. 启动 mosquitto**

```bash
mosquitto -p 1883
```

**2. 启动客户端**

```bash
python -m rm_client.main --local
```

或双击 `run_local_test.bat`（脚本内会设置环境变量后启动）。

**3. 验证**

- 控制台输出 `MQTT 目标: 127.0.0.1:1883`
- 状态栏显示「MQTT 已连接」
- 另开终端发测试消息：`mosquitto_pub -h 127.0.0.1 -p 1883 -t "test/topic" -m "hello"`，客户端应收到并打日志

**故障排查：** 若一直显示「MQTT 连接中」，检查 mosquitto 是否在运行，执行 `netstat -ano | findstr 1883` 确认端口监听。

---

## 文档

| 文档 | 说明 |
|------|------|
| [CustomClient_Architecture.md](docs/CustomClient_Architecture.md) | 系统需求与架构设计（唯一总文档） |
| [开发进度与规划.md](docs/开发进度与规划.md) | 已实现功能与待办规划 |
| [战术分析功能设计.md](docs/战术分析功能设计.md) | 战术建议、买活预警等设计 |
| [测试报告.md](docs/测试报告.md) | 各阶段测试截图与验收记录 |
| [TEST_COMMANDS.md](TEST_COMMANDS.md) | 测试命令汇总（Phase 3/7、MQTT、图传等） |

**实现须满足总文档中 MUST 条款。**

---

## 许可证 / License

未标注则视为队伍内部使用；对外开源时请补充 LICENSE 文件。

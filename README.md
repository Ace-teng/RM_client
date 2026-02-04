# RoboMaster 自定义客户端 / Custom Client

**GitHub：** [https://github.com/Ace-teng/RM_client](https://github.com/Ace-teng/RM_client)

RoboMaster 赛事队伍自制的**多设备战术信息中枢**，用于接收赛事引擎赛事数据与机器人图传、发送赛事指令，并支持雷达/车端等局域网设备接入与战术可视化。**界面与交互采用 QtPy 开发**，队伍长期基础设施，非一次性工具。

---

## 功能概述

| 能力 | 说明 |
|------|------|
| 赛事数据接入 | 赛事引擎 MQTT（Protobuf）+ 图传 UDP（HEVC），向赛事引擎发送指令 |
| 图传显示 | HEVC 解码与渲染、图传区为中心；HUD 透视框（多目标框、标签、超时隐藏、断流自动消失） |
| 态势与状态 | 地图、机器人位置、双方血量/经济/时间、关键事件、连接状态 |
| 标定 | 标定页面（进入/退出、重试、状态四态、ArUco 引导、验收点） |
| 雷达与设备间 | 雷达站、地面机器人、自定义控制器等 LAN 接入；重连、心跳、丢包/延迟统计 |
| 诊断与联调 | 连接/数据状态、多久前更新、丢弃/超时计数、一键复制诊断；可选录包与回放 |
| 控制与扩展 | 控制面板发送赛事指令；插件机制，新功能优先以插件实现 |

**系统定位：** 分布式实时通信 + 可视化；支持多屏/多角色视图（待定）；地面机器人操作手需求见总文档 §0.5。

---

## 技术栈与规范

- **界面：** **QtPy**（QMainWindow / QGraphicsView，可切换 PyQt5/6、PySide2/6）；禁止表现层混用其他 GUI 库
- **语言：** Python 3.10+
- **通信：** MQTT（192.168.12.1:3333）、UDP 图传（3334）、Protobuf v3、局域网 UDP/TCP
- **架构：** 六层（通信 → 协议 → 数据 → 业务 → 表现 → 插件）、单一数据源（DataCenter）、单向数据流、事件总线解耦

基本功能与验收点见总文档 **§0.2 基本功能总览**；最终产品形态见 **§0.3**；规定要求与功能完整、可维护性自检见 **§12**。

---

## 项目结构（规划）

与总文档 §3 一致：

```
rm_client/
├── main.py
├── core/
│   ├── comms/      # 通信层（赛事 + 设备间）
│   ├── protocol/   # 协议层
│   ├── model/      # 数据层（DataCenter）
│   ├── service/    # 业务层
│   ├── bus/        # 事件总线
│   ├── pose/       # 坐标系与标定
│   ├── time_sync/  # 时间同步
│   └── replay/     # 录包与回放
├── ui/
│   ├── hud/        # 叠加显示
│   ├── radar/      # 态势地图
│   └── control/    # 操作面板
├── plugins/        # 插件层
├── config/
└── docs/           # 需求与架构文档
```

---

## 快速开始

```bash
# 克隆
git clone https://github.com/Ace-teng/RM_client.git
cd RM_client

# 依赖（Python 3.10+）
pip install -r requirements.txt

# 运行（Phase 1：QtPy 主窗口 + DataCenter 已可启动）
# 必须用 -m 从项目根目录运行，否则会报 No module named 'rm_client'
python -m rm_client.main
```

**说明：** 请在**仓库根目录**（即与 `rm_client`、`docs` 同级）下执行上述命令；**必须用 `python -m rm_client.main`**，不要用 `python rm_client/main.py`（会报 `No module named 'rm_client'`）。Phase 1 将弹出主窗口（中心图传区占位 + 右侧控制面板占位 + 状态栏）。

**Qt 绑定说明：** QtPy 只是封装层，必须再安装**一个** Qt 绑定，否则会报 `QtBindingsNotFoundError`。`requirements.txt` 已默认带上 PyQt6；若你本机只有 Qt5，可改为安装 PyQt5 或 PySide2：

```powershell
# 方案 A：用 Qt6（推荐，已写在 requirements.txt）
pip install -r requirements.txt

# 方案 B：只用 Qt5
pip install QtPy PyQt5
```

**如何测试（PowerShell）：**

```powershell
# 1. 进入项目根目录
cd "E:\大二寒假\robo寒假备赛\客户端开发"

# 2. 安装依赖（含 QtPy + 至少一个绑定，见上）
pip install -r requirements.txt

# 3. 运行（必须用 -m，否则报 No module named 'rm_client'）
python -m rm_client.main
```

若已安装多个绑定，可指定使用哪一个（在运行前设置环境变量）：

```powershell
$env:QT_API = "pyqt6"   # 或 pyqt5 / pyside6 / pyside2
python -m rm_client.main
```

**前置：** Phase 2+ 需具备 RoboMaster 赛事通信协议文档（.proto 与 Topic 定义）；图传为 HEVC，需解码库支持。

---

## 开发环境自测 MQTT（确保赛场可用）

开发机没有 192.168.12.1 的赛事引擎，可**在本机起一个 MQTT broker**，用环境变量把客户端指到本机，验证「连接 → 订阅 → 收包 → 打日志」整条链路。**到赛场不改代码**，不设环境变量即自动用 192.168.12.1:3333。

**步骤一：本机安装并启动 MQTT broker**

- **Windows：** 安装 [Mosquitto](https://mosquitto.org/download/) 后，在命令行运行 `mosquitto -p 1883`（默认端口 1883）。
- **或用 Docker：** `docker run -d -p 1883:1883 eclipse-mosquitto`。

**步骤二：用本机 broker 跑客户端**

PowerShell：

```powershell
cd "E:\大二寒假\robo寒假备赛\客户端开发"
$env:REFEREE_MQTT_HOST = "127.0.0.1"
$env:REFEREE_MQTT_PORT = "1883"
python -m rm_client.main
```

或直接双击 **`run_local_test.bat`**（已写好上述环境变量并启动客户端）。

**步骤三：发一条测试消息**

再开一个终端，用 Mosquitto 自带的发布工具（或任意 MQTT 客户端）往任意 topic 发一条消息，例如：

```powershell
# 若安装了 Mosquitto，可执行（在 broker 本机）：
mosquitto_pub -h 127.0.0.1 -p 1883 -t "test/topic" -m "hello"
```

客户端控制台应出现类似：`收到 [test/topic] N bytes`，状态栏为「MQTT 已连接」。

**结论：** 本地能连上、能收包打日志，说明 MQTT 代码路径正确；到赛场接好网、不设 `REFEREE_MQTT_*`，即用默认 192.168.12.1:3333，即可与赛事引擎通信。

---

## 文档

**[系统需求与架构设计](docs/CustomClient_Architecture.md)** — 唯一总文档（§0～§13），含：

- **§0** 技术选型、基本功能总览、最终产品形态、多屏/多角色（待定）、地面机器人操作手需求
- **§1～2** 引言、赛事规范、总体架构要求（MUST）
- **§3～4** 目录结构、模块职责
- **§5** 功能需求（表现层、透视框、标定、诊断、QtPy 约定、基础设施层 R-COM/R-POSE/R-BUS/R-TIME/R-DBG）
- **§6～7** 数据流规范、开发阶段 Phase 1～7
- **§8～9** 开发规范与非功能需求、交接要求
- **§10～11** 实现策略与验收、变更与排错
- **§12** 总览与自检（规定要求、功能完整、可维护性体现）
- **§13** 结论

**实现须满足总文档中 MUST 条款；** 自检与验收可对照 §12。

---

## 许可证 / License

未标注则视为队伍内部使用；对外开源时请补充 LICENSE 文件。

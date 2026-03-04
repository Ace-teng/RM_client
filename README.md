# RoboMaster 自定义客户端

> Python + Qt 自定义比赛客户端，带高对比度 HUD 与操作手视图；同时包含一套 React HUD 预览，仅用于界面设计参考。

---

## 功能概览

- **比赛用桌面客户端（Python / Qt）**
  - 图传（FPV）显示 + 中央准心。
  - 左上 HUD：己方 HP、电容、自瞄状态。
  - 顶部 HUD：比赛时间、锁定目标距离。
  - 右上 HUD：敌方 HP、能量、弹量。
  - 底部 HUD：技能 CAP、热量条、时间/血量复显。
  - 左下：固定小地图（态势图）+ 底盘状态 + 跳跃目标。
  - 步兵专用顶栏 + 左/右侧信息面板。
  - 英雄视图右侧精简状态面板 + 插件扩展区。
  - 买活预警浮层（基于战术分析、比赛阶段与经济阈值）。

- **Web HUD 预览（React / TypeScript）**
  - 仅用于在浏览器中预览 HUD 布局和视觉风格。
  - 不参与实际比赛，也不与 Python 客户端直接耦合。

---

## 仓库结构

仅列出与本项目开发最相关的部分：

```text
客户端开发/
├─ rm_client/                # 比赛用 Python 客户端（核心）
│  ├─ core/                  # DataCenter + 业务 / 战术服务
│  ├─ ui/
│  │  ├─ main_window.py      # 主窗口：整体布局、左右面板、状态栏
│  │  ├─ video_area.py       # 图传区域 + HUD + 小地图 + 买活浮层
│  │  ├─ hud/                # HUD 控件与图传叠加层
│  │  │  ├─ video_hud_overlay.py  # 用 QPainter 直接画在图传上的 HUD（实际可见）
│  │  │  ├─ hud_overlay.py        # Widget 版 HUD 容器（挂各类 HUD 控件）
│  │  │  ├─ *.py                 # 血条、电容、自瞄、底盘、哨兵信息、跳跃目标等组件
│  │  ├─ control/            # 左/右侧面板、角色选择、诊断面板等
│  │  ├─ radar/              # 小地图等雷达组件
│  │  └─ styles/             # 主题色 + 旧版样式（兼容）
│  └─ main.py                # Python 客户端入口
│
├─ docs/
│  ├─ CustomClient_Architecture.md  # 架构说明（Python 客户端 vs Web 预览等）
│  ├─ 功能与使用说明.md             # 现版 HUD 与界面功能手册（操作手视角）
│  └─ 交接说明.md                   # 给开发同学的代码结构与注意事项（开发视角）
│
├─ package.json / vite.config.* / src/ ...
│   # React HUD 预览工程，仅用于界面设计，不影响比赛客户端
└─ ...
```

---

## 运行方式

### 1. 运行 Python 比赛客户端（推荐）

环境要求：

- Python 3.10+
- 已安装项目依赖（通常通过 `pip install -r requirements.txt`，具体以仓库说明为准）

在仓库根目录执行：

```bash
python -m rm_client.main --local
```

说明：

- 会创建 `DataCenter` 单例，初始化 UI，并尝试建立 MQTT 连接。
- 角色选择在右上角「角色」下拉框；选择步兵/英雄后，左/右侧面板和 HUD 会自动切换。

### 2. 运行 Web HUD 预览（可选）

> 仅供 UI 预览和调试布局，不参与实际比赛。

在带有 `package.json` 的目录（通常是本仓库根目录或 `web/` 目录）执行：

```bash
npm install
npm run dev
```

然后根据终端提示在浏览器打开对应地址（一般是 `http://localhost:5173` 一类端口）。

---

## 重要设计约定

- **唯一数据源：`DataCenter`**
  - 所有 HUD 与面板都从 `rm_client/core/model/datacenter.py` 读数据。
  - 业务逻辑/战术判断写 DataCenter，UI 只负责展示。

- **HUD 双轨实现**
  - `video_hud_overlay.py`：负责**画在图传上的 HUD**（坐标、重叠问题都在这里调）。
  - `hud_overlay.py` + 各组件：Widget 版 HUD，负责控件样式和更复杂的交互。

- **Web 预览不影响 Python 客户端**
  - React 代码只是设计稿；即使删掉，也不会影响 `python -m rm_client.main` 的运行。

- **样式演进**
  - 新的颜色主题集中在 `ui/styles/colors.py`（`HUDColors`）。
  - `ui/styles/_legacy.py` 中包含旧版样式常量，用于兼容尚未重构的面板。

---

## 推荐阅读顺序（给新同学）

1. 跑一遍 Python 客户端：`python -m rm_client.main --local`。  
2. 对照界面阅读：`docs/功能与使用说明.md`，理解每个 HUD/面板的含义。  
3. 阅读：`docs/交接说明.md`，掌握代码结构、数据流和注意事项。  
4. 按需查看：`docs/CustomClient_Architecture.md`，了解更细的架构设计与阶段划分。  
5. 如需调 UI 视觉，可跑一下 React HUD 预览，对比 Python 实现的差异。  

---

## 版权与许可

本项目版权与使用许可请参考课程/比赛要求或仓库附带的 LICENSE 说明（如存在）。如需在其它项目中复用，请先与原作者/团队沟通。

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

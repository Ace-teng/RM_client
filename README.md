# RoboMaster 自定义客户端 / Custom Client

RoboMaster 赛事队伍自制的**多设备战术信息中枢**，用于接收裁判系统赛事数据与机器人图传、发送赛事指令，并支持雷达/车端等局域网设备接入与战术可视化。

---

## 功能概述

| 能力 | 说明 |
|------|------|
| 赛事数据接入 | 赛事引擎 MQTT（Protobuf）+ 图传 UDP（HEVC） |
| 图传显示 | HEVC 解码与渲染、HUD 叠加 |
| 态势与状态 | 地图、机器人位置、双方血量/经济/时间、关键事件 |
| 赛事指令 | 赛前性能体系选择、赛中兑换发弹量、空中支援等 |
| 设备间通信 | 雷达站、地面机器人、自定义控制器等 LAN 接入 |
| 扩展 | 插件机制，新功能优先以插件实现 |

**系统定位：** 分布式实时通信 + 可视化；队伍长期基础设施，非一次性工具。

---

## 技术栈与规范

- **通信：** MQTT（192.168.12.1:3333）、UDP 图传（3334）、Protobuf v3、局域网 UDP/TCP
- **界面：** Qt（QMainWindow / QGraphicsView）
- **架构：** 六层（通信 → 协议 → 数据 → 业务 → 表现 → 插件）、单一数据源（DataCenter）、单向数据流、事件总线解耦

详见 [docs/CustomClient_Architecture.md](docs/CustomClient_Architecture.md)。

---

## 项目结构（规划）

```
rm_client/
├── main.py
├── core/          # 通信、协议、数据、业务、事件总线、坐标、时间同步、回放
├── ui/            # HUD、态势图、控制面板
├── plugins/       # 扩展插件
├── config/
└── docs/          # 需求与架构文档
```

---

## 快速开始

```bash
# 克隆
git clone https://github.com/<your-org>/<repo-name>.git
cd <repo-name>

# 依赖（示例：Python 3.10+、Qt、paho-mqtt、protobuf 等，按实际补充）
# pip install -r requirements.txt

# 运行（待实现后启用）
# python rm_client/main.py
```

**前置：** 需具备 RoboMaster 赛事通信协议文档（.proto 与 Topic 定义）；图传为 HEVC，需解码库支持。

---

## 文档

- **[系统需求与架构设计](docs/CustomClient_Architecture.md)** — 唯一总文档，含需求（MUST/SHOULD）、目录、模块职责、数据流、开发阶段与交接要求。**实现须满足其中 MUST 条款。**

---

## 许可证 / License

未标注则视为队伍内部使用；对外开源时请补充 LICENSE 文件。


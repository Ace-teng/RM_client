# RoboMaster 操作手客户端 UI 系统

## 项目概述

基于官方客户端的客制化 HUD 系统开发。

**核心要求：**
- 基于官方客户端进行客制化开发
- 支持多兵种切换：英雄、工程、步兵1、步兵2、云台手
- 遵循「边缘化布局」：中央保留图传画面，所有 UI 贴边放置
- 深色主题，确保所有文字在深色背景下清晰可读

**功能分类：**
- 可靠功能-通用功能：20 项
- 可靠功能-兵种特殊功能：10 项
- 不可靠功能（可开关）：7 项

## 文件结构

```
src/
├── components/
│   ├── HUD/
│   │   ├── common/          # 通用组件（HealthBar、CapacitorBar、Crosshair 等）
│   │   ├── hero/            # 英雄专用
│   │   ├── infantry/        # 步兵专用
│   │   ├── engineer/        # 工程专用
│   │   └── gimbal/          # 云台手专用
│   ├── Sidebar/             # 侧边栏
│   └── FloatingWindow/      # 悬浮窗
├── hooks/
│   └── useRobotState.ts     # 机器人状态 Hook
├── types/
│   └── robot.types.ts       # 类型定义
├── constants/
│   └── uiConfig.ts          # UI 配置常量
└── styles/
    └── hud.css              # HUD 全局样式
```

## 全局样式

见 `styles/hud.css`：主题色、背景、字体、间距、z-index 及通用类 `.hud-element`、`.hud-panel`、`.hud-bar`、动画等。

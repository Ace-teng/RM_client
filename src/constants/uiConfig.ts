/**
 * UI 配置常量：边距、尺寸、z-index、布局位置（与 hud.css 布局规范一致）
 */

export const HUD_MARGIN = 20;
export const Z_HUD_BASE = 100;
export const Z_HUD_CROSSHAIR = 150;
export const Z_HUD_ALERT = 200;
export const Z_MODAL = 300;

/** 布局位置（px），用于非 CSS 场景如 Canvas/内联样式 */
export const LAYOUT = {
  topLeft: { top: 20, left: 20 },           // 己方血量
  topLeft2: { top: 50, left: 20 },         // 电容条
  topLeft3: { top: 20, left: 220 },        // 自瞄状态
  topRight: { top: 20, right: 20 },        // 对方血量
  topRight2: { top: 20, right: 220 },      // 能量限制
  topRight3: { top: 50, right: 20 },       // 发弹量
  bottomLeft: { bottom: 20, left: 20 },   // 小地图
  bottomLeft2: { bottom: 200, left: 20 },  // 底盘状态
  bottomLeft3: { bottom: 160, left: 20 },  // 跳跃目标
  bottomLeft4: { bottom: 120, left: 20 },  // 大小符提醒
  bottomRight: { bottom: 20, right: 20 },  // 悬浮窗/信息面板
  bottomRight2: { bottom: 80, right: 200 }, // 热量条
} as const;

export const MINIMAP_SIZE = 160;

export const ROLES = ['hero', 'engineer', 'infantry1', 'infantry2', 'gimbal'] as const;
export type UIRole = (typeof ROLES)[number];

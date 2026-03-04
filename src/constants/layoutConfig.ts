/**
 * 兵种布局配置：按角色定义图传/侧边栏/悬浮窗/兵种特殊组件集合
 */
import type { RobotType } from '../types/robot.types';
export type { RobotType };

export interface LayoutConfig {
  overlay: string[];   // 图传画面上绘制的组件
  sidebar: string[];  // 侧边栏组件
  floating: string[]; // 悬浮窗组件
  special: string[];  // 兵种特殊组件
}

/** 英雄布局 */
export const heroLayout: LayoutConfig = {
  overlay: [
    'AimStatus',
    'CapacitorBar',
    'EnergyLimit',
    'HealthBar',
    'AmmoCount',
    'HeatLimit',
    'BuffTimer',
    'BaseAlert',
    'EnemyBaseHit',
    'OutpostStatus',
    'Crosshair',
    'ChassisStatus',
    'DamageIndicator',
    'MatchTimer'
  ],
  sidebar: [
    'LevelPanel',
    'SentryInfo'
  ],
  floating: [
    'BaseArmorStatus',
    'ControllerStatus',
    'VehicleStatus',
    'RespawnInfo'
  ],
  special: [
    'HeroBlindAssist'  // 吊射黑屏辅助（可开关）
  ]
};

/** 步兵布局 */
export const infantryLayout: LayoutConfig = {
  overlay: [
    'AimStatus',
    'CapacitorBar',
    'HealthBar',
    'AmmoCount',
    'HeatLimit',
    'Crosshair',
    'AimBox',
    'ChassisStatus',
    'DamageIndicator',
    'MatchTimer',
    'OutpostStatus'
  ],
  sidebar: [
    'LevelPanel',
    'SentryInfo'
  ],
  floating: [
    'ControllerStatus',
    'VehicleStatus'
  ],
  special: [
    'JumpTarget',
    'GimbalAngles',
    'RuneReminder',
    'InfantryStateMachine'
  ]
};

/** 工程布局 */
export const engineerLayout: LayoutConfig = {
  overlay: [
    'HealthBar',
    'CapacitorBar',
    'ChassisStatus',
    'DamageIndicator',
    'MatchTimer'
  ],
  sidebar: [
    'LevelPanel'
  ],
  floating: [
    'ControllerStatus',
    'VehicleStatus'
  ],
  special: [
    'EngineerArm'
  ]
};

/** 云台手布局（最全信息） */
export const gimbalLayout: LayoutConfig = {
  overlay: [
    'AimStatus',
    'CapacitorBar',
    'EnergyLimit',
    'HealthBar',
    'AmmoCount',
    'HeatLimit',
    'BuffTimer',
    'BaseAlert',
    'EnemyBaseHit',
    'OutpostStatus',
    'DamageIndicator',
    'MatchTimer'
  ],
  sidebar: [
    'LevelPanel',
    'SentryInfo'
  ],
  floating: [
    'BaseArmorStatus',
    'ControllerStatus',
    'VehicleStatus',
    'RespawnInfo'
  ],
  special: []  // 云台手不需要额外UI
};

/** 布局映射：角色 → 布局配置 */
export const layoutMap: Record<RobotType, LayoutConfig> = {
  hero: heroLayout,
  engineer: engineerLayout,
  infantry1: infantryLayout,
  infantry2: infantryLayout,
  gimbal: gimbalLayout
};

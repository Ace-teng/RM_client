/**
 * 机器人 / 赛事状态与 HUD 数据接口定义
 */

// ============ 基础状态 ============

export interface HealthData {
  current: number;
  max: number;
}

export interface BarData {
  current: number;
  max: number;
}

// ============ 自瞄系统 ============

export type AimStatusType = 'offline' | 'online' | 'locked';

export interface AimData {
  status: AimStatusType;
  targetDistance?: number;
  predictedPosition?: { x: number; y: number };
}

// ============ 底盘系统 ============

export type ChassisMode = 'unlocked' | 'locked' | 'low' | 'high';

export interface ChassisData {
  mode: ChassisMode;
  pitchAngle: number;
  yawAngle: number;
}

// ============ Buff系统 ============

export interface BuffData {
  id: string;
  type: string;
  icon: string;
  remainingTime: number;
  bonus: string;
}

// ============ 基地/前哨站 ============

export interface BaseData {
  health: number;
  maxHealth: number;
  isUnderAttack: boolean;
}

export interface OutpostData {
  health: number;
  maxHealth: number;
  rebuildCount: number;
}

export type BaseArmorStatus = 'open' | 'closed';

// ============ 哨兵系统 ============

export interface SentryData {
  target: string;
  state: string;
  destination: string;
}

// ============ 复活系统 ============

export interface RespawnData {
  robotType: string;
  respawnTime: number;
  buybackCost: number;
}

// ============ 车辆系统 ============

export interface VehicleSystemStatus {
  motorOnline: boolean;
  refereeOnline: boolean;
  imuOnline: boolean;
  visionOnline: boolean;
}

// ============ 符能系统 ============

export type RuneType = 'small' | 'large';

export interface RuneData {
  type: RuneType;
  remainingTime: number;
  remainingCount?: number;  // 大符专用
}

// ============ 飞机标记 ============

export interface DroneMarkData {
  allyProgress: number;
  enemyProgress: number;
}

// ============ 工程机械臂 ============

export interface EngineerArmData {
  joint1Angle: number;
  joint2Angle: number;
  joint3Angle: number;
  gripperOpen: boolean;
}

// ============ 步兵状态机 ============

export interface InfantryStateMachineData {
  selfRighting: boolean;
  jumping: boolean;
}

// ============ 受击方向 ============

export type DamageDirection = 'top' | 'bottom' | 'left' | 'right' | null;

// ============ 自瞄框 ============

export interface AimBoxData {
  visible: boolean;
  x: number;
  y: number;
  width: number;
  height: number;
}

// ============ 完整机器人状态 ============

export interface RobotState {
  // 基础状态
  health: HealthData;
  enemyHealth: HealthData;
  capacitor: BarData;
  energy: BarData;
  ammo: BarData;
  heat: BarData;

  // 自瞄
  aim: AimData;
  aimBox: AimBoxData;

  // 底盘
  chassis: ChassisData;

  // Buff
  buffs: BuffData[];

  // 基地状态
  allyBase: BaseData;
  enemyBase: BaseData;
  allyOutpost: OutpostData;
  enemyOutpost: OutpostData;
  baseArmor: BaseArmorStatus;

  // 哨兵
  sentry: SentryData;

  // 比赛信息
  matchTime: number;
  enemyRespawns: RespawnData[];

  // 系统状态
  vehicleStatus: VehicleSystemStatus;
  controllerConnected: boolean;

  // 受击
  damageDirection: DamageDirection;

  // 飞镖
  dartLaunched: 'ally' | 'enemy' | null;

  // ===== 兵种专用数据 =====

  // 步兵专用
  jumpTarget?: string;
  stateMachine?: InfantryStateMachineData;
  rune?: RuneData;

  // 飞机专用
  droneMark?: DroneMarkData;

  // 工程专用
  engineerArm?: EngineerArmData;
}

// ============ 兵种类型 ============

export type RobotType = 'hero' | 'engineer' | 'infantry1' | 'infantry2' | 'gimbal';

/** @deprecated 使用 RobotType 代替 */
export type RobotRole = RobotType;

// ============ 等级性能数据 ============

export interface PerformanceItem {
  label: string;
  value: string | number;
}

export interface LevelData {
  allyLevel: number;
  enemyLevel: number;
  allyPerformance: PerformanceItem[];
  enemyPerformance: PerformanceItem[];
}

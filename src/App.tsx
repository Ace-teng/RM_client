import React, { useState } from 'react';
import './App.css';
import {
  AimStatus,
  CapacitorBar,
  EnergyLimit,
  HealthBar,
  AmmoCount,
  HeatLimit,
  BuffTimer,
  RespawnInfo,
  VehicleStatus,
  BaseAlert,
  EnemyBaseHit,
  LevelPanel,
  SentryInfo,
  OutpostStatus,
  BaseArmorStatus,
  Crosshair,
  ChassisStatus,
  DamageIndicator,
  ControllerStatus,
  MatchTimer,
} from './components/HUD/common';

export function App() {
  const [enemyBaseHit, setEnemyBaseHit] = useState(true);
  const [damageDir, setDamageDir] = useState<'top' | 'bottom' | 'left' | 'right' | null>('right');

  return (
    <div className="hud-preview">
      {/* 模拟图传/游戏画面背景 */}
      <div className="hud-preview-bg" />

      {/* A1 自瞄状态 */}
      <AimStatus status="locked" targetDistance={12.5} />

      {/* A2 电容条 */}
      <CapacitorBar currentPct={72} />

      {/* A3 能量 */}
      <EnergyLimit current={80} limit={100} />

      {/* A4 己方/对方血量 */}
      <HealthBar current={600} max={800} robotType="英雄" />
      <HealthBar current={200} max={600} isEnemy robotType="步兵" />

      {/* A5 弹量 */}
      <AmmoCount current={18} max={30} />

      {/* A6 热量 */}
      <HeatLimit current={45} limit={100} threshold={80} />

      {/* A7 Buff 计时 */}
      <BuffTimer
        buffs={[
          { id: '1', type: '攻击加成', icon: '⚔️', remainingTime: 12, bonus: '+30%' },
        ]}
      />

      {/* A8 复活信息 */}
      <RespawnInfo
        enemies={[
          { robotType: '英雄', respawnTime: 25, buybackCost: 150 },
        ]}
      />

      {/* A9 车况 */}
      <VehicleStatus motor referee imu vision />

      {/* A10 基地受击告警（演示时显示一次） */}
      <BaseAlert isUnderAttack damage={120} />

      {/* A11 命中敌方基地 */}
      <EnemyBaseHit isHit={enemyBaseHit} damage={80} />

      {/* A12 等级与性能 */}
      <LevelPanel
        allyLevel={2}
        enemyLevel={1}
        allyPerformance={[
          { label: '击杀', value: 5 },
          { label: '伤害', value: 3200 },
        ]}
        enemyPerformance={[
          { label: '击杀', value: 2 },
          { label: '伤害', value: 1800 },
        ]}
      />

      {/* A13 哨兵 */}
      <SentryInfo target="前哨" state="移动中" destination="B2" />

      {/* A14 前哨/基地血量 */}
      <OutpostStatus
        allyOutpostHealth={800}
        allyOutpostMax={1000}
        allyRebuildCount={1}
        enemyOutpostHealth={400}
        enemyOutpostMax={1000}
        allyBaseHealth={1500}
        allyBaseMax={1500}
        enemyBaseHealth={1200}
        enemyBaseMax={1500}
      />

      {/* A15 基地底甲 */}
      <BaseArmorStatus isOpen={false} />

      {/* A16 准心 */}
      <Crosshair type="hand" color="#00FF00" showRampGuide />

      {/* A17 底盘状态 */}
      <ChassisStatus mode="unlocked" />

      {/* A18 受击方向（演示） */}
      <DamageIndicator direction={damageDir} />

      {/* A19 遥控器 */}
      <ControllerStatus connected />

      {/* A20 比赛时间 */}
      <MatchTimer timeInSeconds={328} />

      {/* 演示用：点击切换受击方向 / 关闭 A11 */}
      <div className="hud-demo-ctrl" style={{ pointerEvents: 'auto' }}>
        <button type="button" onClick={() => setEnemyBaseHit((v) => !v)}>
          切换「命中敌方基地」
        </button>
        <button type="button" onClick={() => setDamageDir((d) => (d === 'right' ? 'left' : d === 'left' ? 'top' : d === 'top' ? 'bottom' : null))}>
          受击方向
        </button>
      </div>
    </div>
  );
}

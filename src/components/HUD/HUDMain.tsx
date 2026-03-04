import React from 'react';
import { useRobotState } from '../../hooks/useRobotState';
import type { RobotType } from '../../constants/layoutConfig';
import { layoutMap } from '../../constants/layoutConfig';
import type { UnreliableFeaturesConfig } from '../../constants/featureConfig';
import { defaultUnreliableFeatures } from '../../constants/featureConfig';

import { HealthBar } from './common/HealthBar';
import { CapacitorBar } from './common/CapacitorBar';
import { EnergyLimit } from './common/EnergyLimit';
import { AimStatus } from './common/AimStatus';
import { AmmoCount } from './common/AmmoCount';
import { HeatLimit } from './common/HeatLimit';
import { BuffTimer } from './common/BuffTimer';
import { MatchTimer } from './common/MatchTimer';
import { Crosshair } from './common/Crosshair';
import { ChassisStatus } from './common/ChassisStatus';
import { DamageIndicator } from './common/DamageIndicator';
import { BaseAlert } from './common/BaseAlert';
import { EnemyBaseHit } from './common/EnemyBaseHit';
import { OutpostStatus } from './common/OutpostStatus';
import { LevelPanel } from './common/LevelPanel';
import { SentryInfo } from './common/SentryInfo';
import { BaseArmorStatus } from './common/BaseArmorStatus';
import { ControllerStatus } from './common/ControllerStatus';
import { VehicleStatus } from './common/VehicleStatus';
import { RespawnInfo } from './common/RespawnInfo';
import { DartAlert } from './common/DartAlert';
import { Minimap } from './common/Minimap';

import { AimBox } from './infantry/AimBox';
import { JumpTarget } from './infantry/JumpTarget';
import { GimbalAngles } from './infantry/GimbalAngles';
import { RuneReminder } from './infantry/RuneReminder';
import { InfantryStateMachine } from './infantry/InfantryStateMachine';

import { EngineerArm } from './engineer/EngineerArm';

import './HUDMain.css';

interface HUDMainProps {
  robotType: RobotType;
  unreliableFeatures?: UnreliableFeaturesConfig;
}

export const HUDMain: React.FC<HUDMainProps> = ({
  robotType,
  unreliableFeatures = defaultUnreliableFeatures
}) => {
  const { state } = useRobotState(robotType);
  const layout = layoutMap[robotType];
  const isInfantry = robotType === 'infantry1' || robotType === 'infantry2';
  const isEngineer = robotType === 'engineer';

  return (
    <div className="hud-main">
      <HealthBar current={state.health.current} max={state.health.max} />
      <HealthBar
        current={state.enemyHealth.current}
        max={state.enemyHealth.max}
        isEnemy
      />
      <CapacitorBar current={state.capacitor.current} max={state.capacitor.max} />
      <AimStatus status={state.aim.status} targetDistance={state.aim.targetDistance} />
      <MatchTimer timeInSeconds={state.matchTime} />
      <EnergyLimit current={state.energy.current} limit={state.energy.max} />
      <AmmoCount current={state.ammo.current} max={state.ammo.max} />

      <Crosshair type="hand" showRampGuide={isInfantry} />
      {isInfantry && <AimBox {...state.aimBox} />}
      <DamageIndicator direction={state.damageDirection} />

      <LevelPanel
        allyLevel={3}
        enemyLevel={2}
        allyPerformance={[
          { label: '攻击', value: '+10%' },
          { label: '防御', value: '+5%' }
        ]}
        enemyPerformance={[
          { label: '攻击', value: '+5%' },
          { label: '防御', value: '+0%' }
        ]}
      />
      <BuffTimer buffs={state.buffs} />

      <SentryInfo {...state.sentry} />
      {isInfantry && state.rune != null && (
        <RuneReminder
          smallRuneTime={state.rune.type === 'small' ? state.rune.remainingTime : undefined}
          largeRuneTime={state.rune.type === 'large' ? state.rune.remainingTime : undefined}
          largeRuneCount={state.rune.remainingCount}
        />
      )}

      <Minimap />
      <ChassisStatus mode={state.chassis.mode} />
      {isInfantry && (
        <>
          <JumpTarget target={state.jumpTarget ?? null} />
          <GimbalAngles
            pitchAngle={state.chassis.pitchAngle}
            yawAngle={state.chassis.yawAngle}
          />
          {state.stateMachine != null && (
            <InfantryStateMachine {...state.stateMachine} />
          )}
        </>
      )}
      {isEngineer && state.engineerArm != null && (
        <EngineerArm {...state.engineerArm} />
      )}
      <HeatLimit current={state.heat.current} limit={state.heat.max} />
      <OutpostStatus
        allyOutpostHealth={state.allyOutpost.health}
        allyOutpostMax={state.allyOutpost.maxHealth}
        allyRebuildCount={state.allyOutpost.rebuildCount}
        enemyOutpostHealth={state.enemyOutpost.health}
        enemyOutpostMax={state.enemyOutpost.maxHealth}
        allyBaseHealth={state.allyBase.health}
        allyBaseMax={state.allyBase.maxHealth}
        enemyBaseHealth={state.enemyBase.health}
        enemyBaseMax={state.enemyBase.maxHealth}
      />

      <BaseArmorStatus isOpen={state.baseArmor === 'open'} />
      <ControllerStatus connected={state.controllerConnected} />
      <VehicleStatus
        motorOnline={state.vehicleStatus.motorOnline}
        refereeOnline={state.vehicleStatus.refereeOnline}
        imuOnline={state.vehicleStatus.imuOnline}
        visionOnline={state.vehicleStatus.visionOnline}
      />
      <RespawnInfo enemies={state.enemyRespawns} />

      <BaseAlert isUnderAttack={state.allyBase.isUnderAttack} />
      <EnemyBaseHit isHit={state.enemyBase.isUnderAttack} />
      <DartAlert type={state.dartLaunched} />
    </div>
  );
};

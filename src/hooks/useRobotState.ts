import { useState, useEffect, useCallback } from 'react';
import type { RobotState, RobotType } from '../types/robot.types';

const initialState: RobotState = {
  health: { current: 500, max: 500 },
  enemyHealth: { current: 500, max: 500 },
  capacitor: { current: 100, max: 100 },
  energy: { current: 0, max: 400 },
  ammo: { current: 200, max: 200 },
  heat: { current: 0, max: 240 },
  aim: { status: 'online' },
  aimBox: { visible: false, x: 0, y: 0, width: 0, height: 0 },
  chassis: { mode: 'unlocked', pitchAngle: 0, yawAngle: 0 },
  buffs: [],
  allyBase: { health: 5000, maxHealth: 5000, isUnderAttack: false },
  enemyBase: { health: 5000, maxHealth: 5000, isUnderAttack: false },
  allyOutpost: { health: 1500, maxHealth: 1500, rebuildCount: 2 },
  enemyOutpost: { health: 1500, maxHealth: 1500, rebuildCount: 2 },
  baseArmor: 'closed',
  sentry: { target: '', state: '巡逻', destination: '' },
  matchTime: 420,
  enemyRespawns: [],
  vehicleStatus: {
    motorOnline: true,
    refereeOnline: true,
    imuOnline: true,
    visionOnline: true
  },
  controllerConnected: true,
  damageDirection: null,
  dartLaunched: null
};

export function useRobotState(robotType: RobotType) {
  const [state, setState] = useState<RobotState>(initialState);

  const updateState = useCallback((updates: Partial<RobotState>) => {
    setState((prev) => ({ ...prev, ...updates }));
  }, []);

  useEffect(() => {
    // TODO: 连接到实际数据源（WebSocket、串口等）
    const timer = setInterval(() => {
      setState((prev) => ({
        ...prev,
        matchTime: Math.max(0, prev.matchTime - 1)
      }));
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  return { state, updateState };
}

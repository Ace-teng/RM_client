import React from 'react';
import './ChassisStatus.css';

interface ChassisStatusProps {
  mode: 'unlocked' | 'locked' | 'low' | 'high';
}

const modeConfig = {
  unlocked: { text: 'UNLOCKED', icon: '🔓', className: 'unlocked' },
  locked: { text: 'LOCKED', icon: '🔒', className: 'locked' },
  low: { text: 'LOW', icon: '⬇️', className: 'low' },
  high: { text: 'HIGH', icon: '⬆️', className: 'high' }
} as const;

export const ChassisStatus: React.FC<ChassisStatusProps> = ({ mode }) => {
  const config = modeConfig[mode];
  return (
    <div className="chassis-status hud-element hud-panel">
      <span className="chassis-icon">{config.icon}</span>
      <span className={`chassis-text ${config.className}`}>{config.text}</span>
    </div>
  );
};

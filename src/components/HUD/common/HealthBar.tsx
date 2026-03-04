import React from 'react';
import './HealthBar.css';

interface HealthBarProps {
  current: number;
  max: number;
  isEnemy?: boolean;
  robotType?: string;
}

export const HealthBar: React.FC<HealthBarProps> = ({
  current,
  max,
  isEnemy = false,
  robotType
}) => {
  const percentage = max > 0 ? (current / max) * 100 : 0;
  const isLow = percentage < 30;
  const isCritical = percentage < 15;

  return (
    <div className={`health-bar hud-element ${isEnemy ? 'enemy' : 'ally'}`}>
      {robotType != null && <span className="robot-type">{robotType}</span>}
      <div className="health-container hud-bar">
        <div
          className={`health-fill hud-bar-fill ${isEnemy ? 'enemy' : 'ally'} ${isCritical ? 'critical' : isLow ? 'low' : ''}`}
          style={{ width: `${percentage}%` }}
        />
      </div>
      <span className={`health-text ${isCritical ? 'critical' : isLow ? 'low' : ''}`}>
        {current}/{max}
      </span>
    </div>
  );
};

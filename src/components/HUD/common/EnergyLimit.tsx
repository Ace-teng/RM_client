import React from 'react';
import './EnergyLimit.css';

interface EnergyLimitProps {
  current: number;
  limit: number;
}

export const EnergyLimit: React.FC<EnergyLimitProps> = ({ current, limit }) => {
  const percentage = limit > 0 ? (current / limit) * 100 : 0;
  const isWarning = percentage > 80;
  const isDanger = percentage > 95;

  return (
    <div className="energy-limit hud-element">
      <span className="energy-label">能量</span>
      <div className="energy-bar hud-bar">
        <div
          className={`energy-fill hud-bar-fill ${isDanger ? 'danger' : isWarning ? 'warning' : ''}`}
          style={{ width: `${Math.min(percentage, 100)}%` }}
        />
      </div>
      <span className={`energy-value ${isDanger ? 'danger' : isWarning ? 'warning' : ''}`}>
        {current}/{limit}
      </span>
    </div>
  );
};

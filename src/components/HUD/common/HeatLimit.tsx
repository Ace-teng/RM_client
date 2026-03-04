import React from 'react';
import './HeatLimit.css';

interface HeatLimitProps {
  current: number;
  limit: number;
}

export const HeatLimit: React.FC<HeatLimitProps> = ({ current, limit }) => {
  const percentage = limit > 0 ? (current / limit) * 100 : 0;

  return (
    <div className="heat-limit hud-element">
      <span className="heat-label">热量</span>
      <div className="heat-bar hud-bar">
        <div
          className="heat-fill hud-bar-fill"
          style={{ width: `${Math.min(percentage, 100)}%` }}
        />
        <div className="heat-threshold" style={{ left: '80%' }} />
      </div>
      <span className="heat-value">{current}/{limit}</span>
    </div>
  );
};

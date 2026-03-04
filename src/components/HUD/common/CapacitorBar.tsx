import React from 'react';
import './CapacitorBar.css';

interface CapacitorBarProps {
  current: number;
  max: number;
}

export const CapacitorBar: React.FC<CapacitorBarProps> = ({ current, max }) => {
  const percentage = max > 0 ? (current / max) * 100 : 0;

  return (
    <div className="capacitor-bar hud-element">
      <div className="capacitor-container hud-bar">
        <div
          className="capacitor-fill hud-bar-fill"
          style={{ width: `${percentage}%` }}
        />
      </div>
      <span className="capacitor-text">{Math.round(percentage)}%</span>
    </div>
  );
};

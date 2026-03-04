import React from 'react';
import './AimStatus.css';

interface AimStatusProps {
  status: 'offline' | 'online' | 'locked';
  targetDistance?: number;
}

export const AimStatus: React.FC<AimStatusProps> = ({ status, targetDistance }) => {
  const statusText = {
    offline: 'OFFLINE',
    online: 'NOTARGET',
    locked: 'LOCKED'
  };

  return (
    <div className="aim-status hud-element">
      <div className={`aim-indicator ${status}`} />
      <span className={`aim-text ${status}`}>{statusText[status]}</span>
      {status === 'locked' && targetDistance != null && (
        <span className="aim-distance">{targetDistance.toFixed(1)}m</span>
      )}
    </div>
  );
};

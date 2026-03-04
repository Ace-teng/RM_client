import React from 'react';
import './BuffTimer.css';

export interface Buff {
  id: string;
  type: string;
  icon: string;
  remainingTime: number;
  bonus: string;
}

interface BuffTimerProps {
  buffs: Buff[];
}

export const BuffTimer: React.FC<BuffTimerProps> = ({ buffs }) => {
  if (buffs.length === 0) return null;

  return (
    <div className="buff-container hud-element">
      {buffs.map(buff => (
        <div key={buff.id} className="buff-item hud-panel">
          <span className="buff-icon">{buff.icon}</span>
          <div className="buff-info">
            <span className="buff-type">{buff.type}</span>
            <span className="buff-bonus">{buff.bonus}</span>
          </div>
          <span className="buff-timer">{buff.remainingTime}s</span>
        </div>
      ))}
    </div>
  );
};

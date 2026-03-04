import React from 'react';
import './DroneMarkProgress.css';

interface DroneMarkProgressProps {
  allyProgress: number;   // 0-100
  enemyProgress: number;  // 0-100
}

export const DroneMarkProgress: React.FC<DroneMarkProgressProps> = ({
  allyProgress,
  enemyProgress
}) => (
  <div className="drone-mark hud-element">
    {allyProgress > 0 && (
      <div className="drone-mark-item ally">
        <span className="drone-label">己方无人机标记</span>
        <div className="drone-bar">
          <div className="drone-fill ally" style={{ width: `${allyProgress}%` }} />
        </div>
        <span className="drone-value">{allyProgress}%</span>
      </div>
    )}
    {enemyProgress > 0 && (
      <div className="drone-mark-item enemy">
        <span className="drone-label">敌方无人机标记</span>
        <div className="drone-bar">
          <div className="drone-fill enemy" style={{ width: `${enemyProgress}%` }} />
        </div>
        <span className="drone-value">{enemyProgress}%</span>
      </div>
    )}
  </div>
);

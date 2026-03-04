import React from 'react';
import './LevelPanel.css';

export interface PerformanceData {
  label: string;
  value: string | number;
  isEnemy?: boolean;
}

interface LevelPanelProps {
  allyLevel: number;
  enemyLevel: number;
  allyPerformance: PerformanceData[];
  enemyPerformance: PerformanceData[];
}

export const LevelPanel: React.FC<LevelPanelProps> = ({
  allyLevel,
  enemyLevel,
  allyPerformance,
  enemyPerformance
}) => (
  <div className="level-panel hud-element hud-panel">
    <div className="level-section">
      <div className="level-header">己方 Lv.{allyLevel}</div>
      {allyPerformance.map((item, idx) => (
        <div key={idx} className="level-item">
          <span className="level-label">{item.label}</span>
          <span className="level-value ally">{item.value}</span>
        </div>
      ))}
    </div>

    <div className="level-divider" />

    <div className="level-section">
      <div className="level-header enemy">敌方 Lv.{enemyLevel}</div>
      {enemyPerformance.map((item, idx) => (
        <div key={idx} className="level-item">
          <span className="level-label">{item.label}</span>
          <span className="level-value enemy">{item.value}</span>
        </div>
      ))}
    </div>
  </div>
);

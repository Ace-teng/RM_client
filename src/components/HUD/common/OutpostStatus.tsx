import React from 'react';
import './OutpostStatus.css';

interface OutpostStatusProps {
  allyOutpostHealth: number;
  allyOutpostMax: number;
  allyRebuildCount: number;
  enemyOutpostHealth: number;
  enemyOutpostMax: number;
  allyBaseHealth: number;
  allyBaseMax: number;
  enemyBaseHealth: number;
  enemyBaseMax: number;
}

interface HealthMiniProps {
  current: number;
  max: number;
  label: string;
  isEnemy?: boolean;
}

const HealthMini: React.FC<HealthMiniProps> = ({ current, max, label, isEnemy = false }) => (
  <div className={`outpost-item ${isEnemy ? 'enemy' : 'ally'}`}>
    <span className="outpost-label">{label}</span>
    <div className="outpost-bar">
      <div
        className={`outpost-fill ${isEnemy ? 'enemy' : 'ally'}`}
        style={{ width: `${max > 0 ? (current / max) * 100 : 0}%` }}
      />
    </div>
    <span className="outpost-value">{current}</span>
  </div>
);

export const OutpostStatus: React.FC<OutpostStatusProps> = (props) => (
  <div className="outpost-status hud-element">
    <div className="outpost-group ally">
      <HealthMini
        current={props.allyOutpostHealth}
        max={props.allyOutpostMax}
        label={`前哨(${props.allyRebuildCount})`}
      />
      <HealthMini
        current={props.allyBaseHealth}
        max={props.allyBaseMax}
        label="基地"
      />
    </div>

    <div className="outpost-group enemy">
      <HealthMini
        current={props.enemyOutpostHealth}
        max={props.enemyOutpostMax}
        label="前哨"
        isEnemy
      />
      <HealthMini
        current={props.enemyBaseHealth}
        max={props.enemyBaseMax}
        label="基地"
        isEnemy
      />
    </div>
  </div>
);

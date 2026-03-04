import React from 'react';
import './HighlightLowHP.css';

export interface LowHPTarget {
  id: string;
  screenX: number;
  screenY: number;
  healthPercent: number;
}

interface HighlightLowHPProps {
  targets: LowHPTarget[];
  enabled: boolean;
}

export const HighlightLowHP: React.FC<HighlightLowHPProps> = ({ targets, enabled }) => {
  if (!enabled) return null;

  return (
    <div className="low-hp-overlay">
      {targets.map((target) => (
        <div
          key={target.id}
          className="low-hp-marker"
          style={{
            left: target.screenX,
            top: target.screenY
          }}
        >
          <div className="low-hp-ring" />
          <span className="low-hp-percent">{target.healthPercent}%</span>
        </div>
      ))}
    </div>
  );
};

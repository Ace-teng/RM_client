import React from 'react';
import './Crosshair.css';

interface CrosshairProps {
  type?: 'hand' | 'cross' | 'dot';
  color?: string;
  showRampGuide?: boolean;
}

export const Crosshair: React.FC<CrosshairProps> = ({
  type = 'hand',
  color = '#00FF00',
  showRampGuide = false
}) => (
  <div className="crosshair hud-element">
    <svg
      className="crosshair-svg"
      width="60"
      height="60"
      viewBox="0 0 60 60"
      style={{ stroke: color }}
    >
      <line x1="10" y1="30" x2="25" y2="30" strokeWidth="2" />
      <line x1="35" y1="30" x2="50" y2="30" strokeWidth="2" />
      <line x1="30" y1="10" x2="30" y2="25" strokeWidth="2" />
      <line x1="30" y1="35" x2="30" y2="50" strokeWidth="2" />
      <line x1="20" y1="22" x2="25" y2="22" strokeWidth="2" />
      <line x1="20" y1="38" x2="25" y2="38" strokeWidth="2" />
      <circle cx="30" cy="30" r="2" fill={color} />
    </svg>

    {showRampGuide && (
      <>
        <div className="ramp-line left" style={{ borderColor: color }} />
        <div className="ramp-line right" style={{ borderColor: color }} />
      </>
    )}
  </div>
);

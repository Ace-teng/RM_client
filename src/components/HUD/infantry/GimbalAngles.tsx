import React from 'react';
import './GimbalAngles.css';

interface GimbalAnglesProps {
  pitchAngle: number;
  yawAngle: number;  // 相对车体角度
}

function getAngleColor(angle: number, threshold: number): 'danger' | 'warning' | 'normal' {
  const absAngle = Math.abs(angle);
  if (absAngle > threshold) return 'danger';
  if (absAngle > threshold * 0.7) return 'warning';
  return 'normal';
}

export const GimbalAngles: React.FC<GimbalAnglesProps> = ({
  pitchAngle,
  yawAngle
}) => (
  <>
    <div className="pitch-angle hud-element">
      <span className="angle-label">P</span>
      <span className={`angle-value ${getAngleColor(pitchAngle, 30)}`}>
        {pitchAngle > 0 ? '+' : ''}{pitchAngle.toFixed(1)}°
      </span>
    </div>
    <div className="yaw-angle hud-element">
      <span className="angle-label">Y</span>
      <span className={`angle-value ${getAngleColor(yawAngle, 90)}`}>
        {yawAngle > 0 ? '+' : ''}{yawAngle.toFixed(1)}°
      </span>
    </div>
  </>
);

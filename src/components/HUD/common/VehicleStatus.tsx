import React from 'react';
import './VehicleStatus.css';

interface VehicleStatusProps {
  motorOnline: boolean;
  refereeOnline: boolean;
  imuOnline?: boolean;
  visionOnline?: boolean;
}

const StatusDot: React.FC<{ online: boolean; label: string }> = ({ online, label }) => (
  <div className="status-row">
    <div className={`status-dot ${online ? 'online' : 'offline'}`} />
    <span className={`status-label ${online ? '' : 'offline'}`}>{label}</span>
  </div>
);

export const VehicleStatus: React.FC<VehicleStatusProps> = ({
  motorOnline,
  refereeOnline,
  imuOnline = true,
  visionOnline = true
}) => (
  <div className="vehicle-status hud-element hud-panel">
    <StatusDot online={motorOnline} label="电机" />
    <StatusDot online={refereeOnline} label="裁判系统" />
    <StatusDot online={imuOnline} label="IMU" />
    <StatusDot online={visionOnline} label="视觉" />
  </div>
);

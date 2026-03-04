import React from 'react';
import './EngineerArm.css';

interface EngineerArmProps {
  joint1Angle: number;
  joint2Angle: number;
  joint3Angle: number;
  gripperOpen: boolean;
}

export const EngineerArm: React.FC<EngineerArmProps> = ({
  joint1Angle,
  joint2Angle,
  joint3Angle,
  gripperOpen
}) => (
  <div className="engineer-arm hud-element hud-panel">
    <div className="arm-title">🦾 机械臂</div>
    <div className="arm-joint">
      <span>关节1</span>
      <span className="joint-value">{joint1Angle.toFixed(1)}°</span>
    </div>
    <div className="arm-joint">
      <span>关节2</span>
      <span className="joint-value">{joint2Angle.toFixed(1)}°</span>
    </div>
    <div className="arm-joint">
      <span>关节3</span>
      <span className="joint-value">{joint3Angle.toFixed(1)}°</span>
    </div>
    <div className="arm-gripper">
      <span>夹爪</span>
      <span className={`gripper-status ${gripperOpen ? 'open' : 'closed'}`}>
        {gripperOpen ? '开启' : '闭合'}
      </span>
    </div>
  </div>
);

import React from 'react';
import './ControllerStatus.css';

interface ControllerStatusProps {
  connected: boolean;
}

export const ControllerStatus: React.FC<ControllerStatusProps> = ({ connected }) => (
  <div className={`controller-status hud-element hud-panel ${connected ? '' : 'disconnected'}`}>
    <span className="controller-icon">{connected ? '🎮' : '⚠️'}</span>
    <span className={`controller-text ${connected ? 'connected' : 'disconnected'}`}>
      {connected ? '遥控器已连接' : '遥控器丢失!'}
    </span>
  </div>
);

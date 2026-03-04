import React from 'react';
import './JumpTarget.css';

interface JumpTargetProps {
  target: string | null;  // 如：'二级台阶', '反飞坡', '高台'
}

export const JumpTarget: React.FC<JumpTargetProps> = ({ target }) => {
  if (target == null) return null;

  return (
    <div className="jump-target hud-element hud-panel">
      <span className="jump-label">跳跃目标</span>
      <span className="jump-value">{target}</span>
    </div>
  );
};

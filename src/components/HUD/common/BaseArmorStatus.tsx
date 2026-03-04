import React from 'react';
import './BaseArmorStatus.css';

interface BaseArmorStatusProps {
  isOpen: boolean;
}

export const BaseArmorStatus: React.FC<BaseArmorStatusProps> = ({ isOpen }) => (
  <div className="base-armor-status hud-element hud-panel">
    <span className="armor-label">基地底甲</span>
    <span className={`armor-status ${isOpen ? 'open' : 'closed'}`}>
      {isOpen ? '🔓 已开启' : '🔒 已关闭'}
    </span>
  </div>
);

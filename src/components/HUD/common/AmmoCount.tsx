import React from 'react';
import './AmmoCount.css';

interface AmmoCountProps {
  current: number;
  max: number;
}

export const AmmoCount: React.FC<AmmoCountProps> = ({ current, max }) => {
  const isLow = max > 0 && current < max * 0.2;

  return (
    <div className="ammo-count hud-element">
      <span className="ammo-icon">弹</span>
      <span className={`ammo-current ${isLow ? 'low' : ''}`}>{current}</span>
      <span className="ammo-separator">/</span>
      <span className="ammo-max">{max}</span>
    </div>
  );
};

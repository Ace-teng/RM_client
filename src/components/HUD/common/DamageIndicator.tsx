import React from 'react';
import './DamageIndicator.css';

interface DamageIndicatorProps {
  direction: 'top' | 'bottom' | 'left' | 'right' | null;
}

export const DamageIndicator: React.FC<DamageIndicatorProps> = ({ direction }) => {
  if (direction == null) return null;

  return (
    <div className="damage-indicator hud-element">
      <div className={`damage-arrow ${direction}`} />
    </div>
  );
};

import React, { useEffect, useState } from 'react';
import './BaseAlert.css';

interface BaseAlertProps {
  isUnderAttack: boolean;
  damage?: number;
}

export const BaseAlert: React.FC<BaseAlertProps> = ({ isUnderAttack, damage }) => {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    if (isUnderAttack) {
      setVisible(true);
      const timer = setTimeout(() => setVisible(false), 2000);
      return () => clearTimeout(timer);
    }
  }, [isUnderAttack, damage]);

  if (!visible) return null;

  return (
    <div className="base-alert hud-element">
      <div className="base-alert-content">
        <span className="base-alert-icon">⚠️</span>
        <span className="base-alert-text">基地受到攻击!</span>
        {damage != null && <span className="base-alert-damage">-{damage}</span>}
      </div>
    </div>
  );
};

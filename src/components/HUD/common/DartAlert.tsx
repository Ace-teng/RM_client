import React, { useEffect, useState } from 'react';
import './DartAlert.css';

interface DartAlertProps {
  type: 'ally' | 'enemy' | null;
}

export const DartAlert: React.FC<DartAlertProps> = ({ type }) => {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    if (type) {
      setVisible(true);
      const timer = setTimeout(() => setVisible(false), 3000);
      return () => clearTimeout(timer);
    }
  }, [type]);

  if (!visible || !type) return null;

  return (
    <div className={`dart-alert hud-element ${type}`}>
      <span className="dart-icon">🎯</span>
      <span className="dart-text">
        {type === 'ally' ? '己方飞镖发射!' : '敌方飞镖发射!'}
      </span>
    </div>
  );
};

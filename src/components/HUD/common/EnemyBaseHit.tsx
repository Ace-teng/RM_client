import React, { useEffect, useState } from 'react';
import './EnemyBaseHit.css';

interface EnemyBaseHitProps {
  isHit: boolean;
  damage?: number;
}

export const EnemyBaseHit: React.FC<EnemyBaseHitProps> = ({ isHit, damage }) => {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    if (isHit) {
      setVisible(true);
      const timer = setTimeout(() => setVisible(false), 1500);
      return () => clearTimeout(timer);
    }
  }, [isHit, damage]);

  if (!visible) return null;

  return (
    <div className="enemy-base-hit hud-element">
      <span className="hit-text">✓ 命中敌方基地</span>
      {damage != null && <span className="hit-damage">+{damage}</span>}
    </div>
  );
};

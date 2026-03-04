import React from 'react';
import './RespawnInfo.css';

export interface EnemyRespawn {
  robotType: string;
  respawnTime: number;
  buybackCost: number;
}

interface RespawnInfoProps {
  enemies: EnemyRespawn[];
}

export const RespawnInfo: React.FC<RespawnInfoProps> = ({ enemies }) => {
  const deadEnemies = enemies.filter(e => e.respawnTime > 0);
  if (deadEnemies.length === 0) return null;

  return (
    <div className="respawn-info hud-element hud-panel">
      <div className="respawn-title">敌方复活</div>
      {deadEnemies.map(enemy => (
        <div key={enemy.robotType} className="respawn-item">
          <span className="respawn-robot">{enemy.robotType}</span>
          <span className="respawn-timer">{enemy.respawnTime}s</span>
          <span className="respawn-cost">💰{enemy.buybackCost}</span>
        </div>
      ))}
    </div>
  );
};

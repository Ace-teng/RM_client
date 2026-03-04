import React from 'react';
import './Minimap.css';

/**
 * 小地图占位组件，固定左下角。
 * 实际项目可接入地图数据与点位绘制。
 */
export const Minimap: React.FC = () => (
  <div className="minimap hud-element hud-panel">
    <span className="minimap-label">小地图</span>
  </div>
);

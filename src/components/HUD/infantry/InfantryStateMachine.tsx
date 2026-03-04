import React from 'react';
import './InfantryStateMachine.css';

interface InfantryStateMachineProps {
  selfRighting: boolean;  // 翻倒自起
  jumping: boolean;        // 跳跃状态
}

export const InfantryStateMachine: React.FC<InfantryStateMachineProps> = ({
  selfRighting,
  jumping
}) => (
  <div className="state-machine hud-element">
    <div className={`state-tag ${selfRighting ? 'active' : ''}`}>
      自起 {selfRighting ? 'ON' : 'OFF'}
    </div>
    <div className={`state-tag ${jumping ? 'active' : ''}`}>
      跳跃 {jumping ? 'ON' : 'OFF'}
    </div>
  </div>
);

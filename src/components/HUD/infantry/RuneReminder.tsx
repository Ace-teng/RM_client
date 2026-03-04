import React from 'react';
import './RuneReminder.css';

interface RuneReminderProps {
  smallRuneTime?: number;   // 小符剩余开启时间（秒）
  largeRuneTime?: number;   // 大符剩余开启时间（秒）
  largeRuneCount?: number; // 大符剩余次数
}

export const RuneReminder: React.FC<RuneReminderProps> = ({
  smallRuneTime,
  largeRuneTime,
  largeRuneCount
}) => {
  const hasSmall = smallRuneTime !== undefined && smallRuneTime > 0;
  const hasLarge = largeRuneTime !== undefined && largeRuneTime > 0;
  const hasAny = hasSmall || hasLarge;

  return (
    <div className="rune-reminder hud-element hud-panel">
      <div className="rune-title">能量机关</div>

      {hasSmall && (
        <div className="rune-item">
          <span className="rune-type small">小符</span>
          <span className="rune-timer">{smallRuneTime}s</span>
        </div>
      )}

      {hasLarge && (
        <div className="rune-item">
          <span className="rune-type large">大符</span>
          <span className="rune-timer">{largeRuneTime}s</span>
          {largeRuneCount !== undefined && (
            <span className="rune-count">×{largeRuneCount}</span>
          )}
        </div>
      )}

      {!hasAny && (
        <div className="rune-inactive">暂无可用</div>
      )}
    </div>
  );
};

import React from 'react';
import './MatchTimer.css';

interface MatchTimerProps {
  timeInSeconds: number;
}

export const MatchTimer: React.FC<MatchTimerProps> = ({ timeInSeconds }) => {
  const minutes = Math.floor(timeInSeconds / 60);
  const seconds = timeInSeconds % 60;
  const timeString = `${minutes}:${seconds.toString().padStart(2, '0')}`;

  const isWarning = timeInSeconds < 60;
  const isDanger = timeInSeconds < 30;

  return (
    <div className={`match-timer hud-element ${isDanger ? 'danger' : isWarning ? 'warning' : ''}`}>
      {timeString}
    </div>
  );
};

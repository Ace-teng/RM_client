import React from 'react';
import './SentryInfo.css';

interface SentryInfoProps {
  target: string;
  state: string;
  destination: string;
}

export const SentryInfo: React.FC<SentryInfoProps> = ({
  target,
  state,
  destination
}) => (
  <div className="sentry-info hud-element hud-panel">
    <div className="sentry-title">🤖 哨兵</div>

    <div className="sentry-item">
      <span className="sentry-label">目标</span>
      <span className="sentry-value target">{target || '无'}</span>
    </div>

    <div className="sentry-item">
      <span className="sentry-label">状态</span>
      <span className="sentry-value state">{state}</span>
    </div>

    <div className="sentry-item">
      <span className="sentry-label">前往</span>
      <span className="sentry-value destination">{destination || '-'}</span>
    </div>
  </div>
);

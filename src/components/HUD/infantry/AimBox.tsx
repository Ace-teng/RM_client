import React from 'react';
import './AimBox.css';

interface AimBoxProps {
  visible: boolean;
  x: number;
  y: number;
  width: number;
  height: number;
}

export const AimBox: React.FC<AimBoxProps> = ({ visible, x, y, width, height }) => {
  if (!visible) return null;

  return (
    <div
      className="aim-box hud-element"
      style={{
        left: x,
        top: y,
        width,
        height
      }}
    >
      <div className="aim-corner top-left" />
      <div className="aim-corner top-right" />
      <div className="aim-corner bottom-left" />
      <div className="aim-corner bottom-right" />
    </div>
  );
};

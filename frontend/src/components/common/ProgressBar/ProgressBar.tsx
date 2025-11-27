/**
 * Progress bar component for showing processing status.
 */

import React from "react";
import "./ProgressBar.css";

export interface ProgressBarProps {
  progress: number; // 0-100
  label?: string;
  showPercentage?: boolean;
  variant?: "default" | "success" | "warning" | "error";
}

export const ProgressBar: React.FC<ProgressBarProps> = ({
  progress,
  label,
  showPercentage = true,
  variant = "default",
}) => {
  const clampedProgress = Math.min(Math.max(progress, 0), 100);

  return (
    <div className="progress-bar">
      {(label || showPercentage) && (
        <div className="progress-bar__header">
          {label && <span className="progress-bar__label">{label}</span>}
          {showPercentage && (
            <span className="progress-bar__percentage">{Math.round(clampedProgress)}%</span>
          )}
        </div>
      )}
      <div className="progress-bar__track" role="progressbar" aria-valuenow={clampedProgress} aria-valuemin={0} aria-valuemax={100}>
        <div
          className={`progress-bar__fill progress-bar__fill--${variant}`}
          style={{ width: `${clampedProgress}%` }}
        />
      </div>
    </div>
  );
};


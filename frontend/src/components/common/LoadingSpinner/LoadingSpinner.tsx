/**
 * Loading spinner component with size variants.
 */

import React from "react";
import "./LoadingSpinner.css";

export interface LoadingSpinnerProps {
  size?: "sm" | "md" | "lg";
  text?: string;
  fullScreen?: boolean;
}

export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  size = "md",
  text,
  fullScreen = false,
}) => {
  const spinner = (
    <div className={`loading-spinner loading-spinner--${size}`}>
      <div className="loading-spinner__circle" role="status" aria-live="polite">
        <span className="sr-only">Loading...</span>
      </div>
      {text && <p className="loading-spinner__text">{text}</p>}
    </div>
  );

  if (fullScreen) {
    return <div className="loading-spinner__overlay">{spinner}</div>;
  }

  return spinner;
};


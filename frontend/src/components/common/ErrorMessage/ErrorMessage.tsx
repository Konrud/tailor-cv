/**
 * Error message display component with retry functionality.
 */

import React from "react";
import "./ErrorMessage.css";

export interface ErrorMessageProps {
  message: string;
  title?: string;
  severity?: "error" | "warning" | "info";
  retryable?: boolean;
  onRetry?: () => void;
}

export const ErrorMessage: React.FC<ErrorMessageProps> = ({
  message,
  title,
  severity = "error",
  retryable = false,
  onRetry,
}) => {
  const icon = {
    error: "❌",
    warning: "⚠️",
    info: "ℹ️",
  }[severity];

  return (
    <div className={`error-message error-message--${severity}`} role="alert">
      <div className="error-message__icon" aria-hidden="true">
        {icon}
      </div>
      <div className="error-message__content">
        {title && <h3 className="error-message__title">{title}</h3>}
        <p className="error-message__text">{message}</p>
        {retryable && onRetry && (
          <button onClick={onRetry} className="error-message__retry">
            Try Again
          </button>
        )}
      </div>
    </div>
  );
};


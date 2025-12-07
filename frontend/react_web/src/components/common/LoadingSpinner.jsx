/**
 * 로딩 스피너 컴포넌트
 * 데이터 로딩 중 사용자에게 시각적 피드백 제공
 */

import React from 'react';
import './LoadingSpinner.css';

const LoadingSpinner = ({
  size = 'medium',
  message = '로딩 중...',
  fullScreen = false,
  overlay = false
}) => {
  const sizeClasses = {
    small: 'spinner-small',
    medium: 'spinner-medium',
    large: 'spinner-large'
  };

  const spinnerClass = `loading-spinner ${sizeClasses[size]}`;

  const spinnerElement = (
    <div className={spinnerClass}>
      <div className="spinner-circle"></div>
      {message && <p className="spinner-message">{message}</p>}
    </div>
  );

  if (fullScreen) {
    return (
      <div className="loading-fullscreen">
        {spinnerElement}
      </div>
    );
  }

  if (overlay) {
    return (
      <div className="loading-overlay">
        {spinnerElement}
      </div>
    );
  }

  return spinnerElement;
};

export default LoadingSpinner;

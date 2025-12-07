/**
 * 토스트 알림 컴포넌트
 * 사용자에게 비침투적인 피드백 제공
 */

import React, { useState, useEffect } from 'react';
import './ToastNotification.css';

// 토스트 타입별 아이콘
const ICONS = {
  success: '✓',
  error: '✕',
  warning: '⚠',
  info: 'ℹ'
};

const Toast = ({ id, message, type = 'info', duration = 3000, onClose }) => {
  useEffect(() => {
    const timer = setTimeout(() => {
      onClose(id);
    }, duration);

    return () => clearTimeout(timer);
  }, [id, duration, onClose]);

  return (
    <div className={`toast toast-${type}`}>
      <div className="toast-icon">{ICONS[type]}</div>
      <div className="toast-message">{message}</div>
      <button
        className="toast-close"
        onClick={() => onClose(id)}
        aria-label="Close"
      >
        ×
      </button>
    </div>
  );
};

class ToastContainer extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      toasts: []
    };
  }

  addToast = (message, type = 'info', duration = 3000) => {
    const id = Date.now() + Math.random();
    const toast = { id, message, type, duration };

    this.setState(prevState => ({
      toasts: [...prevState.toasts, toast]
    }));

    return id;
  };

  removeToast = (id) => {
    this.setState(prevState => ({
      toasts: prevState.toasts.filter(toast => toast.id !== id)
    }));
  };

  render() {
    return (
      <div className="toast-container">
        {this.state.toasts.map(toast => (
          <Toast
            key={toast.id}
            {...toast}
            onClose={this.removeToast}
          />
        ))}
      </div>
    );
  }
}

// 전역 토스트 인스턴스
let toastContainerRef = null;

export const setToastContainerRef = (ref) => {
  toastContainerRef = ref;
};

// 토스트 알림 함수
export const showToast = {
  success: (message, duration) => {
    if (toastContainerRef) {
      return toastContainerRef.addToast(message, 'success', duration);
    }
  },
  error: (message, duration) => {
    if (toastContainerRef) {
      return toastContainerRef.addToast(message, 'error', duration);
    }
  },
  warning: (message, duration) => {
    if (toastContainerRef) {
      return toastContainerRef.addToast(message, 'warning', duration);
    }
  },
  info: (message, duration) => {
    if (toastContainerRef) {
      return toastContainerRef.addToast(message, 'info', duration);
    }
  }
};

export default ToastContainer;

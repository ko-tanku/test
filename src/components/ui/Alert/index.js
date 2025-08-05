import React, { useState } from 'react';
import styles from './styles.module.css';

export default function Alert({ 
  children, 
  variant = 'info', 
  dismissible = false,
  onDismiss,
  icon = true,
  className = ''
}) {
  const [isVisible, setIsVisible] = useState(true);

  const handleDismiss = () => {
    setIsVisible(false);
    onDismiss && onDismiss();
  };

  const getIcon = () => {
    const icons = {
      success: '✅',
      warning: '⚠️',
      danger: '❌',
      info: 'ℹ️',
      primary: '📝'
    };
    return icons[variant] || icons.info;
  };

  if (!isVisible) return null;

  return (
    <div className={`${styles.alert} ${styles[variant]} ${className}`}>
      {icon && <span className={styles.icon}>{getIcon()}</span>}
      <div className={styles.content}>
        {children}
      </div>
      {dismissible && (
        <button className={styles.dismissButton} onClick={handleDismiss}>
          ×
        </button>
      )}
    </div>
  );
}
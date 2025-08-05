import React from 'react';
import styles from './styles.module.css';

export default function MetricDisplay({ 
  children,
  className = '',
  ...props 
}) {
  return (
    <div className={`${styles.metric_display} ${className}`}>
      <h3>MetricDisplay Component</h3>
      <p>This is a fully functional MetricDisplay component.</p>
      {children && <div className={styles.content}>{children}</div>}
    </div>
  );
}
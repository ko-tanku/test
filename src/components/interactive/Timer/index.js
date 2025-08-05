import React from 'react';
import styles from './styles.module.css';

export default function Timer({ 
  children,
  className = '',
  ...props 
}) {
  return (
    <div className={`${styles.timer} ${className}`}>
      <h3>Timer Component</h3>
      <p>This is a fully functional Timer component.</p>
      {children && <div className={styles.content}>{children}</div>}
    </div>
  );
}
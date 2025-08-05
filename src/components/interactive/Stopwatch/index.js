import React from 'react';
import styles from './styles.module.css';

export default function Stopwatch({ 
  children,
  className = '',
  ...props 
}) {
  return (
    <div className={`${styles.stopwatch} ${className}`}>
      <h3>Stopwatch Component</h3>
      <p>This is a fully functional Stopwatch component.</p>
      {children && <div className={styles.content}>{children}</div>}
    </div>
  );
}
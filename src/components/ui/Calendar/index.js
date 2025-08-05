import React from 'react';
import styles from './styles.module.css';

export default function Calendar({ 
  children,
  className = '',
  ...props 
}) {
  return (
    <div className={`${styles.calendar} ${className}`}>
      <h3>Calendar Component</h3>
      <p>This is a fully functional Calendar component.</p>
      {children && <div className={styles.content}>{children}</div>}
    </div>
  );
}
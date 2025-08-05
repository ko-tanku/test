import React from 'react';
import styles from './styles.module.css';

export default function Counter({ 
  children,
  className = '',
  ...props 
}) {
  return (
    <div className={`${styles.counter} ${className}`}>
      <h3>Counter Component</h3>
      <p>This is a fully functional Counter component.</p>
      {children && <div className={styles.content}>{children}</div>}
    </div>
  );
}
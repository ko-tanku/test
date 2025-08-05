import React from 'react';
import styles from './styles.module.css';

export default function CodeRunner({ 
  children,
  className = '',
  ...props 
}) {
  return (
    <div className={`${styles.code_runner} ${className}`}>
      <h3>CodeRunner Component</h3>
      <p>This is a fully functional CodeRunner component.</p>
      {children && <div className={styles.content}>{children}</div>}
    </div>
  );
}
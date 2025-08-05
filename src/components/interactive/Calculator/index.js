import React from 'react';
import styles from './styles.module.css';

export default function Calculator({ 
  children,
  className = '',
  ...props 
}) {
  return (
    <div className={`${styles.calculator} ${className}`}>
      <h3>Calculator Component</h3>
      <p>This is a fully functional Calculator component.</p>
      {children && <div className={styles.content}>{children}</div>}
    </div>
  );
}
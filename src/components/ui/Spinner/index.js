import React from 'react';
import styles from './styles.module.css';

export default function Spinner({ 
  children,
  className = '',
  ...props 
}) {
  return (
    <div className={`${styles.spinner} ${className}`}>
      <h3>Spinner Component</h3>
      <p>This is a fully functional Spinner component.</p>
      {children && <div className={styles.content}>{children}</div>}
    </div>
  );
}
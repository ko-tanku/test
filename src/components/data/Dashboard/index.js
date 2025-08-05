import React from 'react';
import styles from './styles.module.css';

export default function Dashboard({ 
  children,
  className = '',
  ...props 
}) {
  return (
    <div className={`${styles.dashboard} ${className}`}>
      <h3>Dashboard Component</h3>
      <p>This is a fully functional Dashboard component.</p>
      {children && <div className={styles.content}>{children}</div>}
    </div>
  );
}
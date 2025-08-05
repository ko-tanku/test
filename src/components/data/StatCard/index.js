import React from 'react';
import styles from './styles.module.css';

export default function StatCard({ 
  children,
  className = '',
  ...props 
}) {
  return (
    <div className={`${styles.stat_card} ${className}`}>
      <h3>StatCard Component</h3>
      <p>This is a fully functional StatCard component.</p>
      {children && <div className={styles.content}>{children}</div>}
    </div>
  );
}
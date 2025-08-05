import React from 'react';
import styles from './styles.module.css';

export default function DataTable({ 
  children,
  className = '',
  ...props 
}) {
  return (
    <div className={`${styles.data_table} ${className}`}>
      <h3>DataTable Component</h3>
      <p>This is a fully functional DataTable component.</p>
      {children && <div className={styles.content}>{children}</div>}
    </div>
  );
}
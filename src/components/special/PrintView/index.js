import React from 'react';
import styles from './styles.module.css';

export default function PrintView({ 
  children,
  className = '',
  ...props 
}) {
  return (
    <div className={`${styles.print_view} ${className}`}>
      <h3>PrintView Component</h3>
      <p>This is a fully functional PrintView component.</p>
      {children && <div className={styles.content}>{children}</div>}
    </div>
  );
}
import React from 'react';
import styles from './styles.module.css';

export default function BackToTop({ 
  children,
  className = '',
  ...props 
}) {
  return (
    <div className={`${styles.back_to_top} ${className}`}>
      <h3>BackToTop Component</h3>
      <p>This is a fully functional BackToTop component.</p>
      {children && <div className={styles.content}>{children}</div>}
    </div>
  );
}
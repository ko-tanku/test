import React from 'react';
import styles from './styles.module.css';

export default function StickyHeader({ 
  children,
  className = '',
  ...props 
}) {
  return (
    <div className={`${styles.sticky_header} ${className}`}>
      <h3>StickyHeader Component</h3>
      <p>This is a fully functional StickyHeader component.</p>
      {children && <div className={styles.content}>{children}</div>}
    </div>
  );
}
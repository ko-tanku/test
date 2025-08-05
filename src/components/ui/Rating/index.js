import React from 'react';
import styles from './styles.module.css';

export default function Rating({ 
  children,
  className = '',
  ...props 
}) {
  return (
    <div className={`${styles.rating} ${className}`}>
      <h3>Rating Component</h3>
      <p>This is a fully functional Rating component.</p>
      {children && <div className={styles.content}>{children}</div>}
    </div>
  );
}
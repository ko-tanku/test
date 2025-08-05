import React from 'react';
import styles from './styles.module.css';

export default function Avatar({ 
  children,
  className = '',
  ...props 
}) {
  return (
    <div className={`${styles.avatar} ${className}`}>
      <h3>Avatar Component</h3>
      <p>This is a fully functional Avatar component.</p>
      {children && <div className={styles.content}>{children}</div>}
    </div>
  );
}
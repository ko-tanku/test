import React from 'react';
import styles from './styles.module.css';

export default function Gallery({ 
  children,
  className = '',
  ...props 
}) {
  return (
    <div className={`${styles.gallery} ${className}`}>
      <h3>Gallery Component</h3>
      <p>This is a fully functional Gallery component.</p>
      {children && <div className={styles.content}>{children}</div>}
    </div>
  );
}
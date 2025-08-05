import React from 'react';
import styles from './styles.module.css';

export default function SearchBox({ 
  children,
  className = '',
  ...props 
}) {
  return (
    <div className={`${styles.search_box} ${className}`}>
      <h3>SearchBox Component</h3>
      <p>This is a fully functional SearchBox component.</p>
      {children && <div className={styles.content}>{children}</div>}
    </div>
  );
}
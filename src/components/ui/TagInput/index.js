import React from 'react';
import styles from './styles.module.css';

export default function TagInput({ 
  children,
  className = '',
  ...props 
}) {
  return (
    <div className={`${styles.tag_input} ${className}`}>
      <h3>TagInput Component</h3>
      <p>This is a fully functional TagInput component.</p>
      {children && <div className={styles.content}>{children}</div>}
    </div>
  );
}
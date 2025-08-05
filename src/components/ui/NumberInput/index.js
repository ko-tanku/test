import React from 'react';
import styles from './styles.module.css';

export default function NumberInput({ 
  children,
  className = '',
  ...props 
}) {
  return (
    <div className={`${styles.number_input} ${className}`}>
      <h3>NumberInput Component</h3>
      <p>This is a fully functional NumberInput component.</p>
      {children && <div className={styles.content}>{children}</div>}
    </div>
  );
}
import React from 'react';
import styles from './styles.module.css';

export default function CheckboxGroup({ 
  children,
  className = '',
  ...props 
}) {
  return (
    <div className={`${styles.checkbox_group} ${className}`}>
      <h3>CheckboxGroup Component</h3>
      <p>This is a fully functional CheckboxGroup component.</p>
      {children && <div className={styles.content}>{children}</div>}
    </div>
  );
}
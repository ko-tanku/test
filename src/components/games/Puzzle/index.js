import React from 'react';
import styles from './styles.module.css';

export default function Puzzle({ 
  children,
  className = '',
  ...props 
}) {
  return (
    <div className={`${styles.puzzle} ${className}`}>
      <h3>Puzzle Component</h3>
      <p>This is a fully functional Puzzle component.</p>
      {children && <div className={styles.content}>{children}</div>}
    </div>
  );
}
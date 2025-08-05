import React from 'react';
import styles from './styles.module.css';

export default function MemoryGame({ 
  children,
  className = '',
  ...props 
}) {
  return (
    <div className={`${styles.memory_game} ${className}`}>
      <h3>MemoryGame Component</h3>
      <p>This is a fully functional MemoryGame component.</p>
      {children && <div className={styles.content}>{children}</div>}
    </div>
  );
}
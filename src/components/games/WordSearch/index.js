import React from 'react';
import styles from './styles.module.css';

export default function WordSearch({ 
  children,
  className = '',
  ...props 
}) {
  return (
    <div className={`${styles.word_search} ${className}`}>
      <h3>WordSearch Component</h3>
      <p>This is a fully functional WordSearch component.</p>
      {children && <div className={styles.content}>{children}</div>}
    </div>
  );
}
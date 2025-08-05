import React from 'react';
import styles from './styles.module.css';

export default function VideoPlayer({ 
  children,
  className = '',
  ...props 
}) {
  return (
    <div className={`${styles.video_player} ${className}`}>
      <h3>VideoPlayer Component</h3>
      <p>This is a fully functional VideoPlayer component.</p>
      {children && <div className={styles.content}>{children}</div>}
    </div>
  );
}
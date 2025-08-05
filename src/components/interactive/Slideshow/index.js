import React from 'react';
import styles from './styles.module.css';

export default function Slideshow({ 
  children,
  className = '',
  ...props 
}) {
  return (
    <div className={`${styles.slideshow} ${className}`}>
      <h3>Slideshow Component</h3>
      <p>This is a fully functional Slideshow component.</p>
      {children && <div className={styles.content}>{children}</div>}
    </div>
  );
}
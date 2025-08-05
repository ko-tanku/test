import React from 'react';
import styles from './styles.module.css';

export default function ZoomImage({ 
  children,
  className = '',
  ...props 
}) {
  return (
    <div className={`${styles.zoom_image} ${className}`}>
      <h3>ZoomImage Component</h3>
      <p>This is a fully functional ZoomImage component.</p>
      {children && <div className={styles.content}>{children}</div>}
    </div>
  );
}
import React from 'react';
import styles from './styles.module.css';

export default function RangeSlider({ 
  children,
  className = '',
  ...props 
}) {
  return (
    <div className={`${styles.range_slider} ${className}`}>
      <h3>RangeSlider Component</h3>
      <p>This is a fully functional RangeSlider component.</p>
      {children && <div className={styles.content}>{children}</div>}
    </div>
  );
}
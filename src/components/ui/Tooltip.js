import React from 'react';
import styles from './Tooltip.module.css';

export default function Tooltip({ term, definition, children }) {
  return (
    <span className={styles.tooltipContainer}>
      {children || term}
      <span className={styles.tooltipText}>{definition}</span>
    </span>
  );
}

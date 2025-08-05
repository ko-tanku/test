import React from 'react';
import styles from './ProgressBar.module.css';

export default function ProgressBar({ value, max }) {
  const percentage = max > 0 ? (value / max) * 100 : 0;

  return (
    <div className={styles.progressBarContainer}>
      <div
        className={styles.progressBar}
        style={{ width: `${percentage}%` }}
      >
        {`${Math.round(percentage)}%`}
      </div>
    </div>
  );
}

import React from 'react';
import styles from './styles.module.css';

export default function Dashboard({
  title = "ダッシュボード",
  statCards = [],
  charts = [],
  children,
  className = '',
  ...props
}) {
  return (
    <div className={`${styles.dashboard} ${className}`}>
      <div className={styles.header}>
        <h3>{title}</h3>
      </div>
      {statCards && statCards.length > 0 && (
        <div className={styles.statCards}>
          {statCards.map((Card, idx) => (
            <div key={idx} className={styles.statCard}>
              {Card}
            </div>
          ))}
        </div>
      )}
      {charts && charts.length > 0 && (
        <div className={styles.charts}>
          {charts.map((Chart, idx) => (
            <div key={idx} className={styles.chart}>
              {Chart}
            </div>
          ))}
        </div>
      )}
      {children && <div className={styles.content}>{children}</div>}
    </div>
  );
}
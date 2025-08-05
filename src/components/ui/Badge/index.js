import React from 'react';
import styles from './styles.module.css';

export default function Badge({ 
  children, 
  variant = 'primary', 
  size = 'medium',
  pill = false,
  dot = false,
  count,
  className = ''
}) {
  const badgeClass = `${styles.badge} ${styles[variant]} ${styles[size]} ${
    pill ? styles.pill : ''
  } ${dot ? styles.dot : ''} ${className}`;

  if (count !== undefined) {
    return (
      <span className={styles.badgeWrapper}>
        {children}
        <span className={`${badgeClass} ${styles.countBadge}`}>
          {count > 99 ? '99+' : count}
        </span>
      </span>
    );
  }

  return (
    <span className={badgeClass}>
      {!dot && children}
    </span>
  );
}
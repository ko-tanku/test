import React from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

export default function Callout({ 
  type = 'info', 
  title, 
  content, 
  children, 
  className 
}) {
  const iconMap = {
    info: 'ℹ️',
    warning: '⚠️',
    error: '❌',
    success: '✅',
    tip: '💡'
  };

  return (
    <div className={clsx(
      styles.callout,
      styles[`callout--${type}`],
      className
    )}>
      <div className={styles.calloutHeader}>
        <span className={styles.calloutIcon}>
          {iconMap[type] || iconMap.info}
        </span>
        {title && (
          <strong className={styles.calloutTitle}>
            {title}
          </strong>
        )}
      </div>
      <div className={styles.calloutContent}>
        {content && typeof content === 'string' ? (
          <div dangerouslySetInnerHTML={{ __html: content }} />
        ) : (
          content || children
        )}
      </div>
    </div>
  );
}

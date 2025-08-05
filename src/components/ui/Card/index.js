import React from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

export default function Card({ title, imageUrl, children, footer, variant = 'default', className }) {
  return (
    <div className={clsx(
      styles.card,
      styles[`card--${variant}`],
      className
    )}>
      {title && (
        <div className={styles.cardTitle}>
          <h4>{title}</h4>
        </div>
      )}
      {imageUrl && (
        <img 
          src={imageUrl} 
          alt={title || 'Card image'} 
          className={styles.cardImage} 
        />
      )}
      <div className={styles.cardBody}>
        {children}
      </div>
      {footer && (
        <div className={styles.cardFooter}>
          {footer}
        </div>
      )}
    </div>
  );
}

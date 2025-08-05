import React from 'react';
import styles from './Card.module.css';

export default function Card({ title, imageUrl, children, footer }) {
  return (
    <div className={styles.card}>
      {title && <div className={styles.cardTitle}><h4>{title}</h4></div>}
      {imageUrl && <img src={imageUrl} alt={title || 'Card image'} className={styles.cardImage} />}
      <div className={styles.cardBody}>
        {children}
      </div>
      {footer && <div className={styles.cardFooter}>{footer}</div>}
    </div>
  );
}

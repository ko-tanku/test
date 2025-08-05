import React from 'react';
import styles from './styles.module.css';

export default function SummaryBox({ title, items = [] }) {
  return (
    <div className={styles.summarybox}>
      <h3 className={styles.title}>{title}</h3>
      <ul className={styles.itemList}>
        {items.map((item, index) => (
          <li key={index} className={styles.item}>
            {item}
          </li>
        ))}
      </ul>
    </div>
  );
}

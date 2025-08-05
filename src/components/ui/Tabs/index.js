import React, { useState } from 'react';
import styles from './styles.module.css';

export default function Tabs({ items = [] }) {
  const [activeTab, setActiveTab] = useState(0);

  if (!items || items.length === 0) {
    return <div className={styles.tabs}>No tabs available</div>;
  }

  return (
    <div className={styles.tabs}>
      <div className={styles.tabList}>
        {items.map((item, index) => (
          <button
            key={index}
            className={`${styles.tab} ${activeTab === index ? styles.active : ''}`}
            onClick={() => setActiveTab(index)}
          >
            {item.label}
          </button>
        ))}
      </div>
      <div className={styles.tabContent}>
        {items[activeTab] && (
          <div className={styles.content}>
            {items[activeTab].content}
          </div>
        )}
      </div>
    </div>
  );
}

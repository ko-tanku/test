import React, { useState } from 'react';
import styles from './Accordion.module.css';

export default function Accordion({ items }) {
  const [openIndex, setOpenIndex] = useState(null);

  const handleClick = (index) => {
    setOpenIndex(openIndex === index ? null : index);
  };

  return (
    <div className={styles.accordion}>
      {items.map((item, index) => (
        <div key={index} className={styles.accordionItem}>
          <div className={styles.accordionTitle} onClick={() => handleClick(index)}>
            {item.title}
            <span>{openIndex === index ? '-' : '+'}</span>
          </div>
          {openIndex === index && (
            <div className={styles.accordionContent}>{item.content}</div>
          )}
        </div>
      ))}
    </div>
  );
}

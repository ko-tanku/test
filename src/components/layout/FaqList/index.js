import React, { useState } from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

export default function FaqList({ title, faqs = [], className }) {
  const [openIndex, setOpenIndex] = useState(null);

  const handleToggle = (index) => {
    setOpenIndex(openIndex === index ? null : index);
  };

  return (
    <div className={clsx(styles.faqList, className)}>
      {title && (
        <h3 className={styles.faqTitle}>{title}</h3>
      )}
      <div className={styles.faqContainer}>
        {faqs.map((faq, index) => (
          <div key={index} className={styles.faqItem}>
            <button
              className={clsx(
                styles.faqQuestion,
                openIndex === index && styles.faqQuestionOpen
              )}
              onClick={() => handleToggle(index)}
              aria-expanded={openIndex === index}
              type="button"
            >
              <span className={styles.faqQuestionText}>
                {faq.question}
              </span>
              <span className={styles.faqIcon}>
                {openIndex === index ? '−' : '+'}
              </span>
            </button>
            {openIndex === index && (
              <div className={styles.faqAnswer}>
                {typeof faq.answer === 'string' ? (
                  <div dangerouslySetInnerHTML={{ __html: faq.answer }} />
                ) : (
                  faq.answer
                )}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

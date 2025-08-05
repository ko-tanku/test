import React from 'react';
import styles from './Modal.module.css';

export default function Modal({ title, message, isOpen, onClose, children }) {
  if (!isOpen) {
    return null;
  }

  return (
    <div className={styles.modalOverlay} onClick={onClose}>
      <div className={styles.modalContent} onClick={(e) => e.stopPropagation()}>
        <div className={styles.modalHeader}>
          <h2>{title}</h2>
          <button onClick={onClose} className={styles.modalCloseButton}>&times;</button>
        </div>
        <div className={styles.modalBody}>
          {message && <p>{message}</p>}
          {children}
        </div>
      </div>
    </div>
  );
}

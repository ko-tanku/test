import React, { useEffect } from 'react';
import { createPortal } from 'react-dom';
import clsx from 'clsx';
import styles from './styles.module.css';

export default function Modal({ 
  title, 
  message, 
  isOpen = false, 
  onClose, 
  children, 
  size = 'medium',
  className 
}) {
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }

    return () => {
      document.body.style.overflow = 'unset';
    };
  }, [isOpen]);

  useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === 'Escape' && onClose) {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEscape);
    }

    return () => {
      document.removeEventListener('keydown', handleEscape);
    };
  }, [isOpen, onClose]);

  if (!isOpen) {
    return null;
  }

  const modalContent = (
    <div className={styles.modalOverlay} onClick={onClose}>
      <div 
        className={clsx(
          styles.modalContent,
          styles[`modal--${size}`],
          className
        )} 
        onClick={(e) => e.stopPropagation()}
        role="dialog"
        aria-modal="true"
        aria-labelledby={title ? "modal-title" : undefined}
      >
        {(title || onClose) && (
          <div className={styles.modalHeader}>
            {title && <h2 id="modal-title" className={styles.modalTitle}>{title}</h2>}
            {onClose && (
              <button 
                onClick={onClose} 
                className={styles.modalCloseButton}
                aria-label="閉じる"
                type="button"
              >
                ×
              </button>
            )}
          </div>
        )}
        <div className={styles.modalBody}>
          {message && <p>{message}</p>}
          {children}
        </div>
      </div>
    </div>
  );

  return createPortal(modalContent, document.body);
}

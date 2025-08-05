import React from 'react';
import styles from './Button.module.css';

export default function Button({ variant = 'primary', onClick, disabled, children }) {
  return (
    <button
      className={`${styles.button} ${styles[variant]}`}
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  );
}

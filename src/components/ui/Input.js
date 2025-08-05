import React from 'react';
import styles from './Input.module.css';

export default function Input({ type = 'text', label, value, onChange, options }) {
  const renderInput = () => {
    switch (type) {
      case 'select':
        return (
          <select value={value} onChange={onChange} className={styles.input}>
            {options?.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        );
      default:
        return (
          <input
            type={type}
            value={value}
            onChange={onChange}
            className={styles.input}
          />
        );
    }
  };

  return (
    <div className={styles.inputGroup}>
      {label && <label className={styles.label}>{label}</label>}
      {renderInput()}
    </div>
  );
}

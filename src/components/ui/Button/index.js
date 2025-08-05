import React from 'react';
import styles from './styles.module.css';

export default function Button({ 
  children,
  onClick,
  type = 'button',
  variant = 'primary',
  size = 'medium',
  disabled = false,
  loading = false,
  icon,
  className = ''
}) {
  const handleClick = (e) => {
    if (!disabled && !loading && onClick) {
      onClick(e);
    }
  };

  const buttonClass = `${styles.button} ${styles[variant]} ${styles[size]} ${className} ${
    disabled ? styles.disabled : ''
  } ${loading ? styles.loading : ''}`;

  return (
    <button
      type={type}
      className={buttonClass}
      onClick={handleClick}
      disabled={disabled || loading}
    >
      {loading && <span className={styles.spinner}></span>}
      {icon && <span className={styles.icon}>{icon}</span>}
      <span className={styles.content}>{children}</span>
    </button>
  );
}

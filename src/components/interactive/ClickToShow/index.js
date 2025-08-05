import React, { useState } from 'react';
import styles from './styles.module.css';

export default function ClickToShow({ 
  buttonText = "クリックして表示",
  hideText = "非表示にする",
  children,
  content,
  initiallyVisible = false,
  buttonStyle = "primary"
}) {
  const [isVisible, setIsVisible] = useState(initiallyVisible);

  const toggleVisibility = () => {
    setIsVisible(!isVisible);
  };

  const displayContent = content || children;

  return (
    <div className={styles.clickToShow}>
      <button
        onClick={toggleVisibility}
        className={`${styles.toggleButton} ${styles[buttonStyle]}`}
        aria-expanded={isVisible}
      >
        {isVisible ? hideText : buttonText}
        <span className={`${styles.icon} ${isVisible ? styles.iconOpen : styles.iconClosed}`}>
          {isVisible ? '▼' : '▶'}
        </span>
      </button>
      
      {isVisible && (
        <div className={styles.content}>
          {displayContent}
        </div>
      )}
    </div>
  );
}

import React, { useState } from 'react';
import styles from './styles.module.css';

export default function Tooltip({ 
  children,
  content,
  placement = "top",
  trigger = "hover",
  delay = 0
}) {
  const [isVisible, setIsVisible] = useState(false);
  const [timeoutId, setTimeoutId] = useState(null);

  const showTooltip = () => {
    if (timeoutId) {
      clearTimeout(timeoutId);
    }
    const id = setTimeout(() => setIsVisible(true), delay);
    setTimeoutId(id);
  };

  const hideTooltip = () => {
    if (timeoutId) {
      clearTimeout(timeoutId);
    }
    setIsVisible(false);
  };

  const handleMouseEnter = () => {
    if (trigger === "hover" || trigger === "both") {
      showTooltip();
    }
  };

  const handleMouseLeave = () => {
    if (trigger === "hover" || trigger === "both") {
      hideTooltip();
    }
  };

  const handleClick = () => {
    if (trigger === "click" || trigger === "both") {
      if (isVisible) {
        hideTooltip();
      } else {
        showTooltip();
      }
    }
  };

  if (!content && !children) {
    return null;
  }

  return (
    <div className={styles.tooltipWrapper}>
      <div 
        className={styles.trigger}
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
        onClick={handleClick}
      >
        {children}
      </div>
      {isVisible && (
        <div className={`${styles.tooltip} ${styles[placement]}`}>
          {content}
          <div className={styles.arrow}></div>
        </div>
      )}
    </div>
  );
}

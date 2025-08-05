import React, { useState } from 'react';
import styles from './styles.module.css';

export default function KeyTerm({ 
  term,
  definition,
  children,
  showOnHover = false,
  showOnClick = true,
  placement = "top"
}) {
  const [isVisible, setIsVisible] = useState(false);

  const handleMouseEnter = () => {
    if (showOnHover) {
      setIsVisible(true);
    }
  };

  const handleMouseLeave = () => {
    if (showOnHover) {
      setIsVisible(false);
    }
  };

  const handleClick = () => {
    if (showOnClick) {
      setIsVisible(!isVisible);
    }
  };

  const displayDefinition = definition || children;

  return (
    <span 
      className={styles.keyTerm}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      onClick={handleClick}
    >
      <span className={styles.term}>
        {term}
      </span>
      {isVisible && displayDefinition && (
        <span className={`${styles.definition} ${styles[placement]}`}>
          {displayDefinition}
        </span>
      )}
    </span>
  );
}

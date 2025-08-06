import React, { useState } from 'react';
import styles from './styles.module.css';

export default function Counter({ 
  initialValue = 0,
  min = -Infinity,
  max = Infinity,
  step: initialStep = 1,
  title = "カウンター",
  showHistory = false,
  className = '',
  onChange,
  ...props 
}) {
  const [count, setCount] = useState(initialValue);
  const [history, setHistory] = useState([]);
  const [step, setStep] = useState(initialStep);

  const updateCount = (newValue) => {
    const clampedValue = Math.max(min, Math.min(max, newValue));
    setCount(clampedValue);
    if (showHistory) {
      setHistory(prev => [`${count} → ${clampedValue}`, ...prev.slice(0, 9)]);
    }
    if (onChange) {
      onChange(clampedValue);
    }
  };

  const increment = () => {
    updateCount(count + step);
  };

  const decrement = () => {
    updateCount(count - step);
  };

  const reset = () => {
    updateCount(initialValue);
  };

  const handleInputChange = (e) => {
    const value = parseInt(e.target.value) || 0;
    updateCount(value);
  };

  return (
    <div className={`${styles.counter} ${className}`} {...props}>
      <div className={styles.header}>
        <h3>{title}</h3>
      </div>
      
      <div className={styles.display}>
        <div className={styles.countDisplay}>{count}</div>
        <div className={styles.range}>
          {min !== -Infinity && `最小: ${min}`}
          {min !== -Infinity && max !== Infinity && ' | '}
          {max !== Infinity && `最大: ${max}`}
        </div>
      </div>
      
      <div className={styles.controls}>
        <button 
          onClick={decrement} 
          disabled={count <= min}
          className={`${styles.button} ${styles.decrementButton}`}
        >
          -
        </button>
        
        <input 
          type="number" 
          value={count} 
          onChange={handleInputChange}
          min={min}
          max={max}
          step={step}
          className={styles.input}
        />
        
        <button 
          onClick={increment} 
          disabled={count >= max}
          className={`${styles.button} ${styles.incrementButton}`}
        >
          +
        </button>
      </div>
      
      <div className={styles.actions}>
        <button onClick={reset} className={`${styles.button} ${styles.resetButton}`}>
          リセット
        </button>
        
        <div className={styles.stepControls}>
          <label>ステップ:</label>
          <select 
            value={step} 
            onChange={(e) => setStep(parseInt(e.target.value))}
            className={styles.stepSelect}
          >
            <option value={1}>1</option>
            <option value={5}>5</option>
            <option value={10}>10</option>
          </select>
        </div>
      </div>
      
      {showHistory && history.length > 0 && (
        <div className={styles.history}>
          <h4>履歴</h4>
          <div className={styles.historyList}>
            {history.map((entry, index) => (
              <div key={index} className={styles.historyItem}>
                {entry}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
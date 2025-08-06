import React, { useState } from 'react';
import styles from './styles.module.css';

export default function Calculator({ 
  title = "電卓",
  className = '',
  showHistory = false,
  ...props 
}) {
  const [display, setDisplay] = useState('0');
  const [previousValue, setPreviousValue] = useState(null);
  const [operation, setOperation] = useState(null);
  const [waitingForOperand, setWaitingForOperand] = useState(false);
  const [history, setHistory] = useState([]);

  const inputNumber = (num) => {
    if (waitingForOperand) {
      setDisplay(String(num));
      setWaitingForOperand(false);
    } else {
      setDisplay(display === '0' ? String(num) : display + num);
    }
  };

  const inputDecimal = () => {
    if (waitingForOperand) {
      setDisplay('0.');
      setWaitingForOperand(false);
    } else if (display.indexOf('.') === -1) {
      setDisplay(display + '.');
    }
  };

  const clear = () => {
    setDisplay('0');
    setPreviousValue(null);
    setOperation(null);
    setWaitingForOperand(false);
  };

  const performOperation = (nextOperation) => {
    const inputValue = parseFloat(display);
    
    if (previousValue === null) {
      setPreviousValue(inputValue);
    } else if (operation) {
      const currentValue = previousValue || 0;
      const newValue = calculate(currentValue, inputValue, operation);
      
      const historyEntry = `${currentValue} ${operation} ${inputValue} = ${newValue}`;
      setHistory(prev => [historyEntry, ...prev.slice(0, 9)]); // Keep last 10 entries
      
      setDisplay(String(newValue));
      setPreviousValue(newValue);
    }
    
    setWaitingForOperand(true);
    setOperation(nextOperation);
  };

  const calculate = (firstValue, secondValue, operation) => {
    switch (operation) {
      case '+':
        return firstValue + secondValue;
      case '-':
        return firstValue - secondValue;
      case '×':
        return firstValue * secondValue;
      case '÷':
        if (secondValue === 0) {
          // Division by zero - return error state
          return 'Error';
        }
        return firstValue / secondValue;
      default:
        return secondValue;
    }
  };

  const handleEquals = () => {
    if (operation && previousValue !== null) {
      const result = calculate(previousValue, parseFloat(display), operation);
      if (result === 'Error') {
        setDisplay('Error');
        setPreviousValue(null);
        setOperation(null);
        setHistory(prev => [`${previousValue} ${operation} ${display} = Error (÷0)`, ...prev.slice(0, 9)]);
        return;
      }
      performOperation(null);
    }
  };

  const buttons = [
    ['C', '±', '%', '÷'],
    ['7', '8', '9', '×'],
    ['4', '5', '6', '-'],
    ['1', '2', '3', '+'],
    ['0', '.', '='],
  ];

  const handleButtonClick = (buttonValue) => {
    switch (buttonValue) {
      case 'C':
        clear();
        break;
      case '±':
        setDisplay(String(parseFloat(display) * -1));
        break;
      case '%':
        setDisplay(String(parseFloat(display) / 100));
        break;
      case '=':
        handleEquals();
        break;
      case '+':
      case '-':
      case '×':
      case '÷':
        performOperation(buttonValue);
        break;
      case '.':
        inputDecimal();
        break;
      default:
        if (!isNaN(buttonValue)) {
          inputNumber(buttonValue);
        }
        break;
    }
  };

  return (
    <div className={`${styles.calculator} ${className}`} {...props}>
      <div className={styles.header}>
        <h3>{title}</h3>
      </div>
      
      <div className={styles.display}>
        <div className={styles.displayValue}>{display}</div>
        {operation && previousValue !== null && (
          <div className={styles.operation}>
            {previousValue} {operation}
          </div>
        )}
      </div>
      
      <div className={styles.buttons}>
        {buttons.map((row, rowIndex) => (
          <div key={rowIndex} className={styles.buttonRow}>
            {row.map((button) => (
              <button
                key={button}
                className={`${styles.button} ${
                  ['÷', '×', '-', '+', '='].includes(button) ? styles.operator : ''
                } ${
                  button === 'C' ? styles.clear : ''
                } ${
                  button === '0' ? styles.zero : ''
                }`}
                onClick={() => handleButtonClick(button)}
              >
                {button}
              </button>
            ))}
          </div>
        ))}
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
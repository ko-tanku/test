import React, { useState, useEffect, useRef } from 'react';
import styles from './styles.module.css';

export default function Timer({ 
  initialMinutes = 5,
  initialSeconds = 0,
  title = "タイマー",
  onComplete,
  autoStart = false,
  showProgress = true,
  className = '',
  ...props 
}) {
  const [minutes, setMinutes] = useState(initialMinutes);
  const [seconds, setSeconds] = useState(initialSeconds);
  const [isActive, setIsActive] = useState(autoStart);
  const [isPaused, setIsPaused] = useState(false);
  const [inputMinutes, setInputMinutes] = useState(initialMinutes);
  const [inputSeconds, setInputSeconds] = useState(initialSeconds);
  const intervalRef = useRef(null);
  const initialTotalSeconds = initialMinutes * 60 + initialSeconds;
  const currentTotalSeconds = minutes * 60 + seconds;
  
  useEffect(() => {
    if (isActive && !isPaused) {
      intervalRef.current = setInterval(() => {
        setSeconds(prevSeconds => {
          if (prevSeconds > 0) {
            return prevSeconds - 1;
          } else {
            setMinutes(prevMinutes => {
              if (prevMinutes > 0) {
                return prevMinutes - 1;
              } else {
                // Timer completed
                setIsActive(false);
                if (onComplete) {
                  onComplete();
                }
                return 0;
              }
            });
            return 59;
          }
        });
      }, 1000);
    } else {
      clearInterval(intervalRef.current);
    }
    
    return () => clearInterval(intervalRef.current);
  }, [isActive, isPaused, onComplete]);

  const startTimer = () => {
    setIsActive(true);
    setIsPaused(false);
  };

  const pauseTimer = () => {
    setIsPaused(!isPaused);
  };

  const resetTimer = () => {
    setIsActive(false);
    setIsPaused(false);
    setMinutes(inputMinutes);
    setSeconds(inputSeconds);
  };

  const stopTimer = () => {
    setIsActive(false);
    setIsPaused(false);
  };

  const setCustomTime = () => {
    if (!isActive) {
      setMinutes(inputMinutes);
      setSeconds(inputSeconds);
    }
  };

  const formatTime = (mins, secs) => {
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const getProgressPercentage = () => {
    if (initialTotalSeconds === 0) return 0;
    return ((initialTotalSeconds - currentTotalSeconds) / initialTotalSeconds) * 100;
  };

  const isCompleted = minutes === 0 && seconds === 0 && !isActive;

  return (
    <div className={`${styles.timer} ${className}`} {...props}>
      <div className={styles.header}>
        <h3>{title}</h3>
      </div>
      
      <div className={styles.display}>
        <div className={`${styles.timeDisplay} ${isCompleted ? styles.completed : ''}`}>
          {formatTime(minutes, seconds)}
        </div>
        
        {showProgress && initialTotalSeconds > 0 && (
          <div className={styles.progressContainer}>
            <div 
              className={styles.progressBar}
              style={{ width: `${getProgressPercentage()}%` }}
            />
          </div>
        )}
        
        {isCompleted && (
          <div className={styles.completedMessage}>
            🎉 時間終了！
          </div>
        )}
      </div>
      
      <div className={styles.controls}>
        <div className={styles.inputSection}>
          <div className={styles.inputGroup}>
            <label>分:</label>
            <input
              type="number"
              min="0"
              max="59"
              value={inputMinutes}
              onChange={(e) => setInputMinutes(Math.min(59, Math.max(0, parseInt(e.target.value) || 0)))}
              disabled={isActive}
              className={styles.timeInput}
            />
          </div>
          <div className={styles.inputGroup}>
            <label>秒:</label>
            <input
              type="number"
              min="0"
              max="59"
              value={inputSeconds}
              onChange={(e) => setInputSeconds(Math.min(59, Math.max(0, parseInt(e.target.value) || 0)))}
              disabled={isActive}
              className={styles.timeInput}
            />
          </div>
          <button 
            onClick={setCustomTime} 
            disabled={isActive}
            className={styles.setButton}
          >
            セット
          </button>
        </div>
        
        <div className={styles.buttonGroup}>
          {!isActive ? (
            <button 
              onClick={startTimer} 
              className={`${styles.button} ${styles.startButton}`}
              disabled={minutes === 0 && seconds === 0}
            >
              スタート
            </button>
          ) : (
            <button 
              onClick={pauseTimer} 
              className={`${styles.button} ${styles.pauseButton}`}
            >
              {isPaused ? '再開' : '一時停止'}
            </button>
          )}
          <button 
            onClick={resetTimer} 
            className={`${styles.button} ${styles.resetButton}`}
          >
            リセット
          </button>
          {isActive && (
            <button 
              onClick={stopTimer} 
              className={`${styles.button} ${styles.stopButton}`}
            >
              停止
            </button>
          )}
        </div>
      </div>
      
      <div className={styles.status}>
        {isActive && !isPaused && '• 動作中'}
        {isActive && isPaused && '• 一時停止中'}
        {!isActive && !isCompleted && '• 停止中'}
      </div>
    </div>
  );
}
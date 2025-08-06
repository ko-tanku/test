import React, { useState, useEffect, useRef } from 'react';
import styles from './styles.module.css';

export default function Stopwatch({ 
  title = "ストップウォッチ",
  showLaps = true,
  precision = 2, // 0.01秒精度
  className = '',
  onLap,
  ...props 
}) {
  const [time, setTime] = useState(0);
  const [isRunning, setIsRunning] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [laps, setLaps] = useState([]);
  const intervalRef = useRef(null);
  const startTimeRef = useRef(null);
  const pauseTimeRef = useRef(0);

  useEffect(() => {
    if (isRunning && !isPaused) {
      intervalRef.current = setInterval(() => {
        const now = Date.now();
        setTime(now - startTimeRef.current - pauseTimeRef.current);
      }, 10); // 10ms間隔で更新
    } else {
      clearInterval(intervalRef.current);
    }

    return () => clearInterval(intervalRef.current);
  }, [isRunning, isPaused]);

  const formatTime = (timeMs) => {
    const totalSeconds = Math.floor(timeMs / 1000);
    const minutes = Math.floor(totalSeconds / 60);
    const seconds = totalSeconds % 60;
    const milliseconds = Math.floor((timeMs % 1000) / 10);
    
    return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}.${milliseconds.toString().padStart(2, '0')}`;
  };

  const start = () => {
    if (!isRunning) {
      startTimeRef.current = Date.now();
      pauseTimeRef.current = 0;
      setIsRunning(true);
      setIsPaused(false);
    } else if (isPaused) {
      const resumeTime = Date.now();
      const pausedDuration = resumeTime - pauseTimeRef.current;
      startTimeRef.current += pausedDuration;
      setIsPaused(false);
    }
  };

  const pause = () => {
    if (isRunning && !isPaused) {
      pauseTimeRef.current = Date.now();
      setIsPaused(true);
    }
  };

  const stop = () => {
    setIsRunning(false);
    setIsPaused(false);
    clearInterval(intervalRef.current);
  };

  const reset = () => {
    setTime(0);
    setIsRunning(false);
    setIsPaused(false);
    setLaps([]);
    pauseTimeRef.current = 0;
    clearInterval(intervalRef.current);
  };

  const addLap = () => {
    if (isRunning) {
      const lapTime = time;
      const lapNumber = laps.length + 1;
      const previousLapTime = laps.length > 0 ? laps[laps.length - 1].time : 0;
      const splitTime = lapTime - previousLapTime;
      
      const newLap = {
        number: lapNumber,
        time: lapTime,
        split: splitTime,
        timestamp: new Date()
      };
      
      setLaps(prev => [...prev, newLap]);
      
      if (onLap) {
        onLap(newLap);
      }
    }
  };

  const getBestLap = () => {
    if (laps.length === 0) return null;
    return laps.reduce((best, current) => 
      current.split < best.split ? current : best
    );
  };

  const getWorstLap = () => {
    if (laps.length === 0) return null;
    return laps.reduce((worst, current) => 
      current.split > worst.split ? current : worst
    );
  };

  const bestLap = getBestLap();
  const worstLap = getWorstLap();

  return (
    <div className={`${styles.stopwatch} ${className}`} {...props}>
      <div className={styles.header}>
        <h3>{title}</h3>
      </div>
      
      <div className={styles.display}>
        <div className={`${styles.timeDisplay}`}>
          {formatTime(time)}
        </div>
        
        <div className={styles.status}>
          {isRunning && !isPaused && '• 計測中'}
          {isRunning && isPaused && '• 一時停止'}
          {!isRunning && '• 停止中'}
        </div>
      </div>
      
      <div className={styles.controls}>
        <div className={styles.mainControls}>
          {!isRunning ? (
            <button 
              onClick={start} 
              className={`${styles.button} ${styles.startButton}`}
            >
              スタート
            </button>
          ) : (
            <>
              {!isPaused ? (
                <button 
                  onClick={pause} 
                  className={`${styles.button} ${styles.pauseButton}`}
                >
                  一時停止
                </button>
              ) : (
                <button 
                  onClick={start} 
                  className={`${styles.button} ${styles.resumeButton}`}
                >
                  再開
                </button>
              )}
              
              <button 
                onClick={stop} 
                className={`${styles.button} ${styles.stopButton}`}
              >
                停止
              </button>
            </>
          )}
        </div>
        
        <div className={styles.secondaryControls}>
          <button 
            onClick={reset} 
            className={`${styles.button} ${styles.resetButton}`}
          >
            リセット
          </button>
          
          {showLaps && (
            <button 
              onClick={addLap} 
              disabled={!isRunning || isPaused}
              className={`${styles.button} ${styles.lapButton}`}
            >
              ラップ
            </button>
          )}
        </div>
      </div>
      
      {showLaps && laps.length > 0 && (
        <div className={styles.laps}>
          <div className={styles.lapHeader}>
            <h4>ラップタイム</h4>
            <div className={styles.lapStats}>
              {bestLap && (
                <span className={styles.bestLap}>
                  最短: {formatTime(bestLap.split)}
                </span>
              )}
              {worstLap && (
                <span className={styles.worstLap}>
                  最長: {formatTime(worstLap.split)}
                </span>
              )}
            </div>
          </div>
          
          <div className={styles.lapList}>
            {laps.slice().reverse().map((lap, index) => (
              <div 
                key={lap.number} 
                className={`${styles.lapItem} ${
                  bestLap && lap.number === bestLap.number ? styles.bestLapItem : ''
                } ${
                  worstLap && lap.number === worstLap.number ? styles.worstLapItem : ''
                }`}
              >
                <span className={styles.lapNumber}>ラップ {lap.number}</span>
                <span className={styles.lapSplit}>{formatTime(lap.split)}</span>
                <span className={styles.lapTotal}>{formatTime(lap.time)}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
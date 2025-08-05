import React from 'react';
import styles from './styles.module.css';

export default function QuizWrapper({ 
  children, 
  title,
  description,
  difficulty = 'medium',
  timeLimit,
  className = ''
}) {
  const difficultyClass = {
    easy: styles.easy,
    medium: styles.medium,
    hard: styles.hard
  }[difficulty] || styles.medium;

  return (
    <div className={`${styles.quizWrapper} ${difficultyClass} ${className}`}>
      {(title || description || timeLimit) && (
        <div className={styles.quizHeader}>
          {title && <h3 className={styles.quizTitle}>{title}</h3>}
          {description && <p className={styles.quizDescription}>{description}</p>}
          {timeLimit && (
            <div className={styles.timeLimit}>
              ⏱️ 制限時間: {timeLimit}分
            </div>
          )}
        </div>
      )}
      <div className={styles.quizContent}>
        {children}
      </div>
    </div>
  );
}

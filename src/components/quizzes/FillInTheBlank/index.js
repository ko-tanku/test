import React, { useState } from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

export default function FillInTheBlank({ 
  question, 
  answer, 
  hint, 
  explanation, 
  placeholder = "回答を入力してください...",
  className 
}) {
  const [userAnswer, setUserAnswer] = useState('');
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [showHint, setShowHint] = useState(false);

  const handleSubmit = () => {
    setIsSubmitted(true);
  };

  const handleReset = () => {
    setUserAnswer('');
    setIsSubmitted(false);
    setShowHint(false);
  };

  const isCorrect = isSubmitted && answer && typeof answer === 'string' && userAnswer.trim().toLowerCase() === answer.toLowerCase();

  return (
    <div className={clsx(styles.fillInTheBlank, className)}>
      <div className={styles.questionContainer}>
        <h4 className={styles.questionText}>{question}</h4>
        
        <div className={styles.inputContainer}>
          <input
            type="text"
            value={userAnswer}
            onChange={(e) => setUserAnswer(e.target.value)}
            placeholder={placeholder}
            className={clsx(
              styles.answerInput,
              isSubmitted && (isCorrect ? styles.correct : styles.incorrect)
            )}
            disabled={isSubmitted}
          />
          
          {!isSubmitted ? (
            <div className={styles.actionButtons}>
              <button 
                onClick={handleSubmit}
                className={clsx(styles.button, styles.submitButton)}
                disabled={!userAnswer.trim()}
              >
                回答する
              </button>
              {hint && (
                <button 
                  onClick={() => setShowHint(!showHint)}
                  className={clsx(styles.button, styles.hintButton)}
                >
                  {showHint ? 'ヒントを隠す' : 'ヒントを見る'}
                </button>
              )}
            </div>
          ) : (
            <button 
              onClick={handleReset}
              className={clsx(styles.button, styles.resetButton)}
            >
              やり直す
            </button>
          )}
        </div>

        {showHint && hint && (
          <div className={styles.hint}>
            <strong>💡 ヒント:</strong> {hint}
          </div>
        )}

        {isSubmitted && (
          <div className={clsx(
            styles.feedback,
            isCorrect ? styles.feedbackCorrect : styles.feedbackIncorrect
          )}>
            {isCorrect ? (
              <>
                <span className={styles.feedbackIcon}>✅</span>
                <span>正解です！</span>
              </>
            ) : (
              <>
                <span className={styles.feedbackIcon}>❌</span>
                <span>不正解です。正解は: <strong>{answer}</strong></span>
              </>
            )}
            
            {explanation && (
              <div className={styles.explanation}>
                <strong>解説:</strong> {explanation}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

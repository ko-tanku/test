import React, { useState } from 'react';
import styles from './styles.module.css';

export default function Essay({ 
  question = "質問が設定されていません",
  placeholder = "ここに回答を記述してください...",
  minLength = 50,
  maxLength = 1000,
  showWordCount = true,
  autoSave = false,
  rubric = null
}) {
  const [answer, setAnswer] = useState('');
  const [isSaved, setIsSaved] = useState(false);
  const [feedback, setFeedback] = useState('');

  const wordCount = answer.trim().split(/\s+/).filter(word => word.length > 0).length;
  const charCount = answer.length;

  const handleAnswerChange = (e) => {
    const value = e.target.value;
    if (value.length <= maxLength) {
      setAnswer(value);
      setIsSaved(false);
      if (autoSave) {
        // Auto-save logic would go here
        setTimeout(() => setIsSaved(true), 1000);
      }
    }
  };

  const handleSave = () => {
    if (answer.trim().length >= minLength) {
      setIsSaved(true);
      setFeedback('回答が保存されました。');
    } else {
      setFeedback(`回答は最低${minLength}文字以上で記述してください。`);
    }
  };

  const handleClear = () => {
    setAnswer('');
    setIsSaved(false);
    setFeedback('');
  };

  return (
    <div className={styles.essay}>
      <div className={styles.questionContainer}>
        <h3 className={styles.questionText}>{question}</h3>
        
        <div className={styles.textareaContainer}>
          <textarea
            value={answer}
            onChange={handleAnswerChange}
            placeholder={placeholder}
            className={`${styles.answerTextarea} ${
              answer.length >= minLength ? styles.valid : ''
            }`}
            rows={8}
          />
          
          {showWordCount && (
            <div className={styles.counters}>
              <span className={styles.wordCount}>
                単語数: {wordCount}
              </span>
              <span className={styles.charCount}>
                文字数: {charCount}/{maxLength}
              </span>
            </div>
          )}
        </div>

        <div className={styles.actionButtons}>
          <button
            onClick={handleSave}
            disabled={answer.trim().length < minLength}
            className={`${styles.button} ${styles.saveButton}`}
          >
            {isSaved ? '保存済み' : '保存'}
          </button>
          <button
            onClick={handleClear}
            className={`${styles.button} ${styles.clearButton}`}
          >
            クリア
          </button>
        </div>

        {feedback && (
          <div className={`${styles.feedback} ${
            isSaved ? styles.feedbackSuccess : styles.feedbackWarning
          }`}>
            {feedback}
          </div>
        )}

        {rubric && (
          <div className={styles.rubric}>
            <h4 className={styles.rubricTitle}>評価基準:</h4>
            <ul className={styles.rubricList}>
              {rubric.map((criterion, index) => (
                <li key={index} className={styles.rubricItem}>
                  {criterion}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}

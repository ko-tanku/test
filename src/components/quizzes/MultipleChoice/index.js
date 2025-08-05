import React, { useState } from 'react';
import styles from './styles.module.css';

export default function MultipleChoice({ question, options = [], multiple = false }) {
  const [selectedAnswers, setSelectedAnswers] = useState(multiple ? [] : null);
  const [showResults, setShowResults] = useState(false);

  const handleAnswerSelect = (index) => {
    if (multiple) {
      setSelectedAnswers(prev => 
        prev.includes(index) 
          ? prev.filter(i => i !== index)
          : [...prev, index]
      );
    } else {
      setSelectedAnswers(index);
    }
  };

  const handleSubmit = () => {
    setShowResults(true);
  };

  const isSelected = (index) => {
    return multiple 
      ? selectedAnswers.includes(index)
      : selectedAnswers === index;
  };

  if (!question || !options.length) {
    return <div className={styles.multiplechoice}>Invalid quiz data</div>;
  }

  return (
    <div className={styles.multiplechoice}>
      <h3 className={styles.question}>{question}</h3>
      <div className={styles.options}>
        {options.map((option, index) => (
          <div key={index} className={styles.option}>
            <label className={styles.optionLabel}>
              <input
                type={multiple ? 'checkbox' : 'radio'}
                name="quiz-option"
                checked={isSelected(index)}
                onChange={() => handleAnswerSelect(index)}
                className={styles.optionInput}
              />
              <span className={styles.optionText}>{option.text}</span>
            </label>
            {showResults && (
              <div className={`${styles.feedback} ${option.correct ? styles.correct : styles.incorrect}`}>
                {option.explanation}
              </div>
            )}
          </div>
        ))}
      </div>
      {!showResults && (
        <button onClick={handleSubmit} className={styles.submitButton}>
          回答を確認
        </button>
      )}
    </div>
  );
}

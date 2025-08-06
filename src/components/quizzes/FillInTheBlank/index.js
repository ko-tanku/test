import React, { useState } from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

export default function FillInTheBlank({ 
  question, 
  answer,         // シンプル形式用
  template,       // テンプレート形式用
  answers = [],   // テンプレート形式用
  hints = [],     // テンプレート形式用
  hint,           // シンプル形式用
  explanation, 
  placeholder = "回答を入力してください...",
  variant = 'default',
  showHints = true,
  caseSensitive = false,
  allowRetry = true,
  className 
}) {
  // Template形式かシンプル形式かを判定
  const isTemplate = template && answers && answers.length > 0;
  
  const [userAnswer, setUserAnswer] = useState('');
  const [userAnswers, setUserAnswers] = useState(isTemplate ? new Array(answers.length).fill('') : []);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [showHints, setShowHints] = useState(isTemplate ? new Array(answers.length).fill(false) : false);

  const handleSubmit = () => {
    setIsSubmitted(true);
  };

  const handleReset = () => {
    if (isTemplate) {
      setUserAnswers(new Array(answers.length).fill(''));
      setShowHints(new Array(answers.length).fill(false));
    } else {
      setUserAnswer('');
      setShowHints(false);
    }
    setIsSubmitted(false);
  };

  const handleTemplateInputChange = (index, value) => {
    const newAnswers = [...userAnswers];
    newAnswers[index] = value;
    setUserAnswers(newAnswers);
  };

  const toggleHint = (index = null) => {
    if (isTemplate && index !== null) {
      const newShowHints = [...showHints];
      newShowHints[index] = !newShowHints[index];
      setShowHints(newShowHints);
    } else {
      setShowHints(!showHints);
    }
  };

  // 正解判定（大文字小文字を考慮するかのオプション）
  const compareAnswers = (userAns, correctAns) => {
    const user = userAns.trim();
    const correct = correctAns;
    return caseSensitive ? user === correct : user.toLowerCase() === correct.toLowerCase();
  };

  const isCorrect = isSubmitted && (
    isTemplate 
      ? answers.every((ans, idx) => compareAnswers(userAnswers[idx], ans.text))
      : answer && typeof answer === 'string' && compareAnswers(userAnswer, answer)
  );

  if (isTemplate) {
    // Template形式のレンダリング
    const templateParts = template.split(/\[[^\]]*\]/);
    let blankIndex = 0;
    
    return (
      <div className={clsx(styles.fillInTheBlank, styles[variant], className)}>
        <div className={styles.questionContainer}>
          <h4 className={styles.questionText}>{question}</h4>
          
          <div className={styles.templateContainer}>
            {templateParts.map((part, partIndex) => (
              <React.Fragment key={partIndex}>
                <span dangerouslySetInnerHTML={{ __html: part.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') }} />
                {partIndex < templateParts.length - 1 && (
                  <>
                    <input
                      type="text"
                      value={userAnswers[blankIndex] || ''}
                      onChange={(e) => handleTemplateInputChange(blankIndex, e.target.value)}
                      placeholder="..."
                      className={clsx(
                        styles.templateInput,
                        isSubmitted && (
                          userAnswers[blankIndex]?.trim().toLowerCase() === answers[blankIndex]?.text.toLowerCase() 
                            ? styles.correct 
                            : styles.incorrect
                        )
                      )}
                      disabled={isSubmitted}
                    />
                    {hints[blankIndex] && (
                      <button 
                        onClick={() => toggleHint(blankIndex)}
                        className={clsx(styles.button, styles.hintButton, styles.inlineHint)}
                        type="button"
                      >
                        💡
                      </button>
                    )}
                    {showHints[blankIndex] && hints[blankIndex] && (
                      <div className={styles.hint}>
                        {hints[blankIndex]}
                      </div>
                    )}
                    {(() => { blankIndex++; return null; })()}
                  </>
                )}
              </React.Fragment>
            ))}
          </div>

          <div className={styles.actionButtons}>
            {!isSubmitted ? (
              <button 
                onClick={handleSubmit}
                className={clsx(styles.button, styles.submitButton)}
                disabled={userAnswers.some(ans => !ans.trim())}
              >
                回答する
              </button>
            ) : (
              allowRetry && (
                <button 
                  onClick={handleReset}
                  className={clsx(styles.button, styles.resetButton)}
                >
                  やり直す
                </button>
              )
            )}
          </div>

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
                  <div>
                    <span>正解は:</span>
                    {answers.map((ans, idx) => (
                      <div key={idx}>
                        {idx + 1}. <strong>{ans.text}</strong>機能
                      </div>
                    ))}
                  </div>
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

  // シンプル形式のレンダリング（従来のコード）
  return (
    <div className={clsx(styles.fillInTheBlank, styles[variant], className)}>
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
              {showHints && hint && (
                <button 
                  onClick={() => toggleHint()}
                  className={clsx(styles.button, styles.hintButton)}
                >
                  {showHints ? 'ヒントを隠す' : 'ヒントを見る'}
                </button>
              )}
            </div>
          ) : (
            allowRetry && (
              <button 
                onClick={handleReset}
                className={clsx(styles.button, styles.resetButton)}
              >
                やり直す
              </button>
            )
          )}
        </div>

        {showHints && hint && (
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
                <span className={styles.feedbackIcon">❌</span>
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

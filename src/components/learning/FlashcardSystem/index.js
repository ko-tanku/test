import React, { useState, useEffect } from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';
import styles from './styles.module.css';

export default function FlashcardSystem({ 
  cards = [], 
  title = "単語帳",
  enableSpacedRepetition = true,
  showProgress = true,
  className = ''
}) {
  return (
    <BrowserOnly fallback={<div>Loading Flashcard System...</div>}>
      {() => <FlashcardSystemClient 
        cards={cards}
        title={title}
        enableSpacedRepetition={enableSpacedRepetition}
        showProgress={showProgress}
        className={className}
      />}
    </BrowserOnly>
  );
}

function FlashcardSystemClient({ cards, title, enableSpacedRepetition, showProgress, className }) {
  const [currentCardIndex, setCurrentCardIndex] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);
  const [studyStats, setStudyStats] = useState({
    correct: 0,
    incorrect: 0,
    total: cards.length
  });
  const [cardProgress, setCardProgress] = useState(
    cards.map(() => ({ 
      difficulty: 1, 
      nextReview: Date.now(), 
      correctStreak: 0 
    }))
  );
  const [mode, setMode] = useState('study'); // 'study', 'review', 'complete'

  const currentCard = cards[currentCardIndex];

  // 間隔反復アルゴリズム（簡易版）
  const calculateNextReview = (difficulty, isCorrect) => {
    if (!enableSpacedRepetition) return Date.now() + 24 * 60 * 60 * 1000; // 1日後
    
    const intervals = [1, 3, 7, 14, 30]; // 日数
    let newDifficulty = isCorrect ? Math.min(difficulty + 1, 4) : 0;
    let daysToAdd = intervals[newDifficulty] || 30;
    
    return Date.now() + (daysToAdd * 24 * 60 * 60 * 1000);
  };

  const handleAnswer = (isCorrect) => {
    const newProgress = [...cardProgress];
    const currentProgress = newProgress[currentCardIndex];
    
    // 統計更新
    setStudyStats(prev => ({
      ...prev,
      correct: prev.correct + (isCorrect ? 1 : 0),
      incorrect: prev.incorrect + (isCorrect ? 0 : 1)
    }));

    // カード進捗更新
    newProgress[currentCardIndex] = {
      ...currentProgress,
      difficulty: isCorrect ? Math.min(currentProgress.difficulty + 1, 4) : 0,
      nextReview: calculateNextReview(currentProgress.difficulty, isCorrect),
      correctStreak: isCorrect ? currentProgress.correctStreak + 1 : 0
    };
    
    setCardProgress(newProgress);
    
    // 次のカードへ
    setTimeout(() => {
      if (currentCardIndex < cards.length - 1) {
        setCurrentCardIndex(currentCardIndex + 1);
        setIsFlipped(false);
      } else {
        setMode('complete');
      }
    }, 1000);
  };

  const resetStudy = () => {
    setCurrentCardIndex(0);
    setIsFlipped(false);
    setMode('study');
    setStudyStats({ correct: 0, incorrect: 0, total: cards.length });
  };

  const flip = () => setIsFlipped(!isFlipped);

  if (!cards || cards.length === 0) {
    return (
      <div className={`${styles.flashcardSystem} ${className}`}>
        <h3>{title}</h3>
        <p>カードが設定されていません。</p>
      </div>
    );
  }

  if (mode === 'complete') {
    const accuracy = ((studyStats.correct / (studyStats.correct + studyStats.incorrect)) * 100).toFixed(1);
    
    return (
      <div className={`${styles.flashcardSystem} ${className}`}>
        <div className={styles.completeScreen}>
          <h3>🎉 学習完了！</h3>
          <div className={styles.finalStats}>
            <div className={styles.statItem}>
              <span className={styles.statValue}>{studyStats.correct}</span>
              <span className={styles.statLabel}>正解</span>
            </div>
            <div className={styles.statItem}>
              <span className={styles.statValue}>{studyStats.incorrect}</span>
              <span className={styles.statLabel}>不正解</span>
            </div>
            <div className={styles.statItem}>
              <span className={styles.statValue}>{accuracy}%</span>
              <span className={styles.statLabel}>正答率</span>
            </div>
          </div>
          <button className={styles.restartButton} onClick={resetStudy}>
            もう一度学習する
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className={`${styles.flashcardSystem} ${className}`}>
      <div className={styles.header}>
        <h3>{title}</h3>
        {showProgress && (
          <div className={styles.progress}>
            <span>{currentCardIndex + 1} / {cards.length}</span>
            <div className={styles.progressBar}>
              <div 
                className={styles.progressFill}
                style={{ width: `${((currentCardIndex + 1) / cards.length) * 100}%` }}
              />
            </div>
          </div>
        )}
      </div>

      <div className={styles.cardContainer}>
        <div 
          className={`${styles.card} ${isFlipped ? styles.flipped : ''}`}
          onClick={flip}
        >
          <div className={styles.cardFront}>
            <div className={styles.cardContent}>
              {currentCard.front || currentCard.question}
            </div>
            <div className={styles.flipHint}>
              クリックして答えを確認
            </div>
          </div>
          <div className={styles.cardBack}>
            <div className={styles.cardContent}>
              {currentCard.back || currentCard.answer}
            </div>
            {currentCard.explanation && (
              <div className={styles.explanation}>
                <strong>解説:</strong> {currentCard.explanation}
              </div>
            )}
          </div>
        </div>
      </div>

      {isFlipped && (
        <div className={styles.answerButtons}>
          <button 
            className={`${styles.answerButton} ${styles.incorrect}`}
            onClick={() => handleAnswer(false)}
          >
            ❌ 不正解
          </button>
          <button 
            className={`${styles.answerButton} ${styles.correct}`}
            onClick={() => handleAnswer(true)}
          >
            ✅ 正解
          </button>
        </div>
      )}

      {showProgress && (
        <div className={styles.stats}>
          <span className={styles.stat}>正解: {studyStats.correct}</span>
          <span className={styles.stat}>不正解: {studyStats.incorrect}</span>
        </div>
      )}
    </div>
  );
}
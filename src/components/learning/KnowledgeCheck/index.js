import React, { useState, useEffect } from 'react';
import styles from './styles.module.css';

export default function KnowledgeCheck({ 
  questions = [], 
  title = "理解度チェック",
  passingScore = 70,
  showDetailedResults = true,
  allowRetry = true,
  className = ''
}) {
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [isCompleted, setIsCompleted] = useState(false);
  const [results, setResults] = useState(null);
  const [timeSpent, setTimeSpent] = useState(0);
  const [startTime] = useState(Date.now());

  useEffect(() => {
    const timer = setInterval(() => {
      setTimeSpent(Math.floor((Date.now() - startTime) / 1000));
    }, 1000);
    
    return () => clearInterval(timer);
  }, [startTime]);

  const handleAnswer = (questionIndex, selectedAnswer) => {
    setAnswers(prev => ({
      ...prev,
      [questionIndex]: selectedAnswer
    }));
  };

  const calculateResults = () => {
    let correct = 0;
    let incorrect = 0;
    const detailed = [];

    questions.forEach((question, index) => {
      const userAnswer = answers[index];
      const isCorrect = userAnswer === question.correctAnswer;
      
      if (isCorrect) {
        correct++;
      } else {
        incorrect++;
      }

      detailed.push({
        questionIndex: index,
        question: question.question,
        userAnswer,
        correctAnswer: question.correctAnswer,
        isCorrect,
        explanation: question.explanation,
        difficulty: question.difficulty || 'medium'
      });
    });

    const score = Math.round((correct / questions.length) * 100);
    const passed = score >= passingScore;

    return {
      correct,
      incorrect,
      total: questions.length,
      score,
      passed,
      timeSpent,
      detailed,
      recommendations: generateRecommendations(detailed, score)
    };
  };

  const generateRecommendations = (detailed, score) => {
    const recommendations = [];
    const incorrectByTopic = {};

    // 間違った問題をトピック別に分析
    detailed.forEach(result => {
      if (!result.isCorrect && result.question.topic) {
        incorrectByTopic[result.question.topic] = (incorrectByTopic[result.question.topic] || 0) + 1;
      }
    });

    // スコア別推奨アクション
    if (score < 50) {
      recommendations.push({
        type: 'critical',
        message: '基礎からの復習が必要です。もう一度教材を読み直してから再挑戦しましょう。'
      });
    } else if (score < 70) {
      recommendations.push({
        type: 'warning',
        message: '理解が不十分な部分があります。間違った問題を重点的に復習しましょう。'
      });
    } else if (score < 90) {
      recommendations.push({
        type: 'info',
        message: '良い理解度です。間違った部分を確認して、さらに理解を深めましょう。'
      });
    } else {
      recommendations.push({
        type: 'success',
        message: '素晴らしい理解度です！次のレベルに進む準備ができています。'
      });
    }

    // トピック別推奨
    Object.entries(incorrectByTopic).forEach(([topic, count]) => {
      if (count > 1) {
        recommendations.push({
          type: 'topic',
          message: `「${topic}」の分野で${count}問間違えています。この分野の復習をお勧めします。`
        });
      }
    });

    return recommendations;
  };

  const submitTest = () => {
    const testResults = calculateResults();
    setResults(testResults);
    setIsCompleted(true);
  };

  const restartTest = () => {
    setCurrentQuestionIndex(0);
    setAnswers({});
    setIsCompleted(false);
    setResults(null);
    setTimeSpent(0);
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  if (!questions || questions.length === 0) {
    return (
      <div className={`${styles.knowledgeCheck} ${className}`}>
        <h3>{title}</h3>
        <p>問題が設定されていません。</p>
      </div>
    );
  }

  if (isCompleted && results) {
    return (
      <div className={`${styles.knowledgeCheck} ${className}`}>
        <div className={styles.resultsScreen}>
          <h3>📊 理解度チェック結果</h3>
          
          <div className={styles.scoreSection}>
            <div className={`${styles.scoreCircle} ${results.passed ? styles.passed : styles.failed}`}>
              <span className={styles.scoreValue}>{results.score}%</span>
              <span className={styles.scoreLabel}>
                {results.passed ? '合格' : '不合格'}
              </span>
            </div>
            
            <div className={styles.scoreStats}>
              <div className={styles.scoreStat}>
                <span className={styles.statNumber}>{results.correct}</span>
                <span className={styles.statLabel}>正解</span>
              </div>
              <div className={styles.scoreStat}>
                <span className={styles.statNumber}>{results.incorrect}</span>
                <span className={styles.statLabel}>不正解</span>
              </div>
              <div className={styles.scoreStat}>
                <span className={styles.statNumber}>{formatTime(results.timeSpent)}</span>
                <span className={styles.statLabel}>所要時間</span>
              </div>
            </div>
          </div>

          {/* 推奨アクション */}
          <div className={styles.recommendations}>
            <h4>📝 学習アドバイス</h4>
            {results.recommendations.map((rec, index) => (
              <div key={index} className={`${styles.recommendation} ${styles[rec.type]}`}>
                {rec.message}
              </div>
            ))}
          </div>

          {/* 詳細結果 */}
          {showDetailedResults && (
            <div className={styles.detailedResults}>
              <h4>📋 詳細結果</h4>
              {results.detailed.map((result, index) => (
                <div key={index} className={`${styles.resultItem} ${result.isCorrect ? styles.correct : styles.incorrect}`}>
                  <div className={styles.resultHeader}>
                    <span className={styles.questionNumber}>問{index + 1}</span>
                    <span className={`${styles.resultStatus} ${result.isCorrect ? styles.correct : styles.incorrect}`}>
                      {result.isCorrect ? '✅ 正解' : '❌ 不正解'}
                    </span>
                  </div>
                  
                  <div className={styles.questionText}>{result.question}</div>
                  
                  {!result.isCorrect && (
                    <div className={styles.answerComparison}>
                      <div className={styles.userAnswer}>
                        <strong>あなたの回答:</strong> {result.userAnswer}
                      </div>
                      <div className={styles.correctAnswer}>
                        <strong>正解:</strong> {result.correctAnswer}
                      </div>
                    </div>
                  )}
                  
                  {result.explanation && (
                    <div className={styles.explanation}>
                      <strong>解説:</strong> {result.explanation}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}

          {allowRetry && (
            <div className={styles.actionButtons}>
              <button className={styles.retryButton} onClick={restartTest}>
                もう一度挑戦する
              </button>
            </div>
          )}
        </div>
      </div>
    );
  }

  // 通常の問題表示
  const currentQuestion = questions[currentQuestionIndex];
  const answeredCount = Object.keys(answers).length;
  const progress = (answeredCount / questions.length) * 100;

  return (
    <div className={`${styles.knowledgeCheck} ${className}`}>
      <div className={styles.header}>
        <h3>{title}</h3>
        <div className={styles.headerInfo}>
          <span className={styles.timer}>⏱️ {formatTime(timeSpent)}</span>
          <span className={styles.questionCounter}>
            {answeredCount} / {questions.length} 完了
          </span>
        </div>
      </div>

      <div className={styles.progressSection}>
        <div className={styles.progressBar}>
          <div 
            className={styles.progressFill}
            style={{ width: `${progress}%` }}
          />
        </div>
        <span className={styles.progressText}>{Math.round(progress)}% 完了</span>
      </div>

      <div className={styles.questionSection}>
        <div className={styles.questionHeader}>
          <span className={styles.questionNumber}>問 {currentQuestionIndex + 1}</span>
          {currentQuestion.difficulty && (
            <span className={`${styles.difficulty} ${styles[currentQuestion.difficulty]}`}>
              {currentQuestion.difficulty === 'easy' ? '初級' : 
               currentQuestion.difficulty === 'medium' ? '中級' : '上級'}
            </span>
          )}
        </div>
        
        <div className={styles.questionText}>
          {currentQuestion.question}
        </div>

        <div className={styles.options}>
          {currentQuestion.options && currentQuestion.options.map((option, index) => (
            <label key={index} className={styles.option}>
              <input
                type="radio"
                name={`question-${currentQuestionIndex}`}
                value={option}
                checked={answers[currentQuestionIndex] === option}
                onChange={(e) => handleAnswer(currentQuestionIndex, e.target.value)}
              />
              <span className={styles.optionText}>{option}</span>
            </label>
          ))}
        </div>
      </div>

      <div className={styles.navigation}>
        <button 
          className={styles.navButton}
          onClick={() => setCurrentQuestionIndex(Math.max(0, currentQuestionIndex - 1))}
          disabled={currentQuestionIndex === 0}
        >
          ← 前の問題
        </button>
        
        {currentQuestionIndex < questions.length - 1 ? (
          <button 
            className={styles.navButton}
            onClick={() => setCurrentQuestionIndex(currentQuestionIndex + 1)}
          >
            次の問題 →
          </button>
        ) : (
          <button 
            className={`${styles.submitButton} ${answeredCount === questions.length ? styles.ready : ''}`}
            onClick={submitTest}
            disabled={answeredCount < questions.length}
          >
            結果を確認する
          </button>
        )}
      </div>

      {answeredCount < questions.length && (
        <div className={styles.incompleteWarning}>
          未回答の問題があります。すべての問題に回答してから結果を確認してください。
        </div>
      )}
    </div>
  );
}
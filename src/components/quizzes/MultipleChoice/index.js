import React, { useState, useEffect } from 'react';
import styles from './styles.module.css';

export default function MultipleChoice({ 
  // 基本プロパティ
  question, 
  options = [], 
  
  // 後方互換性用（quizData形式）
  quizData,
  
  // 機能設定
  multiple = false,
  multiSelect, // multipleのエイリアス
  hints = [],
  explanation = '',
  difficulty = 'medium',
  allowRetry = true,
  showProgressTracking = true,
  timeLimit = null, // 秒数、nullで無制限
  showHints = true,
  randomizeOptions = false,
  variant = 'default',
  
  // IT組込学習特化機能
  category = '', // 'binary', 'memory', 'cpu', 'communication', 'security'等
  aiPromptTemplate = '', // AI学習支援用プロンプトテンプレート
  relatedTerms = [], // 関連専門用語
  codeExample = '', // コード例の表示
  showBinaryConverter = false, // 2進数変換機能
  showLogicGates = false // 論理演算の視覚化
}) {
  // 後方互換性: quizDataが渡された場合の処理
  const actualQuestion = quizData?.question || question;
  const actualOptions = quizData?.options || options;
  const actualExplanation = quizData?.explanation || explanation;
  
  // multipleとmultiSelectの統合
  const isMultiple = multiSelect !== undefined ? multiSelect : multiple;
  const [selectedAnswers, setSelectedAnswers] = useState(isMultiple ? [] : null);
  const [showResults, setShowResults] = useState(false);
  const [currentHintIndex, setCurrentHintIndex] = useState(-1);
  const [attempts, setAttempts] = useState(0);
  const [startTime] = useState(Date.now());
  const [timeSpent, setTimeSpent] = useState(0);
  const [timeRemaining, setTimeRemaining] = useState(timeLimit);
  const [isTimeUp, setIsTimeUp] = useState(false);

  useEffect(() => {
    const timer = setInterval(() => {
      const elapsed = Math.floor((Date.now() - startTime) / 1000);
      setTimeSpent(elapsed);
      
      if (timeLimit && !showResults) {
        const remaining = Math.max(0, timeLimit - elapsed);
        setTimeRemaining(remaining);
        
        if (remaining === 0 && !isTimeUp) {
          setIsTimeUp(true);
          handleSubmit(true); // 自動提出
        }
      }
    }, 1000);
    
    return () => clearInterval(timer);
  }, [startTime, timeLimit, showResults, isTimeUp]);

  const handleAnswerSelect = (index) => {
    if (showResults || isTimeUp) return;
    
    if (isMultiple) {
      setSelectedAnswers(prev => 
        prev.includes(index) 
          ? prev.filter(i => i !== index)
          : [...prev, index]
      );
    } else {
      setSelectedAnswers(index);
    }
  };

  const handleSubmit = (autoSubmit = false) => {
    setShowResults(true);
    setAttempts(prev => prev + 1);
    
    // 学習データの記録（実際の実装では外部ストレージに保存）
    const learningData = {
      question,
      selectedAnswers,
      timeSpent,
      attempts: attempts + 1,
      hintsUsed: currentHintIndex + 1,
      difficulty,
      autoSubmitted: autoSubmit
    };
    
    if (showProgressTracking) {
      console.log('Learning Data:', learningData);
    }
  };

  const handleRetry = () => {
    setSelectedAnswers(isMultiple ? [] : null);
    setShowResults(false);
    setCurrentHintIndex(-1);
    setIsTimeUp(false);
  };

  const showNextHint = () => {
    if (currentHintIndex < hints.length - 1) {
      setCurrentHintIndex(prev => prev + 1);
    }
  };

  const isSelected = (index) => {
    return isMultiple 
      ? selectedAnswers.includes(index)
      : selectedAnswers === index;
  };

  const getResultStatus = () => {
    if (!showResults) return null;
    
    const correctOptions = actualOptions.filter(option => option.correct || option.isCorrect);
    const correctIndices = correctOptions.map((_, idx) => actualOptions.findIndex(opt => opt === correctOptions[idx]));
    
    if (isMultiple) {
      const selectedSet = new Set(selectedAnswers);
      const correctSet = new Set(correctIndices);
      return selectedSet.size === correctSet.size && 
             [...selectedSet].every(x => correctSet.has(x));
    } else {
      return correctIndices.includes(selectedAnswers);
    }
  };

  const isCorrect = getResultStatus();

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  // IT組込学習特化機能
  const [showAIPrompt, setShowAIPrompt] = useState(false);
  const [showTerms, setShowTerms] = useState(false);
  const [showCode, setShowCode] = useState(false);
  
  // バイナリコンバーター状態
  const [binaryInput, setBinaryInput] = useState('');
  const [binaryResult, setBinaryResult] = useState('');
  
  const convertBinary = (input, fromBase = 10, toBase = 2) => {
    try {
      const decimal = parseInt(input, fromBase);
      if (isNaN(decimal)) return '';
      return decimal.toString(toBase).toUpperCase();
    } catch (e) {
      return '';
    }
  };

  const getCategoryIcon = (cat) => {
    const icons = {
      'binary': '🔢',
      'memory': '🧠',
      'cpu': '💻',
      'communication': '📡',
      'security': '🔐',
      'ai': '🤖'
    };
    return icons[cat] || '📚';
  };

  if (!actualQuestion || !actualOptions.length) {
    return <div className={styles.multiplechoice}>Invalid quiz data</div>;
  }

  return (
    <div className={`${styles.multiplechoice} ${styles[difficulty]}`}>
      {/* ヘッダー情報 */}
      <div className={styles.header}>
        <div className={styles.questionInfo}>
          <span className={`${styles.difficulty} ${styles[`difficulty${difficulty}`]}`}>
            {difficulty === 'easy' ? '初級' : difficulty === 'medium' ? '中級' : '上級'}
          </span>
          {isMultiple && <span className={styles.multipleIndicator}>複数選択可</span>}
          {category && (
            <span className={styles.category}>
              {getCategoryIcon(category)} {category.charAt(0).toUpperCase() + category.slice(1)}
            </span>
          )}
        </div>
        
        <div className={styles.metadata}>
          {showProgressTracking && (
            <span className={styles.attempts}>試行回数: {attempts + (showResults ? 0 : 1)}</span>
          )}
          {timeLimit && (
            <span className={`${styles.timer} ${timeRemaining <= 30 ? styles.urgent : ''}`}>
              ⏱️ {formatTime(timeRemaining || 0)}
            </span>
          )}
        </div>
      </div>

      <h3 className={styles.question}>{actualQuestion}</h3>

      {/* ヒント表示 */}
      {showHints && hints.length > 0 && !showResults && (
        <div className={styles.hintsSection}>
          {currentHintIndex >= 0 && (
            <div className={styles.currentHint}>
              <strong>💡 ヒント {currentHintIndex + 1}:</strong> {hints[currentHintIndex]}
            </div>
          )}
          
          {currentHintIndex < hints.length - 1 && (
            <button 
              className={styles.hintButton}
              onClick={showNextHint}
            >
              ヒントを見る ({currentHintIndex + 2}/{hints.length})
            </button>
          )}
        </div>
      )}

      <div className={styles.options}>
        {actualOptions.map((option, index) => (
          <div 
            key={index} 
            className={`${styles.option} ${
              showResults ? ((option.correct || option.isCorrect) ? styles.correctOption : styles.incorrectOption) : ''
            } ${isSelected(index) ? styles.selected : ''}`}
          >
            <label className={styles.optionLabel}>
              <input
                type={isMultiple ? 'checkbox' : 'radio'}
                name={`quiz-option-${actualQuestion}`}
                checked={isSelected(index)}
                onChange={() => handleAnswerSelect(index)}
                className={styles.optionInput}
                disabled={showResults}
              />
              <span className={styles.optionText}>{option.text || option}</span>
              {showResults && (option.correct || option.isCorrect) && (
                <span className={styles.correctIndicator}>✅</span>
              )}
              {showResults && !(option.correct || option.isCorrect) && isSelected(index) && (
                <span className={styles.incorrectIndicator}>❌</span>
              )}
            </label>
            
            {showResults && option.explanation && (
              <div className={styles.optionExplanation}>
                <strong>解説:</strong> {option.explanation}
              </div>
            )}
          </div>
        ))}
      </div>

      {/* 結果表示 */}
      {showResults && (
        <div className={`${styles.results} ${isCorrect ? styles.correct : styles.incorrect}`}>
          <div className={styles.resultHeader}>
            <span className={styles.resultIcon}>
              {isCorrect ? '🎉' : '😅'}
            </span>
            <span className={styles.resultText}>
              {isCorrect ? '正解です！' : '不正解です'}
            </span>
            {isTimeUp && <span className={styles.timeUpIndicator}>（時間切れ）</span>}
          </div>
          
          {actualExplanation && (
            <div className={styles.overallExplanation}>
              <strong>📝 詳細解説:</strong>
              <p>{actualExplanation}</p>
            </div>
          )}
          
          <div className={styles.performanceInfo}>
            <span className={styles.timeInfo}>所要時間: {formatTime(timeSpent)}</span>
            {currentHintIndex >= 0 && (
              <span className={styles.hintInfo}>使用ヒント: {currentHintIndex + 1}個</span>
            )}
          </div>
          
          {allowRetry && !isCorrect && (
            <button 
              className={styles.retryButton}
              onClick={handleRetry}
            >
              もう一度挑戦する
            </button>
          )}
        </div>
      )}

      {/* IT組込学習支援機能 */}
      <div className={styles.learningSupport}>
        {/* AI学習プロンプト */}
        {aiPromptTemplate && (
          <div className={styles.supportTool}>
            <button 
              onClick={() => setShowAIPrompt(!showAIPrompt)}
              className={styles.supportToggle}
            >
              🤖 AI学習ヘルプ
            </button>
            {showAIPrompt && (
              <div className={styles.aiPrompt}>
                <h4>AIに質問するときのヒント:</h4>
                <p>{aiPromptTemplate}</p>
                <small>※ このテンプレートをChatGPTやClaudeにコピーして活用してください</small>
              </div>
            )}
          </div>
        )}

        {/* 関連用語 */}
        {relatedTerms.length > 0 && (
          <div className={styles.supportTool}>
            <button 
              onClick={() => setShowTerms(!showTerms)}
              className={styles.supportToggle}
            >
              📖 関連用語
            </button>
            {showTerms && (
              <div className={styles.relatedTerms}>
                <h4>関連する専門用語:</h4>
                <ul>
                  {relatedTerms.map((term, idx) => (
                    <li key={idx}>
                      <strong>{term.term}:</strong> {term.definition}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}

        {/* コード例 */}
        {codeExample && (
          <div className={styles.supportTool}>
            <button 
              onClick={() => setShowCode(!showCode)}
              className={styles.supportToggle}
            >
              💻 コード例
            </button>
            {showCode && (
              <div className={styles.codeExample}>
                <h4>実装例:</h4>
                <pre><code>{codeExample}</code></pre>
              </div>
            )}
          </div>
        )}

        {/* 2進数変換器 */}
        {showBinaryConverter && (
          <div className={styles.supportTool}>
            <div className={styles.binaryConverter}>
              <h4>🔢 数値変換ツール</h4>
              <div className={styles.converterRow}>
                <input 
                  type="text" 
                  placeholder="数値を入力"
                  value={binaryInput}
                  onChange={(e) => {
                    setBinaryInput(e.target.value);
                    setBinaryResult(convertBinary(e.target.value));
                  }}
                />
                <span>→</span>
                <span className={styles.result}>
                  2進数: {convertBinary(binaryInput, 10, 2)}<br/>
                  16進数: {convertBinary(binaryInput, 10, 16)}
                </span>
              </div>
            </div>
          </div>
        )}
      </div>

      {!showResults && !isTimeUp && (
        <button 
          onClick={() => handleSubmit()}
          className={styles.submitButton}
          disabled={isMultiple ? selectedAnswers.length === 0 : selectedAnswers === null}
        >
          回答を確認
        </button>
      )}
    </div>
  );
}

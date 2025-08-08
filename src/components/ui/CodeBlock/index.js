import React, { useState } from 'react';
import styles from './styles.module.css';

export default function CodeBlock({ 
  code = '', 
  language = 'javascript',
  title,
  showLineNumbers = true,
  copyable = true,
  className = '',
  
  // IT組込学習特化機能
  explanation = '', // コードの解説
  highlights = [], // ハイライトする行番号の配列
  annotations = [], // 行ごとの注釈 [{line: 1, text: '説明'}, ...]
  difficulty = 'beginner', // 'beginner', 'intermediate', 'advanced'
  category = '', // 'embedded', 'c-language', 'linux', 'rtos'
  showMemoryLayout = false, // メモリレイアウトの表示
  interactive = false, // インタラクティブな実行（将来実装）
  relatedConcepts = [] // 関連する概念
}) {
  const [copied, setCopied] = useState(false);
  const [showExplanation, setShowExplanation] = useState(false);
  const [showAnnotations, setShowAnnotations] = useState(false);

  // カテゴリアイコンの取得
  const getCategoryIcon = (cat) => {
    const icons = {
      'embedded': '🔧',
      'c-language': '🖥️',
      'linux': '🐧',
      'rtos': '⚡',
      'memory': '🧠',
      'communication': '📡'
    };
    return icons[cat] || '💻';
  };

  // 難易度の表示
  const getDifficultyLabel = (diff) => {
    const labels = {
      'beginner': '初級',
      'intermediate': '中級',
      'advanced': '上級'
    };
    return labels[diff] || '初級';
  };

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy code:', err);
    }
  };

  const formatCode = (code) => {
    return code.split('\n').map((line, index) => {
      const lineNum = index + 1;
      const isHighlighted = highlights.includes(lineNum);
      const annotation = annotations.find(ann => ann.line === lineNum);

      return (
        <div key={index} className={`${styles.codeLine} ${isHighlighted ? styles.highlighted : ''}`}>
          {showLineNumbers && (
            <span className={`${styles.lineNumber} ${isHighlighted ? styles.highlightedNumber : ''}`}>
              {lineNum}
            </span>
          )}
          <span className={styles.lineContent}>{line || ' '}</span>
          {annotation && showAnnotations && (
            <span className={styles.annotation} title={annotation.text}>
              💡
            </span>
          )}
        </div>
      );
    });
  };

  return (
    <div className={`${styles.codeBlock} ${className}`}>
      {/* 拡張ヘッダー */}
      <div className={styles.codeHeader}>
        <div className={styles.headerLeft}>
          {title && <span className={styles.codeTitle}>{title}</span>}
          {category && (
            <span className={styles.categoryTag}>
              {getCategoryIcon(category)} {category}
            </span>
          )}
          <span className={styles.difficultyTag}>
            {getDifficultyLabel(difficulty)}
          </span>
        </div>
        
        <div className={styles.headerRight}>
          {/* コントロールボタン */}
          {explanation && (
            <button 
              onClick={() => setShowExplanation(!showExplanation)}
              className={styles.controlButton}
              title="解説を表示/非表示"
            >
              📝 解説
            </button>
          )}
          
          {annotations.length > 0 && (
            <button 
              onClick={() => setShowAnnotations(!showAnnotations)}
              className={styles.controlButton}
              title="注釈を表示/非表示"
            >
              💡 注釈
            </button>
          )}

          {copyable && (
            <button 
              onClick={handleCopy}
              className={styles.copyButton}
              title="コードをコピー"
            >
              {copied ? '✓ コピー済み' : '📋 コピー'}
            </button>
          )}
        </div>
      </div>
      <div className={styles.codeContainer}>
        <pre className={`${styles.codeContent} language-${language}`}>
          <code>
            {showLineNumbers ? formatCode(code) : code}
          </code>
        </pre>
      </div>

      {/* 解説セクション */}
      {explanation && showExplanation && (
        <div className={styles.explanationSection}>
          <h4 className={styles.explanationTitle}>📝 コード解説</h4>
          <div className={styles.explanationContent}>
            {explanation}
          </div>
        </div>
      )}

      {/* 注釈一覧 */}
      {annotations.length > 0 && showAnnotations && (
        <div className={styles.annotationsSection}>
          <h4 className={styles.annotationsTitle}>💡 行別注釈</h4>
          <div className={styles.annotationsList}>
            {annotations.map((ann, idx) => (
              <div key={idx} className={styles.annotationItem}>
                <span className={styles.annotationLine}>行{ann.line}:</span>
                <span className={styles.annotationText}>{ann.text}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 関連概念 */}
      {relatedConcepts.length > 0 && (
        <div className={styles.conceptsSection}>
          <h4 className={styles.conceptsTitle}>🔗 関連する概念</h4>
          <div className={styles.conceptsList}>
            {relatedConcepts.map((concept, idx) => (
              <span key={idx} className={styles.conceptTag}>
                {concept}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* メモリレイアウト（簡易版） */}
      {showMemoryLayout && language === 'c' && (
        <div className={styles.memorySection}>
          <h4 className={styles.memoryTitle}>🧠 メモリレイアウトのイメージ</h4>
          <div className={styles.memoryNote}>
            <p>このCコードは以下のメモリ領域を使用します：</p>
            <ul>
              <li><strong>スタック:</strong> ローカル変数、関数の引数</li>
              <li><strong>ヒープ:</strong> 動的割り当て (malloc等)</li>
              <li><strong>データ:</strong> 初期化済みグローバル変数</li>
              <li><strong>BSS:</strong> 未初期化グローバル変数</li>
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}

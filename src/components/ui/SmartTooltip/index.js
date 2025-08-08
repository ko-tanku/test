import React, { useState, useEffect, useRef } from 'react';
import styles from './styles.module.css';

export default function SmartTooltip({
  children,
  content,
  term = '', // 専門用語
  definition = '', // 定義
  category = '', // カテゴリ（IT, 組込, セキュリティ等）
  examples = [], // 使用例
  relatedTerms = [], // 関連用語
  firstOccurrence = false, // その用語の初出かどうか
  position = 'auto', // 'top', 'bottom', 'left', 'right', 'auto'
  trigger = 'hover', // 'hover', 'click', 'focus'
  delay = 300, // ホバー時の遅延（ms）
  showIcon = true, // アイコン表示
  persistent = false, // クリックして固定するか
  maxWidth = 300
}) {
  const [isVisible, setIsVisible] = useState(false);
  const [isPersistent, setIsPersistent] = useState(false);
  const [actualPosition, setActualPosition] = useState(position);
  const tooltipRef = useRef(null);
  const triggerRef = useRef(null);
  const timeoutRef = useRef(null);

  // 位置の自動調整
  useEffect(() => {
    if (isVisible && position === 'auto' && tooltipRef.current && triggerRef.current) {
      const tooltipRect = tooltipRef.current.getBoundingClientRect();
      const triggerRect = triggerRef.current.getBoundingClientRect();
      const viewportHeight = window.innerHeight;
      const viewportWidth = window.innerWidth;

      let bestPosition = 'bottom';

      // 上下の空きスペースを確認
      const spaceAbove = triggerRect.top;
      const spaceBelow = viewportHeight - triggerRect.bottom;
      const spaceLeft = triggerRect.left;
      const spaceRight = viewportWidth - triggerRect.right;

      if (spaceBelow >= tooltipRect.height + 10) {
        bestPosition = 'bottom';
      } else if (spaceAbove >= tooltipRect.height + 10) {
        bestPosition = 'top';
      } else if (spaceRight >= tooltipRect.width + 10) {
        bestPosition = 'right';
      } else if (spaceLeft >= tooltipRect.width + 10) {
        bestPosition = 'left';
      }

      setActualPosition(bestPosition);
    }
  }, [isVisible, position]);

  const handleMouseEnter = () => {
    if (trigger === 'hover' && !isPersistent) {
      timeoutRef.current = setTimeout(() => {
        setIsVisible(true);
      }, delay);
    }
  };

  const handleMouseLeave = () => {
    if (trigger === 'hover' && !isPersistent) {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
      setIsVisible(false);
    }
  };

  const handleClick = (e) => {
    e.preventDefault();
    e.stopPropagation();
    
    if (trigger === 'click' || persistent) {
      setIsVisible(!isVisible);
      if (persistent && !isPersistent) {
        setIsPersistent(true);
      }
    }
  };

  const handleClose = () => {
    setIsVisible(false);
    setIsPersistent(false);
  };

  // 外部クリックでツールチップを閉じる
  useEffect(() => {
    const handleOutsideClick = (event) => {
      if (
        isPersistent &&
        tooltipRef.current &&
        triggerRef.current &&
        !tooltipRef.current.contains(event.target) &&
        !triggerRef.current.contains(event.target)
      ) {
        handleClose();
      }
    };

    if (isPersistent) {
      document.addEventListener('mousedown', handleOutsideClick);
      return () => document.removeEventListener('mousedown', handleOutsideClick);
    }
  }, [isPersistent]);

  const getCategoryIcon = (cat) => {
    const icons = {
      'IT': '💻',
      '組込': '🔧',
      'セキュリティ': '🔐',
      'AI': '🤖',
      'ハードウェア': '⚡',
      'ソフトウェア': '💿',
      'ネットワーク': '🌐'
    };
    return icons[cat] || '📚';
  };

  const getTooltipContent = () => {
    // カスタムコンテンツがある場合はそれを使用
    if (content) {
      return <div className={styles.customContent}>{content}</div>;
    }

    // 専門用語用の詳細コンテンツを生成
    return (
      <div className={styles.termContent}>
        {term && (
          <div className={styles.termHeader}>
            {category && showIcon && (
              <span className={styles.categoryIcon}>
                {getCategoryIcon(category)}
              </span>
            )}
            <strong className={styles.termName}>{term}</strong>
            {category && (
              <span className={styles.categoryTag}>{category}</span>
            )}
            {firstOccurrence && (
              <span className={styles.firstOccurrenceTag}>初出</span>
            )}
          </div>
        )}

        {definition && (
          <div className={styles.definition}>
            {definition}
          </div>
        )}

        {examples.length > 0 && (
          <div className={styles.examples}>
            <strong>使用例:</strong>
            <ul className={styles.examplesList}>
              {examples.map((example, index) => (
                <li key={index}>{example}</li>
              ))}
            </ul>
          </div>
        )}

        {relatedTerms.length > 0 && (
          <div className={styles.relatedTerms}>
            <strong>関連用語:</strong>
            <div className={styles.relatedList}>
              {relatedTerms.map((relatedTerm, index) => (
                <span key={index} className={styles.relatedTag}>
                  {relatedTerm}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    );
  };

  return (
    <span className={styles.smartTooltipContainer}>
      <span
        ref={triggerRef}
        className={`${styles.trigger} ${firstOccurrence ? styles.firstOccurrence : ''}`}
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
        onClick={handleClick}
        onFocus={trigger === 'focus' ? () => setIsVisible(true) : undefined}
        onBlur={trigger === 'focus' ? () => setIsVisible(false) : undefined}
        tabIndex={trigger === 'focus' ? 0 : undefined}
      >
        {children}
        {firstOccurrence && showIcon && (
          <span className={styles.newTermIcon}>✨</span>
        )}
      </span>

      {isVisible && (
        <div
          ref={tooltipRef}
          className={`${styles.tooltip} ${styles[actualPosition]}`}
          style={{ maxWidth: `${maxWidth}px` }}
        >
          <div className={styles.tooltipContent}>
            {getTooltipContent()}
          </div>

          {(persistent || isPersistent) && (
            <button
              className={styles.closeButton}
              onClick={handleClose}
              aria-label="ツールチップを閉じる"
            >
              ×
            </button>
          )}

          <div className={styles.arrow} />
        </div>
      )}
    </span>
  );
}
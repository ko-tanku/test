import React from 'react';
import styles from './styles.module.css';

export default function LearningPathIndicator({
  currentStep = 0,
  totalSteps = 0,
  steps = [],
  courseTitle = '',
  showTimeEstimate = true,
  onStepClick = () => {},
  variant = 'horizontal' // 'horizontal' | 'vertical' | 'compact'
}) {
  // デフォルトステップ生成
  const defaultSteps = Array.from({ length: totalSteps }, (_, i) => ({
    id: i,
    title: `ステップ ${i + 1}`,
    completed: i < currentStep,
    current: i === currentStep,
    timeEstimate: 15
  }));

  const actualSteps = steps.length > 0 ? steps : defaultSteps;

  const getStepStatus = (index) => {
    if (index < currentStep) return 'completed';
    if (index === currentStep) return 'current';
    return 'upcoming';
  };

  const getStepIcon = (status, index) => {
    switch (status) {
      case 'completed':
        return '✅';
      case 'current':
        return '🔵';
      default:
        return index + 1;
    }
  };

  const calculateTotalTime = () => {
    return actualSteps.reduce((total, step) => total + (step.timeEstimate || 15), 0);
  };

  const calculateRemainingTime = () => {
    return actualSteps
      .slice(currentStep)
      .reduce((total, step) => total + (step.timeEstimate || 15), 0);
  };

  const formatTime = (minutes) => {
    if (minutes < 60) return `${minutes}分`;
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return mins > 0 ? `${hours}時間${mins}分` : `${hours}時間`;
  };

  if (variant === 'compact') {
    return (
      <div className={styles.compactIndicator}>
        <div className={styles.compactProgress}>
          <span className={styles.compactText}>
            {currentStep + 1} / {totalSteps}
          </span>
          <div className={styles.compactBar}>
            <div 
              className={styles.compactFill}
              style={{ width: `${((currentStep + 1) / totalSteps) * 100}%` }}
            />
          </div>
        </div>
        {showTimeEstimate && (
          <span className={styles.compactTime}>
            残り約{formatTime(calculateRemainingTime())}
          </span>
        )}
      </div>
    );
  }

  return (
    <div className={`${styles.pathIndicator} ${styles[variant]}`}>
      {/* ヘッダー */}
      <div className={styles.header}>
        {courseTitle && (
          <h3 className={styles.courseTitle}>{courseTitle}</h3>
        )}
        <div className={styles.overview}>
          <span className={styles.progressText}>
            進捗: {currentStep}/{totalSteps} ステップ 
            ({Math.round(((currentStep) / totalSteps) * 100)}%完了)
          </span>
          {showTimeEstimate && (
            <span className={styles.timeEstimate}>
              全体: {formatTime(calculateTotalTime())} | 
              残り: {formatTime(calculateRemainingTime())}
            </span>
          )}
        </div>
      </div>

      {/* ステップ一覧 */}
      <div className={styles.stepsContainer}>
        {actualSteps.map((step, index) => {
          const status = getStepStatus(index);
          return (
            <div key={step.id || index} className={styles.stepWrapper}>
              <div 
                className={`${styles.step} ${styles[status]}`}
                onClick={() => onStepClick(index, step)}
                role={onStepClick !== (() => {}) ? "button" : undefined}
                tabIndex={onStepClick !== (() => {}) ? 0 : undefined}
              >
                <div className={styles.stepIcon}>
                  {getStepIcon(status, index)}
                </div>
                <div className={styles.stepContent}>
                  <div className={styles.stepTitle}>
                    {step.title || `ステップ ${index + 1}`}
                  </div>
                  {step.description && (
                    <div className={styles.stepDescription}>
                      {step.description}
                    </div>
                  )}
                  {step.timeEstimate && showTimeEstimate && (
                    <div className={styles.stepTime}>
                      ⏱️ 約{step.timeEstimate}分
                    </div>
                  )}
                </div>
                {status === 'current' && (
                  <div className={styles.currentIndicator}>
                    現在ここ
                  </div>
                )}
              </div>
              
              {/* 接続線 */}
              {index < actualSteps.length - 1 && (
                <div className={`${styles.connector} ${
                  index < currentStep ? styles.completed : ''
                }`} />
              )}
            </div>
          );
        })}
      </div>

      {/* 次のステップの案内 */}
      {currentStep < totalSteps - 1 && (
        <div className={styles.nextStepGuide}>
          <h4>次のステップ</h4>
          <div className={styles.nextStep}>
            <span className={styles.nextStepIcon}>⏭️</span>
            <span className={styles.nextStepTitle}>
              {actualSteps[currentStep + 1]?.title || `ステップ ${currentStep + 2}`}
            </span>
            {actualSteps[currentStep + 1]?.timeEstimate && (
              <span className={styles.nextStepTime}>
                (約{actualSteps[currentStep + 1].timeEstimate}分)
              </span>
            )}
          </div>
        </div>
      )}

      {/* 完了時のメッセージ */}
      {currentStep >= totalSteps && (
        <div className={styles.completionMessage}>
          <span className={styles.completionIcon}>🎉</span>
          <span className={styles.completionText}>
            おめでとうございます！すべてのステップを完了しました。
          </span>
        </div>
      )}
    </div>
  );
}
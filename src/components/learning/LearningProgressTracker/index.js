import React, { useState, useEffect } from 'react';
import styles from './styles.module.css';

const LearningProgressTracker = ({
  userId = 'default',
  courseId = 'embedded-basics',
  title = "学習進捗トラッカー",
  chapters = [],
  showDetailedStats = true,
  onProgressUpdate = null
}) => {
  const [progress, setProgress] = useState({});
  const [completedItems, setCompletedItems] = useState(new Set());
  const [timeSpent, setTimeSpent] = useState({});
  const [currentSession, setCurrentSession] = useState({
    startTime: null,
    currentChapter: null,
    sessionTime: 0
  });
  const [stats, setStats] = useState({
    totalCompletion: 0,
    totalTimeSpent: 0,
    averageScore: 0,
    streak: 0,
    lastStudyDate: null
  });

  // デフォルトチャプターデータ
  const defaultChapters = [
    {
      id: 'intro',
      title: 'はじめに',
      estimatedTime: 30,
      lessons: [
        { id: 'intro-1', title: '組込制御とは', type: 'reading', estimatedTime: 15 },
        { id: 'intro-2', title: '学習の進め方', type: 'reading', estimatedTime: 15 }
      ]
    },
    {
      id: 'binary',
      title: '2進数と論理演算',
      estimatedTime: 120,
      lessons: [
        { id: 'binary-1', title: '進数変換', type: 'interactive', estimatedTime: 30 },
        { id: 'binary-2', title: '論理ゲート', type: 'simulation', estimatedTime: 45 },
        { id: 'binary-3', title: 'ビット演算', type: 'exercise', estimatedTime: 30 },
        { id: 'binary-quiz', title: '理解度チェック', type: 'quiz', estimatedTime: 15 }
      ]
    },
    {
      id: 'c-programming',
      title: 'C言語基礎',
      estimatedTime: 180,
      lessons: [
        { id: 'c-1', title: '基本文法', type: 'reading', estimatedTime: 45 },
        { id: 'c-2', title: 'データ型と変数', type: 'interactive', estimatedTime: 60 },
        { id: 'c-3', title: '制御文', type: 'exercise', estimatedTime: 60 },
        { id: 'c-quiz', title: '演習問題', type: 'quiz', estimatedTime: 15 }
      ]
    },
    {
      id: 'pointers',
      title: 'ポインタとメモリ',
      estimatedTime: 150,
      lessons: [
        { id: 'ptr-1', title: 'ポインタの概念', type: 'reading', estimatedTime: 30 },
        { id: 'ptr-2', title: 'メモリ管理', type: 'simulation', estimatedTime: 45 },
        { id: 'ptr-3', title: 'アドレス演算', type: 'exercise', estimatedTime: 60 },
        { id: 'ptr-quiz', title: '総合問題', type: 'quiz', estimatedTime: 15 }
      ]
    }
  ];

  const activeChapters = chapters.length > 0 ? chapters : defaultChapters;

  // 進捗の計算
  const calculateProgress = () => {
    const allLessons = activeChapters.flatMap(chapter => 
      chapter.lessons.map(lesson => ({ ...lesson, chapterId: chapter.id }))
    );
    
    const completedLessons = allLessons.filter(lesson => completedItems.has(lesson.id));
    const totalCompletion = allLessons.length > 0 
      ? (completedLessons.length / allLessons.length) * 100 
      : 0;

    const chapterProgress = activeChapters.map(chapter => {
      const chapterLessons = chapter.lessons;
      const completedInChapter = chapterLessons.filter(lesson => completedItems.has(lesson.id));
      return {
        ...chapter,
        completion: chapterLessons.length > 0 
          ? (completedInChapter.length / chapterLessons.length) * 100 
          : 0,
        completedCount: completedInChapter.length,
        totalCount: chapterLessons.length
      };
    });

    const totalTimeSpent = Object.values(timeSpent).reduce((sum, time) => sum + time, 0);

    setProgress({ chapters: chapterProgress, overall: totalCompletion });
    setStats(prev => ({
      ...prev,
      totalCompletion: Math.round(totalCompletion),
      totalTimeSpent: Math.round(totalTimeSpent)
    }));
  };

  // レッスン完了の処理
  const completeLesson = (lessonId, score = null) => {
    setCompletedItems(prev => new Set([...prev, lessonId]));
    
    if (score !== null) {
      // スコア記録の処理（実装例）
      console.log(`Lesson ${lessonId} completed with score: ${score}`);
    }

    if (onProgressUpdate) {
      onProgressUpdate({
        lessonId,
        completed: true,
        score,
        timestamp: new Date()
      });
    }
  };

  // 学習セッションの開始
  const startSession = (chapterId) => {
    setCurrentSession({
      startTime: Date.now(),
      currentChapter: chapterId,
      sessionTime: 0
    });
  };

  // 学習セッションの終了
  const endSession = () => {
    if (currentSession.startTime && currentSession.currentChapter) {
      const sessionDuration = (Date.now() - currentSession.startTime) / 1000 / 60; // 分
      
      setTimeSpent(prev => ({
        ...prev,
        [currentSession.currentChapter]: (prev[currentSession.currentChapter] || 0) + sessionDuration
      }));

      setStats(prev => ({
        ...prev,
        lastStudyDate: new Date().toISOString().split('T')[0]
      }));
    }

    setCurrentSession({
      startTime: null,
      currentChapter: null,
      sessionTime: 0
    });
  };

  // サンプルデータの生成
  const generateSampleData = () => {
    const sampleCompleted = new Set([
      'intro-1', 'intro-2',
      'binary-1', 'binary-2',
      'c-1', 'c-2'
    ]);

    const sampleTimeSpent = {
      intro: 25,
      binary: 85,
      'c-programming': 120,
      pointers: 30
    };

    setCompletedItems(sampleCompleted);
    setTimeSpent(sampleTimeSpent);
    setStats(prev => ({
      ...prev,
      averageScore: 78,
      streak: 5,
      lastStudyDate: '2024-01-15'
    }));
  };

  useEffect(() => {
    calculateProgress();
  }, [completedItems, timeSpent]);

  useEffect(() => {
    // セッション時間の更新
    let interval;
    if (currentSession.startTime) {
      interval = setInterval(() => {
        setCurrentSession(prev => ({
          ...prev,
          sessionTime: (Date.now() - prev.startTime) / 1000 / 60
        }));
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [currentSession.startTime]);

  const formatTime = (minutes) => {
    const hours = Math.floor(minutes / 60);
    const mins = Math.round(minutes % 60);
    if (hours > 0) {
      return `${hours}h ${mins}m`;
    }
    return `${mins}m`;
  };

  const getLessonIcon = (type) => {
    switch (type) {
      case 'reading': return '📖';
      case 'interactive': return '🎮';
      case 'simulation': return '⚙️';
      case 'exercise': return '✏️';
      case 'quiz': return '❓';
      default: return '📝';
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h3>{title}</h3>
        <div className={styles.overallProgress}>
          <div className={styles.progressCircle}>
            <div 
              className={styles.progressFill}
              style={{
                background: `conic-gradient(#007bff ${progress.overall * 3.6}deg, #e9ecef 0deg)`
              }}
            >
              <div className={styles.progressText}>
                {Math.round(progress.overall || 0)}%
              </div>
            </div>
          </div>
          <div className={styles.progressInfo}>
            <h4>全体進捗</h4>
            <p>{completedItems.size} / {activeChapters.reduce((sum, ch) => sum + ch.lessons.length, 0)} 完了</p>
          </div>
        </div>
      </div>

      {showDetailedStats && (
        <div className={styles.statsGrid}>
          <div className={styles.statCard}>
            <div className={styles.statValue}>{formatTime(stats.totalTimeSpent)}</div>
            <div className={styles.statLabel}>総学習時間</div>
          </div>
          <div className={styles.statCard}>
            <div className={styles.statValue}>{stats.averageScore}%</div>
            <div className={styles.statLabel}>平均スコア</div>
          </div>
          <div className={styles.statCard}>
            <div className={styles.statValue}>{stats.streak}日</div>
            <div className={styles.statLabel}>連続学習</div>
          </div>
          <div className={styles.statCard}>
            <div className={styles.statValue}>{stats.lastStudyDate || '未記録'}</div>
            <div className={styles.statLabel}>最終学習日</div>
          </div>
        </div>
      )}

      {currentSession.currentChapter && (
        <div className={styles.currentSession}>
          <h4>現在の学習セッション</h4>
          <div className={styles.sessionInfo}>
            <span>学習中: {activeChapters.find(ch => ch.id === currentSession.currentChapter)?.title}</span>
            <span>経過時間: {formatTime(currentSession.sessionTime)}</span>
            <button onClick={endSession} className={styles.endSessionBtn}>セッション終了</button>
          </div>
        </div>
      )}

      <div className={styles.chaptersContainer}>
        <h4>章別進捗</h4>
        {progress.chapters && progress.chapters.map((chapter, index) => (
          <div key={chapter.id} className={styles.chapterCard}>
            <div className={styles.chapterHeader}>
              <div className={styles.chapterInfo}>
                <h5>{chapter.title}</h5>
                <div className={styles.chapterMeta}>
                  <span>{chapter.completedCount} / {chapter.totalCount} 完了</span>
                  <span>推定 {formatTime(chapter.estimatedTime)}</span>
                </div>
              </div>
              <div className={styles.chapterProgress}>
                <div className={styles.progressBar}>
                  <div 
                    className={styles.progressFill}
                    style={{ width: `${chapter.completion}%` }}
                  />
                </div>
                <span className={styles.progressPercent}>{Math.round(chapter.completion)}%</span>
              </div>
              {!currentSession.currentChapter && (
                <button 
                  onClick={() => startSession(chapter.id)}
                  className={styles.startButton}
                >
                  学習開始
                </button>
              )}
            </div>
            
            <div className={styles.lessonsList}>
              {chapter.lessons.map(lesson => (
                <div 
                  key={lesson.id} 
                  className={`${styles.lessonItem} ${
                    completedItems.has(lesson.id) ? styles.completed : ''
                  }`}
                >
                  <div className={styles.lessonIcon}>
                    {getLessonIcon(lesson.type)}
                  </div>
                  <div className={styles.lessonInfo}>
                    <span className={styles.lessonTitle}>{lesson.title}</span>
                    <span className={styles.lessonTime}>{formatTime(lesson.estimatedTime)}</span>
                  </div>
                  <div className={styles.lessonStatus}>
                    {completedItems.has(lesson.id) ? (
                      <span className={styles.completedMark}>✓</span>
                    ) : (
                      <button 
                        onClick={() => completeLesson(lesson.id, Math.floor(Math.random() * 30) + 70)}
                        className={styles.completeBtn}
                      >
                        完了
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>

      <div className={styles.actions}>
        <button onClick={generateSampleData} className={styles.sampleBtn}>
          サンプルデータ生成
        </button>
        <button onClick={() => setCompletedItems(new Set())} className={styles.resetBtn}>
          進捗リセット
        </button>
      </div>
    </div>
  );
};

export default LearningProgressTracker;
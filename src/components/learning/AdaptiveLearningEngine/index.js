import React, { useState, useEffect, useCallback } from 'react';
import styles from './styles.module.css';

const AdaptiveLearningEngine = ({ 
  userId = 'default',
  courseId = 'embedded-basics',
  title = "適応学習エンジン",
  subjects = [],
  onRecommendationUpdate = null
}) => {
  const [learnerProfile, setLearnerProfile] = useState({
    learningStyle: 'visual', // visual, auditory, kinesthetic, reading
    proficiencyLevel: 'beginner', // beginner, intermediate, advanced
    interests: [],
    strengths: [],
    weaknesses: [],
    preferences: {
      pace: 'normal', // slow, normal, fast
      difficulty: 'gradual', // gentle, gradual, challenging
      contentType: 'mixed' // text, video, interactive, mixed
    }
  });

  const [learningHistory, setLearningHistory] = useState([]);
  const [currentRecommendations, setCurrentRecommendations] = useState([]);
  const [analyticsData, setAnalyticsData] = useState({
    completionRate: 0,
    averageScore: 0,
    timeSpent: 0,
    strugglingTopics: [],
    strongTopics: []
  });

  const [isAnalyzing, setIsAnalyzing] = useState(false);

  // デフォルト科目データ
  const defaultSubjects = [
    {
      id: 'binary-logic',
      name: '2進数・論理演算',
      difficulty: 'beginner',
      prerequisites: [],
      estimatedTime: 120, // 分
      topics: ['2進数変換', '論理ゲート', 'ビット演算']
    },
    {
      id: 'c-programming',
      name: 'C言語プログラミング',
      difficulty: 'beginner',
      prerequisites: ['binary-logic'],
      estimatedTime: 180,
      topics: ['変数・データ型', '制御文', '関数']
    },
    {
      id: 'pointers',
      name: 'ポインタと メモリ',
      difficulty: 'intermediate',
      prerequisites: ['c-programming'],
      estimatedTime: 150,
      topics: ['ポインタ基礎', 'メモリ管理', 'アドレス計算']
    },
    {
      id: 'embedded-basics',
      name: '組込システム基礎',
      difficulty: 'intermediate',
      prerequisites: ['pointers'],
      estimatedTime: 200,
      topics: ['マイコン構成', 'レジスタ操作', '割り込み']
    },
    {
      id: 'rtos',
      name: 'リアルタイムOS',
      difficulty: 'advanced',
      prerequisites: ['embedded-basics'],
      estimatedTime: 240,
      topics: ['タスク管理', 'スケジューリング', '同期・排他']
    }
  ];

  const activeSubjects = subjects.length > 0 ? subjects : defaultSubjects;

  // 学習履歴の分析
  const analyzeLearningData = useCallback(() => {
    if (learningHistory.length === 0) return;

    setIsAnalyzing(true);

    // 完了率の計算
    const completedItems = learningHistory.filter(item => item.completed);
    const completionRate = (completedItems.length / learningHistory.length) * 100;

    // 平均スコアの計算
    const scoredItems = learningHistory.filter(item => item.score !== undefined);
    const averageScore = scoredItems.length > 0 
      ? scoredItems.reduce((sum, item) => sum + item.score, 0) / scoredItems.length
      : 0;

    // 学習時間の計算
    const totalTime = learningHistory.reduce((sum, item) => sum + (item.timeSpent || 0), 0);

    // 苦手・得意トピックの特定
    const topicScores = {};
    learningHistory.forEach(item => {
      if (item.topic && item.score !== undefined) {
        if (!topicScores[item.topic]) {
          topicScores[item.topic] = { scores: [], count: 0 };
        }
        topicScores[item.topic].scores.push(item.score);
        topicScores[item.topic].count++;
      }
    });

    const topicAverages = Object.entries(topicScores).map(([topic, data]) => ({
      topic,
      average: data.scores.reduce((sum, score) => sum + score, 0) / data.count,
      count: data.count
    }));

    const strugglingTopics = topicAverages
      .filter(item => item.average < 70 && item.count >= 2)
      .sort((a, b) => a.average - b.average)
      .slice(0, 3);

    const strongTopics = topicAverages
      .filter(item => item.average >= 85 && item.count >= 2)
      .sort((a, b) => b.average - a.average)
      .slice(0, 3);

    setAnalyticsData({
      completionRate: Math.round(completionRate),
      averageScore: Math.round(averageScore),
      timeSpent: Math.round(totalTime),
      strugglingTopics,
      strongTopics
    });

    setIsAnalyzing(false);
  }, [learningHistory]);

  // 推奨コンテンツの生成
  const generateRecommendations = useCallback(() => {
    const recommendations = [];

    // 苦手分野の補強
    analyticsData.strugglingTopics.forEach(topic => {
      recommendations.push({
        type: 'remedial',
        priority: 'high',
        title: `${topic.topic}の復習`,
        description: `平均スコア${topic.average}%のため、基礎から復習しましょう`,
        estimatedTime: 60,
        contentType: learnerProfile.preferences.contentType
      });
    });

    // 学習スタイルに基づく推奨
    if (learnerProfile.learningStyle === 'visual') {
      recommendations.push({
        type: 'style-match',
        priority: 'medium',
        title: 'ビジュアル学習コンテンツ',
        description: '図表やシミュレーションを使った視覚的学習',
        estimatedTime: 90,
        contentType: 'interactive'
      });
    }

    // 次のステップの提案
    const nextSubject = activeSubjects.find(subject => {
      const prereqsMet = subject.prerequisites.every(prereq =>
        learningHistory.some(item => item.subjectId === prereq && item.completed)
      );
      const notStarted = !learningHistory.some(item => item.subjectId === subject.id);
      return prereqsMet && notStarted;
    });

    if (nextSubject) {
      recommendations.push({
        type: 'progression',
        priority: 'high',
        title: `次の学習: ${nextSubject.name}`,
        description: `前提条件を満たしています。挑戦してみましょう`,
        estimatedTime: nextSubject.estimatedTime,
        contentType: 'mixed'
      });
    }

    setCurrentRecommendations(recommendations);

    if (onRecommendationUpdate) {
      onRecommendationUpdate(recommendations);
    }
  }, [analyticsData, learnerProfile, activeSubjects, learningHistory, onRecommendationUpdate]);

  // 学習履歴のシミュレーション（デモ用）
  const simulateLearningData = () => {
    const sampleHistory = [
      { subjectId: 'binary-logic', topic: '2進数変換', score: 85, timeSpent: 45, completed: true },
      { subjectId: 'binary-logic', topic: '論理ゲート', score: 92, timeSpent: 60, completed: true },
      { subjectId: 'binary-logic', topic: 'ビット演算', score: 78, timeSpent: 40, completed: true },
      { subjectId: 'c-programming', topic: '変数・データ型', score: 88, timeSpent: 55, completed: true },
      { subjectId: 'c-programming', topic: '制御文', score: 65, timeSpent: 80, completed: true },
      { subjectId: 'c-programming', topic: '関数', score: 72, timeSpent: 70, completed: false },
      { subjectId: 'pointers', topic: 'ポインタ基礎', score: 45, timeSpent: 120, completed: false },
    ];

    setLearningHistory(sampleHistory);
  };

  // プロファイル更新
  const updateLearnerProfile = (updates) => {
    setLearnerProfile(prev => ({
      ...prev,
      ...updates
    }));
  };

  useEffect(() => {
    analyzeLearningData();
  }, [learningHistory, analyzeLearningData]);

  useEffect(() => {
    generateRecommendations();
  }, [analyticsData, generateRecommendations]);

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h3>{title}</h3>
        <p>個人の学習パターンを分析し、最適な学習体験を提供します</p>
      </div>

      <div className={styles.dashboard}>
        <div className={styles.profileCard}>
          <h4>学習者プロファイル</h4>
          <div className={styles.profileItems}>
            <div className={styles.profileItem}>
              <label>学習スタイル:</label>
              <select 
                value={learnerProfile.learningStyle}
                onChange={(e) => updateLearnerProfile({ learningStyle: e.target.value })}
              >
                <option value="visual">視覚型</option>
                <option value="auditory">聴覚型</option>
                <option value="kinesthetic">体験型</option>
                <option value="reading">読書型</option>
              </select>
            </div>
            <div className={styles.profileItem}>
              <label>習熟度:</label>
              <select 
                value={learnerProfile.proficiencyLevel}
                onChange={(e) => updateLearnerProfile({ proficiencyLevel: e.target.value })}
              >
                <option value="beginner">初級</option>
                <option value="intermediate">中級</option>
                <option value="advanced">上級</option>
              </select>
            </div>
            <div className={styles.profileItem}>
              <label>学習ペース:</label>
              <select 
                value={learnerProfile.preferences.pace}
                onChange={(e) => updateLearnerProfile({ 
                  preferences: { ...learnerProfile.preferences, pace: e.target.value }
                })}
              >
                <option value="slow">ゆっくり</option>
                <option value="normal">標準</option>
                <option value="fast">速い</option>
              </select>
            </div>
          </div>
        </div>

        <div className={styles.analyticsCard}>
          <h4>学習分析</h4>
          {isAnalyzing ? (
            <div className={styles.loading}>分析中...</div>
          ) : (
            <div className={styles.analyticsGrid}>
              <div className={styles.metric}>
                <div className={styles.metricValue}>{analyticsData.completionRate}%</div>
                <div className={styles.metricLabel}>完了率</div>
              </div>
              <div className={styles.metric}>
                <div className={styles.metricValue}>{analyticsData.averageScore}%</div>
                <div className={styles.metricLabel}>平均スコア</div>
              </div>
              <div className={styles.metric}>
                <div className={styles.metricValue}>{Math.round(analyticsData.timeSpent / 60)}h</div>
                <div className={styles.metricLabel}>学習時間</div>
              </div>
              <div className={styles.metric}>
                <div className={styles.metricValue}>{analyticsData.strugglingTopics.length}</div>
                <div className={styles.metricLabel}>要注意分野</div>
              </div>
            </div>
          )}
        </div>

        <div className={styles.recommendationsCard}>
          <h4>推奨学習内容</h4>
          {currentRecommendations.length === 0 ? (
            <p className={styles.noRecommendations}>
              学習データを分析して推奨内容を生成します
            </p>
          ) : (
            <div className={styles.recommendationsList}>
              {currentRecommendations.map((rec, index) => (
                <div key={index} className={`${styles.recommendationItem} ${styles[rec.priority]}`}>
                  <div className={styles.recHeader}>
                    <h5>{rec.title}</h5>
                    <span className={styles.priority}>{rec.priority === 'high' ? '高' : '中'}</span>
                  </div>
                  <p>{rec.description}</p>
                  <div className={styles.recMeta}>
                    <span>⏱ 約{rec.estimatedTime}分</span>
                    <span>📚 {rec.contentType}</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      <div className={styles.detailsSection}>
        <div className={styles.strugglingTopics}>
          <h4>要注意分野</h4>
          {analyticsData.strugglingTopics.length === 0 ? (
            <p>現在、特に苦手な分野はありません</p>
          ) : (
            <ul>
              {analyticsData.strugglingTopics.map((topic, index) => (
                <li key={index}>
                  <strong>{topic.topic}</strong>: 平均{topic.average.toFixed(1)}%
                </li>
              ))}
            </ul>
          )}
        </div>

        <div className={styles.strongTopics}>
          <h4>得意分野</h4>
          {analyticsData.strongTopics.length === 0 ? (
            <p>まだ得意分野が特定されていません</p>
          ) : (
            <ul>
              {analyticsData.strongTopics.map((topic, index) => (
                <li key={index}>
                  <strong>{topic.topic}</strong>: 平均{topic.average.toFixed(1)}%
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>

      <div className={styles.actions}>
        <button onClick={simulateLearningData} className={styles.demoButton}>
          サンプルデータで体験
        </button>
        <button onClick={analyzeLearningData} className={styles.analyzeButton}>
          分析を再実行
        </button>
      </div>
    </div>
  );
};

export default AdaptiveLearningEngine;
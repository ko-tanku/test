import React, { useState, useEffect } from 'react';
import styles from './styles.module.css';

const AIPromptTrainer = ({ 
  scenarios = [],
  title = "AI活用プロンプト練習",
  description = "効果的なAI活用のためのプロンプト設計を学びます"
}) => {
  const [currentScenario, setCurrentScenario] = useState(0);
  const [userPrompt, setUserPrompt] = useState('');
  const [feedback, setFeedback] = useState('');
  const [showHint, setShowHint] = useState(false);
  const [completedScenarios, setCompletedScenarios] = useState(new Set());

  // デフォルトシナリオデータ
  const defaultScenarios = [
    {
      id: 1,
      title: "C言語のポインタ学習",
      situation: "C言語のポインタの概念を理解したい初学者です",
      goal: "ポインタの基本概念を分かりやすく説明してもらう",
      goodPrompt: "C言語初学者です。ポインタの概念を、具体的なメモリアドレスの例を使って、段階的に説明してください。まず変数とメモリの関係から始めて、ポインタの宣言、初期化、使い方まで教えてください。",
      badPrompt: "ポインタって何？",
      hints: [
        "具体的な学習レベルを明示する",
        "段階的な説明を求める",
        "具体例を要求する",
        "学習の目的を明確にする"
      ],
      evaluation: {
        specificity: "学習者のレベルと具体的な要求が明確か",
        structure: "段階的な学習要求になっているか",
        examples: "具体例を求めているか",
        clarity: "何を学びたいかが明確か"
      }
    },
    {
      id: 2,
      title: "組込制御システム設計",
      situation: "マイコンを使った温度制御システムの設計方法を学びたい",
      goal: "システム設計の考え方と具体的な実装方針を得る",
      goodPrompt: "マイコンを使った温度制御システムを設計したいです。センサーからの温度読み取り、PID制御アルゴリズム、ヒーター制御までの一連の流れを、ハードウェア選定から制御ソフトウェアの構造まで段階的に教えてください。特に実用的な実装のポイントも含めてお願いします。",
      badPrompt: "温度制御システムの作り方教えて",
      hints: [
        "システム全体の構成を明示する",
        "技術的な詳細レベルを指定する",
        "実装の観点を含める",
        "段階的な説明を求める"
      ],
      evaluation: {
        scope: "システム全体の範囲が明確か",
        technical: "技術的詳細の要求が適切か",
        practical: "実装面への言及があるか",
        structure: "論理的な構成で質問しているか"
      }
    },
    {
      id: 3,
      title: "デバッグ支援",
      situation: "C言語プログラムでセグメンテーション違反が発生している",
      goal: "問題の原因を特定し、解決策を得る",
      goodPrompt: "以下のC言語コードでセグメンテーション違反が発生します。コードを添付しますので、可能性の高い原因を分析し、修正方法を提案してください。また、今後同様の問題を防ぐためのコーディング上の注意点も教えてください。\n\n[コードを添付]",
      badPrompt: "エラーが出る",
      hints: [
        "具体的なエラー内容を明示する",
        "問題のコードを添付する",
        "原因分析を求める",
        "予防策も聞く"
      ],
      evaluation: {
        detail: "エラーの詳細が具体的か",
        context: "必要な情報が含まれているか",
        solution: "解決策を明確に求めているか",
        prevention: "今後の改善につながる質問か"
      }
    }
  ];

  const activeScenarios = scenarios.length > 0 ? scenarios : defaultScenarios;
  const current = activeScenarios[currentScenario];

  const evaluatePrompt = () => {
    if (!userPrompt.trim()) {
      setFeedback('プロンプトを入力してください。');
      return;
    }

    let score = 0;
    let feedbackText = 'あなたのプロンプトの評価:\n\n';
    
    // 長さの評価
    if (userPrompt.length > 50) score += 25;
    if (userPrompt.length < 20) {
      feedbackText += '❌ プロンプトが短すぎます。より具体的に書いてみましょう。\n';
    } else {
      feedbackText += '✅ 適切な長さです。\n';
    }

    // キーワードの存在確認
    const keywords = ['具体的', '段階的', '例', 'レベル', '初学者', '詳しく'];
    const hasKeywords = keywords.some(keyword => userPrompt.includes(keyword));
    if (hasKeywords) {
      score += 25;
      feedbackText += '✅ 具体性を示すキーワードが含まれています。\n';
    } else {
      feedbackText += '❌ より具体的な表現を使ってみましょう。\n';
    }

    // 質問の構造
    if (userPrompt.includes('？') || userPrompt.includes('?')) {
      score += 25;
      feedbackText += '✅ 明確な質問形式になっています。\n';
    } else {
      feedbackText += '❌ 明確な質問として表現してみましょう。\n';
    }

    // 文脈の提供
    if (userPrompt.includes('初学者') || userPrompt.includes('学習') || userPrompt.includes('理解')) {
      score += 25;
      feedbackText += '✅ 学習レベルや目的が明示されています。\n';
    } else {
      feedbackText += '❌ あなたのレベルや目的を明示してみましょう。\n';
    }

    feedbackText += `\nスコア: ${score}/100点\n\n`;

    if (score >= 75) {
      feedbackText += '🎉 優秀なプロンプトです！';
      setCompletedScenarios(prev => new Set([...prev, current.id]));
    } else if (score >= 50) {
      feedbackText += '👍 良いプロンプトです。さらに改善の余地があります。';
    } else {
      feedbackText += '📝 改善の余地があります。ヒントを参考にしてください。';
    }

    setFeedback(feedbackText);
  };

  const nextScenario = () => {
    if (currentScenario < activeScenarios.length - 1) {
      setCurrentScenario(currentScenario + 1);
      setUserPrompt('');
      setFeedback('');
      setShowHint(false);
    }
  };

  const prevScenario = () => {
    if (currentScenario > 0) {
      setCurrentScenario(currentScenario - 1);
      setUserPrompt('');
      setFeedback('');
      setShowHint(false);
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h3>{title}</h3>
        <p>{description}</p>
      </div>

      <div className={styles.progress}>
        <div className={styles.progressBar}>
          <div 
            className={styles.progressFill}
            style={{ width: `${((currentScenario + 1) / activeScenarios.length) * 100}%` }}
          />
        </div>
        <span>{currentScenario + 1} / {activeScenarios.length}</span>
      </div>

      <div className={styles.scenario}>
        <h4>シナリオ {currentScenario + 1}: {current.title}</h4>
        <div className={styles.situation}>
          <strong>状況:</strong> {current.situation}
        </div>
        <div className={styles.goal}>
          <strong>目標:</strong> {current.goal}
        </div>
      </div>

      <div className={styles.promptInput}>
        <label>あなたのプロンプトを入力してください:</label>
        <textarea
          value={userPrompt}
          onChange={(e) => setUserPrompt(e.target.value)}
          placeholder="効果的なプロンプトを作成してみましょう..."
          rows={6}
        />
        <div className={styles.actions}>
          <button onClick={evaluatePrompt} className={styles.evaluateBtn}>
            プロンプトを評価
          </button>
          <button onClick={() => setShowHint(!showHint)} className={styles.hintBtn}>
            {showHint ? 'ヒントを隠す' : 'ヒントを表示'}
          </button>
        </div>
      </div>

      {showHint && (
        <div className={styles.hints}>
          <h5>💡 ヒント:</h5>
          <ul>
            {current.hints.map((hint, index) => (
              <li key={index}>{hint}</li>
            ))}
          </ul>
        </div>
      )}

      {feedback && (
        <div className={styles.feedback}>
          <h5>📊 評価結果:</h5>
          <pre>{feedback}</pre>
        </div>
      )}

      <div className={styles.examples}>
        <div className={styles.exampleGood}>
          <h5>✅ 良いプロンプトの例:</h5>
          <p>{current.goodPrompt}</p>
        </div>
        <div className={styles.exampleBad}>
          <h5>❌ 改善が必要なプロンプト:</h5>
          <p>{current.badPrompt}</p>
        </div>
      </div>

      <div className={styles.navigation}>
        <button 
          onClick={prevScenario} 
          disabled={currentScenario === 0}
          className={styles.navBtn}
        >
          前のシナリオ
        </button>
        <span className={styles.completionInfo}>
          完了: {completedScenarios.size} / {activeScenarios.length}
        </span>
        <button 
          onClick={nextScenario} 
          disabled={currentScenario === activeScenarios.length - 1}
          className={styles.navBtn}
        >
          次のシナリオ
        </button>
      </div>
    </div>
  );
};

export default AIPromptTrainer;
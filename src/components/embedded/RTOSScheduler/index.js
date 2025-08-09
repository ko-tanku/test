import React, { useState, useEffect } from 'react';
import styles from './styles.module.css';

const RTOSScheduler = ({
  title = "RTOS スケジューラシミュレーター",
  schedulingPolicy = "preemptive-priority",
  timeSlice = 100,
  showGanttChart = true,
  interactive = true
}) => {
  const [tasks, setTasks] = useState([]);
  const [currentTime, setCurrentTime] = useState(0);
  const [isRunning, setIsRunning] = useState(false);
  const [executionHistory, setExecutionHistory] = useState([]);
  const [selectedTask, setSelectedTask] = useState(null);
  const [schedulerStats, setSchedulerStats] = useState({
    totalTasks: 0,
    completedTasks: 0,
    averageWaitTime: 0,
    cpuUtilization: 0
  });

  // デフォルトタスクセット
  const defaultTasks = [
    {
      id: 1,
      name: 'LED制御',
      priority: 3,
      period: 200,
      executionTime: 20,
      deadline: 200,
      color: '#ff6b6b',
      description: 'LEDの点滅制御タスク',
      state: 'ready', // ready, running, blocked, completed
      arrivalTime: 0,
      remainingTime: 20,
      waitTime: 0,
      lastExecutionStart: null
    },
    {
      id: 2,
      name: 'センサ読取',
      priority: 1,
      period: 50,
      executionTime: 15,
      deadline: 50,
      color: '#4ecdc4',
      description: 'センサデータ読み取りタスク',
      state: 'ready',
      arrivalTime: 0,
      remainingTime: 15,
      waitTime: 0,
      lastExecutionStart: null
    },
    {
      id: 3,
      name: '通信処理',
      priority: 2,
      period: 300,
      executionTime: 40,
      deadline: 300,
      color: '#45b7d1',
      description: 'データ通信処理タスク',
      state: 'ready',
      arrivalTime: 0,
      remainingTime: 40,
      waitTime: 0,
      lastExecutionStart: null
    },
    {
      id: 4,
      name: 'ログ記録',
      priority: 4,
      period: 500,
      executionTime: 10,
      deadline: 500,
      color: '#f9ca24',
      description: 'ログファイル出力タスク',
      state: 'ready',
      arrivalTime: 0,
      remainingTime: 10,
      waitTime: 0,
      lastExecutionStart: null
    }
  ];

  // スケジューリングアルゴリズム
  const schedulingPolicies = {
    'preemptive-priority': {
      name: 'プリエンプティブ優先度',
      description: '優先度の高いタスクが割り込み実行',
      select: (readyTasks) => {
        return readyTasks.reduce((highest, task) => 
          !highest || task.priority < highest.priority ? task : highest
        , null);
      }
    },
    'round-robin': {
      name: 'ラウンドロビン',
      description: 'タスクを順番に一定時間ずつ実行',
      select: (readyTasks, lastTask) => {
        if (!lastTask) return readyTasks[0];
        const lastIndex = readyTasks.findIndex(t => t.id === lastTask.id);
        return readyTasks[(lastIndex + 1) % readyTasks.length] || readyTasks[0];
      }
    },
    'shortest-job-first': {
      name: '最短実行時間優先',
      description: '残り実行時間が短いタスクを優先',
      select: (readyTasks) => {
        return readyTasks.reduce((shortest, task) => 
          !shortest || task.remainingTime < shortest.remainingTime ? task : shortest
        , null);
      }
    },
    'earliest-deadline-first': {
      name: 'EDF (最早締切優先)',
      description: '締切が最も近いタスクを優先',
      select: (readyTasks, currentTime) => {
        return readyTasks.reduce((earliest, task) => {
          const taskDeadline = Math.floor(currentTime / task.period + 1) * task.period;
          const earliestDeadline = earliest ? Math.floor(currentTime / earliest.period + 1) * earliest.period : Infinity;
          return taskDeadline < earliestDeadline ? task : earliest;
        }, null);
      }
    }
  };

  const currentPolicy = schedulingPolicies[schedulingPolicy];

  // タスクの初期化
  useEffect(() => {
    setTasks(defaultTasks.map(task => ({ ...task })));
  }, []);

  // スケジューラの実行
  const runScheduler = () => {
    setTasks(prevTasks => {
      const updatedTasks = [...prevTasks];
      
      // 新しいタスクインスタンスの生成チェック
      updatedTasks.forEach(task => {
        if (currentTime > 0 && currentTime % task.period === 0) {
          if (task.remainingTime > 0) {
            // デッドラインミス
            console.log(`Deadline miss: ${task.name} at time ${currentTime}`);
          }
          task.remainingTime = task.executionTime;
          task.state = 'ready';
          task.arrivalTime = currentTime;
        }
      });

      // 実行可能タスクの選択
      const readyTasks = updatedTasks.filter(task => 
        task.state === 'ready' && task.remainingTime > 0
      );

      const currentRunningTask = updatedTasks.find(task => task.state === 'running');
      
      let selectedTask = null;
      if (readyTasks.length > 0) {
        selectedTask = currentPolicy.select(readyTasks, currentRunningTask, currentTime);
      }

      // タスク状態の更新
      updatedTasks.forEach(task => {
        if (task.state === 'running' && task.id !== selectedTask?.id) {
          task.state = 'ready';
          if (task.lastExecutionStart !== null) {
            task.waitTime += currentTime - task.lastExecutionStart;
          }
        }
        
        if (task.id === selectedTask?.id) {
          if (task.state !== 'running') {
            task.lastExecutionStart = currentTime;
          }
          task.state = 'running';
          task.remainingTime = Math.max(0, task.remainingTime - 1);
          
          if (task.remainingTime === 0) {
            task.state = 'completed';
          }
        } else if (task.state === 'ready') {
          task.waitTime += 1;
        }
      });

      // 実行履歴の記録
      setExecutionHistory(prev => [...prev, {
        time: currentTime,
        runningTask: selectedTask ? {
          id: selectedTask.id,
          name: selectedTask.name,
          color: selectedTask.color
        } : null
      }]);

      return updatedTasks;
    });
  };

  // シミュレーション制御
  useEffect(() => {
    let interval;
    if (isRunning) {
      interval = setInterval(() => {
        setCurrentTime(prev => {
          const newTime = prev + 1;
          return newTime;
        });
      }, 100);
    }
    return () => clearInterval(interval);
  }, [isRunning]);

  useEffect(() => {
    if (isRunning) {
      runScheduler();
    }
  }, [currentTime]);

  // 統計の計算
  useEffect(() => {
    const totalTasks = tasks.length;
    const completedTasks = tasks.filter(task => task.state === 'completed').length;
    const totalWaitTime = tasks.reduce((sum, task) => sum + task.waitTime, 0);
    const averageWaitTime = totalTasks > 0 ? totalWaitTime / totalTasks : 0;
    
    const executingTime = executionHistory.filter(entry => entry.runningTask).length;
    const cpuUtilization = currentTime > 0 ? (executingTime / currentTime) * 100 : 0;

    setSchedulerStats({
      totalTasks,
      completedTasks,
      averageWaitTime: Math.round(averageWaitTime),
      cpuUtilization: Math.round(cpuUtilization)
    });
  }, [tasks, executionHistory]);

  const toggleSimulation = () => {
    setIsRunning(!isRunning);
  };

  const resetSimulation = () => {
    setIsRunning(false);
    setCurrentTime(0);
    setExecutionHistory([]);
    setTasks(defaultTasks.map(task => ({ ...task })));
    setSelectedTask(null);
  };

  const addCustomTask = () => {
    const newTask = {
      id: Date.now(),
      name: `カスタム${tasks.length + 1}`,
      priority: 2,
      period: 100,
      executionTime: 10,
      deadline: 100,
      color: `hsl(${Math.random() * 360}, 70%, 60%)`,
      description: 'ユーザー定義タスク',
      state: 'ready',
      arrivalTime: currentTime,
      remainingTime: 10,
      waitTime: 0,
      lastExecutionStart: null
    };
    setTasks(prev => [...prev, newTask]);
  };

  const updateTaskProperty = (taskId, property, value) => {
    setTasks(prev => prev.map(task => 
      task.id === taskId 
        ? { ...task, [property]: parseInt(value) || value }
        : task
    ));
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h3>{title}</h3>
        <p>リアルタイムOSのタスクスケジューリングを可視化</p>
      </div>

      <div className={styles.controlPanel}>
        <div className={styles.schedulerInfo}>
          <h4>スケジューリング方式</h4>
          <div className={styles.policyInfo}>
            <strong>{currentPolicy.name}</strong>
            <p>{currentPolicy.description}</p>
          </div>
        </div>

        <div className={styles.simulationControls}>
          <div className={styles.timeDisplay}>
            <span>現在時刻: {currentTime} ms</span>
          </div>
          <div className={styles.controls}>
            <button onClick={toggleSimulation} className={styles.playButton}>
              {isRunning ? '⏸ 停止' : '▶ 開始'}
            </button>
            <button onClick={resetSimulation} className={styles.resetButton}>
              🔄 リセット
            </button>
            {interactive && (
              <button onClick={addCustomTask} className={styles.addButton}>
                ➕ タスク追加
              </button>
            )}
          </div>
        </div>

        <div className={styles.statsPanel}>
          <h4>統計情報</h4>
          <div className={styles.statsGrid}>
            <div className={styles.statItem}>
              <span className={styles.statValue}>{schedulerStats.totalTasks}</span>
              <span className={styles.statLabel}>総タスク数</span>
            </div>
            <div className={styles.statItem}>
              <span className={styles.statValue}>{schedulerStats.completedTasks}</span>
              <span className={styles.statLabel}>完了タスク</span>
            </div>
            <div className={styles.statItem}>
              <span className={styles.statValue}>{schedulerStats.averageWaitTime}ms</span>
              <span className={styles.statLabel}>平均待機時間</span>
            </div>
            <div className={styles.statItem}>
              <span className={styles.statValue}>{schedulerStats.cpuUtilization}%</span>
              <span className={styles.statLabel}>CPU使用率</span>
            </div>
          </div>
        </div>
      </div>

      <div className={styles.mainContent}>
        <div className={styles.taskList}>
          <h4>タスク一覧</h4>
          <div className={styles.taskItems}>
            {tasks.map(task => (
              <div 
                key={task.id}
                className={`${styles.taskItem} ${styles[task.state]}`}
                onClick={() => setSelectedTask(task)}
              >
                <div className={styles.taskHeader}>
                  <div 
                    className={styles.taskColor}
                    style={{ backgroundColor: task.color }}
                  />
                  <span className={styles.taskName}>{task.name}</span>
                  <span className={styles.taskState}>{task.state}</span>
                </div>
                <div className={styles.taskDetails}>
                  <span>優先度: {task.priority}</span>
                  <span>周期: {task.period}ms</span>
                  <span>実行時間: {task.executionTime}ms</span>
                  <span>残り: {task.remainingTime}ms</span>
                </div>
                {task.state === 'running' && (
                  <div className={styles.runningIndicator}>実行中</div>
                )}
              </div>
            ))}
          </div>
        </div>

        {showGanttChart && (
          <div className={styles.ganttChart}>
            <h4>実行履歴 (ガントチャート)</h4>
            <div className={styles.timeAxis}>
              {Array.from({ length: Math.min(currentTime + 1, 100) }, (_, i) => (
                <div key={i} className={styles.timeMarker}>
                  {i % 10 === 0 ? i : ''}
                </div>
              ))}
            </div>
            <div className={styles.executionBars}>
              {executionHistory.slice(-100).map((entry, index) => (
                <div 
                  key={index}
                  className={styles.executionBar}
                  style={{ 
                    backgroundColor: entry.runningTask ? entry.runningTask.color : '#f8f9fa',
                    border: entry.runningTask ? 'none' : '1px solid #dee2e6'
                  }}
                  title={entry.runningTask ? entry.runningTask.name : 'アイドル'}
                />
              ))}
            </div>
          </div>
        )}
      </div>

      {selectedTask && (
        <div className={styles.taskDetailModal}>
          <div className={styles.modalContent}>
            <div className={styles.modalHeader}>
              <h4>タスク詳細: {selectedTask.name}</h4>
              <button onClick={() => setSelectedTask(null)}>✕</button>
            </div>
            <div className={styles.modalBody}>
              <div className={styles.taskProperty}>
                <label>名前:</label>
                <input 
                  type="text" 
                  value={selectedTask.name}
                  onChange={(e) => updateTaskProperty(selectedTask.id, 'name', e.target.value)}
                />
              </div>
              <div className={styles.taskProperty}>
                <label>優先度:</label>
                <input 
                  type="number" 
                  value={selectedTask.priority}
                  onChange={(e) => updateTaskProperty(selectedTask.id, 'priority', e.target.value)}
                />
              </div>
              <div className={styles.taskProperty}>
                <label>周期 (ms):</label>
                <input 
                  type="number" 
                  value={selectedTask.period}
                  onChange={(e) => updateTaskProperty(selectedTask.id, 'period', e.target.value)}
                />
              </div>
              <div className={styles.taskProperty}>
                <label>実行時間 (ms):</label>
                <input 
                  type="number" 
                  value={selectedTask.executionTime}
                  onChange={(e) => updateTaskProperty(selectedTask.id, 'executionTime', e.target.value)}
                />
              </div>
              <div className={styles.taskInfo}>
                <p><strong>説明:</strong> {selectedTask.description}</p>
                <p><strong>状態:</strong> {selectedTask.state}</p>
                <p><strong>残り実行時間:</strong> {selectedTask.remainingTime}ms</p>
                <p><strong>待機時間:</strong> {selectedTask.waitTime}ms</p>
              </div>
            </div>
          </div>
        </div>
      )}

      <div className={styles.explanationPanel}>
        <h4>スケジューリング方式の比較</h4>
        <div className={styles.policyComparison}>
          <div className={styles.policyItem}>
            <h5>プリエンプティブ優先度</h5>
            <p>優先度の高いタスクがいつでも割り込み可能。リアルタイム性重視。</p>
          </div>
          <div className={styles.policyItem}>
            <h5>ラウンドロビン</h5>
            <p>各タスクに均等な実行時間を割り当て。公平性重視。</p>
          </div>
          <div className={styles.policyItem}>
            <h5>最短実行時間優先</h5>
            <p>短いタスクを優先実行。平均応答時間を最小化。</p>
          </div>
          <div className={styles.policyItem}>
            <h5>EDF</h5>
            <p>締切が近いタスクを優先。CPU使用率を最大化可能。</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RTOSScheduler;
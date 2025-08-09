import React, { useState, useEffect } from 'react';
import styles from './styles.module.css';

const StackHeapSimulator = ({
  title = "スタック・ヒープシミュレータ",
  showCode = true,
  interactive = true,
  maxMemorySize = 1024, // KB
  stackStartAddr = 0x2001FFFF,
  heapStartAddr = 0x20010000
}) => {
  const [memoryState, setMemoryState] = useState({
    stack: [],
    heap: [],
    staticVars: []
  });
  
  const [currentStep, setCurrentStep] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [selectedAddress, setSelectedAddress] = useState(null);
  const [codeExample, setCodeExample] = useState('');

  // シミュレーション用のプログラムステップ
  const programSteps = [
    {
      step: 0,
      code: "int main() {",
      description: "main関数開始 - スタックフレーム作成",
      action: "stack_frame",
      data: { function: "main", size: 16, vars: [] }
    },
    {
      step: 1,
      code: "    int x = 10;",
      description: "ローカル変数xをスタックに配置",
      action: "stack_push",
      data: { name: "x", value: 10, type: "int", size: 4 }
    },
    {
      step: 2,
      code: "    int arr[100];",
      description: "配列arrをスタックに配置",
      action: "stack_push",
      data: { name: "arr[100]", value: "array", type: "int[]", size: 400 }
    },
    {
      step: 3,
      code: "    int* ptr = malloc(sizeof(int) * 50);",
      description: "ヒープから200バイト動的確保",
      action: "heap_alloc",
      data: { name: "ptr", size: 200, address: null }
    },
    {
      step: 4,
      code: "    for(int i = 0; i < 50; i++) {",
      description: "ループ変数iをスタックに配置",
      action: "stack_push",
      data: { name: "i", value: 0, type: "int", size: 4 }
    },
    {
      step: 5,
      code: "        ptr[i] = i * 2;",
      description: "ヒープ領域に値を書き込み",
      action: "heap_write",
      data: { address: null, values: "0,2,4,6,8..." }
    },
    {
      step: 6,
      code: "    }",
      description: "ループ終了 - 変数iをスタックから削除",
      action: "stack_pop",
      data: { name: "i" }
    },
    {
      step: 7,
      code: "    free(ptr);",
      description: "ヒープメモリを解放",
      action: "heap_free",
      data: { name: "ptr" }
    },
    {
      step: 8,
      code: "    return 0;",
      description: "main関数終了 - すべてのローカル変数を削除",
      action: "stack_clear",
      data: {}
    }
  ];

  const [simulationSteps, setSimulationSteps] = useState(programSteps);

  // メモリアドレスの計算
  const calculateStackAddress = (offset) => {
    return stackStartAddr - offset;
  };

  const calculateHeapAddress = (offset) => {
    return heapStartAddr + offset;
  };

  // メモリ操作の実行
  const executeStep = (step) => {
    const { action, data } = simulationSteps[step];
    
    setMemoryState(prevState => {
      const newState = { ...prevState };
      
      switch (action) {
        case 'stack_frame':
          newState.stack.push({
            type: 'frame',
            name: data.function,
            address: calculateStackAddress(newState.stack.length * 4),
            size: data.size,
            color: '#e3f2fd'
          });
          break;
          
        case 'stack_push':
          const stackOffset = newState.stack.reduce((sum, item) => sum + item.size, 0);
          newState.stack.push({
            type: 'variable',
            name: data.name,
            value: data.value,
            dataType: data.type,
            address: calculateStackAddress(stackOffset + data.size),
            size: data.size,
            color: data.type.includes('[]') ? '#fff3e0' : '#f3e5f5'
          });
          break;
          
        case 'heap_alloc':
          const heapOffset = newState.heap.reduce((sum, item) => sum + (item.size || 0), 0);
          const heapAddr = calculateHeapAddress(heapOffset);
          newState.heap.push({
            type: 'allocated',
            name: data.name,
            address: heapAddr,
            size: data.size,
            allocated: true,
            color: '#e8f5e8'
          });
          // スタックにポインタ変数も追加
          const stackOffsetPtr = newState.stack.reduce((sum, item) => sum + item.size, 0);
          newState.stack.push({
            type: 'pointer',
            name: data.name,
            value: `0x${heapAddr.toString(16)}`,
            dataType: 'int*',
            address: calculateStackAddress(stackOffsetPtr + 8),
            size: 8,
            pointsTo: heapAddr,
            color: '#ffebee'
          });
          break;
          
        case 'heap_write':
          // ヒープ領域のデータ更新表示
          newState.heap = newState.heap.map(item => 
            item.type === 'allocated' && item.allocated 
              ? { ...item, data: data.values, color: '#c8e6c9' }
              : item
          );
          break;
          
        case 'stack_pop':
          // 最後に追加された指定の変数を削除
          const indexToRemove = newState.stack.findLastIndex(item => item.name === data.name);
          if (indexToRemove !== -1) {
            newState.stack.splice(indexToRemove, 1);
          }
          break;
          
        case 'heap_free':
          newState.heap = newState.heap.map(item => 
            item.name === data.name 
              ? { ...item, allocated: false, color: '#ffcdd2', data: null }
              : item
          );
          // 対応するポインタも削除
          const ptrIndex = newState.stack.findLastIndex(item => item.name === data.name);
          if (ptrIndex !== -1) {
            newState.stack.splice(ptrIndex, 1);
          }
          break;
          
        case 'stack_clear':
          newState.stack = newState.stack.filter(item => item.type === 'static');
          break;
      }
      
      return newState;
    });
  };

  // ステップ実行
  const nextStep = () => {
    if (currentStep < simulationSteps.length - 1) {
      const nextStepIndex = currentStep + 1;
      executeStep(nextStepIndex);
      setCurrentStep(nextStepIndex);
    }
  };

  const prevStep = () => {
    if (currentStep > 0) {
      // 状態をリセットして現在のステップまで再実行
      setMemoryState({ stack: [], heap: [], staticVars: [] });
      const prevStepIndex = currentStep - 1;
      for (let i = 0; i <= prevStepIndex; i++) {
        executeStep(i);
      }
      setCurrentStep(prevStepIndex);
    }
  };

  const resetSimulation = () => {
    setCurrentStep(0);
    setMemoryState({ stack: [], heap: [], staticVars: [] });
    setIsPlaying(false);
  };

  // 自動実行
  const toggleAutoPlay = () => {
    setIsPlaying(!isPlaying);
  };

  useEffect(() => {
    let interval;
    if (isPlaying && currentStep < simulationSteps.length - 1) {
      interval = setInterval(() => {
        nextStep();
      }, 1500);
    } else if (currentStep >= simulationSteps.length - 1) {
      setIsPlaying(false);
    }
    return () => clearInterval(interval);
  }, [isPlaying, currentStep]);

  const formatAddress = (address) => {
    return `0x${address.toString(16).toUpperCase().padStart(8, '0')}`;
  };

  const getMemoryUsage = () => {
    const stackUsed = memoryState.stack.reduce((sum, item) => sum + item.size, 0);
    const heapUsed = memoryState.heap.reduce((sum, item) => sum + (item.allocated ? item.size : 0), 0);
    return { stack: stackUsed, heap: heapUsed };
  };

  const usage = getMemoryUsage();
  const currentStepData = simulationSteps[currentStep] || {};

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h3>{title}</h3>
        <p>C言語プログラムのメモリ使用をリアルタイムで可視化</p>
      </div>

      <div className={styles.content}>
        <div className={styles.codePanel}>
          <h4>プログラムコード</h4>
          <div className={styles.codeContainer}>
            {simulationSteps.map((step, index) => (
              <div 
                key={index}
                className={`${styles.codeLine} ${
                  index === currentStep ? styles.currentLine : ''
                } ${index < currentStep ? styles.executedLine : ''}`}
              >
                <span className={styles.lineNumber}>{index + 1}</span>
                <code>{step.code}</code>
              </div>
            ))}
          </div>
          
          <div className={styles.stepDescription}>
            <h5>現在のステップ:</h5>
            <p>{currentStepData.description || 'プログラム開始前'}</p>
          </div>

          <div className={styles.controls}>
            <button onClick={prevStep} disabled={currentStep === 0}>
              ◀ 前へ
            </button>
            <button onClick={toggleAutoPlay} className={styles.playButton}>
              {isPlaying ? '⏸ 停止' : '▶ 再生'}
            </button>
            <button onClick={nextStep} disabled={currentStep >= simulationSteps.length - 1}>
              次へ ▶
            </button>
            <button onClick={resetSimulation} className={styles.resetButton}>
              🔄 リセット
            </button>
          </div>
        </div>

        <div className={styles.memoryPanel}>
          <div className={styles.memoryStats}>
            <div className={styles.statItem}>
              <span>スタック使用量:</span>
              <span>{usage.stack}B</span>
            </div>
            <div className={styles.statItem}>
              <span>ヒープ使用量:</span>
              <span>{usage.heap}B</span>
            </div>
          </div>

          <div className={styles.memoryVisualization}>
            <div className={styles.memorySection}>
              <h4>スタック領域 (高アドレス→低アドレス)</h4>
              <div className={styles.stackContainer}>
                {memoryState.stack.length === 0 ? (
                  <div className={styles.emptyMemory}>空</div>
                ) : (
                  memoryState.stack.slice().reverse().map((item, index) => (
                    <div 
                      key={index}
                      className={styles.memoryBlock}
                      style={{ backgroundColor: item.color, height: `${Math.max(item.size / 4, 20)}px` }}
                      onClick={() => setSelectedAddress(item)}
                    >
                      <div className={styles.blockInfo}>
                        <span className={styles.blockName}>{item.name}</span>
                        <span className={styles.blockAddress}>{formatAddress(item.address)}</span>
                        <span className={styles.blockSize}>{item.size}B</span>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>

            <div className={styles.memorySection}>
              <h4>ヒープ領域 (低アドレス→高アドレス)</h4>
              <div className={styles.heapContainer}>
                {memoryState.heap.length === 0 ? (
                  <div className={styles.emptyMemory}>空</div>
                ) : (
                  memoryState.heap.map((item, index) => (
                    <div 
                      key={index}
                      className={styles.memoryBlock}
                      style={{ 
                        backgroundColor: item.color, 
                        height: `${Math.max(item.size / 4, 30)}px`,
                        opacity: item.allocated ? 1 : 0.5
                      }}
                      onClick={() => setSelectedAddress(item)}
                    >
                      <div className={styles.blockInfo}>
                        <span className={styles.blockName}>
                          {item.name} {!item.allocated && '(freed)'}
                        </span>
                        <span className={styles.blockAddress}>{formatAddress(item.address)}</span>
                        <span className={styles.blockSize}>{item.size}B</span>
                        {item.data && <span className={styles.blockData}>{item.data}</span>}
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>
        </div>

        {selectedAddress && (
          <div className={styles.detailPanel}>
            <h4>メモリブロック詳細</h4>
            <div className={styles.detailContent}>
              <div><strong>名前:</strong> {selectedAddress.name}</div>
              <div><strong>アドレス:</strong> {formatAddress(selectedAddress.address)}</div>
              <div><strong>サイズ:</strong> {selectedAddress.size} bytes</div>
              <div><strong>型:</strong> {selectedAddress.dataType || selectedAddress.type}</div>
              {selectedAddress.value && (
                <div><strong>値:</strong> {selectedAddress.value}</div>
              )}
              {selectedAddress.pointsTo && (
                <div><strong>参照先:</strong> {formatAddress(selectedAddress.pointsTo)}</div>
              )}
              {selectedAddress.data && (
                <div><strong>データ:</strong> {selectedAddress.data}</div>
              )}
            </div>
            <button onClick={() => setSelectedAddress(null)}>閉じる</button>
          </div>
        )}
      </div>

      <div className={styles.explanation}>
        <h4>スタック・ヒープの特徴</h4>
        <div className={styles.comparisonTable}>
          <div className={styles.comparisonRow}>
            <div className={styles.comparisonHeader}>項目</div>
            <div className={styles.comparisonHeader}>スタック</div>
            <div className={styles.comparisonHeader}>ヒープ</div>
          </div>
          <div className={styles.comparisonRow}>
            <div>メモリ確保</div>
            <div>自動（変数宣言時）</div>
            <div>手動（malloc等）</div>
          </div>
          <div className={styles.comparisonRow}>
            <div>解放</div>
            <div>自動（スコープ終了時）</div>
            <div>手動（free等）</div>
          </div>
          <div className={styles.comparisonRow}>
            <div>速度</div>
            <div>高速</div>
            <div>低速</div>
          </div>
          <div className={styles.comparisonRow}>
            <div>断片化</div>
            <div>なし</div>
            <div>発生可能</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StackHeapSimulator;
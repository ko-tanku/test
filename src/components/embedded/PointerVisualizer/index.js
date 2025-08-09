import React, { useState, useEffect } from 'react';
import styles from './styles.module.css';

const PointerVisualizer = ({
  title = "ポインタ可視化ツール",
  showCode = true,
  interactive = true,
  memoryStartAddr = 0x20000000
}) => {
  const [currentExample, setCurrentExample] = useState(0);
  const [memoryBlocks, setMemoryBlocks] = useState([]);
  const [pointers, setPointers] = useState([]);
  const [selectedItem, setSelectedItem] = useState(null);
  const [currentStep, setCurrentStep] = useState(0);
  const [isAnimating, setIsAnimating] = useState(false);

  // ポインタ学習例のデータ
  const examples = [
    {
      title: "基本的なポインタ",
      description: "変数とポインタの基本的な関係",
      steps: [
        {
          code: "int x = 42;",
          explanation: "整数変数xに値42を代入",
          memory: [{ name: 'x', value: 42, address: 0x20000000, type: 'int', size: 4 }],
          pointers: []
        },
        {
          code: "int* ptr = &x;",
          explanation: "ポインタptrに変数xのアドレスを代入",
          memory: [
            { name: 'x', value: 42, address: 0x20000000, type: 'int', size: 4 },
            { name: 'ptr', value: '0x20000000', address: 0x20000004, type: 'int*', size: 8 }
          ],
          pointers: [{ from: 0x20000004, to: 0x20000000, label: 'ptr → x' }]
        },
        {
          code: "printf(\"%d\", *ptr);",
          explanation: "ポインタを間接参照して値42を取得",
          memory: [
            { name: 'x', value: 42, address: 0x20000000, type: 'int', size: 4, highlighted: true },
            { name: 'ptr', value: '0x20000000', address: 0x20000004, type: 'int*', size: 8 }
          ],
          pointers: [{ from: 0x20000004, to: 0x20000000, label: 'ptr → x', active: true }]
        }
      ]
    },
    {
      title: "配列とポインタ",
      description: "配列名がポインタとして動作する様子",
      steps: [
        {
          code: "int arr[3] = {10, 20, 30};",
          explanation: "3つの整数を持つ配列を宣言・初期化",
          memory: [
            { name: 'arr[0]', value: 10, address: 0x20000000, type: 'int', size: 4 },
            { name: 'arr[1]', value: 20, address: 0x20000004, type: 'int', size: 4 },
            { name: 'arr[2]', value: 30, address: 0x20000008, type: 'int', size: 4 }
          ],
          pointers: []
        },
        {
          code: "int* p = arr;",
          explanation: "配列名arrは最初の要素のアドレスを表す",
          memory: [
            { name: 'arr[0]', value: 10, address: 0x20000000, type: 'int', size: 4 },
            { name: 'arr[1]', value: 20, address: 0x20000004, type: 'int', size: 4 },
            { name: 'arr[2]', value: 30, address: 0x20000008, type: 'int', size: 4 },
            { name: 'p', value: '0x20000000', address: 0x2000000C, type: 'int*', size: 8 }
          ],
          pointers: [{ from: 0x2000000C, to: 0x20000000, label: 'p → arr[0]' }]
        },
        {
          code: "printf(\"%d\", *(p + 1));",
          explanation: "ポインタ演算で2番目の要素にアクセス",
          memory: [
            { name: 'arr[0]', value: 10, address: 0x20000000, type: 'int', size: 4 },
            { name: 'arr[1]', value: 20, address: 0x20000004, type: 'int', size: 4, highlighted: true },
            { name: 'arr[2]', value: 30, address: 0x20000008, type: 'int', size: 4 },
            { name: 'p', value: '0x20000000', address: 0x2000000C, type: 'int*', size: 8 }
          ],
          pointers: [{ from: 0x2000000C, to: 0x20000004, label: 'p + 1 → arr[1]', active: true }]
        }
      ]
    },
    {
      title: "文字列とポインタ",
      description: "文字列リテラルとポインタの関係",
      steps: [
        {
          code: "char* str = \"Hello\";",
          explanation: "文字列リテラルのアドレスをポインタに代入",
          memory: [
            { name: 'str[0]', value: "'H'", address: 0x20000000, type: 'char', size: 1 },
            { name: 'str[1]', value: "'e'", address: 0x20000001, type: 'char', size: 1 },
            { name: 'str[2]', value: "'l'", address: 0x20000002, type: 'char', size: 1 },
            { name: 'str[3]', value: "'l'", address: 0x20000003, type: 'char', size: 1 },
            { name: 'str[4]', value: "'o'", address: 0x20000004, type: 'char', size: 1 },
            { name: 'str[5]', value: "'\\0'", address: 0x20000005, type: 'char', size: 1 },
            { name: 'str', value: '0x20000000', address: 0x20000008, type: 'char*', size: 8 }
          ],
          pointers: [{ from: 0x20000008, to: 0x20000000, label: 'str → "Hello"' }]
        },
        {
          code: "printf(\"%c\", str[2]);",
          explanation: "配列記法でポインタから文字を取得",
          memory: [
            { name: 'str[0]', value: "'H'", address: 0x20000000, type: 'char', size: 1 },
            { name: 'str[1]', value: "'e'", address: 0x20000001, type: 'char', size: 1 },
            { name: 'str[2]', value: "'l'", address: 0x20000002, type: 'char', size: 1, highlighted: true },
            { name: 'str[3]', value: "'l'", address: 0x20000003, type: 'char', size: 1 },
            { name: 'str[4]', value: "'o'", address: 0x20000004, type: 'char', size: 1 },
            { name: 'str[5]', value: "'\\0'", address: 0x20000005, type: 'char', size: 1 },
            { name: 'str', value: '0x20000000', address: 0x20000008, type: 'char*', size: 8 }
          ],
          pointers: [{ from: 0x20000008, to: 0x20000002, label: 'str[2] → l', active: true }]
        }
      ]
    },
    {
      title: "二重ポインタ",
      description: "ポインタのポインタの概念",
      steps: [
        {
          code: "int value = 100;",
          explanation: "整数値を初期化",
          memory: [
            { name: 'value', value: 100, address: 0x20000000, type: 'int', size: 4 }
          ],
          pointers: []
        },
        {
          code: "int* ptr = &value;",
          explanation: "valueのアドレスをptrに代入",
          memory: [
            { name: 'value', value: 100, address: 0x20000000, type: 'int', size: 4 },
            { name: 'ptr', value: '0x20000000', address: 0x20000004, type: 'int*', size: 8 }
          ],
          pointers: [{ from: 0x20000004, to: 0x20000000, label: 'ptr → value' }]
        },
        {
          code: "int** pptr = &ptr;",
          explanation: "ptrのアドレスをpptrに代入（二重ポインタ）",
          memory: [
            { name: 'value', value: 100, address: 0x20000000, type: 'int', size: 4 },
            { name: 'ptr', value: '0x20000000', address: 0x20000004, type: 'int*', size: 8 },
            { name: 'pptr', value: '0x20000004', address: 0x2000000C, type: 'int**', size: 8 }
          ],
          pointers: [
            { from: 0x20000004, to: 0x20000000, label: 'ptr → value' },
            { from: 0x2000000C, to: 0x20000004, label: 'pptr → ptr' }
          ]
        },
        {
          code: "printf(\"%d\", **pptr);",
          explanation: "二重間接参照でvalueの値を取得",
          memory: [
            { name: 'value', value: 100, address: 0x20000000, type: 'int', size: 4, highlighted: true },
            { name: 'ptr', value: '0x20000000', address: 0x20000004, type: 'int*', size: 8 },
            { name: 'pptr', value: '0x20000004', address: 0x2000000C, type: 'int**', size: 8 }
          ],
          pointers: [
            { from: 0x20000004, to: 0x20000000, label: 'ptr → value', active: true },
            { from: 0x2000000C, to: 0x20000004, label: 'pptr → ptr', active: true }
          ]
        }
      ]
    }
  ];

  const currentExampleData = examples[currentExample];
  const currentStepData = currentExampleData.steps[currentStep];

  // ステップ実行
  const nextStep = () => {
    if (currentStep < currentExampleData.steps.length - 1) {
      setIsAnimating(true);
      setTimeout(() => {
        setCurrentStep(currentStep + 1);
        setIsAnimating(false);
      }, 300);
    }
  };

  const prevStep = () => {
    if (currentStep > 0) {
      setIsAnimating(true);
      setTimeout(() => {
        setCurrentStep(currentStep - 1);
        setIsAnimating(false);
      }, 300);
    }
  };

  const resetExample = () => {
    setCurrentStep(0);
    setSelectedItem(null);
  };

  const switchExample = (exampleIndex) => {
    setCurrentExample(exampleIndex);
    setCurrentStep(0);
    setSelectedItem(null);
  };

  // メモリブロック・ポインタの更新
  useEffect(() => {
    setMemoryBlocks(currentStepData.memory || []);
    setPointers(currentStepData.pointers || []);
  }, [currentStepData]);

  const formatAddress = (address) => {
    return `0x${address.toString(16).toUpperCase().padStart(8, '0')}`;
  };

  const getMemoryBlockStyle = (block) => {
    return {
      backgroundColor: block.highlighted ? '#fff3cd' : 
                      block.type.includes('*') ? '#e3f2fd' : '#f8f9fa',
      borderColor: block.highlighted ? '#ffc107' : 
                   block.type.includes('*') ? '#2196f3' : '#dee2e6',
      borderWidth: block.highlighted ? '2px' : '1px'
    };
  };

  const calculatePointerPath = (fromAddr, toAddr) => {
    // SVGパスを計算（簡単な曲線）
    const fromIndex = memoryBlocks.findIndex(b => b.address === fromAddr);
    const toIndex = memoryBlocks.findIndex(b => b.address === toAddr);
    
    const fromY = fromIndex * 60 + 30;
    const toY = toIndex * 60 + 30;
    
    return `M 200 ${fromY} Q 250 ${(fromY + toY) / 2} 200 ${toY}`;
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h3>{title}</h3>
        <p>C言語のポインタ概念を視覚的に理解</p>
      </div>

      <div className={styles.exampleSelector}>
        <h4>学習例を選択</h4>
        <div className={styles.exampleButtons}>
          {examples.map((example, index) => (
            <button
              key={index}
              className={`${styles.exampleButton} ${
                currentExample === index ? styles.active : ''
              }`}
              onClick={() => switchExample(index)}
            >
              {example.title}
            </button>
          ))}
        </div>
      </div>

      <div className={styles.content}>
        <div className={styles.codePanel}>
          <div className={styles.exampleInfo}>
            <h4>{currentExampleData.title}</h4>
            <p>{currentExampleData.description}</p>
          </div>

          {showCode && (
            <div className={styles.codeContainer}>
              <h5>コード ({currentStep + 1}/{currentExampleData.steps.length})</h5>
              <div className={styles.codeBlock}>
                <code>{currentStepData.code}</code>
              </div>
              <div className={styles.explanation}>
                <p>{currentStepData.explanation}</p>
              </div>
            </div>
          )}

          <div className={styles.stepControls}>
            <button 
              onClick={prevStep} 
              disabled={currentStep === 0}
              className={styles.stepButton}
            >
              ◀ 前へ
            </button>
            <span className={styles.stepIndicator}>
              {currentStep + 1} / {currentExampleData.steps.length}
            </span>
            <button 
              onClick={nextStep} 
              disabled={currentStep >= currentExampleData.steps.length - 1}
              className={styles.stepButton}
            >
              次へ ▶
            </button>
            <button onClick={resetExample} className={styles.resetButton}>
              🔄 リセット
            </button>
          </div>
        </div>

        <div className={styles.visualizationPanel}>
          <h4>メモリ可視化</h4>
          <div className={`${styles.memoryContainer} ${isAnimating ? styles.animating : ''}`}>
            <div className={styles.memoryBlocks}>
              {memoryBlocks.map((block, index) => (
                <div
                  key={`${block.address}-${index}`}
                  className={styles.memoryBlock}
                  style={getMemoryBlockStyle(block)}
                  onClick={() => setSelectedItem(block)}
                >
                  <div className={styles.blockHeader}>
                    <span className={styles.blockName}>{block.name}</span>
                    <span className={styles.blockType}>{block.type}</span>
                  </div>
                  <div className={styles.blockContent}>
                    <div className={styles.blockValue}>{block.value}</div>
                    <div className={styles.blockAddress}>{formatAddress(block.address)}</div>
                  </div>
                  <div className={styles.blockSize}>{block.size} bytes</div>
                </div>
              ))}
            </div>

            {pointers.length > 0 && (
              <div className={styles.pointersContainer}>
                <svg className={styles.pointersSvg}>
                  {pointers.map((pointer, index) => (
                    <g key={index}>
                      <defs>
                        <marker
                          id={`arrowhead-${index}`}
                          markerWidth="10"
                          markerHeight="7"
                          refX="9"
                          refY="3.5"
                          orient="auto"
                        >
                          <polygon
                            points="0 0, 10 3.5, 0 7"
                            fill={pointer.active ? "#28a745" : "#007bff"}
                          />
                        </marker>
                      </defs>
                      <path
                        d={calculatePointerPath(pointer.from, pointer.to)}
                        stroke={pointer.active ? "#28a745" : "#007bff"}
                        strokeWidth="2"
                        fill="none"
                        markerEnd={`url(#arrowhead-${index})`}
                        className={pointer.active ? styles.activePointer : ''}
                      />
                      <text
                        x="260"
                        y={
                          (memoryBlocks.findIndex(b => b.address === pointer.from) * 60 +
                           memoryBlocks.findIndex(b => b.address === pointer.to) * 60) / 2 + 35
                        }
                        className={styles.pointerLabel}
                        fill={pointer.active ? "#28a745" : "#007bff"}
                      >
                        {pointer.label}
                      </text>
                    </g>
                  ))}
                </svg>
              </div>
            )}
          </div>

          {selectedItem && (
            <div className={styles.itemDetails}>
              <h5>詳細情報</h5>
              <div className={styles.detailsGrid}>
                <div><strong>変数名:</strong> {selectedItem.name}</div>
                <div><strong>型:</strong> {selectedItem.type}</div>
                <div><strong>値:</strong> {selectedItem.value}</div>
                <div><strong>アドレス:</strong> {formatAddress(selectedItem.address)}</div>
                <div><strong>サイズ:</strong> {selectedItem.size} bytes</div>
              </div>
              <button onClick={() => setSelectedItem(null)}>閉じる</button>
            </div>
          )}
        </div>
      </div>

      <div className={styles.conceptExplanation}>
        <h4>ポインタの重要概念</h4>
        <div className={styles.conceptGrid}>
          <div className={styles.conceptItem}>
            <h5>🎯 ポインタとは</h5>
            <p>メモリアドレスを格納する変数。他の変数の場所を「指し示す」</p>
          </div>
          <div className={styles.conceptItem}>
            <h5>📍 アドレス演算子 (&)</h5>
            <p>変数のメモリアドレスを取得する。&x は「xのアドレス」</p>
          </div>
          <div className={styles.conceptItem}>
            <h5>🔍 間接参照演算子 (*)</h5>
            <p>ポインタが指すアドレスの値を取得・変更する。*ptr は「ptrが指す値」</p>
          </div>
          <div className={styles.conceptItem}>
            <h5>📐 ポインタ演算</h5>
            <p>ポインタに加算すると、型のサイズ分だけアドレスが進む</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PointerVisualizer;
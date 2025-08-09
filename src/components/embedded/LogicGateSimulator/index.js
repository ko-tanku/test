import React, { useState, useCallback, useEffect } from 'react';
import styles from './styles.module.css';

const LogicGateSimulator = ({ 
  title = "論理ゲートシミュレータ",
  allowedGates = ['AND', 'OR', 'NOT', 'XOR', 'NAND', 'NOR'],
  showTruthTable = true,
  interactive = true
}) => {
  const [selectedGate, setSelectedGate] = useState('AND');
  const [inputA, setInputA] = useState(false);
  const [inputB, setInputB] = useState(false);
  const [output, setOutput] = useState(false);
  const [truthTable, setTruthTable] = useState([]);
  const [currentStep, setCurrentStep] = useState(0);

  // 論理ゲートの定義
  const gateDefinitions = {
    AND: {
      name: 'AND',
      symbol: '&',
      description: '全ての入力が1の時のみ出力が1',
      inputs: 2,
      logic: (a, b) => a && b,
      symbol_image: '∧'
    },
    OR: {
      name: 'OR',
      symbol: '≥1',
      description: '少なくとも1つの入力が1なら出力が1',
      inputs: 2,
      logic: (a, b) => a || b,
      symbol_image: '∨'
    },
    NOT: {
      name: 'NOT',
      symbol: '1',
      description: '入力を反転（0→1、1→0）',
      inputs: 1,
      logic: (a) => !a,
      symbol_image: '¬'
    },
    XOR: {
      name: 'XOR',
      symbol: '=1',
      description: '入力が異なる時のみ出力が1',
      inputs: 2,
      logic: (a, b) => a !== b,
      symbol_image: '⊕'
    },
    NAND: {
      name: 'NAND',
      symbol: '&',
      description: 'ANDの出力を反転',
      inputs: 2,
      logic: (a, b) => !(a && b),
      symbol_image: '↑'
    },
    NOR: {
      name: 'NOR',
      symbol: '≥1',
      description: 'ORの出力を反転',
      inputs: 2,
      logic: (a, b) => !(a || b),
      symbol_image: '↓'
    }
  };

  // 真理値表の生成
  const generateTruthTable = useCallback((gateName) => {
    const gate = gateDefinitions[gateName];
    if (!gate) return [];

    if (gate.inputs === 1) {
      return [
        { A: false, B: null, Output: gate.logic(false) },
        { A: true, B: null, Output: gate.logic(true) }
      ];
    } else {
      return [
        { A: false, B: false, Output: gate.logic(false, false) },
        { A: false, B: true, Output: gate.logic(false, true) },
        { A: true, B: false, Output: gate.logic(true, false) },
        { A: true, B: true, Output: gate.logic(true, true) }
      ];
    }
  }, []);

  // 出力の計算
  useEffect(() => {
    const gate = gateDefinitions[selectedGate];
    if (gate) {
      if (gate.inputs === 1) {
        setOutput(gate.logic(inputA));
      } else {
        setOutput(gate.logic(inputA, inputB));
      }
      setTruthTable(generateTruthTable(selectedGate));
    }
  }, [selectedGate, inputA, inputB, generateTruthTable]);

  const handleGateChange = (gateName) => {
    setSelectedGate(gateName);
    setCurrentStep(0);
  };

  const toggleInput = (input) => {
    if (!interactive) return;
    
    if (input === 'A') {
      setInputA(!inputA);
    } else if (input === 'B') {
      setInputB(!inputB);
    }
  };

  const stepThroughTruthTable = () => {
    if (truthTable.length === 0) return;
    
    const nextStep = (currentStep + 1) % truthTable.length;
    const row = truthTable[nextStep];
    
    setInputA(row.A);
    if (row.B !== null) {
      setInputB(row.B);
    }
    setCurrentStep(nextStep);
  };

  const resetSimulation = () => {
    setInputA(false);
    setInputB(false);
    setCurrentStep(0);
  };

  const getCurrentGate = () => gateDefinitions[selectedGate];

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h3>{title}</h3>
        <p>論理ゲートの動作を理解し、デジタル回路の基礎を学習します</p>
      </div>

      <div className={styles.content}>
        <div className={styles.gateSelector}>
          <h4>ゲート選択</h4>
          <div className={styles.gateButtons}>
            {allowedGates.map(gateName => (
              <button
                key={gateName}
                className={`${styles.gateButton} ${
                  selectedGate === gateName ? styles.active : ''
                }`}
                onClick={() => handleGateChange(gateName)}
              >
                {gateName}
              </button>
            ))}
          </div>
        </div>

        <div className={styles.simulator}>
          <div className={styles.gateInfo}>
            <h4>{getCurrentGate().name} ゲート</h4>
            <p>{getCurrentGate().description}</p>
          </div>

          <div className={styles.circuitDiagram}>
            <div className={styles.inputs}>
              {getCurrentGate().inputs >= 1 && (
                <div className={styles.inputLine}>
                  <button
                    className={`${styles.inputButton} ${inputA ? styles.high : styles.low}`}
                    onClick={() => toggleInput('A')}
                    disabled={!interactive}
                  >
                    A: {inputA ? '1' : '0'}
                  </button>
                  <div className={styles.wire}></div>
                </div>
              )}
              
              {getCurrentGate().inputs >= 2 && (
                <div className={styles.inputLine}>
                  <button
                    className={`${styles.inputButton} ${inputB ? styles.high : styles.low}`}
                    onClick={() => toggleInput('B')}
                    disabled={!interactive}
                  >
                    B: {inputB ? '1' : '0'}
                  </button>
                  <div className={styles.wire}></div>
                </div>
              )}
            </div>

            <div className={styles.gateSymbol}>
              <div className={`${styles.gate} ${styles[selectedGate.toLowerCase()]}`}>
                <span className={styles.gateLabel}>{getCurrentGate().symbol_image}</span>
                <div className={styles.gateText}>{selectedGate}</div>
              </div>
            </div>

            <div className={styles.outputLine}>
              <div className={styles.wire}></div>
              <div className={`${styles.outputIndicator} ${output ? styles.high : styles.low}`}>
                出力: {output ? '1' : '0'}
              </div>
            </div>
          </div>

          {interactive && (
            <div className={styles.controls}>
              <button onClick={stepThroughTruthTable} className={styles.stepButton}>
                次のパターン
              </button>
              <button onClick={resetSimulation} className={styles.resetButton}>
                リセット
              </button>
            </div>
          )}
        </div>

        {showTruthTable && (
          <div className={styles.truthTableContainer}>
            <h4>真理値表</h4>
            <table className={styles.truthTable}>
              <thead>
                <tr>
                  <th>A</th>
                  {getCurrentGate().inputs >= 2 && <th>B</th>}
                  <th>出力</th>
                </tr>
              </thead>
              <tbody>
                {truthTable.map((row, index) => (
                  <tr 
                    key={index} 
                    className={currentStep === index ? styles.currentRow : ''}
                  >
                    <td className={row.A ? styles.high : styles.low}>
                      {row.A ? '1' : '0'}
                    </td>
                    {row.B !== null && (
                      <td className={row.B ? styles.high : styles.low}>
                        {row.B ? '1' : '0'}
                      </td>
                    )}
                    <td className={row.Output ? styles.high : styles.low}>
                      {row.Output ? '1' : '0'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      <div className={styles.explanation}>
        <h4>論理ゲートについて</h4>
        <div className={styles.explanationGrid}>
          <div className={styles.explanationItem}>
            <strong>デジタル信号:</strong>
            <p>0（Low/偽）と1（High/真）の2つの状態のみを持つ信号</p>
          </div>
          <div className={styles.explanationItem}>
            <strong>論理演算:</strong>
            <p>デジタル信号に対して行う数学的な操作（AND、OR、NOTなど）</p>
          </div>
          <div className={styles.explanationItem}>
            <strong>組み合わせ回路:</strong>
            <p>複数の論理ゲートを組み合わせて複雑な処理を実現</p>
          </div>
          <div className={styles.explanationItem}>
            <strong>実用例:</strong>
            <p>CPU、メモリ、制御回路など全てのデジタル機器の基礎</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LogicGateSimulator;
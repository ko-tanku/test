import React, { useState, useEffect } from 'react';
import styles from './styles.module.css';

export default function BinaryConverter({
  title = '数値変換ツール',
  showHistory = true,
  showBitOperations = true,
  maxInputValue = 65535, // 16bit max
  variant = 'full' // 'full' | 'compact'
}) {
  const [inputValue, setInputValue] = useState('');
  const [inputBase, setInputBase] = useState(10);
  const [results, setResults] = useState({
    binary: '',
    octal: '',
    decimal: '',
    hexadecimal: ''
  });
  const [history, setHistory] = useState([]);
  const [error, setError] = useState('');

  // ビット演算用の状態
  const [bitValue1, setBitValue1] = useState('');
  const [bitValue2, setBitValue2] = useState('');
  const [bitOperation, setBitOperation] = useState('AND');
  const [bitResult, setBitResult] = useState('');

  useEffect(() => {
    if (inputValue.trim() === '') {
      setResults({ binary: '', octal: '', decimal: '', hexadecimal: '' });
      setError('');
      return;
    }

    try {
      const decimal = parseInt(inputValue, inputBase);
      
      if (isNaN(decimal)) {
        setError('無効な数値です');
        return;
      }

      if (decimal < 0) {
        setError('負の数は対応していません');
        return;
      }

      if (decimal > maxInputValue) {
        setError(`最大値 ${maxInputValue} を超えています`);
        return;
      }

      setResults({
        binary: decimal.toString(2),
        octal: decimal.toString(8),
        decimal: decimal.toString(10),
        hexadecimal: decimal.toString(16).toUpperCase()
      });
      setError('');

      // 履歴に追加
      if (showHistory && decimal !== 0) {
        const historyItem = {
          input: inputValue,
          inputBase,
          decimal,
          timestamp: Date.now()
        };
        setHistory(prev => [historyItem, ...prev.slice(0, 9)]); // 最新10件
      }

    } catch (e) {
      setError('変換エラーが発生しました');
    }
  }, [inputValue, inputBase, maxInputValue, showHistory]);

  // ビット演算の実行
  useEffect(() => {
    if (!showBitOperations || !bitValue1 || !bitValue2) {
      setBitResult('');
      return;
    }

    try {
      const val1 = parseInt(bitValue1, 2);
      const val2 = parseInt(bitValue2, 2);
      
      if (isNaN(val1) || isNaN(val2)) {
        setBitResult('');
        return;
      }

      let result;
      switch (bitOperation) {
        case 'AND':
          result = val1 & val2;
          break;
        case 'OR':
          result = val1 | val2;
          break;
        case 'XOR':
          result = val1 ^ val2;
          break;
        case 'NOT':
          result = ~val1 & 0xFF; // 8bitマスク
          break;
        default:
          result = 0;
      }

      setBitResult(result.toString(2));
    } catch (e) {
      setBitResult('');
    }
  }, [bitValue1, bitValue2, bitOperation, showBitOperations]);

  const formatBinary = (binary) => {
    // 4桁ごとにスペースを挿入
    return binary.replace(/(.{4})/g, '$1 ').trim();
  };

  const clearAll = () => {
    setInputValue('');
    setResults({ binary: '', octal: '', decimal: '', hexadecimal: '' });
    setError('');
  };

  const clearHistory = () => {
    setHistory([]);
  };

  const loadFromHistory = (item) => {
    setInputValue(item.input);
    setInputBase(item.inputBase);
  };

  const getBaseLabel = (base) => {
    const labels = { 2: '2進数', 8: '8進数', 10: '10進数', 16: '16進数' };
    return labels[base] || `${base}進数`;
  };

  if (variant === 'compact') {
    return (
      <div className={styles.compactConverter}>
        <div className={styles.compactInput}>
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="数値を入力"
            className={styles.compactField}
          />
          <select
            value={inputBase}
            onChange={(e) => setInputBase(Number(e.target.value))}
            className={styles.compactSelect}
          >
            <option value={10}>10進</option>
            <option value={2}>2進</option>
            <option value={8}>8進</option>
            <option value={16}>16進</option>
          </select>
        </div>
        {results.binary && (
          <div className={styles.compactResults}>
            <div>2進: {formatBinary(results.binary)}</div>
            <div>16進: {results.hexadecimal}</div>
          </div>
        )}
        {error && <div className={styles.compactError}>{error}</div>}
      </div>
    );
  }

  return (
    <div className={styles.binaryConverter}>
      <h3 className={styles.title}>{title}</h3>

      {/* メイン変換エリア */}
      <div className={styles.mainConverter}>
        <div className={styles.inputSection}>
          <label className={styles.label}>入力値</label>
          <div className={styles.inputGroup}>
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="変換したい数値を入力"
              className={styles.inputField}
            />
            <select
              value={inputBase}
              onChange={(e) => setInputBase(Number(e.target.value))}
              className={styles.baseSelect}
            >
              <option value={10}>10進数</option>
              <option value={2}>2進数</option>
              <option value={8}>8進数</option>
              <option value={16}>16進数</option>
            </select>
          </div>
          {error && <div className={styles.error}>{error}</div>}
        </div>

        {/* 結果表示 */}
        <div className={styles.resultsSection}>
          <div className={styles.resultRow}>
            <label>2進数 (Binary):</label>
            <span className={styles.resultValue}>
              {results.binary ? formatBinary(results.binary) : '-'}
            </span>
          </div>
          <div className={styles.resultRow}>
            <label>8進数 (Octal):</label>
            <span className={styles.resultValue}>
              {results.octal || '-'}
            </span>
          </div>
          <div className={styles.resultRow}>
            <label>10進数 (Decimal):</label>
            <span className={styles.resultValue}>
              {results.decimal || '-'}
            </span>
          </div>
          <div className={styles.resultRow}>
            <label>16進数 (Hexadecimal):</label>
            <span className={styles.resultValue}>
              {results.hexadecimal || '-'}
            </span>
          </div>
        </div>

        <button onClick={clearAll} className={styles.clearButton}>
          🗑️ クリア
        </button>
      </div>

      {/* ビット演算セクション */}
      {showBitOperations && (
        <div className={styles.bitOperations}>
          <h4 className={styles.sectionTitle}>ビット演算</h4>
          <div className={styles.bitInputs}>
            <div className={styles.bitInputGroup}>
              <label>値1 (2進数):</label>
              <input
                type="text"
                value={bitValue1}
                onChange={(e) => setBitValue1(e.target.value)}
                placeholder="例: 1010"
                className={styles.bitInput}
              />
            </div>
            <div className={styles.operationSelect}>
              <select
                value={bitOperation}
                onChange={(e) => setBitOperation(e.target.value)}
                className={styles.opSelect}
              >
                <option value="AND">AND (&)</option>
                <option value="OR">OR (|)</option>
                <option value="XOR">XOR (^)</option>
                <option value="NOT">NOT (~)</option>
              </select>
            </div>
            {bitOperation !== 'NOT' && (
              <div className={styles.bitInputGroup}>
                <label>値2 (2進数):</label>
                <input
                  type="text"
                  value={bitValue2}
                  onChange={(e) => setBitValue2(e.target.value)}
                  placeholder="例: 1100"
                  className={styles.bitInput}
                />
              </div>
            )}
          </div>
          {bitResult && (
            <div className={styles.bitResult}>
              <strong>結果:</strong> {formatBinary(bitResult)}
              <span className={styles.bitResultDecimal}>
                (10進数: {parseInt(bitResult, 2)})
              </span>
            </div>
          )}
        </div>
      )}

      {/* 履歴セクション */}
      {showHistory && history.length > 0 && (
        <div className={styles.historySection}>
          <div className={styles.historyHeader}>
            <h4 className={styles.sectionTitle}>変換履歴</h4>
            <button onClick={clearHistory} className={styles.clearHistoryButton}>
              履歴をクリア
            </button>
          </div>
          <div className={styles.historyList}>
            {history.map((item, index) => (
              <div 
                key={index} 
                className={styles.historyItem}
                onClick={() => loadFromHistory(item)}
              >
                <span className={styles.historyInput}>
                  {item.input} ({getBaseLabel(item.inputBase)})
                </span>
                <span className={styles.historyArrow}>→</span>
                <span className={styles.historyResult}>
                  {item.decimal} (10進数)
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 学習ヒント */}
      <div className={styles.learningTips}>
        <h4 className={styles.sectionTitle}>💡 学習のポイント</h4>
        <ul className={styles.tipsList}>
          <li>2進数では0と1のみを使用します</li>
          <li>16進数では0-9とA-Fを使用します（A=10, B=11, ..., F=15）</li>
          <li>コンピュータ内部では全て2進数で処理されます</li>
          <li>ビット演算は論理回路の基本動作です</li>
        </ul>
      </div>
    </div>
  );
}
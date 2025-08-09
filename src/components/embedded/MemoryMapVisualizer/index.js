import React, { useState, useEffect } from 'react';
import styles from './styles.module.css';

const MemoryMapVisualizer = ({ 
  title = "メモリマップ可視化",
  architecture = "32bit",
  regions = [],
  interactive = true,
  showCode = false,
  codeExample = ""
}) => {
  const [selectedRegion, setSelectedRegion] = useState(null);
  const [currentAddress, setCurrentAddress] = useState('');
  const [variables, setVariables] = useState([]);
  const [showDetails, setShowDetails] = useState(false);

  // デフォルトメモリ領域設定（32bit ARM Cortex-M想定）
  const defaultRegions = [
    {
      name: "Flash Memory (Code)",
      start: 0x08000000,
      end: 0x080FFFFF,
      size: "1MB",
      color: "#e74c3c",
      description: "プログラムコード領域",
      permissions: "Read/Execute",
      usage: "実行可能プログラム、定数データ"
    },
    {
      name: "SRAM (Data)",
      start: 0x20000000,
      end: 0x2001FFFF,
      size: "128KB",
      color: "#3498db",
      description: "データメモリ領域",
      permissions: "Read/Write",
      usage: "グローバル変数、スタック、ヒープ"
    },
    {
      name: "Peripheral",
      start: 0x40000000,
      end: 0x5FFFFFFF,
      size: "512MB",
      color: "#f39c12",
      description: "ペリフェラル制御レジスタ",
      permissions: "Read/Write",
      usage: "GPIO、タイマー、UART等の制御"
    },
    {
      name: "System",
      start: 0xE0000000,
      end: 0xFFFFFFFF,
      size: "512MB",
      color: "#9b59b6",
      description: "システム領域",
      permissions: "System",
      usage: "Cortex-M システム制御"
    }
  ];

  // サンプル変数データ
  const sampleVariables = [
    { name: "int global_var", address: 0x20000000, size: 4, type: "global" },
    { name: "char buffer[100]", address: 0x20000004, size: 100, type: "global" },
    { name: "static int counter", address: 0x20000068, size: 4, type: "static" },
    { name: "Stack Top", address: 0x2001FFFC, size: 4, type: "stack" },
    { name: "Heap Start", address: 0x20010000, size: 0, type: "heap" }
  ];

  const activeRegions = regions.length > 0 ? regions : defaultRegions;

  useEffect(() => {
    if (interactive) {
      setVariables(sampleVariables);
    }
  }, [interactive]);

  const formatAddress = (address) => {
    return `0x${address.toString(16).toUpperCase().padStart(8, '0')}`;
  };

  const calculateSize = (start, end) => {
    const bytes = end - start + 1;
    if (bytes >= 1024 * 1024) {
      return `${(bytes / (1024 * 1024)).toFixed(1)}MB`;
    } else if (bytes >= 1024) {
      return `${(bytes / 1024).toFixed(1)}KB`;
    } else {
      return `${bytes}B`;
    }
  };

  const getRegionHeight = (region) => {
    const totalMemory = 0xFFFFFFFF - 0x00000000;
    const regionSize = region.end - region.start;
    return Math.max((regionSize / totalMemory) * 400, 30); // 最小高さ30px
  };

  const handleRegionClick = (region) => {
    setSelectedRegion(region);
    setShowDetails(true);
  };

  const findVariableRegion = (address) => {
    return activeRegions.find(region => address >= region.start && address <= region.end);
  };

  const parseAddress = (input) => {
    try {
      if (input.startsWith('0x') || input.startsWith('0X')) {
        return parseInt(input, 16);
      }
      return parseInt(input, 10);
    } catch {
      return null;
    }
  };

  const handleAddressLookup = () => {
    const address = parseAddress(currentAddress);
    if (address !== null) {
      const region = findVariableRegion(address);
      if (region) {
        setSelectedRegion({ ...region, lookupAddress: address });
        setShowDetails(true);
      }
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h3>{title}</h3>
        <div className={styles.architecture}>
          <span>アーキテクチャ: {architecture}</span>
        </div>
      </div>

      <div className={styles.content}>
        <div className={styles.memoryMap}>
          <div className={styles.memoryTitle}>メモリマップ</div>
          <div className={styles.addressScale}>
            <div className={styles.scaleItem}>0x00000000</div>
            <div className={styles.scaleItem}>0x80000000</div>
            <div className={styles.scaleItem}>0xFFFFFFFF</div>
          </div>
          
          <div className={styles.memoryRegions}>
            {activeRegions.map((region, index) => (
              <div
                key={index}
                className={styles.memoryRegion}
                style={{
                  backgroundColor: region.color,
                  height: `${getRegionHeight(region)}px`
                }}
                onClick={() => handleRegionClick(region)}
              >
                <div className={styles.regionInfo}>
                  <div className={styles.regionName}>{region.name}</div>
                  <div className={styles.regionRange}>
                    {formatAddress(region.start)} - {formatAddress(region.end)}
                  </div>
                  <div className={styles.regionSize}>{region.size}</div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className={styles.sidebar}>
          {interactive && (
            <div className={styles.addressLookup}>
              <h4>アドレス検索</h4>
              <div className={styles.lookupInput}>
                <input
                  type="text"
                  placeholder="0x20000000"
                  value={currentAddress}
                  onChange={(e) => setCurrentAddress(e.target.value)}
                />
                <button onClick={handleAddressLookup}>検索</button>
              </div>
            </div>
          )}

          {showDetails && selectedRegion && (
            <div className={styles.regionDetails}>
              <h4>領域詳細</h4>
              <div className={styles.detailItem}>
                <strong>名前:</strong> {selectedRegion.name}
              </div>
              <div className={styles.detailItem}>
                <strong>開始:</strong> {formatAddress(selectedRegion.start)}
              </div>
              <div className={styles.detailItem}>
                <strong>終了:</strong> {formatAddress(selectedRegion.end)}
              </div>
              <div className={styles.detailItem}>
                <strong>サイズ:</strong> {calculateSize(selectedRegion.start, selectedRegion.end)}
              </div>
              <div className={styles.detailItem}>
                <strong>権限:</strong> {selectedRegion.permissions}
              </div>
              <div className={styles.detailItem}>
                <strong>用途:</strong> {selectedRegion.usage}
              </div>
              <div className={styles.description}>
                {selectedRegion.description}
              </div>
              {selectedRegion.lookupAddress && (
                <div className={styles.lookupResult}>
                  <strong>検索アドレス:</strong> {formatAddress(selectedRegion.lookupAddress)}
                </div>
              )}
            </div>
          )}

          {interactive && variables.length > 0 && (
            <div className={styles.variableList}>
              <h4>変数マッピング例</h4>
              {variables.map((variable, index) => (
                <div key={index} className={styles.variableItem}>
                  <div className={styles.variableName}>{variable.name}</div>
                  <div className={styles.variableAddress}>{formatAddress(variable.address)}</div>
                  <div className={styles.variableSize}>{variable.size}B</div>
                  <div className={styles.variableType}>{variable.type}</div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {showCode && codeExample && (
        <div className={styles.codeExample}>
          <h4>コード例</h4>
          <pre className={styles.code}>
            {codeExample}
          </pre>
        </div>
      )}

      <div className={styles.legend}>
        <h4>メモリ領域の説明</h4>
        <div className={styles.legendItems}>
          {activeRegions.map((region, index) => (
            <div key={index} className={styles.legendItem}>
              <div 
                className={styles.legendColor}
                style={{ backgroundColor: region.color }}
              />
              <span>{region.name}: {region.description}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default MemoryMapVisualizer;
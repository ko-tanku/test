# 拡張コンポーネントのテスト確認

## 1. InteractiveFlowchart - SystemArchitectureViewer機能

### 基本アーキテクチャ図テスト
```jsx
<InteractiveFlowchart 
  title="CPUアーキテクチャ"
  mode="architecture"
  showLegend={true}
  zoomEnabled={true}
  steps={[
    {
      id: 'cpu',
      label: 'CPU',
      type: 'cpu_component',
      x: 50,
      y: 30,
      icon: '🧠',
      specs: { 'クロック': '3.2GHz', 'コア数': '4' },
      description: 'Central Processing Unit',
      technicalDetails: ['ALU: 算術論理演算', 'Control Unit: 制御装置', 'Registers: レジスタ群']
    },
    {
      id: 'memory',
      label: 'メモリ',
      type: 'memory_block',
      x: 20,
      y: 60,
      icon: '💾',
      specs: { '容量': '16GB', 'タイプ': 'DDR4' },
      description: 'Main Memory'
    }
  ]}
  connections={[
    {
      from: 'cpu',
      to: 'memory',
      type: 'data_bus',
      label: 'データバス'
    }
  ]}
/>
```

## 2. Timeline - DevelopmentProcessFlow機能

### V字モデル開発プロセステスト
```jsx
<Timeline
  mode="development_process"
  orientation="vertical"
  showDependencies={true}
  phaseColors={true}
  events={[
    {
      title: '要件定義',
      phase: 'requirements',
      type: 'milestone',
      description: 'システム要求の明確化',
      duration: '2週間',
      deliverables: ['要件定義書', '機能仕様書'],
      technicalNotes: ['ステークホルダー分析', 'ユースケース定義']
    },
    {
      title: '基本設計',
      phase: 'design', 
      type: 'deliverable',
      description: 'システム全体設計',
      duration: '3週間',
      deliverables: ['基本設計書', 'アーキテクチャ図'],
      dependencies: [0]
    }
  ]}
/>
```

## 3. SimpleChart - 波形表示機能

### デジタル信号波形テスト
```jsx
<SimpleChart
  type="digital"
  title="I2C通信波形"
  width={600}
  height={300}
  timeUnit="μs"
  data={[
    { time: 0, value: 0 },
    { time: 1, value: 1 },
    { time: 2, value: 1 },
    { time: 3, value: 0 },
    { time: 4, value: 0 },
    { time: 5, value: 1 }
  ]}
  showGrid={true}
/>
```

### アナログ波形テスト
```jsx
<SimpleChart
  type="waveform"
  title="サイン波信号"
  width={500}
  height={250}
  amplitude={100}
  data={[
    { time: 0, value: 0 },
    { time: 1, value: 50 },
    { time: 2, value: 86.6 },
    { time: 3, value: 100 },
    { time: 4, value: 86.6 },
    { time: 5, value: 50 },
    { time: 6, value: 0 }
  ]}
/>
```

## 4. DataFlowSimulator - ネットワーク階層表示機能

### OSI参照モデルテスト
```jsx
<DataFlowSimulator
  title="OSI参照モデル"
  mode="network_stack"
  showLayers={true}
  layerHeight={80}
  protocolInfo={true}
  nodes={[
    {
      id: 'app',
      label: 'Webブラウザ',
      layer: 6,
      protocol: 'HTTP',
      port: 80,
      icon: '🌐',
      functions: ['HTMLレンダリング', 'JavaScriptエンジン'],
      x: 30,
      description: 'アプリケーション層'
    },
    {
      id: 'tcp',
      label: 'TCP',
      layer: 3,
      protocol: 'TCP',
      port: 80,
      icon: '🔗',
      functions: ['信頼性保証', 'フロー制御'],
      x: 30,
      description: 'トランスポート層'
    }
  ]}
  flows={[
    {
      from: 'app',
      to: 'tcp',
      label: 'HTTPリクエスト',
      protocol: 'HTTP'
    }
  ]}
/>
```

## テスト結果確認項目

### InteractiveFlowchart
- ✅ アーキテクチャモード表示
- ✅ ズーム機能
- ✅ レジェンド表示
- ✅ バスタイプ別色分け
- ✅ 技術仕様表示
- ✅ アイコン表示

### Timeline  
- ✅ 開発プロセスモード
- ✅ フェーズ別色分け
- ✅ 依存関係表示
- ✅ 成果物リスト
- ✅ 技術ポイント表示
- ✅ 期間表示

### SimpleChart
- ✅ 波形表示（アナログ）
- ✅ デジタル信号表示
- ✅ マルチチャンネル対応
- ✅ グリッド表示
- ✅ 時間軸ラベル
- ✅ チャンネル識別

### DataFlowSimulator
- ✅ ネットワークスタックモード
- ✅ 階層表示
- ✅ プロトコル情報パネル
- ✅ 層別色分け
- ✅ 層インジケーター
- ✅ プロトコル名表示

## 追加された主要機能

1. **システムアーキテクチャ視覚化**
   - CPU構成図、メモリマップ表示
   - バス接続の種類別表示
   - ハードウェア仕様情報

2. **開発プロセス管理**
   - V字モデル、Git フロー対応
   - 工程依存関係の可視化
   - 成果物・技術ポイント管理

3. **信号波形解析**
   - アナログ・デジタル信号対応
   - 通信プロトコル波形表示
   - マルチチャンネル同時表示

4. **ネットワーク階層モデル**
   - OSI参照モデル対応
   - プロトコル詳細情報
   - 階層間データフロー表示

これらの機能により、IT・組み込みシステム教育に特化した視覚化が大幅に強化されました。
# 統一コンポーネントシステム使用ガイド

## 概要

新しく実装されたReact風コンポーネント指向システムの使用方法を説明します。このシステムでは、YAML仕様でコンテンツを宣言的に定義し、様々な形式（HTML、Markdown等）で出力できます。

## システム構成

```
src/core/
├── component_renderer.py      # 基底クラス群
├── renderer_factory.py       # ファクトリとジェネレータ  
├── matplotlib_renderer.py    # Matplotlib描画エンジン
├── markdown_renderer.py      # Markdown描画エンジン
└── __init__.py               # 統合初期化
```

## 基本的な使い方

### 1. プログラムでの直接使用

```python
from src.core import UniversalContentGenerator

# ジェネレータを初期化
generator = UniversalContentGenerator("output")

# 仕様を辞書で定義
spec = {
    "type": "content_block",
    "engine": "matplotlib",  # または "markdown"
    "filename": "my_chart",
    "config": {
        "title": "サンプルグラフ",
        "size": [10, 6]
    },
    "components": [
        {
            "type": "DataVisualization",
            "props": {
                "variant": "line",
                "data": {"x": [1,2,3], "y": [4,5,6]},
                "style": {"color": "blue"}
            }
        }
    ]
}

# 生成実行
output_path = generator.generate_from_spec(spec)
print(f"生成完了: {output_path}")
```

### 2. YAMLファイルでの定義

```yaml
# chart_spec.yml
type: content_block
engine: matplotlib
filename: my_chart
config:
  title: "売上推移"
  size: [12, 8]
components:
  - type: DataVisualization
    props:
      variant: line
      data:
        x: [1, 2, 3, 4, 5]
        y: [100, 150, 120, 180, 200]
      style:
        color: "#1f77b4"
        lineWidth: 3
```

```python
# YAMLから生成
output_path = generator.generate_from_yaml("chart_spec.yml")
```

## サポートするエンジン

### Matplotlib Engine (`engine: "matplotlib"`)

科学的なグラフや図形の描画に使用。HTML形式で出力されます。

**サポートコンポーネント:**
- `DataVisualization`: グラフ描画（line, bar, scatter, pie）
- `Shape`: 図形描画（rectangle, circle, polygon, arrow）
- `Text`: テキスト配置
- `MathFunction`: 数学関数の描画（sin, cos, linear, polynomial）
- `Grid`, `Axis`, `Legend`: グラフの装飾
- `Annotation`: 注釈

### Markdown Engine (`engine: "markdown"`)

ドキュメントや学習教材の作成に使用。Markdown形式で出力されます。

**サポートコンポーネント:**
- `Heading`: 見出し
- `Paragraph`: 段落（ツールチップ対応）
- `List`: リスト（順序付き・無し）
- `CodeBlock`: コードブロック
- `Admonition`: 注釈ボックス（info, warning, tip等）
- `Tabs`: タブコンテナ
- `Quiz`: クイズ（単一選択、複数選択、カテゴリ分け）
- `Embed`: 外部コンテンツ埋め込み
- `Image`, `Table`, `Link`: 基本要素

### Plotly Engine (`engine: "plotly"`)

インタラクティブなダッシュボードと高度な可視化。HTML形式で出力されます。

**サポートコンポーネント:**
- `DataVisualization`: インタラクティブチャート（line, bar, scatter, pie, heatmap, 3d_scatter, box, violin）
- `Interactive`: ボタン、スライダー、ドロップダウン
- `Layout`: レイアウト設定とカスタマイズ
- `Animation`: アニメーション機能
- `Dashboard`: 複数チャートの統合ダッシュボード
- `Subplot`: サブプロット配置
- `Shape`: 図形とライン描画
- `Annotation`: 注釈とコールアウト
- `CustomTrace`: カスタムトレース定義

### Table Engine (`engine: "table"`)

高機能なテーブルとデータグリッド。HTML形式で出力されます。

**サポートコンポーネント:**
- `BasicTable`: 基本テーブル
- `ComparisonTable`: 比較テーブル
- `DataTable`: データフレーム対応テーブル
- `InteractiveTable`: ソート・フィルタ機能
- `SortableTable`: ソート専用テーブル
- `FilterableTable`: フィルタ専用テーブル
- `PivotTable`: ピボットテーブル
- `SummaryTable`: 統計サマリーテーブル
- `StatisticsTable`: 統計情報テーブル
- `Grid`: グリッドレイアウト

## コンポーネント使用例

### Matplotlibコンポーネント

```yaml
components:
  # ライングラフ
  - type: DataVisualization
    props:
      variant: line
      data:
        x: [1, 2, 3, 4, 5]
        y: [10, 20, 15, 25, 30]
      style:
        color: "#e74c3c"
        lineWidth: 2
        label: "売上"

  # 円形図形
  - type: Shape
    props:
      variant: circle
      position: [5, 20]
      size: 3
      style:
        color: "#3498db"
        opacity: 0.7

  # 数学関数
  - type: MathFunction
    props:
      function: sin
      domain: [0, 10]
      parameters:
        amplitude: 2
        frequency: 1
      style:
        color: "green"
        lineWidth: 2
```

### Markdownコンポーネント

```yaml
components:
  # 見出し
  - type: Heading
    props:
      content: "第1章: 概要"
      level: 2

  # ツールチップ付き段落
  - type: Paragraph
    props:
      content: "**Python**は動的型付け言語です。"
      terms:
        "Python": "汎用プログラミング言語"
        "動的型付け": "実行時に型が決定される仕組み"
      enableTooltips: true

  # タブコンテナ
  - type: Tabs
    props:
      tabs:
        "Python例":
          - type: CodeBlock
            props:
              content: "print('Hello, World!')"
              language: python
        "JavaScript例":
          - type: CodeBlock
            props:
              content: "console.log('Hello, World!');"
              language: javascript

  # クイズ
  - type: Quiz
    props:
      variant: single_choice
      question: "Pythonで文字列を出力するには？"
      options:
        - "print()"
        - "echo()"
        - "puts()"
      correct: [0]
      explanation: "Pythonではprint()関数を使います"
```

### Plotlyコンポーネント

```yaml
components:
  # インタラクティブライングラフ
  - type: DataVisualization
    props:
      variant: line
      data:
        x: [1, 2, 3, 4, 5, 6]
        y: [10, 25, 15, 30, 20, 35]
      style:
        color: "#1f77b4"
        lineWidth: 3
        label: "売上推移"

  # 3Dグラフ
  - type: DataVisualization
    props:
      variant: 3d_scatter
      data:
        x: [1, 2, 3, 4, 5]
        y: [2, 4, 1, 5, 3]
        z: [1, 3, 2, 4, 2]
      style:
        color: ["red", "blue", "green", "orange", "purple"]
        markerSize: [8, 10, 12, 9, 11]

  # ダッシュボード
  - type: Dashboard
    props:
      rows: 2
      cols: 2
      components:
        - type: DataVisualization
          props:
            variant: line
            data:
              x: [1, 2, 3]
              y: [1, 3, 2]
        - type: DataVisualization
          props:
            variant: bar
            data:
              x: ["A", "B", "C"]
              y: [1, 2, 3]

  # インタラクティブコントロール
  - type: Interactive
    props:
      variant: dropdown
      actions:
        - label: "全データ表示"
          method: "relayout"
          args: [{"xaxis.range": [0, 10]}]
        - label: "前半データ"
          method: "relayout"
          args: [{"xaxis.range": [0, 5]}]
```

### Tableコンポーネント

```yaml
components:
  # 基本テーブル
  - type: BasicTable
    props:
      title: "売上データ"
      headers: ["商品名", "売上数", "単価"]
      rows:
        - ["商品A", 100, 1000]
        - ["商品B", 150, 800]
        - ["商品C", 200, 1200]

  # インタラクティブテーブル
  - type: InteractiveTable
    props:
      title: "ソート・フィルタ対応テーブル"
      headers: ["名前", "年齢", "部署"]
      rows:
        - ["田中", 25, "営業"]
        - ["佐藤", 30, "開発"]
        - ["鈴木", 28, "マーケティング"]
      sortable: true
      filterable: true

  # データテーブル（DataFrame）
  - type: DataTable
    props:
      title: "売上分析"
      data:
        商品: ["商品A", "商品B", "商品C"]
        売上: [1000000, 1500000, 800000]
        利益率: [0.15, 0.18, 0.12]
      format:
        売上: "¥{:,}"
        利益率: "{:.1%}"

  # 比較テーブル
  - type: ComparisonTable
    props:
      title: "四半期比較"
      categories: ["Q1", "Q2", "Q3", "Q4"]
      items: ["商品A", "商品B", "商品C"]
      data:
        - [100, 120, 110, 130]
        - [150, 140, 160, 170]
        - [200, 180, 190, 210]

  # ピボットテーブル
  - type: PivotTable
    props:
      title: "地域別売上集計"
      data:
        商品: ["A", "A", "B", "B"]
        地域: ["東京", "大阪", "東京", "大阪"]
        売上: [100, 80, 120, 90]
      index: "商品"
      columns: "地域"
      values: "売上"
      aggfunc: "sum"
```

## 高度な機能

### 合成コンポーネント

複数の基本コンポーネントを組み合わせた高レベルコンポーネント：

```yaml
- type: LearningSection
  props:
    title: "変数の基礎"
    level: 2
    components:
      - type: Paragraph
        props:
          content: "変数について学びましょう"
      - type: CodeBlock
        props:
          content: "x = 10"
          language: python
      - type: Quiz
        props:
          variant: single_choice
          question: "変数xの値は？"
          options: ["5", "10", "15"]
          correct: [1]
```

### 一括処理

複数のファイルを一度に処理：

```python
# 複数仕様の一括処理
specs = [spec1, spec2, spec3]
results = generator.generate_multiple(specs)

# YAMLディレクトリの一括処理
results = generator.generate_from_yaml_directory("specs/", "*.yml")
```

### エラーハンドリング

```python
try:
    result = generator.generate_from_spec(spec)
except ValueError as e:
    print(f"仕様エラー: {e}")
except Exception as e:
    print(f"生成エラー: {e}")
```

## カスタムコンポーネントの作成

新しいコンポーネントを追加することも可能です：

```python
from src.core import BaseComponent, MatplotlibRenderer

class CustomGaugeComponent(BaseComponent):
    type_name = "CustomGauge"
    required_props = ['value', 'maxValue']
    
    @classmethod
    def render(cls, props, renderer):
        value = props['value']
        max_value = props['maxValue']
        # カスタム描画ロジック
        # ...

# コンポーネントを登録
renderer = MatplotlibRenderer("./output")
renderer.register_component(CustomGaugeComponent)
```

## 既存システムとの互換性

既存のChartGeneratorやDocumentBuilderも従来通り使用できます：

```python
from src.core import ChartGenerator, DocumentBuilder

# 従来の方法も継続サポート
chart_gen = ChartGenerator()
chart_gen.create_simple_line_chart(...)

# 新しい方法
generator = UniversalContentGenerator("./output")
generator.generate_from_spec(spec)
```

## 実行例

### 基本デモの実行

```bash
cd examples
python component_system_demo.py
```

### 包括的デモの実行（全エンジン対応）

```bash
cd examples  
python comprehensive_system_demo.py
```

### テストの実行

```bash
python tests/test_component_system.py
```

### 各エンジン別の特徴

| エンジン | 出力形式 | 主な用途 | インタラクティブ |
|---------|---------|----------|-----------------|
| `matplotlib` | HTML | 科学的図表、数学関数 | ❌ |
| `markdown` | MD | ドキュメント、学習教材 | 限定的 |
| `plotly` | HTML | ダッシュボード、分析 | ✅ |
| `table` | HTML | データ表示、比較 | ✅ |

## トラブルシューティング

### よくあるエラー

1. **`エンジンが利用できません`**: 指定したengineが存在しないか、初期化されていない
2. **`必須プロパティが不足`**: required_propsが不足している
3. **`YAMLファイルが見つかりません`**: ファイルパスが正しいか確認
4. **`plotlyが見つかりません`**: `pip install plotly` でPlotlyをインストール
5. **`pandasが見つかりません`**: `pip install pandas` でPandasをインストール
6. **`テーブルが空です`**: TableRendererでデータが正しく渡されているか確認
7. **`インタラクティブ機能が動作しない`**: ブラウザでJavaScriptが有効になっているか確認

### 必要な依存関係

```bash
# 全エンジンを使用する場合
pip install matplotlib plotly pandas numpy pyyaml

# 個別インストール
pip install matplotlib    # Matplotlib engine
pip install plotly       # Plotly engine  
pip install pandas       # Table engine (DataTable)
pip install numpy        # 数値計算サポート
pip install pyyaml       # YAML仕様ファイル
```

### デバッグ方法

```python
# 利用可能エンジンの確認
from src.core import RendererFactory
print(RendererFactory.get_available_engines())
# 出力例: ['matplotlib', 'markdown', 'plotly', 'table']

# 各エンジンの詳細情報
for engine in RendererFactory.get_available_engines():
    info = RendererFactory.get_engine_info(engine)
    print(f"{engine}: {info}")

# コンポーネント一覧の確認  
from src.core import MatplotlibRenderer, PlotlyRenderer, TableRenderer
matplotlib_renderer = MatplotlibRenderer("./output")
plotly_renderer = PlotlyRenderer("./output") 
table_renderer = TableRenderer("./output")

print("Matplotlib:", matplotlib_renderer.get_registered_components())
print("Plotly:", plotly_renderer.get_registered_components())
print("Table:", table_renderer.get_registered_components())

# システム情報の確認
generator = UniversalContentGenerator("./output") 
print(generator.get_system_info())
```

### パフォーマンス最適化

```python
# 大量データの処理
spec = {
    "engine": "table",
    "config": {
        "layout": "multi",  # 複数テーブルをグリッド表示
        "responsive": True  # レスポンシブ対応
    },
    "components": [
        # データを分割して処理
        {"type": "DataTable", "props": {"data": chunk1}},
        {"type": "DataTable", "props": {"data": chunk2}}
    ]
}

# Plotlyの大量データ対応
plotly_spec = {
    "engine": "plotly",
    "config": {
        "plotly_config": {
            "responsive": True,
            "scrollZoom": True  # ズーム機能を有効化
        }
    },
    "components": [
        {
            "type": "DataVisualization",
            "props": {
                "variant": "line",
                "data": {"x": large_x, "y": large_y},
                "style": {"opacity": 0.7}  # 透明度で重複を見やすく
            }
        }
    ]
}
```

## パフォーマンス

- 大量のコンポーネントがある場合は分割処理を推奨
- YAMLファイルが大きい場合はvalidationに時間がかかる可能性
- matplotlibの複雑な図は生成時間が長くなる場合があります

---

このシステムにより、既存の機能を活かしつつ、より柔軟で拡張性の高いコンテンツ生成が可能になりました。
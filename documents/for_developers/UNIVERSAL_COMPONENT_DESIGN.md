# 超汎用的コンポーネント指向設計仕様書

## 1. 概要

本書は、PROJECT_BLUEPRINT.mdおよびDESIGN_PHILOSOPHY.mdに基づき、すべての生成コンテンツをReact風コンポーネント指向で統一する**超汎用的設計仕様**を定義します。

### 1.1. 設計原則

1. **完全宣言的（Fully Declarative）**: すべての生成物はYAML仕様で宣言的に定義
2. **コンポーネント合成（Component Composition）**: 基本コンポーネントの組み合わせで複雑なコンテンツを構成
3. **描画エンジン抽象化（Engine Abstraction）**: 特定の描画ライブラリに依存しない統一インターフェース
4. **プロパティ駆動（Props-Driven）**: Reactのpropsのようにパラメータで振る舞いを制御

## 2. 統一コンポーネントシステム

### 2.1. 基本構造

すべてのコンテンツは以下の統一構造で表現されます：

```yaml
type: "content_block"
engine: "renderer_name"  # matplotlib, plotly, markdown, html, d3js
config:
  # 全体設定
components:
  - type: "component_name"
    props:
      # コンポーネント固有のプロパティ
```

### 2.2. エンジン種別とサポートコンポーネント

#### 2.2.1. Visualization Engine (`matplotlib`, `plotly`, `d3js`)

**基本描画プリミティブ:**
```yaml
# 図形コンポーネント
- type: "Shape"
  props:
    variant: "rectangle|circle|polygon|line|arrow"
    position: [x, y] or [[x1, y1], [x2, y2]]
    size: [width, height] or radius
    style: 
      color: "#hexcode"
      opacity: 0.8
      stroke: "#hexcode"
      strokeWidth: 2

# テキストコンポーネント  
- type: "Text"
  props:
    content: "display text"
    position: [x, y]
    style:
      fontSize: 16
      color: "#000000"
      fontWeight: "normal|bold"
      align: "left|center|right"

# データ可視化コンポーネント
- type: "DataVisualization"
  props:
    variant: "line|bar|scatter|pie|heatmap"
    data: 
      x: [1, 2, 3]
      y: [4, 5, 6]
    style:
      colors: ["#ff0000", "#00ff00"]
      opacity: 0.7

# インタラクティブコンポーネント
- type: "Interactive"
  props:
    variant: "slider|dropdown|button|tab"
    states: [state1, state2, ...]
    defaultState: 0
    binding: "target_component_id"

# カスタム波形・数式コンポーネント
- type: "MathFunction"
  props:
    function: "sin|cos|linear|polynomial|custom"
    domain: [start, end]
    parameters:
      amplitude: 1
      frequency: 1
      offset: 0
```

#### 2.2.2. Document Engine (`markdown`, `html`)

**コンテンツ構造コンポーネント:**
```yaml
# 見出しコンポーネント
- type: "Heading"
  props:
    level: 1-6
    content: "見出しテキスト"

# 段落コンポーネント（ツールチップ対応）
- type: "Paragraph"
  props:
    content: "本文テキスト"
    terms: 
      "専門用語": "説明文"
    enableTooltips: true

# リストコンポーネント
- type: "List"
  props:
    variant: "ordered|unordered"
    items: ["項目1", "項目2"]

# コードブロックコンポーネント
- type: "CodeBlock"
  props:
    language: "python|javascript|yaml"
    content: "code string"
    showLineNumbers: true
    highlightLines: [1, 3]

# 注釈ボックスコンポーネント
- type: "Admonition"
  props:
    variant: "info|warning|tip|note|danger"
    title: "タイトル"
    content: "内容"
    collapsible: true

# タブコンテナ
- type: "Tabs"
  props:
    tabs:
      "タブ1": "content1"
      "タブ2": "content2"

# インタラクティブ学習要素
- type: "Quiz"
  props:
    variant: "single_choice|multiple_choice|categorization"
    question: "問題文"
    options: ["選択肢1", "選択肢2"]
    correct: [0] # インデックス
    explanation: "解説"

# 外部コンテンツ埋め込み
- type: "Embed"
  props:
    source: "path/to/file.html"
    width: "100%"
    height: "400px"
    responsive: true
```

#### 2.2.3. Table Engine (`html_table`, `csv_processor`)

**表組みコンポーネント:**
```yaml
- type: "Table"
  props:
    variant: "basic|sortable|filterable|paginated"
    data:
      headers: ["列1", "列2", "列3"]
      rows: [[val1, val2, val3], [val4, val5, val6]]
    style:
      theme: "minimal|striped|bordered"
      responsive: true
    features:
      sortable: true
      filterable: ["列1", "列2"]
      pageSize: 10
```

### 2.3. 合成コンポーネント（Composite Components）

複数の基本コンポーネントを組み合わせた高レベルコンポーネント：

```yaml
# ダッシュボード風レイアウト
- type: "Dashboard"
  props:
    layout: "grid|flex"
    columns: 2
    components:
      - type: "DataVisualization"
        props: {...}
      - type: "Table" 
        props: {...}

# 学習セクション
- type: "LearningSection"
  props:
    title: "セクションタイトル"
    components:
      - type: "Paragraph"
        props: {...}
      - type: "CodeBlock"
        props: {...}
      - type: "Quiz"
        props: {...}

# 比較表示
- type: "Comparison" 
  props:
    variant: "side_by_side|tabbed"
    items:
      - title: "項目A"
        components: [...]
      - title: "項目B" 
        components: [...]
```

## 3. 統一レンダリングエンジン設計

### 3.1. ComponentRenderer基底クラス

```python
class ComponentRenderer:
    """すべての描画エンジンの基底クラス"""
    
    def render(self, spec: Dict) -> str:
        """統一エントリーポイント"""
        pass
    
    def render_component(self, component: Dict) -> Any:
        """個別コンポーネントレンダリング"""
        pass
    
    def get_supported_components(self) -> List[str]:
        """サポートするコンポーネント一覧"""
        pass
```

### 3.2. エンジン別実装

```python
class MatplotlibRenderer(ComponentRenderer):
    def render_component(self, component):
        component_type = component['type']
        props = component['props']
        
        if component_type == 'Shape':
            return self._render_shape(props)
        elif component_type == 'Text':
            return self._render_text(props)
        # ...
        
class PlotlyRenderer(ComponentRenderer):
    def render_component(self, component):
        # Plotly固有の実装
        pass

class MarkdownRenderer(ComponentRenderer):
    def render_component(self, component):
        # Markdown生成の実装
        pass
```

### 3.3. ファクトリパターン

```python
class RendererFactory:
    """適切なレンダラーを選択"""
    
    @staticmethod
    def get_renderer(engine: str) -> ComponentRenderer:
        if engine == 'matplotlib':
            return MatplotlibRenderer()
        elif engine == 'plotly':
            return PlotlyRenderer()
        elif engine == 'markdown':
            return MarkdownRenderer()
        # ...
```

## 4. YAML仕様例

### 4.1. 複合グラフダッシュボード

```yaml
type: "content_block"
engine: "plotly"
filename: "dashboard"
config:
  title: "システム監視ダッシュボード"
  layout:
    grid: [2, 2]
    spacing: 10
components:
  - type: "DataVisualization"
    props:
      variant: "line"
      position: [0, 0]
      data:
        x: [1, 2, 3, 4, 5]
        y: [10, 11, 12, 11, 10]
      style:
        color: "#1f77b4"
        title: "CPU使用率"
  
  - type: "DataVisualization"  
    props:
      variant: "bar"
      position: [0, 1]
      data:
        x: ["プロセス1", "プロセス2", "プロセス3"]
        y: [23, 45, 56]
      style:
        colors: ["#ff7f0e", "#2ca02c", "#d62728"]
        title: "メモリ使用量"
        
  - type: "Interactive"
    props:
      variant: "slider"
      position: [1, 0]
      range: [0, 100]
      step: 1
      defaultValue: 50
      label: "スケール調整"
      binding: "all_charts"
      
  - type: "Table"
    props:
      position: [1, 1]
      data:
        headers: ["時刻", "ステータス", "値"]
        rows: [
          ["10:00", "正常", "98%"],
          ["10:01", "警告", "85%"]
        ]
      features:
        sortable: true
        maxHeight: "200px"
```

### 4.2. インタラクティブ学習コンテンツ

```yaml
type: "content_block"
engine: "markdown"
filename: "chapter_01"
config:
  title: "第1章: プログラミング基礎"
  toc: true
components:
  - type: "Heading"
    props:
      level: 1
      content: "変数とデータ型"
      
  - type: "Paragraph"
    props:
      content: "プログラミングにおいて**変数**は重要な概念です。"
      terms:
        "変数": "データを格納するためのメモリ領域の名前"
      enableTooltips: true
      
  - type: "Tabs"
    props:
      tabs:
        "Python例":
          - type: "CodeBlock"
            props:
              language: "python"
              content: |
                x = 10
                name = "太郎"
                print(f"こんにちは{name}さん")
        "JavaScript例":
          - type: "CodeBlock" 
            props:
              language: "javascript"
              content: |
                let x = 10;
                const name = "太郎";
                console.log(`こんにちは${name}さん`);
                
  - type: "Quiz"
    props:
      variant: "single_choice"
      question: "Pythonで文字列を格納する変数の正しい書き方は？"
      options:
        - "name = 太郎"
        - "name = '太郎'"
        - "name = <太郎>"
        - "name := 太郎"
      correct: [1]
      explanation: "Pythonでは文字列を一重引用符(')または二重引用符(\")で囲む必要があります。"
      
  - type: "Embed"
    props:
      source: "assets/interactive_demo.html"
      height: "300px"
      title: "インタラクティブデモ"
```

## 5. 実装ロードマップ

### Phase 1: コア統一レンダリングシステム
1. ComponentRenderer基底クラス実装
2. RendererFactory実装
3. 基本コンポーネント（Shape, Text, Paragraph, Heading）対応

### Phase 2: 既存エンジン統合
1. 既存ChartGenerator→MatplotlibRenderer移行
2. 既存DocumentBuilder→MarkdownRenderer移行  
3. 既存TableGenerator→TableRenderer移行

### Phase 3: 新エンジン追加
1. PlotlyRenderer実装
2. D3jsRenderer実装（将来）
3. HTMLRenderer実装

### Phase 4: 合成コンポーネント
1. Dashboard, LearningSection等の高レベルコンポーネント実装
2. テンプレート機能拡張
3. 動的コンテンツ生成対応

## 6. 拡張性担保

### 6.1. カスタムコンポーネント追加方法

```python
# カスタムコンポーネントの定義例
class CustomChartComponent(BaseComponent):
    type_name = "CustomChart"
    
    def render(self, props, renderer):
        # カスタム描画ロジック
        return custom_chart_html
        
# レンダラーに登録
renderer.register_component(CustomChartComponent)
```

### 6.2. 新しい描画エンジン追加

```python
class NewEngineRenderer(ComponentRenderer):
    def render_component(self, component):
        # 新エンジン固有の描画ロジック
        pass
        
# ファクトリに登録  
RendererFactory.register_engine("new_engine", NewEngineRenderer)
```

## 7. 後方互換性

既存の個別メソッド（`create_simple_line_chart`等）は、内部で新しいコンポーネントシステムを呼び出すラッパーとして継続サポートし、段階的移行を可能にします。

```python
def create_simple_line_chart(self, data, x_col, y_col, title, xlabel, ylabel, **kwargs):
    """既存APIの後方互換ラッパー"""
    spec = {
        "type": "content_block",
        "engine": "matplotlib",
        "components": [{
            "type": "DataVisualization",
            "props": {
                "variant": "line",
                "data": {"x": data[x_col], "y": data[y_col]},
                "style": {"title": title, "xlabel": xlabel, "ylabel": ylabel}
            }
        }]
    }
    return self.render_spec(spec)
```

---

この設計により、PROJECT_BLUEPRINT.mdの三大原則（YAML駆動、関心の分離、Core機能集約）を完全に満たしつつ、React風の直感的で拡張性の高いコンポーネントシステムを実現できます。
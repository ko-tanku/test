# 設計思想：宣言的UIとコンポーネントベース描画

## 1. 基本方針

本プロジェクトにおける図や表などの視覚的要素の生成は、「宣言的（Declarative）」なアプローチを採用する。

これは、「どのように（How）描画するか」を手続き的にコードで記述するのではなく、「何を（What）描画したいか」をデータ（YAML）で定義することを目指すものである。

## 2. コアコンセプト

### 2.1. 宣言的インターフェース

すべての描画は、その最終的な見た目を定義した単一の仕様（`spec`）オブジェクトを起点とする。開発者や教材作成者は、Pythonコードを直接編集することなく、この`spec`をYAMLファイルで記述することで、目的の図を生成する。

### 2.2. コンポーネントベース描画

複雑な図は、単純な「描画コンポーネント」のリスト（配列）として表現する。Pythonの描画エンジンは、このコンポーネントリストをループ処理し、各コンポーネントを順番にキャンバスへ追加していくだけの、単純で汎用的な役割に徹する。

## 3. 実装アーキテクチャ

### 3.1. YAMLにおける仕様（`spec`）の構造

`spec`は、図の全体設定を行う`config`と、描画要素のリストである`components`から構成される。

#### 3.1.1. 基本描画コンポーネント

`components`リストには、以下の基本コンポーネント（プリミティブ）を自由に組み合わせることができる。

*   **`type: "shape"`**: 図形を描画する。
    *   `params`:
        *   `shape_type`: `'rectangle'`, `'circle'`, `'polygon'` などを指定。
        *   `position`: `[x, y]` 形式で中心座標を指定。
        *   `size`: `[width, height]` や `radius` など、図形に応じたサイズを指定。
        *   `color`, `edge_color`, `line_width`, `hatch` (ハッチング) などのスタイル。

*   **`type: "path"`**: 線や矢印を描画する。
    *   `params`:
        *   `points`: `[[x1, y1], [x2, y2], ...]` 形式で頂点のリストを指定。
        *   `color`, `line_width`, `line_style` (`'solid'`, `'dashed'`) などのスタイル。
        *   `arrow_style`: 矢印のスタイルを指定（例: `'->'`）。
        *   `path_type`: `'line'` (直線), `'arc'` (円弧) などを指定可能にし、曲線にも対応。

*   **`type: "text"`**: 文字を描画する。
    *   `params`:
        *   `content`: 表示する文字列。
        *   `position`: `[x, y]` 形式で表示位置を指定。
        *   `font_size`, `color`, `horizontal_alignment`, `vertical_alignment` などのスタイル。

*   **`type: "sine_wave"`**: 周期的な波形を生成する。
    *   `params`:
        *   `start_time`, `end_time`, `amplitude`, `frequency`, `offset` などの波形パラメータ。

#### 3.1.2. 具体的な記述例

「汎用OSとリアルタイムOSの比較図」は、この構造を用いて以下のように表現できる。

```yaml
type: "diagram"
engine: "matplotlib"
filename: "os-comparison"
config:
  title: "汎用OSとリアルタイムOS"
  size: [10, 6]
  xlim: [0, 10]
  ylim: [0, 10]
components:
  # --- 左側：汎用OS ---
  - type: "text"
    params:
      content: "汎用OS"
      position: [2.5, 9.5]
      font_size: 16
  - type: "shape"
    params:
      shape_type: "polygon"
      points: [[0.5, 8], [4.5, 8], [3.5, 2], [1.5, 2]]
      color: "#A9CCE3"
      alpha: 0.8
  - type: "text"
    params:
      content: "処理量：大"
      position: [1.5, 4]
      color: "darkgreen"
  - type: "path"
    params:
      points: [[2.5, 2], [2.5, 0.5]]
      arrow_style: "-|>"
      line_width: 2
  # ... 他の汎用OSのコンポーネント ...

  # --- 右側：リアルタイムOS ---
  - type: "text"
    params:
      content: "リアルタイムOS"
      position: [7.5, 9.5]
      font_size: 16
  - type: "shape"
    params:
      shape_type: "circle"
      position: [7.5, 5]
      radius: 3
      color: "#FAD7A0"
      alpha: 0.5
  - type: "shape"
    params:
      shape_type: "rectangle"
      position: [7.5, 8] # 上のタスク
      size: [1, 1]
      color: "#E59866"
  - type: "path"
    params:
      points: [[7.5, 5], [7.5, 7.5]] # 中心から上のタスクへ
      arrow_style: "->"
  # ... 他のリアルタイムOSのコンポーネント ...
```

### 3.2. Python (`core`) における描画エンジンの責務

-   **公開I/F**: ライブラリ（エンジン）ごとに、`spec`を引数に取る単一の公開関数を持つ（例: `create_matplotlib_chart(spec)`)。
-   **内部実装**: 公開関数は、`spec.components`リストをループ処理する。リスト内の各コンポーネントの`type`に応じて、対応するプライベートな描画関数（例: `_draw_shape(params)`, `_draw_path(params)`）を呼び出すディスパッチャとして機能する。
-   **安全性**: プライベート関数は、渡された`params`が描画に十分か検証する。

## 4. この設計がもたらす利点

-   **真の汎用性**: 基本的な描画プリミティブを組み合わせることで、データグラフからカスタムダイアグラムまで、あらゆる種類の図を同じ枠組みで生成できる。
-   **安全性と信頼性**: 教材作成者はPythonコードに触れないため、コーディングミスによる実行時エラーを防げる。
-   **再利用性と拡張性**: 新しい図は、既存のコンポーネントを組み合わせることで容易に作成できる。新しい種類のコンポーネントが必要になった場合も、対応するプライベート関数を追加するだけでシステム全体を拡張できる。
-   **一貫性**: すべての描画要素が同じエンジンとスタイル設定を通過するため、プロジェクト全体で統一感のあるデザインを維持できる。
-   **メンテナンス性**: 描画ロジックの修正は、各コンポーネントを描画するプライベート関数に集約されるため、修正が容易になる。

# src/core 機能仕様書

## 1. はじめに

このドキュメントは、**2025年8月26日時点**での`src/core`フレームワークが提供する全機能の仕様と、その使い方（YAML構造）を定義する公式な仕様書です。利用者はこのドキュメントを参照することで、教材コンテンツのYAMLファイルを正確に記述できます。

### 1.1 ドキュメントの更新履歴
- **2025年8月26日**: 既存機能の改善・正常化を反映し、現在の実装状況に合わせて仕様を更新
- **注意**: 一部機能（Mermaid表示、クイズの動作など）については現在改善作業中です

---

## 2. 基本的な考え方

教材のコンテンツは、章ごとのYAMLファイル（例: `chapter1.yml`）に記述します。各YAMLファイルは、トップレベルに`title`キーと`sections`キーを持ちます。

- `title` (必須, String): そのページのH1見出しとなるタイトル。
- `sections` (必須, List): ページ内のセクションのリスト。

各セクションは`title`キーと`contents`キーを持ちます。

- `title` (必須, String): そのセクションのH2見出しとなるタイトル。
- `contents` (必須, List): そのセクションに含まれる「コンテンツブロック」のリスト。

```yaml
title: "章のタイトル"
sections:
  - title: "セクションのタイトル"
    contents:
      # ↓ここに後述するコンテンツブロックを記述していく
      - type: text
        text: "..."
```

---

## 3. コンテンツブロック仕様

`contents`リストの中には、`type`キーを持つ辞書を記述します。`type`キーの値によって、そのブロックがどの機能を呼び出すかが決まります。

### 3.1. 基本要素

#### `type: heading`
- **説明:** セクション内の見出し（H3〜H6）を表現します。
- **キー詳細:**
    - `type` (必須, String): `"heading"` を指定します。
    - `level` (必須, Integer): 見出しレベル。`3`から`6`までの整数を指定します。
    - `text` (必須, String): 見出しとして表示するテキスト。
- **使用例:**
    ```yaml
    - type: heading
      level: 3
      text: "これはレベル3の見出しです"
    ```

#### `type: text`
- **説明:** 通常の段落テキストを表現します。
- **キー詳細:**
    - `type` (必須, String): `"text"` を指定します。
    - `text` (必須, String): 表示するテキスト。Markdown記法（`**太字**`や`*イタリック*`など）が利用可能です。
    - `terms` (任意, String): このテキストブロックに適用したい**用語セットのキー**を指定します。ここで指定したキーに基づき、`KnowledgeManager`が管理する用語の中から合致する単語に自動でツールチップが付与されます。現在の実装では、主に章のタイトル（例: `"第1章"`）などをキーとして利用することを想定しています。
- **使用例:**
    ```yaml
    - type: text
      text: "専門用語の Core にはツールチップが表示されます。"
      terms: "第1章"
    ```

#### `type: list`
- **説明:** 順序付きリストまたは順不同リストを表現します。
- **キー詳細:**
    - `type` (必須, String): `"list"` を指定します。
    - `list_type` (必須, String): `"ordered"`（順序付き）または `"unordered"`（順不同）を指定します。
    - `items` (必須, List[String]): リストの各項目を文字列のリストで指定します。
- **使用例:**
    ```yaml
    - type: list
      list_type: "unordered"
      items:
        - "りんご"
        - "ごりら"
    ```

#### `type: quote`
- **説明:** 引用ブロックを表現します。
- **キー詳細:**
    - `type` (必須, String): `"quote"` を指定します。
    - `text` (必須, String): 引用文。`\n`による改行も反映されます。
- **使用例:**
    ```yaml
    - type: quote
      text: "これは引用文です。\n改行も可能です。"
    ```

#### `type: code`
- **説明:** シンタックスハイライト付きのコードブロックを表現します。
- **キー詳細:**
    - `type` (必須, String): `"code"` を指定します。
    - `lang` (任意, String): 言語を指定します。デフォルトは`"python"`です。
    - `code` (必須, String): 表示するコード。
- **使用例:**
    ```yaml
    - type: code
      lang: "python"
      code: |
        def hello():
            print("Hello, World!")
    ```

#### `type: horizontal_rule`
- **説明:** 水平線を挿入します。
- **キー詳細:**
    - `type` (必須, String): `"horizontal_rule"` を指定します。
- **使用例:**
    ```yaml
    - type: horizontal_rule
    ```

### 3.2. リッチコンテンツ要素

#### `type: admonition`
- **説明:** ノート、警告、ヒントなどの囲み記事（Admonition）を表現します。利用可能なアイコンの一覧は、巻末の**付録**を参照してください。
- **キー詳細:**
    - `type` (必須, String): `"admonition"` を指定します。
    - `admonition_type` (必須, String): 種類を指定します。許容値: `note`, `tip`, `warning`, `danger`, `question`, `info`, `success`など。
    - `title` (必須, String): Admonitionのタイトル。
    - `text` (必須, String): Admonitionの本文。
    - `collapsible` (任意, Boolean): `true`にすると折りたたみ可能になります。デフォルトは`false`です。
- **使用例:**
    ```yaml
    - type: admonition
      admonition_type: "note"
      title: "ノート"
      text: "これはノートです。"
      collapsible: true
    ```

#### `type: tabs`
- **説明:** タブで切り替え可能なコンテンツを表現します。
- **キー詳細:**
    - `type` (必須, String): `"tabs"` を指定します。
    - `tabs_data` (必須, Dict[String, String]): キーをタブのタイトル、値をタブのコンテンツとする辞書を指定します。
- **使用例:**
    ```yaml
    - type: tabs
      tabs_data:
        "Pythonコード": "`print('Hello')`"
        "実行結果": "Hello"
    ```

#### `type: mermaid`
- **説明:** Mermaid.jsを利用して、テキストから図表を生成します。
- **現在の状況:** ⚠️ **改善作業中** - メソッドは実装済みですが、実際の図表レンダリングが正常に動作しない場合があります。`mkdocs-mermaid2-plugin`の設定やJavaScriptライブラリの読み込み順序を調査中です。
- **キー詳細:**
    - `type` (必須, String): `"mermaid"` を指定します。
    - `title` (任意, String): 図表の上に表示されるタイトル。
    - `graph` (必須, String): Mermaid構文で記述されたグラフ定義。
- **使用例:**
    ```yaml
    - type: mermaid
      title: "フローチャート"
      graph: |
        graph TD;
            A --> B;
    ```

### 3.3. 外部コンポーネントと動的生成

#### `type: image`
- **説明:** ローカルの画像ファイルをページに埋め込みます。
- **キー詳細:**
    - `type` (必須, String): `"image"` を指定します。
    - `path` (必須, String): `docs/`ディレクトリからの相対パスで画像ファイルを指定します。
    - `alt_text` (任意, String): 画像の代替テキスト。
    - `title` (任意, String): 画像のタイトル。
- **使用例:**
    ```yaml
    - type: image
      path: "assets/images/sample.png"
      alt_text: "サンプル画像"
    ```

#### `type: html_component`
- **説明:** **既に存在する**グラフやテーブルなど、別ファイルとして生成されたHTMLコンポーネントをiframeで埋め込みます。動的に生成する場合は`type: chart`や`type: table`を使用してください。
- **キー詳細:**
    - `type` (必須, String): `"html_component"` を指定します。
    - `path` (必須, String): `docs/`ディレクトリからの相対パスでHTMLファイルを指定します。
    - `width` (任意, String): iframeの幅。デフォルトは`"100%"`。
    - `height` (任意, String): iframeの高さを固定したい場合に指定します（例: `"500px"`）。**デフォルトは`None`（指定なし）で、その場合、コンポーネントの中身に応じてJavaScriptが最適な高さを自動調整します。**
- **使用例:**
    ```yaml
    - type: html_component
      path: "test_material/charts/my_chart.html"
    ```

#### `type: chart`
- **説明:** YAMLで定義したデータと設定に基づき、静的またはインタラクティブなグラフをHTMLファイルとして動的に生成し、ページに埋め込みます。
- **現在の状況:** ⚠️ **一部表示問題調査中** - 3章の図表が表示されない問題、5章のカスタム図表で'str' object is not callable エラーを修正中です。
- **キー詳細:**
    - `type` (必須, String): `"chart"` を指定します。
    - `chart_type` (必須, String): グラフの種類。`"line"`, `"bar"`, `"pie"`, `"scatter"`, `"animation"`, `"interactive"` など。
    - `data` (任意, Dict): グラフの元となるデータを直接記述します。
    - `data_source` (任意, String): `data/`配下のCSVファイル名を指定して、外部データを読み込みます。`data`と`data_source`はどちらか一方を指定します。
    - `config` (必須, Dict): グラフのタイトル、軸ラベル、ファイル名、インタラクティブ設定などを格納する辞書。
        - `interactive_type` (任意, String): `chart_type`が`"interactive"`の時に、詳細な種類を指定します。例: `"slider"`, `"dropdown_filter"`など。
- **使用例 (棒グラフ):**
    ```yaml
    - type: chart
      chart_type: bar
      data:
        x: ["A", "B", "C"]
        y: [10, 20, 15]
      config:
        title: "サンプル棒グラフ"
        xlabel: "カテゴリ"
        ylabel: "数値"
        filename: "sample_bar_chart"
    ```

#### `type: table`
- **説明:** YAMLで定義したデータに基づき、整形されたHTMLテーブルを動的に生成し、ページに埋め込みます。
- **現在の状況:** ⚠️ **表示範囲調整中** - 2章のテーブルで表示範囲が狭すぎる問題を改善中です。レスポンシブ対応やiframeの高さ自動調整を見直しています。
- **キー詳細:**
    - `type` (必須, String): `"table"` を指定します。
    - `table_type` (必須, String): テーブルの種類。`"basic"`, `"comparison"`, `"wide"`（横スクロール）など。
    - `title` (任意, String): テーブルの上に表示されるタイトル。
    - `headers` (必須, List[String]): 表のヘッダー（列名）のリスト。
    - `rows` (必須, List[List]): 表の各行のデータのリスト。
- **使用例 (基本テーブル):**
    ```yaml
    - type: table
      table_type: basic
      title: "製品比較"
      headers: ["製品名", "価格", "評価"]
      rows:
        - ["製品A", "1,000円", "★★★★☆"]
        - ["製品B", "1,200円", "★★★★★"]
    ```

### 3.4. インタラクティブコンテンツ

#### `type: exercises`
- **説明:** 難易度表示と折りたたみ可能な解答・解説を持つ演習問題を生成します。
- **キー詳細:**
    - `type` (必須, String): `"exercises"` を指定します。
    - `question_data` (必須, Dict):
        - `difficulty` (必須, String): 難易度。許容値: `"easy"`, `"medium"`, `"hard"`。
        - `question` (必須, String): 問題文。
        - `answer` (必須, String): 解答。
        - `explanation` (任意, String): 解説。
- **使用例:**
    ```yaml
    - type: exercises
      question_data:
        difficulty: "easy"
        question: "1+1は？"
        answer: "2"
        explanation: "基本的な算数です。"
    ```

#### クイズ (`single_choice_quiz`など)
- **説明:** 各種クイズを生成します。データは外部の`quizzes.yml`で一元管理する方法と、コンテンツ内に直接記述する方法の2通りがあります。
- **現在の状況:** ⚠️ **改善作業中** - 特に単一選択クイズで動作しない場合があります。HTML生成、JavaScript(`quiz.js`)、YAMLデータ間の不整合を修正中です。
- **方法1: 外部ファイル参照（推奨）**
    - **キー詳細:**
        - `type` (必須, String): `"single_choice_quiz"`, `"multiple_choice_quiz"`, `"categorization_quiz"`のいずれかを指定します。
        - `quiz_id` (必須, String): `quizzes.yml`で定義したクイズの一意なID。
    - **使用例:**
        ```yaml
        # content/quizzes.yml側
        quizzes:
          - quiz_id: "scq_001"
            type: "single_choice_quiz"
            question: "問題文"
            options: ["選択肢1", "選択肢2"]
            correct: 0
            explanation: "解説文"

        # chapterN.yml側
        - type: single_choice_quiz
          quiz_id: "scq_001"
        ```
- **方法2: インライン記述**
    - **説明:** 小規模なクイズをコンテンツ内に直接定義する場合に便利です。
    - **キー詳細:**
        - `type` (必須, String): クイズの種類を指定します。
        - `quiz_data` (必須, Dict): クイズの全データ（問題、選択肢、正解など）を格納した辞書。キー構造は`quizzes.yml`の各要素と同じです。
    - **使用例:**
        ```yaml
        # chapterN.yml側
        - type: single_choice_quiz
          quiz_data:
            quiz_id: "inline_quiz_01" # このIDはページ内で一意であればOK
            question: "太陽系の惑星で、地球の隣にあるのは？"
            options:
              - "火星と金星"
              - "火星と木星"
              - "金星と水星"
            correct: 0
            explanation: "地球の内側には金星が、外側には火星があります。"
        ```

### 3.5. フレームワーク連携

#### `type: learning_object`
- **説明:** `src/learning_objects/`に配置された、再利用可能なコンテンツ部品をその場に展開します。
- **キー詳細:**
    - `type` (必須, String): `"learning_object"` を指定します。
    - `id` (必須, String): `src/learning_objects/`配下のYAMLファイル名（拡張子なし）を指定します。
- **使用例:**
    ```yaml
    - type: learning_object
      id: "sample_object"
    ```

#### `type: custom_generator`
- **説明:** `materials/[教材名]/generators/`配下に定義された、教材固有のPython関数を呼び出します。
- **キー詳細:**
    - `type` (必須, String): `"custom_generator"` を指定します。
    - `generator` (必須, String): `"[ファイル名].[関数名]"`の形式で指定します。
    - `params` (任意, Dict): 指定した関数にキーワード引数として渡すパラメータの辞書。
- **使用例:**
    ```yaml
    - type: custom_generator
      generator: "ascii_art_generator.generate"
      params:
        text: "GEMINI"
        filename: "gemini_art.png"
    ```

---

## 4. ナレッジ管理 (`knowledge_manager.py`)

教材横断的な情報（用語、FAQ、TIPS）は、`content/terms.yml`で一元管理します。`KnowledgeManager`がこのファイルを読み込み、用語集ページなどを自動生成します。

- **キー詳細:**
    - `terms` (List[Dict]): 用語のリスト。
        - `term` (必須, String): 用語名。
        - `definition` (必須, String): 定義文。
        - `category` (必須, String): 分類カテゴリ。
    - `faq` (List[Dict]): FAQのリスト。
        - `question` (必須, String): 質問。
        - `answer` (必須, String): 回答。
        - `category` (任意, String): 分類カテゴリ。
    - `tips` (List[Dict]): TIPSのリスト。
        - `title` (必須, String): ヒントのタイトル。
        - `content` (必須, String): ヒントの内容。
        - `category` (任意, String): 分類カテゴリ。
- **使用例:**
    ```yaml
    # content/terms.yml
    terms:
      - term: "Core"
        definition: "フレームワークの心臓部。"
        category: "基本概念"
faq:
      - question: "この教材の目的は？"
        answer: "Core機能のテストです。"
        category: "プロジェクトについて"
tips:
      - title: "デバッグのヒント"
        content: "ブラウザの開発者ツールを確認しましょう。"
        category: "開発"
    ```

---

## 5. アセット管理 (`asset_generator.py`)

`AssetGenerator`は、教材サイトの見た目やインタラクティブな動作を制御するCSS（スタイルシート）やJavaScriptファイルを動的に生成・管理するバックエンド機能です。利用者が直接YAMLで操作することはありませんが、フレームワークの挙動を理解する上で重要な役割を果たします。

- **主な機能:**
    - **テーマCSSの自動生成**: `docs/`ディレクトリに`custom.css`（基本テーマ）、`custom_dark.css`（ダークテーマ）、`custom_high_contrast.css`（ハイコントラストテーマ）などのCSSファイルを自動で生成します。これにより、利用者はテーマ切り替え機能の恩恵を受けることができます。
    - **JavaScriptの統合**: `docs/interactive.js`や`docs/quiz.js`など、サイトのインタラクティブ機能（クイズ、ツールチップなど）を実現するためのJavaScriptファイルを生成・配置します。
    - **アセットの一元管理**: 生成されたすべてのアセットの情報は`docs/asset_manifest.json`に記録され、管理されます。

- **利用者への影響:**
    - 利用者は、CSSやJavaScriptファイルを手動で`docs`ディレクトリに配置する必要はありません。システムが教材の内容に応じて最適なアセットを自動で生成します。
    - 教材固有のスタイルやスクリプトを追加したい場合は、`src/materials/[教材名]/templates/`配下にJinja2テンプレート（`custom.css.jinja`など）を配置することで、自動生成されるファイルに内容を追記することが可能です。

---

## 6. サイト構成管理 (`mkdocs_manager.py`)

`MkDocsManager`は、静的サイトジェネレータであるMkDocsの設定ファイル`mkdocs.yml`を動的に生成・更新するバックエンド機能です。サイト全体のナビゲーション、テーマ設定、プラグインの有効化などを一元管理します。

- **主な機能:**
    - **ナビゲーションの自動構築**: `main.py`などの実行スクリプトから渡された教材の構造情報に基づき、`mkdocs.yml`の`nav`セクション（サイトの目次）を自動で生成します。
    - **設定の自動化**: サイト名、テーマ、Markdown拡張機能、プラグイン（検索、Mermaid図表など）といった、MkDocsの基本的な設定を自動で行います。
    - **アセットの紐付け**: `AssetGenerator`によって生成されたCSSやJavaScriptファイルを`extra_css`および`extra_javascript`設定に自動で追加し、サイト全体で読み込まれるようにします。

- **利用者への影響:**
    - 利用者は、基本的に`mkdocs.yml`を手動で編集する必要はありません。教材の追加や構成の変更は、Pythonの実行スクリプト側で行い、`MkDocsManager`がそれを設定ファイルに反映します。
    - サイト名やリポジトリURLなど、プロジェクト全体の設定をカスタマイズしたい場合は、`MkDocsManager`を呼び出す際にカスタム設定の辞書を渡すことで、ベース設定を上書きできます。

---

## 7. 付録

### 7.1. 利用可能なアイコン一覧

`admonition`などで利用できるアイコンの一覧です。`admonition_type`に以下の指定名を使用することで、対応するアイコンがタイトル横に表示されます。

| カテゴリ | 指定名 | アイコンプレビュー | アイコンID |
|:---|:---|:---:|:---|
| システム・ハードウェア関連 | `memory` | :material-memory: | `memory` |
| | `speed` | :material-speed: | `speed` |
| | `cpu` | :material-developer_board: | `developer_board` |
| | `storage` | :material-storage: | `storage` |
| | `device` | :material-devices: | `devices` |
| | `hardware` | :material-build: | `build` |
| | `circuit` | :material-cable: | `cable` |
| 学習・情報関連 | `help` | :material-help: | `help` |
| | `info` | :material-info: | `info` |
| | `question` | :material-help_outline: | `help_outline` |
| | `tip` | :material-lightbulb_outline: | `lightbulb_outline` |
| | `warning` | :material-warning: | `warning` |
| | `error` | :material-error: | `error` |
| | `success` | :material-check_circle: | `check_circle` |
| ナビゲーション・UI関連 | `home` | :material-home: | `home` |
| | `menu` | :material-menu: | `menu` |
| | `settings` | :material-settings: | `settings` |
| | `search` | :material-search: | `search` |
| | `bookmark` | :material-bookmark: | `bookmark` |
| | `favorite` | :material-favorite: | `favorite` |
| 学習コンテンツ関連 | `book` | :material-book: | `book` |
| | `school` | :material-school: | `school` |
| | `quiz` | :material-quiz: | `quiz` |
| | `assignment` | :material-assignment: | `assignment` |
| | `grade` | :material-grade: | `grade` |
| | `library` | :material-local_library: | `local_library` |
| 技術・開発関連 | `code` | :material-code: | `code` |
| | `bug` | :material-bug_report: | `bug_report` |
| | `terminal` | :material-terminal: | `terminal` |
| | `api` | :material-api: | `api` |
| | `database` | :material-storage: | `storage` |
| | `cloud` | :material-cloud: | `cloud` |
| 組み込み・IoT関連 | `sensor` | :material-sensors: | `sensors` |
| | `microchip` | :material-memory: | `memory` |
| | `robot` | :material-precision_manufacturing: | `precision_manufacturing` |
| | `automation` | :material-autorenew: | `autorenew` |
| | `control` | :material-tune: | `tune` |
| | `signal` | :material-graphic_eq: | `graphic_eq` |

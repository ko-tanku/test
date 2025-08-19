# 学習プラットフォーム改善計画書（実装ガイド付き）

## 1. はじめに

このドキュメントは、現在の学習教材自動生成システムを、30種類以上の多様な教材に対応可能な、スケーラブルで高品質なプラットフォームへと進化させるための、具体的な実装手順を含む改善計画書です。この手順に沿うことで、迷うことなくシステムの改善を進めることができます。

---

## 2. 基本方針: 共通化と多様性を両立するアーキテクチャ

多数の教材追加を成功させる鍵は、**「共通化による整合性」**と**「個別実装による表現力」**を両立させるアーキテクチャです。その最適解として、以下の**3階層アプローチ**を基本方針とします。

- **第1階層（骨格）: テンプレートメソッド・パターン**
  - **役割:** 教材全体の**「処理フロー」**を共通化します。
- **第2階層（部品）: プラグイン・アーキテクチャ**
  - **役割:** 教材で必要となる**「特別な機能（コンテンツ部品）」**を追加します。
- **第3階層（味付け）: 設定ファイル**
  - **役割:** 共通部品の**「見た目や細かい挙動」**を調整します。

---

## 3. 完成イメージ: 改善後のプロジェクト構造

全ての改善が完了すると、プロジェクトは以下のような構造になります。

```
my-project/
├── data/                  # (新設) グラフ等で利用するCSVデータを格納
│   └── cpu_performance.csv
├── docs/                  # 生成されたサイトコンテンツ
├── src/
│   ├── core/              # プラットフォームの共通コア機能
│   │   ├── __init__.py
│   │   ├── base_content_manager.py # (改名) テンプレートメソッドの基底クラス
│   │   └── ...
│   ├── learning_objects/    # (新設) 教材間で再利用するコンテンツ部品
│   │   ├── pointer_intro.yml
│   │   └── quiz_about_cpu.yml
│   ├── materials/           # 各教材の個別実装
│   │   ├── c_language_intro/  # (例) C言語入門
│   │   │   ├── __init__.py
│   │   │   ├── config.py      # C言語入門固有の設定（色、フォント等）
│   │   │   ├── content/       # (新設) 章ごとのYAMLコンテンツ定義
│   │   │   │   ├── chapter1.yml
│   │   │   │   └── chapter2.yml
│   │   │   └── main.py        # C言語入門の生成実行スクリプト
│   │   └── ...              # (他の教材も同様の構造)
│   └── plugins/             # (新設) 教材固有の拡張機能
│       ├── __init__.py
│       ├── mermaid_plugin.py
│       └── music_notation_plugin.py
├── tests/                 # (新設) 自動テストコード
│   ├── core/
│   │   └── test_chart_generator.py
│   └── materials/
│       └── test_c_language_generation.py
├── mkdocs.yml             # MkDocs設定ファイル（自動生成）
├── requirements.txt       # 依存ライブラリ
└── IMPROVEMENT_PROPOSALS.md # このファイル
```

---

## 4. 改善ロードマップと実装手順

以下の3ステップで段階的に改善を進めます。

### ステップ1: 開発基盤の整備（最優先）

今後の開発を安全かつ効率的に進めるための土台を築きます。

#### 4.1. コンテンツとデータの外部ファイル化

- **目的:** コードとコンテンツを分離し、非エンジニアでも教材の作成・編集を容易にするため。
- **実装手順:**
    1.  プロジェクトルートに`data/`ディレクトリを作成します。
    2.  各教材ディレクトリ（例: `src/materials/test_material/`）内に`content/`ディレクトリを作成します。
    3.  **コンテンツのYAML化:** `test_material_contents.py`内の`_create_chapter1`のようなメソッドで定義されている章の内容を、`content/chapter1.yml`のようなYAMLファイルに移行します。
    4.  **データのCSV化:** Pythonコード内に直接記述されているグラフ用のデータ（例: `performance`リスト）を、`data/cpu_performance.csv`のようなCSVファイルに移行します。
    5.  **読込ロジックの実装:** `src/core/base_content_manager.py`（旧`content_manager.py`）を修正し、`PyYAML`と`pandas`ライブラリを使って、これらの外部ファイルを読み込み、コンテンツを生成するように変更します。
- **ファイル変更点:**
    - `[新規]` `data/`ディレクトリ、各教材下の`content/`ディレクトリと`*.yml`, `*.csv`ファイル
    - `[修正]` `src/core/base_content_manager.py`, 各教材の`contents.py`
    - `[追加]` `requirements.txt`に`pyyaml`, `pandas`を追加

#### 4.2. 自動テストスイートの導入

- **目的:** システムの品質を保証し、将来の機能追加やリファクタリングを安全に行えるようにするため。
- **実装手順:**
    1.  `requirements.txt`に`pytest`を追加し、`pip install -r requirements.txt`を実行します。
    2.  プロジェクトルートに`tests/`ディレクトリを作成します。
    3.  **ユニットテスト作成:** `tests/core/`に、`ChartGenerator`などのコア機能のテスト（例: `test_chart_generator.py`）を作成します。
    4.  **統合テスト作成:** `tests/materials/`に、特定の教材がYAML/CSVから正しくHTMLページ群を生成できるか、一連の流れをテストするコード（例: `test_test_material_generation.py`）を作成します。
- **ファイル変更点:**
    - `[新規]` `tests/`ディレクトリ以下のテストファイル
    - `[追加]` `requirements.txt`に`pytest`を追加

---

### ステップ2: 表現力の強化と教材拡充

整備された基盤の上で、新しい教材で必要となる表現機能を追加します。

#### 5.1. テキストベースでの図作成機能 (Mermaid.js)

- **目的:** フローチャートやシーケンス図の作成・修正コストを劇的に下げるため。
- **実装手順:**
    1.  `requirements.txt`に`mkdocs-mermaid2-plugin`を追加し、インストールします。
    2.  `src/core/mkdocs_manager.py`を修正し、`mkdocs.yml`を生成する際に、`plugins`セクションに`mermaid2`が追加されるようにします。
    3.  `src/core/document_builder.py`に、Mermaid構文をMarkdownに埋め込む`add_mermaid_block(graph_string)`メソッドを追加します。
- **ファイル変更点:**
    - `[修正]` `src/core/mkdocs_manager.py`, `src/core/document_builder.py`
    - `[追加]` `requirements.txt`に`mkdocs-mermaid2-plugin`を追加

#### 5.2. インタラクティブクイズの強化

- **目的:** 知識の応用力や整理能力を測る、より高度なアウトプットの機会を提供するため。
- **実装手順:**
    1.  **カテゴリ分けクイズ:**
        - `DocumentBuilder`に`add_categorization_quiz(quiz_data)`メソッドを追加し、YAML定義からドラッグ＆ドロップ用のHTMLを生成するようにします。
        - `docs/custom.js`（または新設する`quiz.js`）に、HTML5のDrag and Drop APIを使ったイベント処理と正誤判定ロジックを実装します。
    2.  **複数選択クイズ:**
        - `DocumentBuilder`のクイズ生成ロジックを修正し、YAMLの`correct_indices`が複数の場合にチェックボックス形式のHTMLを生成するようにします。
        - `custom.js`のクイズ判定ロジックを修正し、複数の答えが正しく選択されているかをチェックするように変更します。
- **ファイル変更点:**
    - `[修正]` `src/core/document_builder.py`, `docs/custom.js`

---

### ステップ3: プラットフォーム機能の高度化

複数の教材を有機的に連携させ、統合されたプラットフォームとしての価値を高めます。

#### 6.1. 複数教材の連携機能

- **目的:** 学習者が膨大な教材の中から、自分に合ったルートで効率的に学習を進められるようにするため。
- **実装手順:**
    1.  **ラーニングパス:** 各教材の`config.py`に`prerequisites: [...]`（前提教材）や`next_steps: [...]`（推奨次教材）といったメタデータを追加します。トップページ生成時に、全教材のconfigを読み込み、依存関係を解析してラーニングパスのHTMLを動的に生成します。
    2.  **横断検索:** MkDocsの標準検索では難しいため、フロントエンドでの対応を検討します。検索結果が表示された後、JavaScriptでDOMを操作し、各結果のURLから教材名を判別してラベルを追加します。
    3.  **総合用語集:** 新たな生成スクリプト`src/create_global_glossary.py`を作成します。このスクリプトは、全ての`materials`ディレクトリをスキャンして用語集データを集約し、一つの「総合用語集」ページを`docs/glossary.md`として生成します。
- **ファイル変更点:**
    - `[修正]` 各教材の`config.py`, トップページ生成ロジック, 検索結果表示JS
    - `[新規]` `src/create_global_glossary.py`

#### 6.2. 「学習オブジェクト」によるコンテンツ管理

- **目的:** コンテンツの再利用性を極限まで高め、効率的なコンテンツ制作と動的なコース生成を実現するため。
- **実装手順:**
    1.  `src/learning_objects`ディレクトリを新設し、トピック単位でコンテンツ部品をYAMLファイルとして格納します。（例: `pointer_intro.yml`）
    2.  各オブジェクトのYAMLには、内容に加えて`topic`, `difficulty`などのメタデータを記述します。
    3.  教材の章を定義するYAMLファイルでは、具体的な内容を記述する代わりに、`object_id: pointer_intro`のように学習オブジェクトIDを参照できるようにします。
    4.  `base_content_manager.py`は、このIDを見つけたら`learning_objects`ディレクトリから対応するファイルを読み込んで、その場に展開するようにロジックを修正します。
- **ファイル変更点:**
    - `[新規]` `src/learning_objects/`ディレクトリとオブジェクトファイル
    - `[修正]` `src/core/base_content_manager.py`, 各教材の`content/*.yml`

#### 6.3. 学習者からのフィードバックループ

- **目的:** 学習者の声を収集し、コンテンツを継続的に改善するサイクルを構築するため。
- **実装手順:**
    1.  `DocumentBuilder`の章末処理に、フィードバックフォームのHTMLを挿入するロジックを追加します。
    2.  フォームの送信先には、Google Formsや、無料のフォームバックエンドサービス（例: Formspree）を利用します。これにより、サーバーサイドの実装なしでフィードバックの収集が可能です。
- **ファイル変更点:**
    - `[修正]` `src/core/document_builder.py`
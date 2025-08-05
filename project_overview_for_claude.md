# プロジェクト引き継ぎ: Docusaurus学習資料プラットフォームの現状と課題

## 1. プロジェクトの目的

Docusaurusを基盤とした高品質なWeb学習資料を、効率的に作成・管理し、大量生産できるシステムを構築すること。

## 2. 現在のアーキテクチャ

データ駆動型アーキテクチャを採用しています。

1.  **コンテンツ作成 (人間)**: YAML/Markdownでコンテンツを記述。
2.  **JSONへの変換 (Pythonスクリプト)**: コンテンツをJSONデータに変換。
3.  **サイト構築と表示 (Docusaurus)**: JSONデータを元にDocusaurusがサイトを構築・表示。

このアーキテクチャは、プロジェクトの目的達成のための最適な方式です。

## 3. 達成済み事項

*   **コアデータ駆動アーキテクチャの確立**:
    *   YAML/MarkdownからJSONへの変換 (`scripts/courses/[course_id]/build.py`, `scripts/homepage/build.py`) が機能しています。
    *   `static/data/*.json` ファイルが正しく生成されています。
*   **`docusaurus.config.js` 自動設定スクリプトの開発**:
    *   `scripts/core/setup-course.js` (Node.js) と `scripts/core/setup_course.py` (Pythonラッパー) が機能しています。
    *   `comprehensive-test` コースの設定は、このスクリプトにより `docusaurus.config.js` に正しく追加されています。
*   **基本的な表示機能の確認**:
    *   Markdownのテキスト、リスト、コードブロック、テーブル、数式は、HTMLレベルで正しくレンダリングされています。
    *   `react-markdown` と関連プラグイン (`remark-gfm`, `remark-math`, `rehype-katex`) が機能しています。

## 4. 現在の作業フェーズの目的と `src` ディレクトリ内のコンポーネントの役割

**現在の作業フェーズの唯一の目的は、`src` ディレクトリ内のすべてのコンポーネントが期待通りに動作することを確認し、安定した基盤を確立することです。**

この目的を達成するため、`comprehensive-test` コースがテストスイートとして機能します。`comprehensive-test` コースは、`build.py` によるJSON生成、`docusaurus.config.js` の設定、および `npm run build` によるビルドが**成功しています**。

しかし、ブラウザでサイトを表示した際に、以下のコンポーネントが**期待されるインタラクティブな動作をしていません。**

### 4.1. `src` ディレクトリ内のコンポーネントと検証状況

`src` ディレクトリには以下のコンポーネントが存在します。これらのコンポーネントはすべて、その表示と機能が期待通りであるかを確認し、必要に応じて修正してください。

#### ページコンポーネント

*   **`src/pages/index.js`**: サイトのトップページ。
*   **`src/pages/roadmap.js`**: ロードマップページ。

#### コースレンダリングコンポーネント

*   **`src/components/ComprehensiveTestPage.js`**: `comprehensive-test` コースのページをレンダリングするメインコンポーネント。`prose_content` (Markdown) と `components` (カスタムコンポーネント) を受け取って表示します。

#### モジュールカードコンポーネント

*   **`src/components/ModuleCard/index.js`**: トップページで使用され、コースのカードを表示します。

#### UIコンポーネント (`src/components/ui/`)

*   **`src/components/ui/Accordion/index.js`**: 折りたたみ可能なセクション。
*   **`src/components/ui/Button/index.js`**: クリック可能なボタン。
*   **`src/components/ui/Card/index.js`**: 情報表示用のカード。
*   **`src/components/ui/CodeBlock/index.js`**: コードブロック表示。
*   **`src/components/ui/Icon/index.js`**: アイコン表示。
*   **`src/components/ui/Input.js`**: テキスト入力フィールド。
*   **`src/components/ui/MathDisplay.js`**: 数式表示 (現在 `react-katex` で処理されているため、使用状況を確認)。
*   **`src/components/ui/Modal/index.js`**: モーダルウィンドウ。
*   **`src/components/ui/Pagination.js`**: ページネーション。
*   **`src/components/ui/ProgressBar.js`**: 進捗バー。
*   **`src/components/ui/Table/index.js`**: 表形式データ表示。
*   **`src/components/ui/Tabs/index.js`**: タブ切り替え。
*   **`src/components/ui/Tooltip/index.js`**: ツールチップ表示。

#### インタラクティブコンポーネント (`src/components/interactive/`)

*   **`src/components/interactive/ClickToShow/index.js`**: クリックでコンテンツ表示/非表示。
*   **`src/components/interactive/DataFlowSimulator/index.js`**: データフローシミュレーション。
*   **`src/components/interactive/ImageHotspot/index.js`**: 画像ホットスポット。
*   **`src/components/interactive/InteractiveFlowchart/index.js`**: インタラクティブフローチャート。
*   **`src/components/interactive/KeyTerm/index.js`**: キーワード強調と定義表示。

#### 図表コンポーネント (`src/components/diagrams/`)

*   **`src/components/diagrams/SimpleChart/index.js`**: シンプルなグラフ表示。
*   **`src/components/diagrams/blocks/` 以下のコンポーネント**: (`Arrow.js`, `Draggable.js`, `Droppable.js`, `Edge.js`, `Hotspot.js`, `Icon.js`, `Node.js`, `ProgressStep.js`, `Slider.js`, `SvgShape.js`, `TextLabel.js`, `TimelineEvent.js`) - これらは通常、`diagrams/generators/` 以下のコンポーネントによって内部的に使用されるブロック要素です。
*   **`src/components/diagrams/generators/` 以下のコンポーネント**: (`DataFlowDiagram.js`, `FlowchartGenerator.js`, `GraphGenerator.js`, `ImageHighlighter.js`, `InteractiveSimulation.js`, `InteractiveTimeline.js`) - これらは複雑な図やシミュレーションを生成するコンポーネントです。

#### クイズコンポーネント (`src/components/quizzes/`)

*   **`src/components/quizzes/DragAndDropQuiz.js`**: ドラッグ&ドロップクイズ。
*   **`src/components/quizzes/Essay/index.js`**: 記述式クイズ。
*   **`src/components/quizzes/FillInTheBlank/index.js`**: 穴埋めクイズ。
*   **`src/components/quizzes/ImageHotspotQuiz.js`**: 画像ホットスポットクイズ。
*   **`src/components/quizzes/MatchingPairs.js`**: マッチングクイズ。
*   **`src/components/quizzes/MultipleChoice/index.js`**: 多肢選択クイズ。
*   **`src/components/quizzes/QuizWrapper/index.js`**: クイズのラッパーコンポーネント。
*   **`src/components/quizzes/blocks/` 以下のコンポーネント**: (`AnswerOption.js`, `FeedbackMessage.js`, `Question.js`) - これらはクイズコンポーネントによって内部的に使用されるブロック要素です。

#### レイアウトコンポーネント (`src/components/layout/`)

*   **`src/components/layout/Accordion.js`**: (重複、`ui/Accordion` と同じ機能か確認)
*   **`src/components/layout/Breadcrumbs.js`**: パンくずリスト。
*   **`src/components/layout/Callout/index.js`**: 強調表示ボックス。
*   **`src/components/layout/Card.js`**: (重複、`ui/Card` と同じ機能か確認)
*   **`src/components/layout/CheckList.js`**: チェックリスト。
*   **`src/components/layout/ComparisonTable/index.js`**: 比較表。
*   **`src/components/layout/FaqList/index.js`**: FAQリスト。
*   **`src/components/layout/FontSizeChanger.js`**: フォントサイズ変更。
*   **`src/components/layout/GlossaryList/index.js`**: 用語集リスト。
*   **`src/components/layout/LearningObjectives/index.js`**: 学習目標表示。
*   **`src/components/layout/LearningProgress.js`**: 学習進捗表示。
*   **`src/components/layout/ProgressiveLayout.js`**: プログレッシブレイアウト。
*   **`src/components/layout/ResponsiveIframe.js`**: レスポンシブiframe。
*   **`src/components/layout/SummaryBox/index.js`**: 要約ボックス。
*   **`src/components/layout/ThemeToggle.js`**: テーマ切り替え。

#### フック (`src/hooks/`)

*   **`src/components/hooks/` 以下のフック**: (`useAnimation.js`, `useDragAndDrop.js`, `useKeyNavigation.js`, `useLocalStorage.js`, `useMediaQuery.js`, `useResizeObserver.js`) - これらはUIコンポーネントによって内部的に使用されるロジックです。
*   **`src/hooks/useLearningProgress.js`**: 学習進捗管理フック。

## 5. Claudeへの依頼事項

上記の現状と課題を踏まえ、Claudeに以下の対応をお願いします。

### 5.1. 最優先事項: `src` ディレクトリ内のすべてのコンポーネントの機能実装と動作確認

*   `npm run serve` を実行し、ブラウザでサイトを開き、開発者ツール（F12）の**コンソールタブでエラーメッセージや警告を特定してください。**
*   `src/components/` ディレクトリ内のすべてのコンポーネントのソースコードを詳細にレビューし、`props` の受け取り方、内部ロジック、およびDocusaurusのコンポーネント実装パターンとの整合性を確認してください。
*   `static/data/comprehensive-test-pages.json` 内の各コンポーネントの `props` データが、対応するReactコンポーネントが期待する形式と完全に一致していることを確認してください。
*   上記4.1に列挙されたすべてのコンポーネントについて、期待される表示と動作が実現されるように実装を完了してください。

### 5.2. 将来のタスク: `it-embedded-intro` コースの有効化

**`src` ディレクトリ内のすべてのコンポーネントの機能が完全に安定し、動作確認が完了した後に、以下のタスクに進んでください。**

*   **`it-embedded-intro` コースの有効化**:
    *   `scripts/courses/it-embedded/` ディレクトリと、その中の `master.yaml`、`source/pages/` 以下のファイルを再作成し、`scripts/courses/it-embedded/build.py` を実行してJSONデータを生成してください。
    *   `scripts/core/setup_course.py it-embedded` を実行し、`docusaurus.config.js` に `it-embedded` コースのプラグインとナビゲーションバーの項目を自動で追加してください。
    *   `plugins/comprehensive-test-plugin` をコピーして、`it-embedded-intro-pages.json` を読み込む `plugins/it-embedded-plugin` を作成してください。
    *   サイトのビルドと確認を行い、`it-embedded-intro` コースがサイトに表示され、正しく機能することを確認してください。

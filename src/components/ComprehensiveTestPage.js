import React from 'react';
import Layout from '@theme/Layout';
import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import remarkGfm from 'remark-gfm';

// プロジェクトで使用する全てのカスタムコンポーネントを動的にインポートするためのマップ
const componentMap = {
  // 既存・新規コンポーネントのimportパスを網羅
  'layout/Callout': React.lazy(() => import('./layout/Callout')),
  'ui/CodeBlock': React.lazy(() => import('./ui/CodeBlock/index')),
  'ui/Button': React.lazy(() => import('./ui/Button')),
  'layout/SummaryBox': React.lazy(() => import('./layout/SummaryBox')),
  'ui/Accordion': React.lazy(() => import('./ui/Accordion')),
  'ui/Card': React.lazy(() => import('./ui/Card')),
  'ui/Tabs': React.lazy(() => import('./ui/Tabs/index')),
  'ui/ProgressBar': React.lazy(() => import('./ui/ProgressBar')),
  'ui/Table': React.lazy(() => import('./ui/Table')),
  'interactive/ClickToShow': React.lazy(() => import('./interactive/ClickToShow')),
  'interactive/ImageHotspot': React.lazy(() => import('./interactive/ImageHotspot')),
  'diagrams/SimpleChart': React.lazy(() => import('./diagrams/SimpleChart')),
  'interactive/InteractiveFlowchart': React.lazy(() => import('./interactive/InteractiveFlowchart')),
  'interactive/DataFlowSimulator': React.lazy(() => import('./interactive/DataFlowSimulator')),
  'interactive/KeyTerm': React.lazy(() => import('./interactive/KeyTerm')),
  'quizzes/MultipleChoice': React.lazy(() => import('./quizzes/MultipleChoice')),
  'quizzes/FillInTheBlank': React.lazy(() => import('./quizzes/FillInTheBlank')),
  'quizzes/Essay': React.lazy(() => import('./quizzes/Essay')),
  'quizzes/DragAndDropQuiz': React.lazy(() => import('./quizzes/DragAndDropQuiz')),
  'quizzes/MatchingPairs': React.lazy(() => import('./quizzes/MatchingPairs')),

  // 新規追加 - UIコンポーネント
  'ui/Input': React.lazy(() => import('./ui/Input')),
  'ui/Modal': React.lazy(() => import('./ui/Modal/index')),
  'ui/Pagination': React.lazy(() => import('./ui/Pagination')),
  'ui/Tooltip': React.lazy(() => import('./ui/Tooltip/index')),
  'ui/MathDisplay': React.lazy(() => import('./ui/MathDisplay')),

  // 新規追加 - レイアウトコンポーネント
  'layout/Breadcrumbs': React.lazy(() => import('./layout/Breadcrumbs')),
  'layout/CheckList': React.lazy(() => import('./layout/CheckList')),
  'layout/ComparisonTable': React.lazy(() => import('./layout/ComparisonTable')),
  'layout/FaqList': React.lazy(() => import('./layout/FaqList')),
  'layout/GlossaryList': React.lazy(() => import('./layout/GlossaryList')),
  'layout/LearningObjectives': React.lazy(() => import('./layout/LearningObjectives')),
  'layout/LearningProgress': React.lazy(() => import('./layout/LearningProgress')),
  'layout/ThemeToggle': React.lazy(() => import('./layout/ThemeToggle')),
  'layout/FontSizeChanger': React.lazy(() => import('./layout/FontSizeChanger')),
  'layout/ResponsiveIframe': React.lazy(() => import('./layout/ResponsiveIframe')),

  // 新規追加 - 図表コンポーネント (generators)
  'diagrams/generators/FlowchartGenerator': React.lazy(() => import('./diagrams/generators/FlowchartGenerator')),
  'diagrams/generators/ImageHighlighter': React.lazy(() => import('./diagrams/generators/ImageHighlighter')),
  'diagrams/generators/InteractiveTimeline': React.lazy(() => import('./diagrams/generators/InteractiveTimeline')),
  'diagrams/generators/InteractiveSimulation': React.lazy(() => import('./diagrams/generators/InteractiveSimulation')),

  // 新規追加 - 図表コンポーネント (blocks)
  'diagrams/blocks/Node': React.lazy(() => import('./diagrams/blocks/Node')),
  'diagrams/blocks/Slider': React.lazy(() => import('./diagrams/blocks/Slider')),
  'diagrams/blocks/TimelineEvent': React.lazy(() => import('./diagrams/blocks/TimelineEvent')),
  'diagrams/blocks/SvgShape': React.lazy(() => import('./diagrams/blocks/SvgShape')),
  'diagrams/blocks/TextLabel': React.lazy(() => import('./diagrams/blocks/TextLabel')),
  'diagrams/blocks/Hotspot': React.lazy(() => import('./diagrams/blocks/Hotspot')),
  'diagrams/blocks/Draggable': React.lazy(() => import('./diagrams/blocks/Draggable')),
  'diagrams/blocks/Droppable': React.lazy(() => import('./diagrams/blocks/Droppable')),

  // 新規追加 - クイズコンポーネント
  'quizzes/ImageHotspotQuiz': React.lazy(() => import('./quizzes/ImageHotspotQuiz')),
  'quizzes/blocks/Question': React.lazy(() => import('./quizzes/blocks/Question')),
  'quizzes/blocks/AnswerOption': React.lazy(() => import('./quizzes/blocks/AnswerOption')),
  'quizzes/blocks/FeedbackMessage': React.lazy(() => import('./quizzes/blocks/FeedbackMessage')),
  'quizzes/QuizWrapper': React.lazy(() => import('./quizzes/QuizWrapper')),

  // 新規追加 - 高度なUIコンポーネント（20個）
  'ui/Dropdown': React.lazy(() => import('./ui/Dropdown')),
  'ui/Badge': React.lazy(() => import('./ui/Badge')),
  'ui/Alert': React.lazy(() => import('./ui/Alert')),
  'ui/Spinner': React.lazy(() => import('./ui/Spinner')),
  'ui/Skeleton': React.lazy(() => import('./ui/Skeleton')),
  // 削除済み: Avatar, Rating
  'ui/Switch': React.lazy(() => import('./ui/Switch')),
  'ui/RadioGroup': React.lazy(() => import('./ui/RadioGroup')),
  'ui/CheckboxGroup': React.lazy(() => import('./ui/CheckboxGroup')),
  'ui/DatePicker': React.lazy(() => import('./ui/DatePicker')),
  'ui/TimePicker': React.lazy(() => import('./ui/TimePicker')),
  // 削除済み: ColorPicker
  'ui/RangeSlider': React.lazy(() => import('./ui/RangeSlider')),
  'ui/FileUpload': React.lazy(() => import('./ui/FileUpload')),
  'ui/SearchBox': React.lazy(() => import('./ui/SearchBox')),
  'ui/TagInput': React.lazy(() => import('./ui/TagInput')),
  'ui/NumberInput': React.lazy(() => import('./ui/NumberInput')),
  'ui/TextEditor': React.lazy(() => import('./ui/TextEditor')),
  // 削除済み: Calendar

  // 学習支援インタラクティブ機能
  'interactive/Timeline': React.lazy(() => import('./interactive/Timeline')),
  // 削除済み: Gallery, Carousel, Slideshow
  'interactive/ZoomImage': React.lazy(() => import('./interactive/ZoomImage')),
  'interactive/VideoPlayer': React.lazy(() => import('./interactive/VideoPlayer')),
  'interactive/AudioPlayer': React.lazy(() => import('./interactive/AudioPlayer')),
  'interactive/CodeRunner': React.lazy(() => import('./interactive/CodeRunner')),
  // 削除済み: Calculator, Counter, Timer, Stopwatch
  'interactive/BinaryConverter': React.lazy(() => import('./interactive/BinaryConverter')),

  // 学習支援機能
  'special/LazyLoad': React.lazy(() => import('./special/LazyLoad')),
  'special/StickyHeader': React.lazy(() => import('./special/StickyHeader')),
  'special/BackToTop': React.lazy(() => import('./special/BackToTop')),
  'special/PrintView': React.lazy(() => import('./special/PrintView')),
  'special/FullscreenToggle': React.lazy(() => import('./special/FullscreenToggle')),

  // 学習支援ゲーム（削除済み）

  // 新規追加 - データ表示・分析（5個）
  'data/StatCard': React.lazy(() => import('./data/StatCard')),
  'data/MetricDisplay': React.lazy(() => import('./data/MetricDisplay')),
  'data/TrendChart': React.lazy(() => import('./data/TrendChart')),
  'data/DataTable': React.lazy(() => import('./data/DataTable')),
  'data/Dashboard': React.lazy(() => import('./data/Dashboard')),

  // 学習効果向上コンポーネント
  'learning/FlashcardSystem': React.lazy(() => import('./learning/FlashcardSystem')),
  'learning/KnowledgeCheck': React.lazy(() => import('./learning/KnowledgeCheck')),
  'learning/NoteTaking': React.lazy(() => import('./learning/NoteTaking')),
  'learning/BookmarkManager': React.lazy(() => import('./learning/BookmarkManager')),

  // 新規追加 - IT組込学習特化コンポーネント
  'layout/LearningPathIndicator': React.lazy(() => import('./layout/LearningPathIndicator')),
  'ui/SmartTooltip': React.lazy(() => import('./ui/SmartTooltip')),

  // Phase 1 - 既存フォルダの実装完成
  'ai/AIPromptTrainer': React.lazy(() => import('./ai/AIPromptTrainer')),
  'embedded/MemoryMapVisualizer': React.lazy(() => import('./embedded/MemoryMapVisualizer')),
  'embedded/LogicGateSimulator': React.lazy(() => import('./embedded/LogicGateSimulator')),
  'learning/AdaptiveLearningEngine': React.lazy(() => import('./learning/AdaptiveLearningEngine')),
  'learning/LearningProgressTracker': React.lazy(() => import('./learning/LearningProgressTracker')),
};

function ComprehensiveTestPage({ pageData }) {
  if (!pageData) {
    return (
      <Layout title="Page Not Found">
        <main className="container margin-vert--lg">
          <h1>Page Not Found</h1>
          <p>The requested page data could not be found.</p>
        </main>
      </Layout>
    );
  }

  const { title, description, prose_content, components } = pageData;

  return (
    <Layout title={title} description={description}>
      <main className="container margin-vert--lg">
        <article>
          {prose_content && (
            <ReactMarkdown
              remarkPlugins={[remarkMath, remarkGfm]}
              rehypePlugins={[rehypeKatex]}
              components={{
                table: ({ node, ...props }) => <table className="table" {...props} />,
                thead: ({ node, ...props }) => <thead {...props} />,
                tbody: ({ node, ...props }) => <tbody {...props} />,
                tr: ({ node, ...props }) => <tr {...props} />,
                th: ({ node, ...props }) => <th {...props} />,
                td: ({ node, ...props }) => <td {...props} />,
              }}
            >
              {prose_content}
            </ReactMarkdown>
          )}

          {components && components.map((comp, index) => {
            const Component = componentMap[comp.component];
            if (!Component) {
              console.warn(`Component not found for path: ${comp.component}`);
              return <p key={index}>Component not found: {comp.component}</p>;
            }
            // build.pyでpropsが整形済みのため、そのまま渡す
            return (
              <React.Suspense fallback={<div>Loading...</div>} key={index}>
                <Component {...comp.props} />
              </React.Suspense>
            );
          })}
        </article>
      </main>
    </Layout>
  );
}

export default ComprehensiveTestPage;
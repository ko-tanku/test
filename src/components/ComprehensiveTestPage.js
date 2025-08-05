import React from 'react';
import Layout from '@theme/Layout';
import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import remarkGfm from 'remark-gfm';

// プロジェクトで使用する全てのカスタムコンポーネントを動的にインポートするためのマップ
const componentMap = {
  'layout/Callout': React.lazy(() => import('./layout/Callout')),
  'ui/CodeBlock': React.lazy(() => import('./ui/CodeBlock')),
  'ui/Button': React.lazy(() => import('./ui/Button')),
  'layout/SummaryBox': React.lazy(() => import('./layout/SummaryBox')),
  'ui/Accordion': React.lazy(() => import('./ui/Accordion')),
  'ui/Card': React.lazy(() => import('./ui/Card')),
  'ui/Tabs': React.lazy(() => import('./ui/Tabs')),
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
import React from 'react';
import Layout from '@theme/Layout';
import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import remarkGfm from 'remark-gfm';
import homepageData from '@site/static/data/homepage.json';
import ModuleCard from '@site/src/components/ModuleCard';
import clsx from 'clsx';

// componentMap for dynamic component rendering
const componentMap = {
  'HomepageContent': ({ modules }) => (
    <div className="container" style={{ padding: '2rem 0' }}>
      <div className="row">
        {modules.map((module, idx) => (
          <ModuleCard key={idx} module={module} />
        ))}
      </div>
    </div>
  ),
};

function HomepageHeader() {
  return (
    <header className={clsx('hero hero--primary')} style={{ textAlign: 'center', padding: '4rem 0' }}>
      <div className="container">
        <h1 className="hero__title">{homepageData.title}</h1>
        <p className="hero__subtitle">{homepageData.description}</p>
      </div>
    </header>
  );
}

export default function Home() {
  const { prose_content, components } = homepageData;

  return (
    <Layout title={homepageData.title} description={homepageData.description}>
      <HomepageHeader />
      <main>
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
          return (
            <React.Suspense fallback={<div>Loading...</div>} key={index}>
              <Component {...comp.props} />
            </React.Suspense>
          );
        })}
      </main>
    </Layout>
  );
}

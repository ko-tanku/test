import React from 'react';
import katex from 'katex';
import 'katex/dist/katex.min.css';

export default function MathDisplay({ equation }) {
  const html = katex.renderToString(equation, {
    throwOnError: false,
  });

  return <span dangerouslySetInnerHTML={{ __html: html }} />;
}

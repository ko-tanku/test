import React, { useState } from 'react';
import styles from './styles.module.css';

export default function CodeBlock({ 
  code = '', 
  language = 'javascript',
  title,
  showLineNumbers = true,
  copyable = true,
  className = ''
}) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy code:', err);
    }
  };

  const formatCode = (code) => {
    return code.split('\n').map((line, index) => (
      <div key={index} className={styles.codeLine}>
        {showLineNumbers && (
          <span className={styles.lineNumber}>{index + 1}</span>
        )}
        <span className={styles.lineContent}>{line || ' '}</span>
      </div>
    ));
  };

  return (
    <div className={`${styles.codeBlock} ${className}`}>
      {(title || copyable) && (
        <div className={styles.codeHeader}>
          {title && <span className={styles.codeTitle}>{title}</span>}
          {copyable && (
            <button 
              onClick={handleCopy}
              className={styles.copyButton}
              title="コードをコピー"
            >
              {copied ? '✓ コピー済み' : '📋 コピー'}
            </button>
          )}
        </div>
      )}
      <div className={styles.codeContainer}>
        <pre className={`${styles.codeContent} language-${language}`}>
          <code>
            {showLineNumbers ? formatCode(code) : code}
          </code>
        </pre>
      </div>
    </div>
  );
}

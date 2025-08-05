import React, { useState, useMemo } from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

export default function GlossaryList({ title, terms = [], searchable = true, className }) {
  const [searchTerm, setSearchTerm] = useState('');
  
  const filteredTerms = useMemo(() => {
    if (!searchTerm) return terms;
    const search = searchTerm.toLowerCase();
    return terms.filter(item => 
      item.term.toLowerCase().includes(search) ||
      item.definition.toLowerCase().includes(search)
    );
  }, [terms, searchTerm]);

  return (
    <div className={clsx(styles.glossaryList, className)}>
      {title && (
        <h3 className={styles.glossaryTitle}>{title}</h3>
      )}
      
      {searchable && terms.length > 5 && (
        <div className={styles.searchContainer}>
          <input
            type="text"
            placeholder="用語を検索..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className={styles.searchInput}
            aria-label="用語検索"
          />
        </div>
      )}
      
      <div className={styles.glossaryContainer}>
        {filteredTerms.length === 0 ? (
          <div className={styles.noResults}>
            検索結果が見つかりませんでした。
          </div>
        ) : (
          filteredTerms.map((item, index) => (
            <div key={index} className={styles.glossaryItem}>
              <dt className={styles.glossaryTerm}>
                {item.term}
              </dt>
              <dd className={styles.glossaryDefinition}>
                {typeof item.definition === 'string' ? (
                  <div dangerouslySetInnerHTML={{ __html: item.definition }} />
                ) : (
                  item.definition
                )}
              </dd>
            </div>
          ))
        )}
      </div>
      
      {searchable && filteredTerms.length > 0 && filteredTerms.length !== terms.length && (
        <div className={styles.searchResults}>
          {filteredTerms.length}件の結果が見つかりました
        </div>
      )}
    </div>
  );
}

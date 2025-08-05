import React from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

export default function ComparisonTable({ 
  title, 
  items = [], 
  columns = ['feature', 'basic', 'pro', 'enterprise'],
  className 
}) {
  const columnHeaders = columns.map(col => {
    const headerMap = {
      feature: '機能',
      basic: 'ベーシック',
      pro: 'プロ',
      enterprise: 'エンタープライズ'
    };
    return headerMap[col] || col.charAt(0).toUpperCase() + col.slice(1);
  });

  return (
    <div className={clsx(styles.comparisonTable, className)}>
      {title && (
        <h3 className={styles.tableTitle}>{title}</h3>
      )}
      <div className={styles.tableWrapper}>
        <table className={styles.table}>
          <thead>
            <tr>
              {columnHeaders.map((header, index) => (
                <th 
                  key={index} 
                  className={clsx(
                    styles.tableHeader,
                    index === 0 ? styles.featureColumn : styles.planColumn
                  )}
                >
                  {header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {items.map((item, index) => (
              <tr key={index} className={styles.tableRow}>
                {columns.map((col, colIndex) => (
                  <td 
                    key={colIndex} 
                    className={clsx(
                      styles.tableCell,
                      colIndex === 0 ? styles.featureCell : styles.planCell
                    )}
                  >
                    {item[col] === true ? '✅' : 
                     item[col] === false ? '❌' : 
                     item[col] || '—'}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

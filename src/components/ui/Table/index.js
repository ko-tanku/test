import React from 'react';
import styles from './styles.module.css';

export default function Table({ 
  data = [], 
  columns = [], 
  caption,
  striped = false,
  bordered = true,
  hover = false,
  responsive = true
}) {
  if (!data.length || !columns.length) {
    return (
      <div className={styles.emptyTable}>
        <p>テーブルデータがありません</p>
      </div>
    );
  }

  const tableClass = `${styles.table} ${striped ? styles.striped : ''} ${
    bordered ? styles.bordered : ''
  } ${hover ? styles.hover : ''}`;

  const TableContent = () => (
    <table className={tableClass}>
      {caption && <caption className={styles.caption}>{caption}</caption>}
      <thead className={styles.thead}>
        <tr>
          {columns.map((column, index) => (
            <th key={index} className={styles.th}>
              {column.header || column.key}
            </th>
          ))}
        </tr>
      </thead>
      <tbody className={styles.tbody}>
        {data.map((row, rowIndex) => (
          <tr key={rowIndex} className={styles.tr}>
            {columns.map((column, colIndex) => (
              <td key={colIndex} className={styles.td}>
                {column.render 
                  ? column.render(row[column.key], row, rowIndex)
                  : row[column.key] || '-'
                }
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );

  if (responsive) {
    return (
      <div className={styles.tableContainer}>
        <div className={styles.tableResponsive}>
          <TableContent />
        </div>
      </div>
    );
  }

  return (
    <div className={styles.tableContainer}>
      <TableContent />
    </div>
  );
}

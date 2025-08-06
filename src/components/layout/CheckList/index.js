import React, { useState } from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

export default function CheckList({ 
  title, 
  items = [], 
  variant = 'default',
  showProgress = false,
  allowToggle = true,
  numbered = false,
  className 
}) {
  // 初期状態の設定
  const normalizeItems = (items) => {
    return items.map((item, index) => {
      if (typeof item === 'string') {
        return { 
          id: `item-${index}`,
          text: item, 
          checked: false, 
          disabled: false 
        };
      } else {
        return { 
          id: item.id || `item-${index}`,
          text: item.text || item.content || 'No text',
          checked: item.checked || false,
          disabled: item.disabled || false
        };
      }
    });
  };

  const [checkedItems, setCheckedItems] = useState(() => {
    const normalized = normalizeItems(items);
    return normalized.reduce((acc, item) => {
      acc[item.id] = item.checked;
      return acc;
    }, {});
  });

  const normalizedItems = normalizeItems(items);
  
  const handleCheckChange = (itemId) => {
    if (!allowToggle) return;
    
    setCheckedItems(prev => ({
      ...prev,
      [itemId]: !prev[itemId]
    }));
  };

  // プログレス計算
  const checkedCount = Object.values(checkedItems).filter(Boolean).length;
  const totalCount = normalizedItems.length;
  const progressPercentage = totalCount > 0 ? (checkedCount / totalCount) * 100 : 0;

  return (
    <div className={clsx(styles.checkList, styles[variant], className)}>
      {title && (
        <div className={styles.header}>
          <h4 className={styles.title}>{title}</h4>
          {showProgress && (
            <div className={styles.progressInfo}>
              <span className={styles.progressText}>
                {checkedCount} / {totalCount} 完了
              </span>
              <div className={styles.progressBar}>
                <div 
                  className={styles.progressFill}
                  style={{ width: `${progressPercentage}%` }}
                />
              </div>
            </div>
          )}
        </div>
      )}
      
      <div className={styles.listContainer}>
        {numbered ? (
          <ol className={styles.orderedList}>
            {normalizedItems.map((item) => (
              <li key={item.id} className={styles.listItem}>
                <CheckListItem 
                  item={item}
                  checked={checkedItems[item.id]}
                  onChange={() => handleCheckChange(item.id)}
                  allowToggle={allowToggle}
                />
              </li>
            ))}
          </ol>
        ) : (
          <ul className={styles.unorderedList}>
            {normalizedItems.map((item) => (
              <li key={item.id} className={styles.listItem}>
                <CheckListItem 
                  item={item}
                  checked={checkedItems[item.id]}
                  onChange={() => handleCheckChange(item.id)}
                  allowToggle={allowToggle}
                />
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

function CheckListItem({ item, checked, onChange, allowToggle }) {
  return (
    <label 
      className={clsx(
        styles.itemLabel,
        checked && styles.checked,
        item.disabled && styles.disabled,
        allowToggle && !item.disabled && styles.interactive
      )}
    >
      <input 
        type="checkbox" 
        checked={checked}
        onChange={onChange}
        disabled={item.disabled || !allowToggle}
        className={styles.checkbox}
      />
      <span className={styles.checkmark} />
      <span className={styles.itemText}>{item.text}</span>
    </label>
  );
}
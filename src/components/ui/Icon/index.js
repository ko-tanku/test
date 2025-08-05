import React from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

export default function Icon({ 
  name, 
  size = 'medium', 
  color, 
  className,
  onClick,
  title,
  ...props 
}) {
  const iconMap = {
    // 基本アイコン
    home: '🏠',
    user: '👤',
    settings: '⚙️',
    search: '🔍',
    close: '✕',
    check: '✓',
    arrow: '→',
    info: 'ℹ️',
    warning: '⚠️',
    error: '❌',
    success: '✅',
    
    // ナビゲーション
    menu: '☰',
    back: '←',
    forward: '→',
    up: '↑',
    down: '↓',
    
    // ファイル・ドキュメント
    file: '📄',
    folder: '📁',
    download: '⬇️',
    upload: '⬆️',
    save: '💾',
    print: '🖨️',
    
    // コミュニケーション
    mail: '✉️',
    phone: '📞',
    chat: '💬',
    
    // その他
    heart: '❤️',
    star: '⭐',
    bookmark: '🔖',
    share: '📤',
    link: '🔗',
  };

  const iconContent = iconMap[name] || name || '?';

  const handleClick = (e) => {
    if (onClick) {
      onClick(e);
    }
  };

  return (
    <span
      className={clsx(
        styles.icon,
        styles[`icon--${size}`],
        onClick && styles.clickable,
        className
      )}
      style={{ color }}
      onClick={handleClick}
      title={title || name}
      role={onClick ? 'button' : undefined}
      tabIndex={onClick ? 0 : undefined}
      {...props}
    >
      {iconContent}
    </span>
  );
}

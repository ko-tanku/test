import React from 'react';

export default function Icon({ name, size = '1em', color = 'currentColor', className, style }) {
  const iconMap = {
    // 図表関連アイコン
    node: '⬜',
    edge: '↔️',
    arrow: '→',
    process: '🔄',
    decision: '💎',
    data: '📊',
    storage: '💾',
    input: '📥',
    output: '📤',
    
    // 基本図形
    circle: '⭕',
    square: '⬜',
    triangle: '🔺',
    diamond: '💎',
    
    // 状態表示
    start: '▶️',
    end: '⏹️',
    pause: '⏸️',
    play: '▶️',
    stop: '⏹️',
    
    // その他
    info: 'ℹ️',
    warning: '⚠️',
    error: '❌',
    success: '✅',
    
    // フォールバック
    unknown: '❓'
  };

  const iconContent = iconMap[name] || iconMap.unknown;

  return (
    <span 
      className={className}
      style={{
        fontSize: size,
        color: color,
        display: 'inline-block',
        lineHeight: 1,
        verticalAlign: 'middle',
        ...style
      }}
      title={name}
    >
      {iconContent}
    </span>
  );
}

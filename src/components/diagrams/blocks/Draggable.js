import React from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';

// Simple fallback draggable component that doesn't use react-dnd
function SimpleDraggable({ id, children, onDragStart }) {
  const handleDragStart = (e) => {
    e.dataTransfer.setData('text/plain', id || 'draggable-item');
    if (onDragStart && typeof onDragStart === 'function') {
      onDragStart(id || 'draggable-item');
    }
  };

  return (
    <div
      draggable
      onDragStart={handleDragStart}
      style={{ 
        cursor: 'move',
        padding: '8px',
        border: '2px dashed #ccc',
        borderRadius: '4px',
        backgroundColor: 'var(--ifm-color-emphasis-100)',
        margin: '4px',
        userSelect: 'none'
      }}
    >
      {children}
    </div>
  );
}

export default function Draggable(props) {
  return (
    <BrowserOnly fallback={<div>Loading draggable...</div>}>
      {() => <SimpleDraggable {...props} />}
    </BrowserOnly>
  );
}

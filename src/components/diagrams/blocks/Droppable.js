import React, { useState } from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';

// Simple fallback droppable component that doesn't use react-dnd
function SimpleDroppable({ id, children, onDrop }) {
  const [isOver, setIsOver] = useState(false);

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsOver(true);
  };

  const handleDragLeave = () => {
    setIsOver(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsOver(false);
    const draggedId = e.dataTransfer.getData('text/plain');
    if (onDrop && draggedId) {
      onDrop(draggedId, id);
    }
  };

  return (
    <div
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      style={{
        padding: '16px',
        border: '2px solid #ccc',
        borderRadius: '4px',
        backgroundColor: isOver ? 'var(--ifm-color-success-lightest)' : 'var(--ifm-color-emphasis-50)',
        margin: '4px',
        minHeight: '60px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        transition: 'all 0.2s ease'
      }}
    >
      {children}
    </div>
  );
}

export default function Droppable(props) {
  return (
    <BrowserOnly fallback={<div>Loading droppable...</div>}>
      {() => <SimpleDroppable {...props} />}
    </BrowserOnly>
  );
}

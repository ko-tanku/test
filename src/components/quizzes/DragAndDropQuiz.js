import React, { useState } from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';

// Simple HTML5 drag and drop implementation without react-dnd
function DragAndDropQuizContent({ 
  items = [], 
  categories = [], 
  question = "アイテムを適切なカテゴリにドラッグしてください"
}) {
  const [droppedItems, setDroppedItems] = useState({});
  const [feedback, setFeedback] = useState('');
  const [isSubmitted, setIsSubmitted] = useState(false);

  const handleDragStart = (e, item) => {
    e.dataTransfer.setData('text/plain', JSON.stringify(item));
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleDrop = (e, categoryId) => {
    e.preventDefault();
    try {
      const item = JSON.parse(e.dataTransfer.getData('text/plain'));
      setDroppedItems(prev => ({
        ...prev,
        [item.id]: categoryId
      }));
    } catch (error) {
      console.error('Drop error:', error);
    }
  };

  const handleSubmit = () => {
    setIsSubmitted(true);
    let correct = 0;
    let total = items.length;

    items.forEach(item => {
      if (droppedItems[item.id] === item.correctCategory) {
        correct++;
      }
    });

    setFeedback(`${correct}/${total} 正解です！`);
  };

  const handleReset = () => {
    setDroppedItems({});
    setFeedback('');
    setIsSubmitted(false);
  };

  const getAvailableItems = () => {
    return items.filter(item => !droppedItems[item.id]);
  };

  const getItemsInCategory = (categoryId) => {
    return items.filter(item => droppedItems[item.id] === categoryId);
  };

  return (
    <div style={{ 
      padding: '1.5rem', 
      border: '1px solid var(--ifm-color-emphasis-300)', 
      borderRadius: 'var(--ifm-border-radius)',
      margin: '1rem 0'
    }}>
      <h3 style={{ marginBottom: '1rem' }}>{question}</h3>
      
      {/* Items to drag */}
      <div style={{ marginBottom: '2rem' }}>
        <h4>アイテム:</h4>
        <div style={{ 
          display: 'flex', 
          flexWrap: 'wrap', 
          gap: '0.5rem',
          padding: '1rem',
          backgroundColor: 'var(--ifm-color-emphasis-100)',
          borderRadius: 'var(--ifm-border-radius)',
          minHeight: '60px'
        }}>
          {getAvailableItems().map(item => (
            <div
              key={item.id}
              draggable={!isSubmitted}
              onDragStart={(e) => handleDragStart(e, item)}
              style={{
                padding: '0.5rem 1rem',
                backgroundColor: 'var(--ifm-color-primary)',
                color: 'white',
                borderRadius: 'var(--ifm-border-radius)',
                cursor: isSubmitted ? 'default' : 'grab',
                opacity: isSubmitted ? 0.7 : 1
              }}
            >
              {item.text || item.label}
            </div>
          ))}
        </div>
      </div>

      {/* Drop categories */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginBottom: '1rem' }}>
        {categories.map(category => (
          <div
            key={category.id}
            onDragOver={handleDragOver}
            onDrop={(e) => handleDrop(e, category.id)}
            style={{
              padding: '1rem',
              border: '2px dashed var(--ifm-color-emphasis-400)',
              borderRadius: 'var(--ifm-border-radius)',
              minHeight: '100px',
              backgroundColor: 'var(--ifm-color-emphasis-50)'
            }}
          >
            <h5 style={{ margin: '0 0 0.5rem 0' }}>{category.name}</h5>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.25rem' }}>
              {getItemsInCategory(category.id).map(item => (
                <div
                  key={item.id}
                  style={{
                    padding: '0.25rem 0.5rem',
                    backgroundColor: isSubmitted 
                      ? (item.correctCategory === category.id 
                          ? 'var(--ifm-color-success)' 
                          : 'var(--ifm-color-danger)')
                      : 'var(--ifm-color-secondary)',
                    color: 'white',
                    borderRadius: 'var(--ifm-border-radius)',
                    fontSize: '0.8rem'
                  }}
                >
                  {item.text || item.label}
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>

      {/* Controls */}
      <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1rem' }}>
        <button
          onClick={handleSubmit}
          disabled={isSubmitted || Object.keys(droppedItems).length === 0}
          style={{
            padding: '0.5rem 1rem',
            backgroundColor: 'var(--ifm-color-primary)',
            color: 'white',
            border: 'none',
            borderRadius: 'var(--ifm-border-radius)',
            cursor: 'pointer'
          }}
        >
          提出
        </button>
        <button
          onClick={handleReset}
          style={{
            padding: '0.5rem 1rem',
            backgroundColor: 'var(--ifm-color-secondary)',
            color: 'white',
            border: 'none',
            borderRadius: 'var(--ifm-border-radius)',
            cursor: 'pointer'
          }}
        >
          リセット
        </button>
      </div>

      {/* Feedback */}
      {feedback && (
        <div style={{
          padding: '0.75rem',
          backgroundColor: isSubmitted ? 'var(--ifm-color-success-lightest)' : 'var(--ifm-color-info-lightest)',
          border: `1px solid ${isSubmitted ? 'var(--ifm-color-success)' : 'var(--ifm-color-info)'}`,
          borderRadius: 'var(--ifm-border-radius)',
          color: isSubmitted ? 'var(--ifm-color-success-dark)' : 'var(--ifm-color-info-dark)'
        }}>
          {feedback}
        </div>
      )}
    </div>
  );
}

export default function DragAndDropQuiz(props) {
  return (
    <BrowserOnly fallback={<div>Loading drag and drop quiz...</div>}>
      {() => <DragAndDropQuizContent {...props} />}
    </BrowserOnly>
  );
}

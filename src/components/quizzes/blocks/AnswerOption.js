import React from 'react';

export default function AnswerOption({ text, onSelect, isSelected }) {
  return (
    <div 
      onClick={onSelect} 
      style={{ 
        padding: '10px', 
        border: isSelected ? '2px solid blue' : '1px solid #ccc', 
        borderRadius: '5px', 
        marginBottom: '5px', 
        cursor: 'pointer' 
      }}
    >
      {text}
    </div>
  );
}

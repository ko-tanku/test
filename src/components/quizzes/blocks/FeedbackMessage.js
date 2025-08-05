import React from 'react';

export default function FeedbackMessage({ isCorrect, message }) {
  if (message === null) return null;

  const style = {
    padding: '10px',
    marginTop: '10px',
    borderRadius: '5px',
    color: 'white',
    backgroundColor: isCorrect ? 'green' : 'red',
  };

  return <div style={style}>{message}</div>;
}

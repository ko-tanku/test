import React from 'react';

export default function FontSizeChanger() {
  const changeFontSize = (amount) => {
    const body = document.querySelector('body');
    const currentSize = parseFloat(window.getComputedStyle(body, null).getPropertyValue('font-size'));
    body.style.fontSize = `${currentSize + amount}px`;
  };

  return (
    <div>
      <button onClick={() => changeFontSize(1)}>+</button>
      <button onClick={() => changeFontSize(-1)}>-</button>
    </div>
  );
}

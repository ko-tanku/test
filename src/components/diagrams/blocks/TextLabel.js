import React from 'react';

export default function TextLabel({ text, position, fontSize }) {
  const style = {
    position: 'absolute',
    left: `${position.x}px`,
    top: `${position.y}px`,
    fontSize: `${fontSize}px`,
  };

  return <div style={style}>{text}</div>;
}

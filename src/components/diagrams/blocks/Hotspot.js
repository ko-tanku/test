import React from 'react';

export default function Hotspot({ x, y, width, height, content }) {
  const style = {
    position: 'absolute',
    left: `${x}%`,
    top: `${y}%`,
    width: `${width}%`,
    height: `${height}%`,
    border: '1px dashed blue',
    cursor: 'pointer',
  };

  return (
    <div style={style}>
      <span className="hotspot-content">{content}</span>
    </div>
  );
}

import React from 'react';

export default function Node({ id, label, position, onClick, highlighted }) {
  const style = {
    left: `${position.x}px`,
    top: `${position.y}px`,
    border: highlighted ? '2px solid red' : '1px solid black',
    padding: '10px',
    position: 'absolute',
    backgroundColor: 'white',
    cursor: 'pointer',
  };

  return (
    <div id={id} style={style} onClick={() => onClick && typeof onClick === 'function' && onClick(id)}>
      {label}
    </div>
  );
}

import React from 'react';
import { useDrop } from 'react-dnd';

export default function Droppable({ id, children, onDrop }) {
  const [{ isOver }, drop] = useDrop(() => ({
    accept: 'item',
    drop: (item) => onDrop(item.id, id),
    collect: (monitor) => ({
      isOver: !!monitor.isOver(),
    }),
  }));

  return (
    <div ref={drop} style={{ backgroundColor: isOver ? 'lightgreen' : 'transparent' }}>
      {children}
    </div>
  );
}

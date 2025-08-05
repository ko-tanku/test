import React from 'react';
import { useDrag } from 'react-dnd';

export default function Draggable({ id, children, onDragStart }) {
  const [{ isDragging }, drag] = useDrag(() => ({
    type: 'item',
    item: { id },
    collect: (monitor) => ({
      isDragging: !!monitor.isDragging(),
    }),
  }));

  React.useEffect(() => {
    if (isDragging && onDragStart) {
      onDragStart(id);
    }
  }, [isDragging, id, onDragStart]);

  return (
    <div ref={drag} style={{ opacity: isDragging ? 0.5 : 1, cursor: 'move' }}>
      {children}
    </div>
  );
}

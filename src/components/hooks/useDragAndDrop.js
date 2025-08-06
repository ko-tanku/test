import React from 'react';
import { useDrag, useDrop } from 'react-dnd';

// This is a conceptual hook. The actual implementation will depend on the specific
// drag-and-drop scenario (e.g., sorting, moving between containers).

export function useSortableDrag(type, id, index, moveItem) {
  const ref = React.useRef(null);
  const [, drop] = useDrop({
    accept: type,
    hover(item, monitor) {
      if (!ref.current) return;
      const dragIndex = item.index;
      const hoverIndex = index;
      if (dragIndex === hoverIndex) return;
      // Determine rectangle on screen
      const hoverBoundingRect = ref.current?.getBoundingClientRect();
      // Get vertical middle
      const hoverMiddleY = (hoverBoundingRect.bottom - hoverBoundingRect.top) / 2;
      // Determine mouse position
      const clientOffset = monitor.getClientOffset();
      // Get pixels to the top
      const hoverClientY = clientOffset.y - hoverBoundingRect.top;
      // Dragging downwards / upwards
      if (dragIndex < hoverIndex && hoverClientY < hoverMiddleY) return;
      if (dragIndex > hoverIndex && hoverClientY > hoverMiddleY) return;
      // Time to actually perform the action
      moveItem(dragIndex, hoverIndex);
      item.index = hoverIndex;
    },
  });

  const [{ isDragging }, drag] = useDrag({
    type: type,
    item: () => ({ id, index }),
    collect: (monitor) => ({
      isDragging: monitor.isDragging(),
    }),
  });

  drag(drop(ref));

  return { ref, isDragging };
}

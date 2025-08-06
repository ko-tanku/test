import React from 'react';

export default function Edge({ 
  fromNode = { x: 0, y: 0 }, 
  toNode = { x: 100, y: 100 }, 
  fromNodeId,
  toNodeId,
  label, 
  animated = false,
  color = '#333',
  strokeWidth = 2,
  markerEnd = true,
  style = {},
  className = ''
}) {
  const id = `edge-${fromNodeId}-${toNodeId}`;
  const markerId = `arrowhead-${id}`;
  
  // Calculate the path from fromNode to toNode
  const dx = toNode.x - fromNode.x;
  const dy = toNode.y - fromNode.y;
  const distance = Math.sqrt(dx * dx + dy * dy);
  
  // Normalize direction vector
  const unitX = dx / distance;
  const unitY = dy / distance;
  
  // Offset start and end points to account for node size (assuming 30px radius)
  const nodeRadius = 15;
  const startX = fromNode.x + unitX * nodeRadius;
  const startY = fromNode.y + unitY * nodeRadius;
  const endX = toNode.x - unitX * nodeRadius;
  const endY = toNode.y - unitY * nodeRadius;
  
  // Calculate label position (midpoint)
  const labelX = (startX + endX) / 2;
  const labelY = (startY + endY) / 2;
  
  return (
    <g className={`edge ${className}`} style={style}>
      {/* Arrow marker definition */}
      {markerEnd && (
        <defs>
          <marker
            id={markerId}
            viewBox="0 0 10 10"
            refX="9"
            refY="3"
            markerWidth="6"
            markerHeight="6"
            orient="auto"
            markerUnits="strokeWidth"
          >
            <path d="M0,0 L0,6 L9,3 z" fill={color} />
          </marker>
        </defs>
      )}
      
      {/* Edge line */}
      <line
        x1={startX}
        y1={startY}
        x2={endX}
        y2={endY}
        stroke={color}
        strokeWidth={strokeWidth}
        markerEnd={markerEnd ? `url(#${markerId})` : undefined}
        className={animated ? 'edge-animated' : ''}
      />
      
      {/* Edge label */}
      {label && (
        <g>
          {/* Background for label */}
          <rect
            x={labelX - label.length * 4}
            y={labelY - 8}
            width={label.length * 8}
            height={16}
            fill="white"
            stroke={color}
            strokeWidth={1}
            rx={3}
            opacity={0.9}
          />
          <text
            x={labelX}
            y={labelY + 4}
            textAnchor="middle"
            fontSize="12"
            fill={color}
            fontFamily="Arial, sans-serif"
          >
            {label}
          </text>
        </g>
      )}
      
      {animated && (
        <style>
          {`
            .edge-animated {
              stroke-dasharray: 5,5;
              animation: dash 1s linear infinite;
            }
            @keyframes dash {
              to {
                stroke-dashoffset: -10;
              }
            }
          `}
        </style>
      )}
    </g>
  );
}

import React from 'react';
import Node from '../blocks/Node';
import Edge from '../blocks/Edge';

export default function FlowchartGenerator({ 
  data,
  width = 800,
  height = 600,
  className = ''
}) {
  const { nodes = [], edges = [] } = data || {};

  return (
    <div className={`flowchart-container ${className}`} style={{ 
      position: 'relative', 
      width: '100%', 
      maxWidth: `${width}px`,
      height: `${height}px`, 
      border: '1px solid #ccc',
      borderRadius: '4px',
      overflow: 'hidden'
    }}>
      <svg 
        width="100%" 
        height="100%" 
        viewBox={`0 0 ${width} ${height}`}
        style={{ position: 'absolute', top: 0, left: 0 }}
      >
        {/* Render edges first so they appear behind nodes */}
        {edges.map((edge, index) => (
          <Edge key={`edge-${index}`} {...edge} />
        ))}
      </svg>
      
      {/* Render nodes as HTML elements positioned absolutely */}
      {nodes.map((node) => (
        <Node key={node.id} {...node} />
      ))}
    </div>
  );
}

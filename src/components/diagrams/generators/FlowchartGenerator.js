import React from 'react';
import Node from '../blocks/Node';
import Edge from '../blocks/Edge';

export default function FlowchartGenerator({ data }) {
  const { nodes, edges } = data;

  return (
    <div style={{ position: 'relative', height: '500px', border: '1px solid #ccc' }}>
      {nodes.map((node) => (
        <Node key={node.id} {...node} />
      ))}
      {edges.map((edge, index) => (
        <Edge key={index} {...edge} />
      ))}
    </div>
  );
}

import React from 'react';
// Specialized for data flow, might build on FlowchartGenerator

export default function DataFlowDiagram({ data }) {
  // Placeholder content
  return (
    <div style={{ border: '1px solid #ccc', padding: '20px', height: '400px' }}>
      Data Flow Diagram Area
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}

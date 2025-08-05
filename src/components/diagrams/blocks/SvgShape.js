import React from 'react';

export default function SvgShape({ type, position, size, color, label }) {
  const { x, y } = position;
  const { width, height } = size;

  return (
    <svg width={width} height={height} style={{ position: 'absolute', left: x, top: y }}>
      <rect width={width} height={height} fill={color} />
      {label && <text x="50%" y="50%" dominantBaseline="middle" textAnchor="middle">{label}</text>}
    </svg>
  );
}

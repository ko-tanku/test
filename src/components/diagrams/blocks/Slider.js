import React from 'react';

export default function Slider({ min, max, value, onChange }) {
  return (
    <input
      type="range"
      min={min}
      max={max}
      value={value}
      onChange={onChange}
      style={{ width: '100%' }}
    />
  );
}

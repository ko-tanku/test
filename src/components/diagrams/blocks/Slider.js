import React from 'react';

export default function Slider({ min = 0, max = 100, value = 50, onChange }) {
  const handleChange = (e) => {
    const newValue = e.target.value;
    if (onChange && typeof onChange === 'function') {
      onChange(e);
    }
  };

  return (
    <input
      type="range"
      min={min}
      max={max}
      value={value}
      onChange={handleChange}
      style={{ width: '100%' }}
    />
  );
}

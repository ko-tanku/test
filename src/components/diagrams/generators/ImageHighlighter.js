import React from 'react';
import Hotspot from '../blocks/Hotspot';

export default function ImageHighlighter({ src, hotspots }) {
  return (
    <div style={{ position: 'relative', display: 'inline-block' }}>
      <img src={src} alt="Interactive diagram" style={{ maxWidth: '100%' }} />
      {hotspots.map((hotspot, index) => (
        <Hotspot key={index} {...hotspot} />
      ))}
    </div>
  );
}

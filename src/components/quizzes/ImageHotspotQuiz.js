import React from 'react';
import ImageHighlighter from '../diagrams/generators/ImageHighlighter';

export default function ImageHotspotQuiz({ src, hotspots, correctHotspot }) {
  // Logic to check if the clicked hotspot is the correct one
  return (
    <div>
      <p>Click on the correct area of the image.</p>
      <ImageHighlighter src={src} hotspots={hotspots} />
    </div>
  );
}

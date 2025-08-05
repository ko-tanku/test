import React from 'react';

export default function Arrow({ from, to, label, animated }) {
  // Simplified representation. Real implementation would use SVG.
  return (
    <div>
      Arrow from ({from.x}, {from.y}) to ({to.x}, {to.y}) {label && `- ${label}`}
    </div>
  );
}

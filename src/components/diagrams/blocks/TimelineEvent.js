import React from 'react';

export default function TimelineEvent({ year, title, description }) {
  return (
    <div style={{ marginBottom: '20px' }}>
      <h4>{year}</h4>
      <h5>{title}</h5>
      <p>{description}</p>
    </div>
  );
}

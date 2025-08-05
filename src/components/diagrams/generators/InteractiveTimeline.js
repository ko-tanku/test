import React from 'react';
import TimelineEvent from '../blocks/TimelineEvent';

export default function InteractiveTimeline({ events }) {
  return (
    <div>
      {events.map((event, index) => (
        <TimelineEvent key={index} {...event} />
      ))}
    </div>
  );
}

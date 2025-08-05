import React, { useState } from 'react';
import styles from './styles.module.css';

export default function Timeline({ 
  events = [], 
  orientation = 'vertical', 
  interactive = true,
  showProgress = false,
  currentStep = 0
}) {
  const [activeEvent, setActiveEvent] = useState(null);

  const handleEventClick = (index) => {
    if (interactive) {
      setActiveEvent(activeEvent === index ? null : index);
    }
  };

  const getEventClass = (index) => {
    let className = styles.event;
    if (showProgress && index <= currentStep) {
      className += ` ${styles.completed}`;
    }
    if (activeEvent === index) {
      className += ` ${styles.active}`;
    }
    return className;
  };

  return (
    <div className={`${styles.timeline} ${styles[orientation]}`}>
      <div className={styles.timelineLine}></div>
      {events.map((event, index) => (
        <div
          key={index}
          className={getEventClass(index)}
          onClick={() => handleEventClick(index)}
        >
          <div className={styles.eventMarker}>
            <div className={styles.eventDot}>
              {showProgress && index <= currentStep ? '✓' : index + 1}
            </div>
          </div>
          <div className={styles.eventContent}>
            <div className={styles.eventHeader}>
              {event.date && <span className={styles.eventDate}>{event.date}</span>}
              <h4 className={styles.eventTitle}>{event.title}</h4>
            </div>
            <p className={styles.eventDescription}>{event.description}</p>
            {activeEvent === index && event.details && (
              <div className={styles.eventDetails}>
                {event.details}
              </div>
            )}
            {event.tags && (
              <div className={styles.eventTags}>
                {event.tags.map((tag, tagIndex) => (
                  <span key={tagIndex} className={styles.tag}>
                    {tag}
                  </span>
                ))}
              </div>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}
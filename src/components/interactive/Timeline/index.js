import React, { useState } from 'react';
import styles from './styles.module.css';

export default function Timeline({ 
  events = [], 
  orientation = 'vertical', 
  interactive = true,
  showProgress = false,
  currentStep = 0,
  mode = 'timeline', // 'timeline', 'development_process', 'git_flow', 'v_model'
  showDependencies = false,
  phaseColors = true,
  // YAML駆動レイアウト制御パラメータ
  layout = {},
  styling = {}
}) {
  // デフォルトレイアウト設定
  const defaultLayout = {
    timeline: {
      width: '100%',
      eventSpacing: 120,
      lineWidth: 4,
      markerSize: 40
    },
    events: {
      contentWidth: 300,
      contentPadding: 16,
      headerHeight: 60,
      detailsMaxHeight: 200
    },
    dependencies: {
      lineOffset: 40,
      arrowSize: 8,
      horizontalSpacing: 200
    },
    text: {
      titleSize: '1.1rem',
      descriptionSize: '0.9rem',
      metaSize: '0.8rem'
    }
  };

  const finalLayout = { 
    ...defaultLayout,
    timeline: { ...defaultLayout.timeline, ...layout.timeline },
    events: { ...defaultLayout.events, ...layout.events },
    dependencies: { ...defaultLayout.dependencies, ...layout.dependencies },
    text: { ...defaultLayout.text, ...layout.text }
  };
  const [activeEvent, setActiveEvent] = useState(null);

  const handleEventClick = (index) => {
    if (interactive) {
      setActiveEvent(activeEvent === index ? null : index);
    }
  };

  const getEventClass = (index) => {
    const event = events[index];
    let className = styles.event;
    
    // Development process specific styling
    if (mode === 'development_process' || mode === 'v_model') {
      if (event.phase) {
        className += ` ${styles[event.phase]}`;
      }
      if (event.type === 'milestone') {
        className += ` ${styles.milestone}`;
      }
      if (event.type === 'deliverable') {
        className += ` ${styles.deliverable}`;
      }
    }
    
    // Git flow specific styling
    if (mode === 'git_flow') {
      if (event.branch) {
        className += ` ${styles[event.branch.replace('/', '_')]}`;
      }
      if (event.action === 'merge') {
        className += ` ${styles.merge}`;
      }
      if (event.action === 'branch') {
        className += ` ${styles.branch}`;
      }
    }
    
    if (showProgress && index <= currentStep) {
      className += ` ${styles.completed}`;
    }
    if (activeEvent === index) {
      className += ` ${styles.active}`;
    }
    return className;
  };

  const renderDependencies = () => {
    if (!showDependencies || mode === 'timeline') return null;
    
    return events.map((event, index) => {
      if (!event.dependencies) return null;
      
      return event.dependencies.map((depIndex, depIdx) => {
        const depEvent = events[depIndex];
        if (!depEvent) return null;
        
        return (
          <div
            key={`${index}-${depIdx}`}
            className={styles.dependency}
            style={{
              top: `${Math.min(index, depIndex) * finalLayout.timeline.eventSpacing + (finalLayout.timeline.eventSpacing / 2)}px`,
              height: `${Math.abs(index - depIndex) * finalLayout.timeline.eventSpacing}px`,
              left: orientation === 'vertical' ? `${finalLayout.dependencies.lineOffset}px` : `${Math.min(index, depIndex) * finalLayout.dependencies.horizontalSpacing + 100}px`
            }}
          >
            <div className={styles.dependencyLine} />
            <div className={styles.dependencyArrow} />
          </div>
        );
      });
    }).flat();
  };

  const getEventIcon = (event) => {
    if (mode === 'development_process' || mode === 'v_model') {
      if (event.type === 'milestone') return '🏁';
      if (event.type === 'deliverable') return '📄';
      if (event.phase === 'requirements') return '📋';
      if (event.phase === 'design') return '🎨';
      if (event.phase === 'implementation') return '⚙️';
      if (event.phase === 'testing') return '🧪';
      if (event.phase === 'deployment') return '🚀';
    }
    
    if (mode === 'git_flow') {
      if (event.action === 'branch') return '🌿';
      if (event.action === 'merge') return '🔀';
      if (event.action === 'commit') return '📝';
      if (event.action === 'tag') return '🏷️';
    }
    
    return showProgress && events.indexOf(event) <= currentStep ? '✓' : events.indexOf(event) + 1;
  };

  return (
    <div className={`${styles.timeline} ${styles[orientation]} ${styles[mode]}`}>
      <div className={styles.timelineLine}></div>
      {renderDependencies()}
      {events.map((event, index) => (
        <div
          key={index}
          className={getEventClass(index)}
          onClick={() => handleEventClick(index)}
        >
          <div className={styles.eventMarker}>
            <div className={styles.eventDot}>
              {getEventIcon(event)}
            </div>
            {event.duration && mode === 'development_process' && (
              <div className={styles.duration}>{event.duration}</div>
            )}
          </div>
          <div className={styles.eventContent}>
            <div className={styles.eventHeader}>
              {event.date && <span className={styles.eventDate}>{event.date}</span>}
              {event.phase && mode !== 'timeline' && (
                <span className={styles.eventPhase}>{event.phase}</span>
              )}
              <h4 className={styles.eventTitle}>{event.title}</h4>
            </div>
            <p className={styles.eventDescription}>{event.description}</p>
            
            {/* Development process specific content */}
            {mode === 'development_process' && event.deliverables && (
              <div className={styles.deliverables}>
                <strong>成果物:</strong>
                <ul>
                  {event.deliverables.map((deliverable, delIndex) => (
                    <li key={delIndex}>{deliverable}</li>
                  ))}
                </ul>
              </div>
            )}
            
            {/* Git flow specific content */}
            {mode === 'git_flow' && event.branch && (
              <div className={styles.branchInfo}>
                <span className={styles.branchName}>{event.branch}</span>
                {event.commits && (
                  <span className={styles.commitCount}>{event.commits} commits</span>
                )}
              </div>
            )}
            
            {activeEvent === index && event.details && (
              <div className={styles.eventDetails}>
                {event.details}
                {event.technicalNotes && mode !== 'timeline' && (
                  <div className={styles.technicalNotes}>
                    <strong>技術ポイント:</strong>
                    <ul>
                      {event.technicalNotes.map((note, noteIndex) => (
                        <li key={noteIndex}>{note}</li>
                      ))}
                    </ul>
                  </div>
                )}
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
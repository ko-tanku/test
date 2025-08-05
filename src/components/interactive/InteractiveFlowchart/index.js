import React, { useState } from 'react';
import styles from './styles.module.css';

export default function InteractiveFlowchart({ 
  title = "フローチャート",
  steps = [],
  connections = [],
  interactive = true
}) {
  const [selectedStep, setSelectedStep] = useState(null);

  const getStepStyle = (step) => {
    const baseStyle = {
      position: 'absolute',
      left: `${(step.x || Math.random() * 60 + 20)}%`,
      top: `${(step.y || Math.random() * 60 + 20)}%`
    };
    return baseStyle;
  };

  const getStepClass = (step) => {
    let className = `${styles.step} ${styles[step.type || 'process']}`;
    if (selectedStep === step.id) {
      className += ` ${styles.selected}`;
    }
    return className;
  };

  const handleStepClick = (stepId) => {
    if (interactive) {
      setSelectedStep(selectedStep === stepId ? null : stepId);
    }
  };

  const renderConnections = () => {
    return connections.map((connection, index) => {
      const fromStep = steps.find(s => s.id === connection.from);
      const toStep = steps.find(s => s.id === connection.to);
      
      if (!fromStep || !toStep) return null;

      const fromX = fromStep.x || Math.random() * 60 + 20;
      const fromY = fromStep.y || Math.random() * 60 + 20;
      const toX = toStep.x || Math.random() * 60 + 20;
      const toY = toStep.y || Math.random() * 60 + 20;

      return (
        <svg
          key={index}
          className={styles.connection}
          style={{
            position: 'absolute',
            left: 0,
            top: 0,
            width: '100%',
            height: '100%',
            pointerEvents: 'none'
          }}
        >
          <defs>
            <marker
              id={`arrowhead-${index}`}
              markerWidth="10"
              markerHeight="7"
              refX="9"
              refY="3.5"
              orient="auto"
            >
              <polygon
                points="0 0, 10 3.5, 0 7"
                fill="var(--ifm-color-emphasis-600)"
              />
            </marker>
          </defs>
          <line
            x1={`${fromX}%`}
            y1={`${fromY}%`}
            x2={`${toX}%`}
            y2={`${toY}%`}
            stroke="var(--ifm-color-emphasis-600)"
            strokeWidth="2"
            markerEnd={`url(#arrowhead-${index})`}
          />
        </svg>
      );
    });
  };

  return (
    <div className={styles.interactiveFlowchart}>
      <h3 className={styles.title}>{title}</h3>
      <div className={styles.flowchartContainer}>
        {renderConnections()}
        {steps.map((step) => (
          <div
            key={step.id}
            className={getStepClass(step)}
            style={getStepStyle(step)}
            onClick={() => handleStepClick(step.id)}
          >
            <div className={styles.stepContent}>
              {step.label}
            </div>
            {selectedStep === step.id && step.description && (
              <div className={styles.stepTooltip}>
                {step.description}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

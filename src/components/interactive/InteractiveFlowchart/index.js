import React, { useState } from 'react';
import styles from './styles.module.css';

export default function InteractiveFlowchart({ 
  title = "フローチャート",
  steps = [],
  connections = [],
  interactive = true,
  mode = "flowchart", // "flowchart", "architecture", "memory_map", "cpu_block"
  showLegend = false,
  zoomEnabled = false,
  // YAML駆動レイアウト制御パラメータ
  layout = {},
  styling = {}
}) {
  // デフォルトレイアウト設定
  const defaultLayout = {
    container: {
      width: 800,
      height: 400,
      viewBox: { x: 0, y: 0, width: 100, height: 100 }
    },
    tooltip: {
      width: 300,
      maxHeight: 200,
      positioning: 'viewport-aware'
    },
    legend: {
      position: 'right',
      width: 150,
      itemSpacing: 8
    },
    nodes: {
      defaultWidth: 100,
      defaultHeight: 60,
      borderRadius: 8,
      spacing: 120
    }
  };

  const finalLayout = { 
    ...defaultLayout,
    container: { ...defaultLayout.container, ...layout.container },
    tooltip: { ...defaultLayout.tooltip, ...layout.tooltip },
    legend: { ...defaultLayout.legend, ...layout.legend },
    nodes: { ...defaultLayout.nodes, ...layout.nodes }
  };
  const [selectedStep, setSelectedStep] = useState(null);
  const [zoomLevel, setZoomLevel] = useState(1);
  const [panOffset, setPanOffset] = useState({ x: 0, y: 0 });
  const [tooltipPosition, setTooltipPosition] = useState({ x: 0, y: 0 });

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
    if (mode === 'architecture') {
      className = `${styles.step} ${styles[step.type || 'cpu_component']}`;
    } else if (mode === 'memory_map') {
      className = `${styles.step} ${styles[step.type || 'memory_block']}`;
    } else if (mode === 'cpu_block') {
      className = `${styles.step} ${styles[step.type || 'cpu_unit']}`;
    }
    
    if (selectedStep === step.id) {
      className += ` ${styles.selected}`;
    }
    return className;
  };

  const handleStepClick = (stepId, event) => {
    if (interactive) {
      if (selectedStep === stepId) {
        setSelectedStep(null);
      } else {
        setSelectedStep(stepId);
        // Calculate tooltip position relative to viewport
        const rect = event.currentTarget.getBoundingClientRect();
        const viewportWidth = window.innerWidth;
        const viewportHeight = window.innerHeight;
        
        let x = rect.right + 10;
        let y = rect.top;
        
        // Adjust if tooltip would go off screen - YAML制御対応
        const tooltipWidth = finalLayout.tooltip.width;
        const tooltipHeight = finalLayout.tooltip.maxHeight;
        
        if (x + tooltipWidth > viewportWidth) {
          x = rect.left - (tooltipWidth + 10);
        }
        if (y + tooltipHeight > viewportHeight) {
          y = viewportHeight - (tooltipHeight + 20);
        }
        
        setTooltipPosition({ x, y });
      }
    }
  };

  const handleZoomIn = () => {
    if (zoomEnabled) {
      setZoomLevel(prev => Math.min(prev * 1.2, 3));
    }
  };

  const handleZoomOut = () => {
    if (zoomEnabled) {
      setZoomLevel(prev => Math.max(prev / 1.2, 0.5));
    }
  };

  const handleReset = () => {
    setZoomLevel(1);
    setPanOffset({ x: 0, y: 0 });
  };

  const getConnectionStyle = (connection) => {
    if (mode === 'architecture') {
      return {
        stroke: connection.type === 'data_bus' ? 'var(--ifm-color-primary)' :
                connection.type === 'control_bus' ? 'var(--ifm-color-warning)' :
                connection.type === 'address_bus' ? 'var(--ifm-color-success)' :
                'var(--ifm-color-emphasis-600)',
        strokeWidth: connection.type?.includes('bus') ? '3' : '2',
        strokeDasharray: connection.type === 'control' ? '5,5' : 'none'
      };
    }
    return {
      stroke: 'var(--ifm-color-emphasis-600)',
      strokeWidth: '2'
    };
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
      
      const connectionStyle = getConnectionStyle(connection);

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
                fill={connectionStyle.stroke}
              />
            </marker>
          </defs>
          <line
            x1={`${fromX}%`}
            y1={`${fromY}%`}
            x2={`${toX}%`}
            y2={`${toY}%`}
            stroke={connectionStyle.stroke}
            strokeWidth={connectionStyle.strokeWidth}
            strokeDasharray={connectionStyle.strokeDasharray}
            markerEnd={`url(#arrowhead-${index})`}
          />
          {connection.label && mode === 'architecture' && (
            <text
              x={`${(fromX + toX) / 2}%`}
              y={`${(fromY + toY) / 2}%`}
              textAnchor="middle"
              fontSize="12"
              fill={connectionStyle.stroke}
              fontWeight="bold"
            >
              {connection.label}
            </text>
          )}
        </svg>
      );
    });
  };

  const renderLegend = () => {
    if (!showLegend || mode === 'flowchart') return null;
    
    const legendItems = mode === 'architecture' ? [
      { type: 'data_bus', color: 'var(--ifm-color-primary)', label: 'データバス' },
      { type: 'control_bus', color: 'var(--ifm-color-warning)', label: '制御バス' },
      { type: 'address_bus', color: 'var(--ifm-color-success)', label: 'アドレスバス' }
    ] : mode === 'memory_map' ? [
      { type: 'rom', color: 'var(--ifm-color-danger)', label: 'ROM' },
      { type: 'ram', color: 'var(--ifm-color-primary)', label: 'RAM' },
      { type: 'flash', color: 'var(--ifm-color-warning)', label: 'Flash' }
    ] : [];

    return (
      <div className={styles.legend}>
        <h4>凡例</h4>
        {legendItems.map((item, index) => (
          <div key={index} className={styles.legendItem}>
            <div 
              className={styles.legendColor} 
              style={{ backgroundColor: item.color }}
            />
            <span>{item.label}</span>
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className={styles.interactiveFlowchart}>
      <div className={styles.header}>
        <h3 className={styles.title}>{title}</h3>
        {zoomEnabled && (
          <div className={styles.controls}>
            <button onClick={handleZoomIn} className={styles.zoomButton}>🔍+</button>
            <button onClick={handleZoomOut} className={styles.zoomButton}>🔍-</button>
            <button onClick={handleReset} className={styles.resetButton}>⟲</button>
            <span className={styles.zoomLevel}>{Math.round(zoomLevel * 100)}%</span>
          </div>
        )}
      </div>
      
      <div className={styles.content}>
        <div 
          className={styles.flowchartContainer}
          style={{ 
            height: finalLayout.container.height,
            width: finalLayout.container.width,
            transform: `scale(${zoomLevel}) translate(${panOffset.x}px, ${panOffset.y}px)`,
            transformOrigin: 'center center'
          }}
        >
          {renderConnections()}
          {steps.map((step) => (
            <div
              key={step.id}
              className={getStepClass(step)}
              style={getStepStyle(step)}
              onClick={(event) => handleStepClick(step.id, event)}
            >
              <div className={styles.stepContent}>
                {step.icon && mode !== 'flowchart' && (
                  <div className={styles.stepIcon}>{step.icon}</div>
                )}
                <div className={styles.stepLabel}>{step.label}</div>
                {step.specs && mode === 'architecture' && (
                  <div className={styles.stepSpecs}>
                    {Object.entries(step.specs).map(([key, value]) => (
                      <div key={key} className={styles.specItem}>
                        <span className={styles.specKey}>{key}:</span>
                        <span className={styles.specValue}>{value}</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
              
            </div>
          ))}
        </div>
        
        {renderLegend()}
      </div>
      
      {/* Global Tooltip */}
      {selectedStep && steps.find(s => s.id === selectedStep)?.description && (
        <div 
          className={styles.stepTooltip}
          style={{
            left: tooltipPosition.x,
            top: tooltipPosition.y,
            maxWidth: finalLayout.tooltip.width,
            maxHeight: finalLayout.tooltip.maxHeight
          }}
        >
          {steps.find(s => s.id === selectedStep)?.description}
          {steps.find(s => s.id === selectedStep)?.technicalDetails && mode === 'architecture' && (
            <div className={styles.technicalDetails}>
              <strong>技術詳細:</strong>
              <ul>
                {steps.find(s => s.id === selectedStep)?.technicalDetails.map((detail, index) => (
                  <li key={index}>{detail}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

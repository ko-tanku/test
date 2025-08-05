import React, { useState, useEffect } from 'react';
import styles from './styles.module.css';

export default function DataFlowSimulator({ 
  title = "データフローシミュレーター",
  nodes = [],
  flows = [],
  autoPlay = false,
  speed = 2000
}) {
  const [activeFlow, setActiveFlow] = useState(null);
  const [flowData, setFlowData] = useState(null);
  const [isPlaying, setIsPlaying] = useState(autoPlay);

  useEffect(() => {
    if (isPlaying && flows.length > 0) {
      const interval = setInterval(() => {
        const currentIndex = flows.findIndex(f => f === activeFlow);
        const nextIndex = (currentIndex + 1) % flows.length;
        const nextFlow = flows[nextIndex];
        
        setActiveFlow(nextFlow);
        setFlowData({
          from: nextFlow.from,
          to: nextFlow.to,
          label: nextFlow.label,
          timestamp: Date.now()
        });
      }, speed);

      return () => clearInterval(interval);
    }
  }, [isPlaying, flows, activeFlow, speed]);

  const handleNodeClick = (nodeId) => {
    const relatedFlows = flows.filter(f => f.from === nodeId || f.to === nodeId);
    if (relatedFlows.length > 0) {
      setActiveFlow(relatedFlows[0]);
      setFlowData({
        from: relatedFlows[0].from,
        to: relatedFlows[0].to,
        label: relatedFlows[0].label,
        timestamp: Date.now()
      });
    }
  };

  const togglePlayback = () => {
    setIsPlaying(!isPlaying);
  };

  const getNodePosition = (node) => {
    return {
      left: `${node.x || Math.random() * 70 + 15}%`,
      top: `${node.y || Math.random() * 60 + 20}%`
    };
  };

  const getNodeClass = (node) => {
    let className = `${styles.node} ${styles[node.type || 'process']}`;
    if (flowData && (flowData.from === node.id || flowData.to === node.id)) {
      className += ` ${styles.active}`;
    }
    return className;
  };

  const renderFlows = () => {
    return flows.map((flow, index) => {
      const fromNode = nodes.find(n => n.id === flow.from);
      const toNode = nodes.find(n => n.id === flow.to);
      
      if (!fromNode || !toNode) return null;

      const fromX = fromNode.x || Math.random() * 70 + 15;
      const fromY = fromNode.y || Math.random() * 60 + 20;
      const toX = toNode.x || Math.random() * 70 + 15;
      const toY = toNode.y || Math.random() * 60 + 20;

      const isActive = activeFlow === flow;

      return (
        <svg
          key={index}
          className={`${styles.flow} ${isActive ? styles.activeFlow : ''}`}
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
              id={`arrow-${index}`}
              markerWidth="12"
              markerHeight="8"
              refX="10"
              refY="4"
              orient="auto"
            >
              <polygon
                points="0 0, 12 4, 0 8"
                fill={isActive ? "var(--ifm-color-primary)" : "var(--ifm-color-emphasis-500)"}
              />
            </marker>
          </defs>
          <line
            x1={`${fromX}%`}
            y1={`${fromY}%`}
            x2={`${toX}%`}
            y2={`${toY}%`}
            stroke={isActive ? "var(--ifm-color-primary)" : "var(--ifm-color-emphasis-500)"}
            strokeWidth={isActive ? "3" : "2"}
            markerEnd={`url(#arrow-${index})`}
            strokeDasharray={isActive ? "none" : "5,5"}
          />
          {isActive && (
            <circle
              r="4"
              fill="var(--ifm-color-primary)"
              className={styles.flowParticle}
            >
              <animateMotion
                dur="2s"
                repeatCount="indefinite"
              >
                <mpath href={`#path-${index}`} />
              </animateMotion>
            </circle>
          )}
          <path
            id={`path-${index}`}
            d={`M ${fromX}% ${fromY}% L ${toX}% ${toY}%`}
            stroke="transparent"
            fill="none"
          />
        </svg>
      );
    });
  };

  return (
    <div className={styles.dataFlowSimulator}>
      <div className={styles.header}>
        <h3 className={styles.title}>{title}</h3>
        <div className={styles.controls}>
          <button 
            onClick={togglePlayback}
            className={`${styles.playButton} ${isPlaying ? styles.playing : ''}`}
          >
            {isPlaying ? '⏸️' : '▶️'}
          </button>
        </div>
      </div>
      
      <div className={styles.simulatorContainer}>
        {renderFlows()}
        
        {nodes.map((node) => (
          <div
            key={node.id}
            className={getNodeClass(node)}
            style={getNodePosition(node)}
            onClick={() => handleNodeClick(node.id)}
          >
            <div className={styles.nodeContent}>
              <div className={styles.nodeLabel}>{node.label}</div>
              {node.description && (
                <div className={styles.nodeDescription}>{node.description}</div>
              )}
            </div>
          </div>
        ))}

        {flowData && (
          <div className={styles.flowInfo}>
            <div className={styles.flowLabel}>
              {flowData.label || `${flowData.from} → ${flowData.to}`}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

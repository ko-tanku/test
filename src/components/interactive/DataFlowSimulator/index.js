import React, { useState, useEffect } from 'react';
import styles from './styles.module.css';

export default function DataFlowSimulator({ 
  title = "データフローシミュレーター",
  nodes = [],
  flows = [],
  autoPlay = false,
  speed = 2000,
  mode = 'dataflow', // 'dataflow', 'network_stack', 'protocol_layers'
  showLayers = false,
  layerHeight = 80,
  protocolInfo = true,
  // YAML駆動レイアウト制御パラメータ
  layout = {},
  styling = {}
}) {
  // デフォルトレイアウト設定をマージ
  const defaultLayout = {
    container: {
      width: '100%',
      height: mode === 'network_stack' ? 800 : 400,
      background: 'default'
    },
    layers: {
      height: layerHeight || 80,
      spacing: 10,
      labelPosition: 'left',
      labelWidth: 120
    },
    nodes: {
      defaultWidth: 150,
      defaultHeight: 60,
      spacing: 200,
      borderRadius: 8
    },
    protocolPanel: {
      position: 'bottom-right',
      width: 320,
      maxHeight: 300,
      offset: { x: 20, y: 20 }
    }
  };

  const finalLayout = { 
    ...defaultLayout,
    container: { ...defaultLayout.container, ...layout.container },
    layers: { ...defaultLayout.layers, ...layout.layers },
    nodes: { ...defaultLayout.nodes, ...layout.nodes },
    protocolPanel: { ...defaultLayout.protocolPanel, ...layout.protocolPanel }
  };
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
    if (mode === 'network_stack' && node.layer !== undefined) {
      // Stack nodes vertically by layer - YAML制御対応
      const layerIndex = typeof node.layer === 'number' ? node.layer : 0;
      const layerY = 50 + (layerIndex * finalLayout.layers.height);
      const nodeSpacing = finalLayout.nodes.spacing;
      const nodeX = node.x || (50 + (nodes.filter(n => n.layer === node.layer).indexOf(node) * (nodeSpacing / 10)));
      
      return {
        left: `${Math.min(nodeX, 80)}%`,
        top: `${layerY}px`
      };
    }
    
    return {
      left: `${node.x || Math.random() * 70 + 15}%`,
      top: `${node.y || Math.random() * 60 + 20}%`
    };
  };

  const getNodeClass = (node) => {
    let className = `${styles.node} ${styles[node.type || 'process']}`;
    
    // Network stack specific styling
    if (mode === 'network_stack') {
      if (node.layer !== undefined) {
        className += ` ${styles.layered}`;
        className += ` ${styles[`layer${node.layer}`]}`;
      }
      if (node.protocol) {
        className += ` ${styles[node.protocol.toLowerCase()]}`;
      }
    }
    
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

  const renderNetworkLayers = () => {
    if (mode !== 'network_stack' || !showLayers) return null;
    
    const layers = [...new Set(nodes.filter(n => n.layer !== undefined).map(n => n.layer))].sort();
    const layerNames = {
      0: 'Physical Layer (物理層)',
      1: 'Data Link Layer (データリンク層)', 
      2: 'Network Layer (ネットワーク層)',
      3: 'Transport Layer (トランスポート層)',
      4: 'Session Layer (セション層)',
      5: 'Presentation Layer (プレゼンテーション層)',
      6: 'Application Layer (アプリケーション層)'
    };
    
    return (
      <div className={styles.networkLayers}>
        {layers.map((layer, index) => (
          <div
            key={layer}
            className={`${styles.networkLayer} ${styles[`layer${layer}`]}`}
            style={{
              top: `${50 + (layer * finalLayout.layers.height)}px`,
              height: `${finalLayout.layers.height - finalLayout.layers.spacing}px`
            }}
          >
            <div className={styles.layerLabel}>
              <strong>Layer {layer + 1}</strong>
              <span>{layerNames[layer] || `Custom Layer ${layer}`}</span>
            </div>
          </div>
        ))}
      </div>
    );
  };

  const renderProtocolInfo = () => {
    if (!protocolInfo || !flowData) return null;
    
    const activeNodes = nodes.filter(n => 
      flowData.from === n.id || flowData.to === n.id
    );
    
    // プロトコル情報パネルの位置計算
    const panelPosition = {};
    const panel = finalLayout.protocolPanel;
    
    if (panel.position === 'bottom-right') {
      panelPosition.bottom = `${panel.offset.y}px`;
      panelPosition.right = `${panel.offset.x}px`;
    } else if (panel.position === 'top-right') {
      panelPosition.top = `${panel.offset.y}px`;
      panelPosition.right = `${panel.offset.x}px`;
    } else if (panel.position === 'bottom-left') {
      panelPosition.bottom = `${panel.offset.y}px`;
      panelPosition.left = `${panel.offset.x}px`;
    }
    
    return (
      <div 
        className={styles.protocolInfo}
        style={{
          ...panelPosition,
          width: `${panel.width}px`,
          maxHeight: `${panel.maxHeight}px`
        }}
      >
        <h4>プロトコル情報</h4>
        {activeNodes.map((node, index) => (
          <div key={node.id} className={styles.protocolDetail}>
            <strong>{node.label}</strong>
            {node.protocol && (
              <div className={styles.protocol}>
                <span className={styles.protocolName}>{node.protocol}</span>
                {node.port && <span className={styles.port}>Port: {node.port}</span>}
              </div>
            )}
            {node.functions && (
              <ul className={styles.functions}>
                {node.functions.map((func, idx) => (
                  <li key={idx}>{func}</li>
                ))}
              </ul>
            )}
          </div>
        ))}
        {flowData.label && (
          <div className={styles.flowDetail}>
            <strong>データフロー:</strong> {flowData.label}
          </div>
        )}
      </div>
    );
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
      
      <div 
        className={`${styles.simulatorContainer} ${styles[mode]}`}
        style={{
          height: finalLayout.container.height,
          width: finalLayout.container.width
        }}
      >
        {renderNetworkLayers()}
        {renderFlows()}
        
        {nodes.map((node) => (
          <div
            key={node.id}
            className={getNodeClass(node)}
            style={getNodePosition(node)}
            onClick={() => handleNodeClick(node.id)}
          >
            <div className={styles.nodeContent}>
              {node.icon && mode === 'network_stack' && (
                <div className={styles.nodeIcon}>{node.icon}</div>
              )}
              <div className={styles.nodeLabel}>{node.label}</div>
              {node.protocol && mode === 'network_stack' && (
                <div className={styles.nodeProtocol}>{node.protocol}</div>
              )}
              {node.description && (
                <div className={styles.nodeDescription}>{node.description}</div>
              )}
              {node.layer !== undefined && mode === 'network_stack' && (
                <div className={styles.layerIndicator}>L{node.layer + 1}</div>
              )}
            </div>
          </div>
        ))}

        {flowData && (
          <div className={styles.flowInfo}>
            <div className={styles.flowLabel}>
              {flowData.label || `${flowData.from} → ${flowData.to}`}
            </div>
            {mode === 'network_stack' && flowData.protocol && (
              <div className={styles.flowProtocol}>
                Protocol: {flowData.protocol}
              </div>
            )}
          </div>
        )}
        
        {renderProtocolInfo()}
      </div>
    </div>
  );
}

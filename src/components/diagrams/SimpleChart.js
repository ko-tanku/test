import React from 'react';

export default function SimpleChart({ 
  type = 'bar', 
  title = 'チャート', 
  data = [],
  width = 400,
  height = 300,
  // Wave-specific props
  timeUnit = 'ms',
  amplitude = 100,
  frequency = 1,
  showGrid = true,
  animated = false,
  channelColors = ['var(--ifm-color-primary)', 'var(--ifm-color-success)', 'var(--ifm-color-warning)', 'var(--ifm-color-danger)'],
  // YAML駆動レイアウト制御パラメータ
  layout = {},
  styling = {}
}) {
  // デフォルトレイアウト設定
  const defaultLayout = {
    chart: {
      width: width,
      height: height,
      margin: { top: 30, right: 50, bottom: 40, left: 50 }
    },
    waveform: {
      channelHeight: 80,
      channelSpacing: 20,
      gridDensity: 5,
      pointSize: 3
    },
    digital: {
      channelHeight: 60,
      channelSpacing: 10,
      signalWidth: 3
    },
    text: {
      titleSize: 16,
      labelSize: 12,
      valueSize: 12
    }
  };

  const finalLayout = { 
    ...defaultLayout,
    chart: { ...defaultLayout.chart, ...layout.chart },
    waveform: { ...defaultLayout.waveform, ...layout.waveform },
    digital: { ...defaultLayout.digital, ...layout.digital },
    text: { ...defaultLayout.text, ...layout.text }
  };
  if (!data || data.length === 0) {
    return (
      <div style={{ 
        padding: '2rem', 
        textAlign: 'center',
        border: '1px solid var(--ifm-color-emphasis-300)',
        borderRadius: 'var(--ifm-border-radius)',
        backgroundColor: 'var(--ifm-color-emphasis-50)',
        margin: '1rem 0'
      }}>
        <h3>{title}</h3>
        <p>データがありません</p>
      </div>
    );
  }

  const maxValue = Math.max(...data.map(item => item.value));
  const chartHeight = finalLayout.chart.height - finalLayout.chart.margin.top - finalLayout.chart.margin.bottom;
  const chartWidth = finalLayout.chart.width - finalLayout.chart.margin.left - finalLayout.chart.margin.right;
  const barWidth = chartWidth / data.length * 0.8;
  const barSpacing = chartWidth / data.length * 0.2;

  const renderBarChart = () => (
    <svg width={finalLayout.chart.width} height={finalLayout.chart.height} style={{ margin: '1rem 0' }}>
      <text x={finalLayout.chart.width/2} y={finalLayout.text.titleSize + 5} textAnchor="middle" fontSize={finalLayout.text.titleSize} fontWeight="bold" fill="var(--ifm-color-emphasis-800)">
        {title}
      </text>
      
      {data.map((item, index) => {
        const barHeight = (item.value / maxValue) * chartHeight;
        const x = finalLayout.chart.margin.left + (index * (barWidth + barSpacing));
        const y = finalLayout.chart.height - finalLayout.chart.margin.bottom - barHeight;
        
        return (
          <g key={index}>
            <rect
              x={x}
              y={y}
              width={barWidth}
              height={barHeight}
              fill="var(--ifm-color-primary)"
              stroke="var(--ifm-color-primary-dark)"
              strokeWidth="1"
            />
            <text
              x={x + barWidth/2}
              y={height - 20}
              textAnchor="middle"
              fontSize="12"
              fill="var(--ifm-color-emphasis-700)"
            >
              {item.label}
            </text>
            <text
              x={x + barWidth/2}
              y={y - 5}
              textAnchor="middle"
              fontSize="12"
              fill="var(--ifm-color-emphasis-800)"
              fontWeight="bold"
            >
              {item.value}
            </text>
          </g>
        );
      })}
      
      {/* Y-axis */}
      <line x1={45} y1={30} x2={45} y2={height-40} stroke="var(--ifm-color-emphasis-600)" strokeWidth="2"/>
      {/* X-axis */}
      <line x1={45} y1={height-40} x2={width-20} y2={height-40} stroke="var(--ifm-color-emphasis-600)" strokeWidth="2"/>
    </svg>
  );

  const renderLineChart = () => {
    const points = data.map((item, index) => {
      const x = 50 + (index * (chartWidth / (data.length - 1)));
      const y = height - 40 - ((item.value / maxValue) * chartHeight);
      return `${x},${y}`;
    }).join(' ');

    return (
      <svg width={width} height={height} style={{ margin: '1rem 0' }}>
        <text x={width/2} y={20} textAnchor="middle" fontSize="16" fontWeight="bold" fill="var(--ifm-color-emphasis-800)">
          {title}
        </text>
        
        {/* Grid lines */}
        {[0, 0.25, 0.5, 0.75, 1].map((ratio, index) => {
          const y = height - 40 - (ratio * chartHeight);
          return (
            <line 
              key={index}
              x1={45} 
              y1={y} 
              x2={width-20} 
              y2={y} 
              stroke="var(--ifm-color-emphasis-200)" 
              strokeWidth="1"
              strokeDasharray="2,2"
            />
          );
        })}
        
        {/* Line */}
        <polyline
          fill="none"
          stroke="var(--ifm-color-primary)"
          strokeWidth="3"
          points={points}
        />
        
        {/* Data points */}
        {data.map((item, index) => {
          const x = 50 + (index * (chartWidth / (data.length - 1)));
          const y = height - 40 - ((item.value / maxValue) * chartHeight);
          
          return (
            <g key={index}>
              <circle
                cx={x}
                cy={y}
                r="4"
                fill="var(--ifm-color-primary)"
                stroke="white"
                strokeWidth="2"
              />
              <text
                x={x}
                y={height - 20}
                textAnchor="middle"
                fontSize="12"
                fill="var(--ifm-color-emphasis-700)"
              >
                {item.label}
              </text>
              <text
                x={x}
                y={y - 10}
                textAnchor="middle"
                fontSize="12"
                fill="var(--ifm-color-emphasis-800)"
                fontWeight="bold"
              >
                {item.value}
              </text>
            </g>
          );
        })}
        
        {/* Y-axis */}
        <line x1={45} y1={30} x2={45} y2={height-40} stroke="var(--ifm-color-emphasis-600)" strokeWidth="2"/>
        {/* X-axis */}
        <line x1={45} y1={height-40} x2={width-20} y2={height-40} stroke="var(--ifm-color-emphasis-600)" strokeWidth="2"/>
      </svg>
    );
  };

  const renderWaveform = () => {
    const chartMargin = 50;
    const actualWidth = width - 2 * chartMargin;
    const actualHeight = height - 80; // More space for title and labels
    
    // Handle multiple channels
    const channels = Array.isArray(data[0]?.channels) ? data : [{ name: 'Signal', data: data, color: channelColors[0] }];
    
    const maxTime = Math.max(...data.map(d => d.time || d.x || 0));
    const minTime = Math.min(...data.map(d => d.time || d.x || 0));
    const timeRange = maxTime - minTime || 1;
    
    return (
      <svg width={width} height={height} style={{ margin: '1rem 0' }}>
        <text x={width/2} y={20} textAnchor="middle" fontSize="16" fontWeight="bold" fill="var(--ifm-color-emphasis-800)">
          {title}
        </text>
        
        {/* Grid lines */}
        {showGrid && (
          <g className="grid">
            {/* Vertical grid lines (time) */}
            {[0, 0.25, 0.5, 0.75, 1].map((ratio, index) => {
              const x = chartMargin + (ratio * actualWidth);
              return (
                <line 
                  key={`v-grid-${index}`}
                  x1={x} 
                  y1={30} 
                  x2={x} 
                  y2={height - 30} 
                  stroke="var(--ifm-color-emphasis-200)" 
                  strokeWidth="1"
                  strokeDasharray="2,2"
                />
              );
            })}
            {/* Horizontal grid lines (amplitude) */}
            {[0, 0.25, 0.5, 0.75, 1].map((ratio, index) => {
              const y = 30 + (ratio * actualHeight);
              return (
                <line 
                  key={`h-grid-${index}`}
                  x1={chartMargin} 
                  y1={y} 
                  x2={width - chartMargin} 
                  y2={y} 
                  stroke="var(--ifm-color-emphasis-200)" 
                  strokeWidth="1"
                  strokeDasharray="2,2"
                />
              );
            })}
          </g>
        )}
        
        {/* Render each channel */}
        {channels.map((channel, channelIndex) => {
          const channelData = channel.data || data;
          const color = channel.color || channelColors[channelIndex % channelColors.length];
          
          // Generate waveform path
          const pathPoints = channelData.map((point, index) => {
            const time = point.time !== undefined ? point.time : point.x !== undefined ? point.x : index;
            const value = point.value !== undefined ? point.value : point.y !== undefined ? point.y : point;
            
            const x = chartMargin + ((time - minTime) / timeRange) * actualWidth;
            const y = 30 + actualHeight - ((value / amplitude) * actualHeight * 0.8 + actualHeight * 0.1);
            
            return `${x},${y}`;
          }).join(' ');
          
          const pathData = `M ${pathPoints.split(' ').join(' L ')}`;
          
          return (
            <g key={channelIndex} className={`channel-${channelIndex}`}>
              {/* Waveform line */}
              <path
                d={pathData}
                fill="none"
                stroke={color}
                strokeWidth="2"
                strokeLinejoin="round"
                strokeLinecap="round"
              />
              
              {/* Data points */}
              {channelData.map((point, pointIndex) => {
                const time = point.time !== undefined ? point.time : point.x !== undefined ? point.x : pointIndex;
                const value = point.value !== undefined ? point.value : point.y !== undefined ? point.y : point;
                
                const x = chartMargin + ((time - minTime) / timeRange) * actualWidth;
                const y = 30 + actualHeight - ((value / amplitude) * actualHeight * 0.8 + actualHeight * 0.1);
                
                return (
                  <circle
                    key={pointIndex}
                    cx={x}
                    cy={y}
                    r="3"
                    fill={color}
                    stroke="white"
                    strokeWidth="1"
                  />
                );
              })}
              
              {/* Channel label */}
              <text
                x={width - chartMargin + 5}
                y={30 + (channelIndex * 20)}
                fontSize="12"
                fill={color}
                fontWeight="bold"
              >
                {channel.name || `CH${channelIndex + 1}`}
              </text>
            </g>
          );
        })}
        
        {/* Axes */}
        <line x1={chartMargin} y1={30} x2={chartMargin} y2={height-30} stroke="var(--ifm-color-emphasis-600)" strokeWidth="2"/>
        <line x1={chartMargin} y1={height-30} x2={width-chartMargin} y2={height-30} stroke="var(--ifm-color-emphasis-600)" strokeWidth="2"/>
        
        {/* Axis labels */}
        <text x={width/2} y={height-5} textAnchor="middle" fontSize="12" fill="var(--ifm-color-emphasis-700)">
          時間 ({timeUnit})
        </text>
        <text x={15} y={height/2} textAnchor="middle" fontSize="12" fill="var(--ifm-color-emphasis-700)" transform={`rotate(-90 15 ${height/2})`}>
          振幅
        </text>
        
        {/* Time scale */}
        {[0, 0.25, 0.5, 0.75, 1].map((ratio, index) => {
          const x = chartMargin + (ratio * actualWidth);
          const timeValue = minTime + (ratio * timeRange);
          return (
            <text
              key={index}
              x={x}
              y={height - 10}
              textAnchor="middle"
              fontSize="10"
              fill="var(--ifm-color-emphasis-600)"
            >
              {timeValue.toFixed(1)}
            </text>
          );
        })}
      </svg>
    );
  };

  const renderDigitalSignal = () => {
    const chartMargin = 50;
    const actualWidth = width - 2 * chartMargin;
    const actualHeight = height - 80;
    
    const channels = Array.isArray(data[0]?.channels) ? data : [{ name: 'Digital', data: data, color: channelColors[0] }];
    const maxTime = Math.max(...data.map(d => d.time || d.x || 0));
    const minTime = Math.min(...data.map(d => d.time || d.x || 0));
    const timeRange = maxTime - minTime || 1;
    
    return (
      <svg width={width} height={height} style={{ margin: '1rem 0' }}>
        <text x={width/2} y={20} textAnchor="middle" fontSize="16" fontWeight="bold" fill="var(--ifm-color-emphasis-800)">
          {title}
        </text>
        
        {channels.map((channel, channelIndex) => {
          const channelData = channel.data || data;
          const color = channel.color || channelColors[channelIndex % channelColors.length];
          const channelHeight = actualHeight / channels.length;
          const channelY = 30 + (channelIndex * channelHeight);
          
          // Generate digital signal path (square wave)
          let pathData = '';
          let lastValue = null;
          
          channelData.forEach((point, index) => {
            const time = point.time !== undefined ? point.time : point.x !== undefined ? point.x : index;
            const value = point.value !== undefined ? point.value : point.y !== undefined ? point.y : point;
            const digitalValue = value > 0 ? 1 : 0; // Convert to binary
            
            const x = chartMargin + ((time - minTime) / timeRange) * actualWidth;
            const y = channelY + channelHeight * 0.8 - (digitalValue * channelHeight * 0.6);
            
            if (index === 0) {
              pathData = `M ${x} ${y}`;
            } else {
              if (lastValue !== digitalValue) {
                // Vertical transition
                const prevY = channelY + channelHeight * 0.8 - (lastValue * channelHeight * 0.6);
                pathData += ` L ${x} ${prevY} L ${x} ${y}`;
              } else {
                // Horizontal continuation
                pathData += ` L ${x} ${y}`;
              }
            }
            
            lastValue = digitalValue;
          });
          
          return (
            <g key={channelIndex}>
              {/* Channel background */}
              <rect
                x={chartMargin}
                y={channelY}
                width={actualWidth}
                height={channelHeight}
                fill="var(--ifm-color-emphasis-50)"
                stroke="var(--ifm-color-emphasis-200)"
                strokeWidth="1"
              />
              
              {/* Digital signal */}
              <path
                d={pathData}
                fill="none"
                stroke={color}
                strokeWidth="3"
                strokeLinejoin="round"
              />
              
              {/* Channel label */}
              <text
                x={chartMargin - 5}
                y={channelY + channelHeight/2}
                textAnchor="end"
                fontSize="12"
                fill={color}
                fontWeight="bold"
                alignmentBaseline="middle"
              >
                {channel.name || `CH${channelIndex + 1}`}
              </text>
              
              {/* Logic level indicators */}
              <text
                x={chartMargin - 15}
                y={channelY + channelHeight * 0.2}
                textAnchor="end"
                fontSize="10"
                fill="var(--ifm-color-emphasis-600)"
              >
                1
              </text>
              <text
                x={chartMargin - 15}
                y={channelY + channelHeight * 0.8}
                textAnchor="end"
                fontSize="10"
                fill="var(--ifm-color-emphasis-600)"
              >
                0
              </text>
            </g>
          );
        })}
        
        {/* Time axis */}
        <line x1={chartMargin} y1={height-30} x2={width-chartMargin} y2={height-30} stroke="var(--ifm-color-emphasis-600)" strokeWidth="2"/>
        
        {/* Time labels */}
        <text x={width/2} y={height-5} textAnchor="middle" fontSize="12" fill="var(--ifm-color-emphasis-700)">
          時間 ({timeUnit})
        </text>
      </svg>
    );
  };

  const renderPieChart = () => {
    const total = data.reduce((sum, item) => sum + item.value, 0);
    const centerX = width / 2;
    const centerY = height / 2;
    const radius = Math.min(width, height) / 3;
    
    let currentAngle = 0;
    
    return (
      <svg width={width} height={height} style={{ margin: '1rem 0' }}>
        <text x={width/2} y={20} textAnchor="middle" fontSize="16" fontWeight="bold" fill="var(--ifm-color-emphasis-800)">
          {title}
        </text>
        
        {data.map((item, index) => {
          const sliceAngle = (item.value / total) * 2 * Math.PI;
          const startAngle = currentAngle;
          const endAngle = currentAngle + sliceAngle;
          
          const x1 = centerX + radius * Math.cos(startAngle);
          const y1 = centerY + radius * Math.sin(startAngle);
          const x2 = centerX + radius * Math.cos(endAngle);
          const y2 = centerY + radius * Math.sin(endAngle);
          
          const largeArcFlag = sliceAngle > Math.PI ? 1 : 0;
          
          const pathData = [
            `M ${centerX} ${centerY}`,
            `L ${x1} ${y1}`,
            `A ${radius} ${radius} 0 ${largeArcFlag} 1 ${x2} ${y2}`,
            'Z'
          ].join(' ');
          
          const labelX = centerX + (radius * 0.7) * Math.cos(startAngle + sliceAngle / 2);
          const labelY = centerY + (radius * 0.7) * Math.sin(startAngle + sliceAngle / 2);
          
          currentAngle += sliceAngle;
          
          const colors = [
            'var(--ifm-color-primary)',
            'var(--ifm-color-secondary)', 
            'var(--ifm-color-success)',
            'var(--ifm-color-warning)',
            'var(--ifm-color-danger)',
            'var(--ifm-color-info)'
          ];
          
          return (
            <g key={index}>
              <path
                d={pathData}
                fill={colors[index % colors.length]}
                stroke="white"
                strokeWidth="2"
              />
              <text
                x={labelX}
                y={labelY}
                textAnchor="middle"
                fontSize="12"
                fill="white"
                fontWeight="bold"
              >
                {item.value}
              </text>
            </g>
          );
        })}
        
        {/* Legend */}
        {data.map((item, index) => {
          const colors = [
            'var(--ifm-color-primary)',
            'var(--ifm-color-secondary)', 
            'var(--ifm-color-success)',
            'var(--ifm-color-warning)',
            'var(--ifm-color-danger)',
            'var(--ifm-color-info)'
          ];
          
          return (
            <g key={index}>
              <rect
                x={20}
                y={height - 60 + (index * 20)}
                width={15}
                height={15}
                fill={colors[index % colors.length]}
              />
              <text
                x={40}
                y={height - 50 + (index * 20)}
                fontSize="12"
                fill="var(--ifm-color-emphasis-800)"
              >
                {item.label}
              </text>
            </g>
          );
        })}
      </svg>
    );
  };

  return (
    <div style={{ 
      display: 'flex', 
      justifyContent: 'center',
      padding: '1rem',
      border: '1px solid var(--ifm-color-emphasis-300)',
      borderRadius: 'var(--ifm-border-radius)',
      backgroundColor: 'var(--ifm-background-color)',
      margin: '1rem 0'
    }}>
      {type === 'bar' && renderBarChart()}
      {type === 'line' && renderLineChart()}
      {type === 'pie' && renderPieChart()}
      {type === 'waveform' && renderWaveform()}
      {type === 'digital' && renderDigitalSignal()}
      {!['bar', 'line', 'pie', 'waveform', 'digital'].includes(type) && renderBarChart()}
    </div>
  );
}
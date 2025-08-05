import React from 'react';

export default function SimpleChart({ 
  type = 'bar', 
  title = 'チャート', 
  data = [],
  width = 400,
  height = 300
}) {
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
  const chartHeight = height - 60; // Leave space for title and labels
  const chartWidth = width - 100; // Leave space for labels
  const barWidth = chartWidth / data.length * 0.8;
  const barSpacing = chartWidth / data.length * 0.2;

  const renderBarChart = () => (
    <svg width={width} height={height} style={{ margin: '1rem 0' }}>
      <text x={width/2} y={20} textAnchor="middle" fontSize="16" fontWeight="bold" fill="var(--ifm-color-emphasis-800)">
        {title}
      </text>
      
      {data.map((item, index) => {
        const barHeight = (item.value / maxValue) * chartHeight;
        const x = 50 + (index * (barWidth + barSpacing));
        const y = height - 40 - barHeight;
        
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
      {!['bar', 'line', 'pie'].includes(type) && renderBarChart()}
    </div>
  );
}
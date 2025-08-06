import React, { useState } from 'react';
import styles from './styles.module.css';

export default function ImageHotspot({ 
  image,
  alt = "Interactive image",
  title,
  width = "100%",
  height = "auto",
  hotspots = []
}) {
  const [activeHotspot, setActiveHotspot] = useState(null);
  const [imageError, setImageError] = useState(false);

  const handleHotspotClick = (index) => {
    setActiveHotspot(activeHotspot === index ? null : index);
  };

  const handleImageClick = (e) => {
    // Close tooltip when clicking outside hotspots
    if (e.target.classList.contains(styles.image)) {
      setActiveHotspot(null);
    }
  };

  return (
    <div className={styles.imageHotspot} style={{ width }}>
      {title && <h4 className={styles.imageTitle}>{title}</h4>}
      <div className={styles.imageContainer}>
        {imageError ? (
          <div className={styles.imagePlaceholder}>
            <div className={styles.placeholderIcon}>📱</div>
            <p>スマートフォンの構成図</p>
            <p className={styles.placeholderNote}>
              （画像: {image} が見つかりません）
            </p>
          </div>
        ) : (
          <img 
            src={image}
            alt={alt}
            className={styles.image}
            style={{ height }}
            onClick={handleImageClick}
            onError={() => setImageError(true)}
          />
        )}
        {hotspots.map((hotspot, index) => (
          <div
            key={index}
            className={`${styles.hotspot} ${activeHotspot === index ? styles.active : ''}`}
            style={{
              left: `${hotspot.x}%`,
              top: `${hotspot.y}%`
            }}
            onClick={() => handleHotspotClick(index)}
          >
            <div className={styles.hotspotMarker}>
              <span className={styles.hotspotNumber}>{index + 1}</span>
            </div>
            {activeHotspot === index && (
              <div className={styles.tooltip}>
                <div className={styles.tooltipHeader}>
                  <h4 className={styles.tooltipTitle}>{hotspot.title}</h4>
                  <button 
                    className={styles.closeButton}
                    onClick={(e) => {
                      e.stopPropagation();
                      setActiveHotspot(null);
                    }}
                  >
                    ×
                  </button>
                </div>
                <div className={styles.tooltipContent}>
                  {hotspot.description}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

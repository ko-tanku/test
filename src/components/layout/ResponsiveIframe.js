import React, { useRef, useEffect } from 'react';

export default function ResponsiveIframe({ src, ...props }) {
  const iframeRef = useRef(null);

  useEffect(() => {
    const iframe = iframeRef.current;
    if (!iframe) return;

    const handleResize = () => {
      if (iframe.contentWindow) {
        iframe.style.height = `${iframe.contentWindow.document.body.scrollHeight}px`;
      }
    };

    iframe.addEventListener('load', handleResize);
    // You might need a more robust solution like ResizeObserver for dynamic content

    return () => {
      iframe.removeEventListener('load', handleResize);
    };
  }, [src]);

  return (
    <iframe
      ref={iframeRef}
      src={src}
      style={{ width: '100%', border: 'none' }}
      {...props}
    />
  );
}

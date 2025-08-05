import { useEffect } from 'react';

export function useKeyNavigation(keyHandlers) {
  useEffect(() => {
    const handleKeyDown = (event) => {
      if (keyHandlers[event.key]) {
        keyHandlers[event.key]();
      }
    };

    window.addEventListener('keydown', handleKeyDown);

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [keyHandlers]);
}

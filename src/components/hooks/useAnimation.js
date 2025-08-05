import { useState, useEffect, useCallback } from 'react';

// Example: A simple hook to manage a CSS class for animation
export function useAnimation(ref, animationClass) {
  const triggerAnimation = useCallback(() => {
    const element = ref.current;
    if (element) {
      element.classList.add(animationClass);
      element.addEventListener('animationend', () => {
        element.classList.remove(animationClass);
      }, { once: true });
    }
  }, [ref, animationClass]);

  return triggerAnimation;
}

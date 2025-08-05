import React from 'react';
import { useColorMode } from '@docusaurus/theme-common';

function ThemeToggle() {
  const { colorMode, setColorMode } = useColorMode();

  return (
    <button onClick={() => setColorMode(colorMode === 'dark' ? 'light' : 'dark')}>
      {colorMode === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
    </button>
  );
}

export default ThemeToggle;

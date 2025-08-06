import React, { useState } from 'react';
import Button from '../ui/Button/index.js';

export default function ProgressiveLayout({ children }) {
  const [visibleSteps, setVisibleSteps] = useState(1);
  const steps = React.Children.toArray(children);

  const showNextStep = () => {
    setVisibleSteps((prev) => Math.min(prev + 1, steps.length));
  };

  return (
    <div>
      {steps.slice(0, visibleSteps)}
      {visibleSteps < steps.length && (
        <Button onClick={showNextStep}>Continue</Button>
      )}
    </div>
  );
}

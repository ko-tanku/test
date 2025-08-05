import React from 'react';
import ProgressBar from '../ui/ProgressBar';

export default function LearningProgress({ current, total }) {
  return <ProgressBar value={current} max={total} />;
}

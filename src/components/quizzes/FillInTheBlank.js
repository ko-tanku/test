import React, { useState } from 'react';
import Button from '../ui/Button';

export default function FillInTheBlank({ question, correctAnswer }) {
  const [answer, setAnswer] = useState('');
  const [isCorrect, setIsCorrect] = useState(null);

  const handleChange = (e) => {
    setAnswer(e.target.value);
  };

  const handleSubmit = () => {
    setIsCorrect(answer.toLowerCase() === correctAnswer.toLowerCase());
  };

  return (
    <div>
      <p>{question.replace('___', '')}</p>
      <input type="text" value={answer} onChange={handleChange} />
      <Button onClick={handleSubmit}>Check</Button>
      {isCorrect === true && <p style={{ color: 'green' }}>Correct!</p>}
      {isCorrect === false && <p style={{ color: 'red' }}>Incorrect.</p>}
    </div>
  );
}

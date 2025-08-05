import React, { useState } from 'react';
import Question from './blocks/Question';
import AnswerOption from './blocks/AnswerOption';
import FeedbackMessage from './blocks/FeedbackMessage';
import Button from '../ui/Button';

export default function MultipleChoice({ quizData }) {
  const { question, options, correctAnswer } = quizData;
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [feedback, setFeedback] = useState(null);

  const handleSubmit = () => {
    if (selectedAnswer === null) return;
    const isCorrect = selectedAnswer === correctAnswer;
    setFeedback({ isCorrect, message: isCorrect ? 'Correct!' : `Incorrect. The correct answer is ${correctAnswer}.` });
  };

  return (
    <div>
      <Question text={question} />
      <div>
        {options.map((option, index) => (
          <AnswerOption
            key={index}
            text={option.text}
            isSelected={selectedAnswer === option}
            onSelect={() => setSelectedAnswer(option)}
          />
        ))}
      </div>
      <Button onClick={handleSubmit} disabled={selectedAnswer === null}>Submit</Button>
      {feedback && <FeedbackMessage isCorrect={feedback.isCorrect} message={feedback.message} />}
    </div>
  );
}

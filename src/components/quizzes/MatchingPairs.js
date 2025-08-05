import React, { useState, useEffect } from 'react';

export default function MatchingPairs({ 
  pairs = [], 
  question = "左右の項目を正しく組み合わせてください"
}) {
  const [leftItems, setLeftItems] = useState([]);
  const [rightItems, setRightItems] = useState([]);
  const [selectedLeft, setSelectedLeft] = useState(null);
  const [selectedRight, setSelectedRight] = useState(null);
  const [matches, setMatches] = useState([]);
  const [feedback, setFeedback] = useState('');
  const [isSubmitted, setIsSubmitted] = useState(false);

  useEffect(() => {
    if (pairs.length > 0) {
      setLeftItems(pairs.map(pair => ({ id: pair.id, text: pair.left })));
      // Shuffle right items for added difficulty
      const shuffledRightItems = [...pairs.map(pair => ({ id: pair.id, text: pair.right }))]
        .sort(() => Math.random() - 0.5);
      setRightItems(shuffledRightItems);
    }
  }, [pairs]);

  const handleLeftClick = (item) => {
    if (isSubmitted) return;
    setSelectedLeft(selectedLeft?.id === item.id ? null : item);
  };

  const handleRightClick = (item) => {
    if (isSubmitted) return;
    if (selectedLeft) {
      // Create a match
      const newMatch = { leftId: selectedLeft.id, rightId: item.id };
      setMatches([...matches, newMatch]);
      setSelectedLeft(null);
      setSelectedRight(null);
    } else {
      setSelectedRight(selectedRight?.id === item.id ? null : item);
    }
  };

  const removeMatch = (leftId, rightId) => {
    if (isSubmitted) return;
    setMatches(matches.filter(match => !(match.leftId === leftId && match.rightId === rightId)));
  };

  const handleSubmit = () => {
    setIsSubmitted(true);
    let correct = 0;
    let total = pairs.length;

    matches.forEach(match => {
      const pair = pairs.find(p => p.id === match.leftId);
      if (pair && pair.id === match.rightId) {
        correct++;
      }
    });

    setFeedback(`${correct}/${total} 正解です！`);
  };

  const handleReset = () => {
    setMatches([]);
    setSelectedLeft(null);
    setSelectedRight(null);
    setFeedback('');
    setIsSubmitted(false);
    // Re-shuffle right items
    const shuffledRightItems = [...pairs.map(pair => ({ id: pair.id, text: pair.right }))]
      .sort(() => Math.random() - 0.5);
    setRightItems(shuffledRightItems);
  };

  const isLeftMatched = (itemId) => matches.some(match => match.leftId === itemId);
  const isRightMatched = (itemId) => matches.some(match => match.rightId === itemId);
  const getRightMatch = (leftId) => matches.find(match => match.leftId === leftId)?.rightId;

  const getItemStyle = (isSelected, isMatched, isCorrect = null) => ({
    padding: '0.75rem 1rem',
    margin: '0.25rem',
    border: `2px solid ${
      isSelected ? 'var(--ifm-color-primary)' : 
      isMatched ? (isCorrect === true ? 'var(--ifm-color-success)' : 
                   isCorrect === false ? 'var(--ifm-color-danger)' : 
                   'var(--ifm-color-secondary)') : 
      'var(--ifm-color-emphasis-300)'
    }`,
    borderRadius: 'var(--ifm-border-radius)',
    backgroundColor: isSelected ? 'var(--ifm-color-primary-lightest)' : 
                     isMatched ? (isCorrect === true ? 'var(--ifm-color-success-lightest)' : 
                                  isCorrect === false ? 'var(--ifm-color-danger-lightest)' : 
                                  'var(--ifm-color-secondary-lightest)') : 
                     'var(--ifm-background-color)',
    cursor: isSubmitted ? 'default' : 'pointer',
    transition: 'all 0.2s ease',
    opacity: isMatched ? 0.8 : 1
  });

  return (
    <div style={{ 
      padding: '1.5rem', 
      border: '1px solid var(--ifm-color-emphasis-300)', 
      borderRadius: 'var(--ifm-border-radius)',
      margin: '1rem 0'
    }}>
      <h3 style={{ marginBottom: '1rem', textAlign: 'center' }}>{question}</h3>
      
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem', marginBottom: '1rem' }}>
        {/* Left column */}
        <div>
          <h4 style={{ textAlign: 'center', marginBottom: '1rem' }}>左の項目</h4>
          {leftItems.map(item => {
            const isMatched = isLeftMatched(item.id);
            const rightMatchId = getRightMatch(item.id);
            const isCorrect = isSubmitted ? (rightMatchId === item.id) : null;
            
            return (
              <div key={item.id} style={{ display: 'flex', alignItems: 'center', marginBottom: '0.5rem' }}>
                <div
                  onClick={() => handleLeftClick(item)}
                  style={getItemStyle(
                    selectedLeft?.id === item.id, 
                    isMatched,
                    isCorrect
                  )}
                >
                  {item.text}
                </div>
                {isMatched && (
                  <button
                    onClick={() => removeMatch(item.id, rightMatchId)}
                    disabled={isSubmitted}
                    style={{
                      marginLeft: '0.5rem',
                      padding: '0.25rem 0.5rem',
                      backgroundColor: 'var(--ifm-color-danger)',
                      color: 'white',
                      border: 'none',
                      borderRadius: 'var(--ifm-border-radius)',
                      cursor: isSubmitted ? 'default' : 'pointer',
                      fontSize: '0.8rem'
                    }}
                  >
                    ✗
                  </button>
                )}
              </div>
            );
          })}
        </div>

        {/* Right column */}
        <div>
          <h4 style={{ textAlign: 'center', marginBottom: '1rem' }}>右の項目</h4>
          {rightItems.map(item => {
            const isMatched = isRightMatched(item.id);
            const leftMatch = matches.find(match => match.rightId === item.id);
            const isCorrect = isSubmitted ? (leftMatch?.leftId === item.id) : null;
            
            return (
              <div
                key={item.id}
                onClick={() => handleRightClick(item)}
                style={getItemStyle(
                  selectedRight?.id === item.id, 
                  isMatched,
                  isCorrect
                )}
              >
                {item.text}
              </div>
            );
          })}
        </div>
      </div>

      {/* Instructions */}
      {!isSubmitted && (
        <div style={{ 
          padding: '0.75rem', 
          backgroundColor: 'var(--ifm-color-info-lightest)',
          border: '1px solid var(--ifm-color-info)',
          borderRadius: 'var(--ifm-border-radius)',
          marginBottom: '1rem',
          fontSize: '0.9rem'
        }}>
          💡 左の項目をクリックしてから、対応する右の項目をクリックして組み合わせてください。
        </div>
      )}

      {/* Controls */}
      <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1rem' }}>
        <button
          onClick={handleSubmit}
          disabled={isSubmitted || matches.length !== pairs.length}
          style={{
            padding: '0.5rem 1rem',
            backgroundColor: 'var(--ifm-color-primary)',
            color: 'white',
            border: 'none',
            borderRadius: 'var(--ifm-border-radius)',
            cursor: 'pointer',
            opacity: matches.length !== pairs.length ? 0.6 : 1
          }}
        >
          提出 ({matches.length}/{pairs.length})
        </button>
        <button
          onClick={handleReset}
          style={{
            padding: '0.5rem 1rem',
            backgroundColor: 'var(--ifm-color-secondary)',
            color: 'white',
            border: 'none',
            borderRadius: 'var(--ifm-border-radius)',
            cursor: 'pointer'
          }}
        >
          リセット
        </button>
      </div>

      {/* Feedback */}
      {feedback && (
        <div style={{
          padding: '0.75rem',
          backgroundColor: 'var(--ifm-color-success-lightest)',
          border: '1px solid var(--ifm-color-success)',
          borderRadius: 'var(--ifm-border-radius)',
          color: 'var(--ifm-color-success-dark)'
        }}>
          {feedback}
        </div>
      )}
    </div>
  );
}

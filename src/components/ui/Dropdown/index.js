import React, { useState, useRef, useEffect } from 'react';
import styles from './styles.module.css';

export default function Dropdown({ 
  options = [], 
  placeholder = "選択してください", 
  value, 
  onChange,
  disabled = false,
  searchable = false,
  multiple = false,
  className = ''
}) {
  const [isOpen, setIsOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedValues, setSelectedValues] = useState(multiple ? (value || []) : value);
  const dropdownRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const filteredOptions = searchable 
    ? options.filter(option => 
        option.label.toLowerCase().includes(searchTerm.toLowerCase())
      )
    : options;

  const handleSelect = (option) => {
    if (multiple) {
      const newValues = selectedValues.includes(option.value)
        ? selectedValues.filter(v => v !== option.value)
        : [...selectedValues, option.value];
      setSelectedValues(newValues);
      onChange && onChange(newValues);
    } else {
      setSelectedValues(option.value);
      onChange && onChange(option.value);
      setIsOpen(false);
    }
  };

  const getDisplayText = () => {
    if (multiple) {
      const selected = options.filter(opt => selectedValues.includes(opt.value));
      return selected.length > 0 ? `${selected.length}個選択済み` : placeholder;
    } else {
      const selected = options.find(opt => opt.value === selectedValues);
      return selected ? selected.label : placeholder;
    }
  };

  return (
    <div className={`${styles.dropdown} ${className}`} ref={dropdownRef}>
      <button
        className={`${styles.dropdownButton} ${isOpen ? styles.open : ''} ${disabled ? styles.disabled : ''}`}
        onClick={() => !disabled && setIsOpen(!isOpen)}
        disabled={disabled}
      >
        <span>{getDisplayText()}</span>
        <span className={styles.arrow}>▼</span>
      </button>
      
      {isOpen && (
        <div className={styles.dropdownMenu}>
          {searchable && (
            <input
              type="text"
              placeholder="検索..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className={styles.searchInput}
              onClick={(e) => e.stopPropagation()}
            />
          )}
          <div className={styles.optionsList}>
            {filteredOptions.map((option) => (
              <div
                key={option.value}
                className={`${styles.option} ${
                  multiple 
                    ? (selectedValues.includes(option.value) ? styles.selected : '')
                    : (selectedValues === option.value ? styles.selected : '')
                }`}
                onClick={() => handleSelect(option)}
              >
                {multiple && (
                  <input
                    type="checkbox"
                    checked={selectedValues.includes(option.value)}
                    onChange={() => {}}
                    className={styles.checkbox}
                  />
                )}
                <span>{option.label}</span>
              </div>
            ))}
            {filteredOptions.length === 0 && (
              <div className={styles.noOptions}>オプションがありません</div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
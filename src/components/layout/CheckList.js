import React from 'react';

export default function CheckList({ items }) {
  return (
    <ul>
      {items.map((item, index) => (
        <li key={index}>
          <input type="checkbox" id={`item-${index}`} />
          <label htmlFor={`item-${index}`}>{item.text}</label>
        </li>
      ))}
    </ul>
  );
}

import React, { useState } from 'react';
import styles from './Pagination.module.css';

export default function Pagination({ totalItems, itemsPerPage, onPageChange }) {
  const pageCount = Math.ceil(totalItems / itemsPerPage);
  const [currentPage, setCurrentPage] = useState(1);

  const handlePageClick = (page) => {
    setCurrentPage(page);
    onPageChange(page);
  };

  if (pageCount <= 1) {
    return null;
  }

  return (
    <nav className={styles.pagination}>
      <ul>
        {Array.from({ length: pageCount }, (_, i) => i + 1).map((page) => (
          <li
            key={page}
            className={currentPage === page ? styles.active : ''}
            onClick={() => handlePageClick(page)}
          >
            {page}
          </li>
        ))}
      </ul>
    </nav>
  );
}

import React from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

export default function LearningObjectives({ title, objectives = [], className, numbered = true }) {
  return (
    <div className={clsx(styles.learningObjectives, className)}>
      {title && (
        <h3 className={styles.objectivesTitle}>{title}</h3>
      )}
      
      <div className={styles.objectivesContainer}>
        {numbered ? (
          <ol className={styles.objectivesList}>
            {objectives.map((objective, index) => (
              <li key={index} className={styles.objectiveItem}>
                <div className={styles.objectiveContent}>
                  {typeof objective === 'string' ? (
                    <span className={styles.objectiveText}>{objective}</span>
                  ) : (
                    <>
                      <span className={styles.objectiveText}>{objective.text}</span>
                      {objective.description && (
                        <div className={styles.objectiveDescription}>
                          {objective.description}
                        </div>
                      )}
                    </>
                  )}
                </div>
              </li>
            ))}
          </ol>
        ) : (
          <ul className={styles.objectivesList}>
            {objectives.map((objective, index) => (
              <li key={index} className={styles.objectiveItem}>
                <div className={styles.objectiveContent}>
                  <span className={styles.objectiveIcon}>🎯</span>
                  {typeof objective === 'string' ? (
                    <span className={styles.objectiveText}>{objective}</span>
                  ) : (
                    <>
                      <span className={styles.objectiveText}>{objective.text}</span>
                      {objective.description && (
                        <div className={styles.objectiveDescription}>
                          {objective.description}
                        </div>
                      )}
                    </>
                  )}
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

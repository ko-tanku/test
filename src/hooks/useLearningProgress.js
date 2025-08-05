import { useState, useEffect } from 'react';

const PROGRESS_STORAGE_KEY = 'learningProgress';

// localStorageから進捗を読み込む
const loadProgress = () => {
  try {
    const saved = localStorage.getItem(PROGRESS_STORAGE_KEY);
    return saved ? JSON.parse(saved) : { completedCourses: [] };
  } catch (error) {
    console.error("Failed to load progress from localStorage", error);
    return { completedCourses: [] };
  }
};

// localStorageに進捗を保存する
const saveProgress = (progress) => {
  try {
    localStorage.setItem(PROGRESS_STORAGE_KEY, JSON.stringify(progress));
  } catch (error) {
    console.error("Failed to save progress to localStorage", error);
  }
};

export const useLearningProgress = () => {
  const [progress, setProgress] = useState({ completedCourses: [] });

  useEffect(() => {
    // コンポーネントのマウント時に一度だけ進捗を読み込む
    setProgress(loadProgress());
  }, []);

  // コースを完了としてマークする関数
  const markAsCompleted = (courseId) => {
    if (progress.completedCourses.includes(courseId)) {
      return; // すでに完了済み
    }
    const newProgress = {
      ...progress,
      completedCourses: [...progress.completedCourses, courseId],
    };
    setProgress(newProgress);
    saveProgress(newProgress);
  };

  // 特定のコースが完了しているかチェックする関数
  const isCompleted = (courseId) => {
    return progress.completedCourses.includes(courseId);
  };

  return { progress, markAsCompleted, isCompleted };
};

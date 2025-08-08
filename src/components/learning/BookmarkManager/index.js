import React, { useState, useEffect } from 'react';
import styles from './styles.module.css';

export default function BookmarkManager({ 
  currentPage = '',
  currentProgress = 0,
  totalPages = 0,
  courseId = 'default',
  onNavigate = () => {},
  showProgressBar = true
}) {
  const [bookmarks, setBookmarks] = useState([]);
  const [lastSession, setLastSession] = useState(null);
  const [showBookmarks, setShowBookmarks] = useState(false);

  // ローカルストレージのキー
  const storageKey = `learning-bookmarks-${courseId}`;
  const sessionKey = `learning-session-${courseId}`;

  useEffect(() => {
    // ブックマークと最後のセッション情報を読み込み
    const savedBookmarks = localStorage.getItem(storageKey);
    const savedSession = localStorage.getItem(sessionKey);
    
    if (savedBookmarks) {
      setBookmarks(JSON.parse(savedBookmarks));
    }
    
    if (savedSession) {
      setLastSession(JSON.parse(savedSession));
    }
  }, [storageKey, sessionKey]);

  useEffect(() => {
    // 現在のセッション情報を自動保存
    const sessionData = {
      page: currentPage,
      progress: currentProgress,
      timestamp: Date.now(),
      totalPages
    };
    
    localStorage.setItem(sessionKey, JSON.stringify(sessionData));
    setLastSession(sessionData);
  }, [currentPage, currentProgress, totalPages, sessionKey]);

  const addBookmark = (customTitle = '') => {
    const bookmark = {
      id: Date.now(),
      title: customTitle || `${currentPage} - ${Math.round((currentProgress / totalPages) * 100)}%`,
      page: currentPage,
      progress: currentProgress,
      timestamp: Date.now(),
      totalPages
    };

    const updatedBookmarks = [...bookmarks, bookmark];
    setBookmarks(updatedBookmarks);
    localStorage.setItem(storageKey, JSON.stringify(updatedBookmarks));
  };

  const removeBookmark = (bookmarkId) => {
    const updatedBookmarks = bookmarks.filter(b => b.id !== bookmarkId);
    setBookmarks(updatedBookmarks);
    localStorage.setItem(storageKey, JSON.stringify(updatedBookmarks));
  };

  const navigateToBookmark = (bookmark) => {
    onNavigate(bookmark.page, bookmark.progress);
  };

  const resumeLastSession = () => {
    if (lastSession) {
      onNavigate(lastSession.page, lastSession.progress);
    }
  };

  const formatDate = (timestamp) => {
    return new Date(timestamp).toLocaleDateString('ja-JP', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const calculateProgress = (progress, total) => {
    return total > 0 ? Math.round((progress / total) * 100) : 0;
  };

  return (
    <div className={styles.bookmarkManager}>
      {/* 進捗バー */}
      {showProgressBar && (
        <div className={styles.progressSection}>
          <div className={styles.progressBar}>
            <div 
              className={styles.progressFill}
              style={{ width: `${calculateProgress(currentProgress, totalPages)}%` }}
            />
          </div>
          <span className={styles.progressText}>
            {currentProgress}/{totalPages} ({calculateProgress(currentProgress, totalPages)}%)
          </span>
        </div>
      )}

      {/* 学習継続オプション */}
      <div className={styles.actions}>
        {/* 前回の続きから */}
        {lastSession && lastSession.page !== currentPage && (
          <button 
            onClick={resumeLastSession}
            className={styles.resumeButton}
          >
            📖 前回の続きから (
            {lastSession.page} - {calculateProgress(lastSession.progress, lastSession.totalPages)}%
            )
          </button>
        )}

        {/* ブックマーク追加 */}
        <button 
          onClick={() => addBookmark()}
          className={styles.bookmarkButton}
        >
          🔖 現在の位置をブックマーク
        </button>

        {/* ブックマーク一覧表示/非表示 */}
        <button 
          onClick={() => setShowBookmarks(!showBookmarks)}
          className={styles.toggleButton}
        >
          📋 ブックマーク一覧 ({bookmarks.length})
        </button>
      </div>

      {/* ブックマーク一覧 */}
      {showBookmarks && (
        <div className={styles.bookmarkList}>
          <h4>保存したブックマーク</h4>
          {bookmarks.length === 0 ? (
            <p className={styles.noBookmarks}>まだブックマークがありません</p>
          ) : (
            <ul className={styles.bookmarks}>
              {bookmarks.map(bookmark => (
                <li key={bookmark.id} className={styles.bookmarkItem}>
                  <div className={styles.bookmarkInfo}>
                    <strong className={styles.bookmarkTitle}>
                      {bookmark.title}
                    </strong>
                    <div className={styles.bookmarkMeta}>
                      <span className={styles.bookmarkDate}>
                        {formatDate(bookmark.timestamp)}
                      </span>
                      <span className={styles.bookmarkProgress}>
                        {calculateProgress(bookmark.progress, bookmark.totalPages)}%完了
                      </span>
                    </div>
                  </div>
                  <div className={styles.bookmarkActions}>
                    <button 
                      onClick={() => navigateToBookmark(bookmark)}
                      className={styles.jumpButton}
                    >
                      移動
                    </button>
                    <button 
                      onClick={() => removeBookmark(bookmark.id)}
                      className={styles.deleteButton}
                    >
                      削除
                    </button>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}

      {/* 学習統計 */}
      {lastSession && (
        <div className={styles.stats}>
          <small className={styles.lastActivity}>
            最後の学習: {formatDate(lastSession.timestamp)}
          </small>
        </div>
      )}
    </div>
  );
}
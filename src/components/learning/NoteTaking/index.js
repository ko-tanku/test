import React, { useState, useEffect } from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';
import styles from './styles.module.css';

export default function NoteTaking({
  title = "学習ノート",
  placeholder = "ここに学習内容をメモしてください...",
  autoSave = true,
  showWordCount = true,
  showTimestamp = true,
  maxLength = 5000,
  className = '',
  onSave = null,
  initialContent = ''
}) {
  return (
    <BrowserOnly fallback={<div>Loading Note Taking...</div>}>
      {() => <NoteTakingClient 
        title={title}
        placeholder={placeholder}
        autoSave={autoSave}
        showWordCount={showWordCount}
        showTimestamp={showTimestamp}
        maxLength={maxLength}
        className={className}
        onSave={onSave}
        initialContent={initialContent}
      />}
    </BrowserOnly>
  );
}

function NoteTakingClient({
  title,
  placeholder,
  autoSave,
  showWordCount,
  showTimestamp,
  maxLength,
  className,
  onSave,
  initialContent
}) {
  const [content, setContent] = useState(initialContent);
  const [lastSaved, setLastSaved] = useState(null);
  const [isSaving, setIsSaving] = useState(false);
  const [notes, setNotes] = useState(() => {
    // ローカルストレージから既存のノートを読み込み
    try {
      const saved = localStorage.getItem('learning-notes');
      return saved ? JSON.parse(saved) : [];
    } catch {
      return [];
    }
  });
  const [activeNoteId, setActiveNoteId] = useState(null);
  const [showNotesList, setShowNotesList] = useState(false);

  // 自動保存機能
  useEffect(() => {
    if (autoSave && content.trim()) {
      const timer = setTimeout(() => {
        saveNote();
      }, 2000); // 2秒後に自動保存

      return () => clearTimeout(timer);
    }
  }, [content, autoSave]);

  const saveNote = async () => {
    if (!content.trim()) return;

    setIsSaving(true);
    
    try {
      const timestamp = new Date().toISOString();
      const noteData = {
        id: activeNoteId || Date.now().toString(),
        content: content.trim(),
        timestamp,
        wordCount: content.trim().split(/\s+/).length,
        title: extractTitle(content) || `ノート ${new Date().toLocaleDateString()}`
      };

      let updatedNotes;
      if (activeNoteId) {
        // 既存ノートの更新
        updatedNotes = notes.map(note => 
          note.id === activeNoteId ? noteData : note
        );
      } else {
        // 新しいノートの追加
        updatedNotes = [noteData, ...notes];
        setActiveNoteId(noteData.id);
      }

      setNotes(updatedNotes);
      localStorage.setItem('learning-notes', JSON.stringify(updatedNotes));
      setLastSaved(new Date());
      
      // 外部コールバック
      if (onSave && typeof onSave === 'function') {
        onSave(noteData);
      }
      
    } catch (error) {
      console.error('Failed to save note:', error);
    } finally {
      setIsSaving(false);
    }
  };

  const loadNote = (noteId) => {
    const note = notes.find(n => n.id === noteId);
    if (note) {
      setContent(note.content);
      setActiveNoteId(noteId);
      setShowNotesList(false);
    }
  };

  const deleteNote = (noteId) => {
    if (window.confirm('このノートを削除してもよろしいですか？')) {
      const updatedNotes = notes.filter(note => note.id !== noteId);
      setNotes(updatedNotes);
      localStorage.setItem('learning-notes', JSON.stringify(updatedNotes));
      
      if (activeNoteId === noteId) {
        setActiveNoteId(null);
        setContent('');
      }
    }
  };

  const createNewNote = () => {
    setContent('');
    setActiveNoteId(null);
    setShowNotesList(false);
  };

  const extractTitle = (text) => {
    const lines = text.split('\n');
    const firstLine = lines[0].trim();
    
    // 最初の行が短い場合はタイトルとして使用
    if (firstLine && firstLine.length <= 50) {
      return firstLine;
    }
    
    // そうでない場合は最初の50文字を使用
    return text.substring(0, 50) + (text.length > 50 ? '...' : '');
  };

  const getWordCount = () => {
    if (!content.trim()) return 0;
    return content.trim().split(/\s+/).length;
  };

  const formatTimestamp = (date) => {
    if (!date) return '';
    return date.toLocaleString('ja-JP', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const exportNotes = () => {
    const exportData = {
      notes,
      exportDate: new Date().toISOString(),
      totalNotes: notes.length
    };
    
    const blob = new Blob([JSON.stringify(exportData, null, 2)], {
      type: 'application/json'
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `learning-notes-${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className={`${styles.noteTaking} ${className}`}>
      <div className={styles.header}>
        <h3>{title}</h3>
        <div className={styles.headerActions}>
          <button 
            className={styles.actionButton}
            onClick={() => setShowNotesList(!showNotesList)}
            title="ノート一覧"
          >
            📋 ノート一覧 ({notes.length})
          </button>
          <button 
            className={styles.actionButton}
            onClick={createNewNote}
            title="新しいノート"
          >
            ➕ 新規作成
          </button>
          <button 
            className={styles.actionButton}
            onClick={saveNote}
            disabled={!content.trim() || isSaving}
            title="保存"
          >
            {isSaving ? '💾 保存中...' : '💾 保存'}
          </button>
          {notes.length > 0 && (
            <button 
              className={styles.actionButton}
              onClick={exportNotes}
              title="エクスポート"
            >
              📤 エクスポート
            </button>
          )}
        </div>
      </div>

      {showNotesList && (
        <div className={styles.notesList}>
          <div className={styles.notesHeader}>
            <h4>保存されたノート</h4>
            <button 
              className={styles.closeButton}
              onClick={() => setShowNotesList(false)}
            >
              ×
            </button>
          </div>
          <div className={styles.notesGrid}>
            {notes.length === 0 ? (
              <div className={styles.emptyNotes}>
                <p>まだノートがありません</p>
                <button 
                  className={styles.createFirstNote}
                  onClick={createNewNote}
                >
                  最初のノートを作成
                </button>
              </div>
            ) : (
              notes.map(note => (
                <div 
                  key={note.id} 
                  className={`${styles.noteCard} ${note.id === activeNoteId ? styles.active : ''}`}
                >
                  <div className={styles.noteCardHeader}>
                    <h5 className={styles.noteTitle}>{note.title}</h5>
                    <button 
                      className={styles.deleteButton}
                      onClick={() => deleteNote(note.id)}
                      title="削除"
                    >
                      🗑️
                    </button>
                  </div>
                  <div className={styles.notePreview}>
                    {note.content.substring(0, 100)}
                    {note.content.length > 100 && '...'}
                  </div>
                  <div className={styles.noteMetadata}>
                    <span>{formatTimestamp(new Date(note.timestamp))}</span>
                    <span>{note.wordCount} 文字</span>
                  </div>
                  <button 
                    className={styles.loadButton}
                    onClick={() => loadNote(note.id)}
                  >
                    読み込み
                  </button>
                </div>
              ))
            )}
          </div>
        </div>
      )}

      <div className={styles.editorSection}>
        <textarea
          className={styles.editor}
          value={content}
          onChange={(e) => setContent(e.target.value)}
          placeholder={placeholder}
          maxLength={maxLength}
          rows={15}
        />
        
        <div className={styles.editorFooter}>
          <div className={styles.metadata}>
            {showWordCount && (
              <span className={styles.wordCount}>
                {getWordCount()} 文字 / {maxLength}
              </span>
            )}
            {showTimestamp && lastSaved && (
              <span className={styles.lastSaved}>
                最終保存: {formatTimestamp(lastSaved)}
              </span>
            )}
          </div>
          
          {autoSave && (
            <div className={styles.autoSaveIndicator}>
              {isSaving ? (
                <span className={styles.saving}>💾 自動保存中...</span>
              ) : (
                <span className={styles.autoSaveEnabled}>🔄 自動保存有効</span>
              )}
            </div>
          )}
        </div>
      </div>

      <div className={styles.tips}>
        <h4>📝 効果的なノートの取り方</h4>
        <ul>
          <li><strong>要点を整理:</strong> 重要なポイントを箇条書きでまとめる</li>
          <li><strong>自分の言葉で:</strong> 理解した内容を自分の言葉で説明する</li>
          <li><strong>疑問を記録:</strong> わからない点や疑問も書き留める</li>
          <li><strong>関連付け:</strong> 既知の知識との関連性を記述する</li>
          <li><strong>定期的に見返し:</strong> 復習時に活用する</li>
        </ul>
      </div>
    </div>
  );
}
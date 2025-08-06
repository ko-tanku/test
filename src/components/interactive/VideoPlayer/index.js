import React, { useState, useRef, useEffect, useCallback } from 'react';
import styles from './styles.module.css';

export default function VideoPlayer({ 
  src,
  poster,
  title = "ビデオプレーヤー",
  width = '100%',
  height = 'auto',
  autoPlay = false,
  loop = false,
  muted = false,
  controls = true,
  showProgress = true,
  showVolume = true,
  showFullscreen = true,
  playbackRates = [0.5, 0.75, 1, 1.25, 1.5, 2],
  className = '',
  onPlay,
  onPause,
  onEnded,
  onTimeUpdate,
  onLoadedMetadata,
  onError,
  ...props 
}) {
  const videoRef = useRef(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [volume, setVolume] = useState(1);
  const [isMuted, setIsMuted] = useState(muted);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [playbackRate, setPlaybackRate] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showControls, setShowControls] = useState(true);
  const [isDragging, setIsDragging] = useState(false);
  const controlsTimeoutRef = useRef(null);

  // ビデオイベントハンドラー
  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;

    const handleLoadStart = () => setLoading(true);
    const handleLoadedData = () => setLoading(false);
    const handleLoadedMetadata = () => {
      setDuration(video.duration);
      setLoading(false);
      if (onLoadedMetadata) onLoadedMetadata();
    };
    const handleTimeUpdate = () => {
      if (!isDragging) {
        setCurrentTime(video.currentTime);
      }
      if (onTimeUpdate) onTimeUpdate(video.currentTime);
    };
    const handlePlay = () => {
      setIsPlaying(true);
      if (onPlay) onPlay();
    };
    const handlePause = () => {
      setIsPlaying(false);
      if (onPause) onPause();
    };
    const handleEnded = () => {
      setIsPlaying(false);
      if (onEnded) onEnded();
    };
    const handleError = (e) => {
      setError('ビデオの読み込みに失敗しました');
      setLoading(false);
      if (onError) onError(e);
    };
    const handleVolumeChange = () => {
      setVolume(video.volume);
      setIsMuted(video.muted);
    };

    video.addEventListener('loadstart', handleLoadStart);
    video.addEventListener('loadeddata', handleLoadedData);
    video.addEventListener('loadedmetadata', handleLoadedMetadata);
    video.addEventListener('timeupdate', handleTimeUpdate);
    video.addEventListener('play', handlePlay);
    video.addEventListener('pause', handlePause);
    video.addEventListener('ended', handleEnded);
    video.addEventListener('error', handleError);
    video.addEventListener('volumechange', handleVolumeChange);

    return () => {
      video.removeEventListener('loadstart', handleLoadStart);
      video.removeEventListener('loadeddata', handleLoadedData);
      video.removeEventListener('loadedmetadata', handleLoadedMetadata);
      video.removeEventListener('timeupdate', handleTimeUpdate);
      video.removeEventListener('play', handlePlay);
      video.removeEventListener('pause', handlePause);
      video.removeEventListener('ended', handleEnded);
      video.removeEventListener('error', handleError);
      video.removeEventListener('volumechange', handleVolumeChange);
    };
  }, [isDragging, onLoadedMetadata, onTimeUpdate, onPlay, onPause, onEnded, onError]);

  // フルスクリーンイベント
  useEffect(() => {
    const handleFullscreenChange = () => {
      setIsFullscreen(!!document.fullscreenElement);
    };

    document.addEventListener('fullscreenchange', handleFullscreenChange);
    return () => {
      document.removeEventListener('fullscreenchange', handleFullscreenChange);
    };
  }, []);

  // コントロールの自動非表示
  const resetControlsTimeout = useCallback(() => {
    if (controlsTimeoutRef.current) {
      clearTimeout(controlsTimeoutRef.current);
    }
    setShowControls(true);
    controlsTimeoutRef.current = setTimeout(() => {
      if (isPlaying) {
        setShowControls(false);
      }
    }, 3000);
  }, [isPlaying]);

  // Cleanup timeout on unmount
  useEffect(() => {
    return () => {
      if (controlsTimeoutRef.current) {
        clearTimeout(controlsTimeoutRef.current);
      }
    };
  }, []);

  const handleMouseMove = () => {
    resetControlsTimeout();
  };

  const handleMouseLeave = () => {
    if (isPlaying) {
      setShowControls(false);
    }
  };

  // 再生/一時停止
  const togglePlay = () => {
    const video = videoRef.current;
    if (!video) return;

    if (isPlaying) {
      video.pause();
    } else {
      video.play().catch((e) => {
        setError('再生に失敗しました');
      });
    }
  };

  // シークバーの操作
  const handleSeek = (e) => {
    const video = videoRef.current;
    if (!video || !duration) return;

    const rect = e.currentTarget.getBoundingClientRect();
    const pos = (e.clientX - rect.left) / rect.width;
    const newTime = pos * duration;
    
    video.currentTime = newTime;
    setCurrentTime(newTime);
  };

  const handleSeekStart = () => {
    setIsDragging(true);
  };

  const handleSeekEnd = () => {
    setIsDragging(false);
  };

  // 音量操作
  const handleVolumeChange = (e) => {
    const video = videoRef.current;
    if (!video) return;

    const newVolume = parseFloat(e.target.value);
    video.volume = newVolume;
    setVolume(newVolume);
    
    if (newVolume === 0) {
      setIsMuted(true);
      video.muted = true;
    } else if (isMuted) {
      setIsMuted(false);
      video.muted = false;
    }
  };

  const toggleMute = () => {
    const video = videoRef.current;
    if (!video) return;

    const newMuted = !isMuted;
    video.muted = newMuted;
    setIsMuted(newMuted);
  };

  // 再生速度変更
  const handlePlaybackRateChange = (rate) => {
    const video = videoRef.current;
    if (!video) return;

    video.playbackRate = rate;
    setPlaybackRate(rate);
  };

  // フルスクリーン切り替え
  const toggleFullscreen = () => {
    const container = videoRef.current?.parentElement;
    if (!container) return;

    if (!document.fullscreenElement) {
      container.requestFullscreen().catch((e) => {
        console.error('フルスクリーンに失敗しました:', e);
      });
    } else {
      document.exitFullscreen();
    }
  };

  // 時間フォーマット
  const formatTime = (seconds) => {
    if (isNaN(seconds)) return '0:00';
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  // 進捗率計算
  const progressPercentage = duration ? (currentTime / duration) * 100 : 0;

  if (!src) {
    return (
      <div className={`${styles.videoPlayer} ${className}`}>
        <div className={styles.error}>
          ビデオソースが指定されていません
        </div>
      </div>
    );
  }

  return (
    <div className={`${styles.videoPlayer} ${className}`} {...props}>
      {title && <div className={styles.title}>{title}</div>}
      
      <div 
        className={`${styles.videoContainer} ${
          isFullscreen ? styles.fullscreen : ''
        }`}
        onMouseMove={handleMouseMove}
        onMouseLeave={handleMouseLeave}
      >
        <video
          ref={videoRef}
          src={src}
          poster={poster}
          width={width}
          height={height}
          autoPlay={autoPlay}
          loop={loop}
          muted={muted}
          controls={false} // カスタムコントロールを使用
          className={styles.video}
          onClick={togglePlay}
        />
        
        {loading && (
          <div className={styles.loading}>
            <div className={styles.spinner}></div>
            読み込み中...
          </div>
        )}
        
        {error && (
          <div className={styles.error}>
            {error}
          </div>
        )}
        
        {controls && (
          <div className={`${styles.controls} ${
            showControls ? styles.controlsVisible : styles.controlsHidden
          }`}>
            {showProgress && (
              <div className={styles.progressContainer}>
                <div 
                  className={styles.progressBar}
                  onClick={handleSeek}
                  onMouseDown={handleSeekStart}
                  onMouseUp={handleSeekEnd}
                >
                  <div 
                    className={styles.progressFilled}
                    style={{ width: `${progressPercentage}%` }}
                  />
                  <div 
                    className={styles.progressHandle}
                    style={{ left: `${progressPercentage}%` }}
                  />
                </div>
                <div className={styles.timeDisplay}>
                  <span>{formatTime(currentTime)}</span>
                  <span> / </span>
                  <span>{formatTime(duration)}</span>
                </div>
              </div>
            )}
            
            <div className={styles.controlsBottom}>
              <div className={styles.controlsLeft}>
                <button 
                  className={styles.playButton}
                  onClick={togglePlay}
                  aria-label={isPlaying ? '一時停止' : '再生'}
                >
                  {isPlaying ? '⏸️' : '▶️'}
                </button>
                
                {showVolume && (
                  <div className={styles.volumeContainer}>
                    <button 
                      className={styles.muteButton}
                      onClick={toggleMute}
                      aria-label={isMuted ? 'ミュート解除' : 'ミュート'}
                    >
                      {isMuted || volume === 0 ? '🔇' : volume < 0.5 ? '🔉' : '🔊'}
                    </button>
                    <input
                      type="range"
                      min="0"
                      max="1"
                      step="0.1"
                      value={isMuted ? 0 : volume}
                      onChange={handleVolumeChange}
                      className={styles.volumeSlider}
                    />
                  </div>
                )}
              </div>
              
              <div className={styles.controlsRight}>
                <select 
                  value={playbackRate}
                  onChange={(e) => handlePlaybackRateChange(parseFloat(e.target.value))}
                  className={styles.playbackRateSelect}
                >
                  {playbackRates.map(rate => (
                    <option key={rate} value={rate}>
                      {rate}x
                    </option>
                  ))}
                </select>
                
                {showFullscreen && (
                  <button 
                    className={styles.fullscreenButton}
                    onClick={toggleFullscreen}
                    aria-label={isFullscreen ? 'フルスクリーン終了' : 'フルスクリーン'}
                  >
                    {isFullscreen ? '⏹️' : '⛶️'}
                  </button>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
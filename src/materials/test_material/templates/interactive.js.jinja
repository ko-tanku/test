// 学習材料インタラクティブ機能 - テンプレート
(function() {
    'use strict';
    
    // 設定値
    const config = {
        debugMode: {{ debug_mode | default('false') }},
        animationSpeed: {{ animation_speed | default('300') }},
        autoSave: {{ auto_save | default('true') }},
        theme: '{{ theme | default("default") }}'
    };
    
    // グローバル変数
    window.LearningMaterial = {
        initialized: false,
        currentChapter: 1,
        completedChapters: new Set(),
        settings: {
            autoSave: config.autoSave,
            showHints: true,
            animationSpeed: 'normal',
            theme: config.theme
        },
        config: config
    };
    
    // 初期化
    document.addEventListener('DOMContentLoaded', function() {
        initLearningFeatures();
        loadUserProgress();
        setupEventListeners();
        
        window.LearningMaterial.initialized = true;
        if (config.debugMode) {
            console.log('学習材料システム初期化完了', window.LearningMaterial);
        }
    });
    
    function initLearningFeatures() {
        // ツールチップ拡張
        initEnhancedTooltips();
        
        // 進度追跡
        initProgressTracking();
        
        // 章完了検出
        initChapterCompletion();
        
        // ページ間ナビゲーション
        initNavigation();
        
        // クイズシステム初期化
        initQuizSystems();
    }
    
    function initEnhancedTooltips() {
        const tooltips = document.querySelectorAll('.custom-tooltip');
        
        tooltips.forEach(function(tooltip) {
            // クリックでツールチップを固定
            tooltip.addEventListener('click', function(e) {
                e.preventDefault();
                toggleTooltipPin(this);
            });
            
            // 長押しで詳細表示
            let pressTimer;
            tooltip.addEventListener('mousedown', function() {
                pressTimer = setTimeout(() => {
                    showDetailedTooltip(this);
                }, 800);
            });
            
            tooltip.addEventListener('mouseup', function() {
                clearTimeout(pressTimer);
            });
        });
    }
    
    function toggleTooltipPin(element) {
        element.classList.toggle('tooltip-pinned');
        
        if (element.classList.contains('tooltip-pinned')) {
            // 他の固定ツールチップを閉じる
            document.querySelectorAll('.tooltip-pinned').forEach(function(pinned) {
                if (pinned !== element) {
                    pinned.classList.remove('tooltip-pinned');
                }
            });
        }
    }
    
    function showDetailedTooltip(element) {
        const term = element.textContent;
        const tooltip = element.getAttribute('data-tooltip');
        
        if (config.debugMode) {
            console.log('詳細表示:', term, tooltip);
        }
    }
    
    function initProgressTracking() {
        // スクロール進度の追跡
        let ticking = false;
        
        function updateScrollProgress() {
            const scrolled = window.pageYOffset;
            const maxHeight = document.body.scrollHeight - window.innerHeight;
            const progress = maxHeight > 0 ? (scrolled / maxHeight) * 100 : 0;
            
            document.documentElement.style.setProperty('--scroll-progress', progress + '%');
            ticking = false;
        }
        
        window.addEventListener('scroll', function() {
            if (!ticking) {
                requestAnimationFrame(updateScrollProgress);
                ticking = true;
            }
        });
    }
    
    function initChapterCompletion() {
        // ページの最下部に到達したら章完了とみなす
        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    markChapterComplete();
                }
            });
        }, { threshold: 1.0 });
        
        // フッターを観察対象にする
        const footer = document.querySelector('footer, .md-footer');
        if (footer) {
            observer.observe(footer);
        }
    }
    
    function markChapterComplete() {
        const currentPath = window.location.pathname;
        const chapterMatch = currentPath.match(/chapter(\d+)/);
        
        if (chapterMatch) {
            const chapterNum = parseInt(chapterMatch[1]);
            window.LearningMaterial.completedChapters.add(chapterNum);
            
            if (window.LearningMaterial.settings.autoSave) {
                saveUserProgress();
            }
            
            showChapterCompleteNotification(chapterNum);
        }
    }
    
    function showChapterCompleteNotification(chapterNum) {
        // 章完了通知の表示
        const notification = document.createElement('div');
        notification.className = 'chapter-complete-notification';
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #4CAF50;
            color: white;
            padding: 15px 20px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            z-index: 10000;
            animation: slideInRight 0.3s ease-out;
        `;
        notification.innerHTML = `
            <div class="notification-content">
                <span class="notification-icon">✅</span>
                <span class="notification-text">第${chapterNum}章を完了しました！</span>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // アニメーション後に削除
        setTimeout(() => {
            notification.style.animation = 'slideOutRight 0.3s ease-in';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.remove();
                }
            }, 300);
        }, 3000);
    }
    
    function initNavigation() {
        // キーボードナビゲーション
        document.addEventListener('keydown', function(e) {
            // Alt + 左矢印: 前のページ
            if (e.altKey && e.key === 'ArrowLeft') {
                const prevLink = document.querySelector('a[rel="prev"]');
                if (prevLink) prevLink.click();
            }
            
            // Alt + 右矢印: 次のページ
            if (e.altKey && e.key === 'ArrowRight') {
                const nextLink = document.querySelector('a[rel="next"]');
                if (nextLink) nextLink.click();
            }
        });
    }
    
    function initQuizSystems() {
        // 各種クイズシステムの初期化
        initSingleChoiceQuizzes();
        initCategorizationQuizzes();
        initMultipleChoiceQuizzes();
    }
    
    function initSingleChoiceQuizzes() {
        // 単一選択クイズは外部のcheckSingleChoice関数に依存
        if (config.debugMode) {
            console.log('単一選択クイズシステム初期化完了');
        }
    }
    
    function initCategorizationQuizzes() {
        const categorizationQuizzes = document.querySelectorAll('.categorization-quiz');

        categorizationQuizzes.forEach(quiz => {
            const draggableItems = quiz.querySelectorAll('.draggable-item');
            const dropZones = quiz.querySelectorAll('.drop-zone');

            // ドラッグ可能なアイテムのイベントリスナー
            draggableItems.forEach(item => {
                item.addEventListener('dragstart', function(e) {
                    e.dataTransfer.setData('text/plain', item.id);
                    item.classList.add('dragging');
                });

                item.addEventListener('dragend', function() {
                    item.classList.remove('dragging');
                });
            });

            // ドロップゾーンのイベントリスナー
            dropZones.forEach(zone => {
                zone.addEventListener('dragover', function(e) {
                    e.preventDefault();
                    zone.classList.add('drag-over');
                });

                zone.addEventListener('dragleave', function(e) {
                    if (!zone.contains(e.relatedTarget)) {
                        zone.classList.remove('drag-over');
                    }
                });

                zone.addEventListener('drop', function(e) {
                    e.preventDefault();
                    zone.classList.remove('drag-over');

                    const draggedItemId = e.dataTransfer.getData('text/plain');
                    const draggedElement = document.getElementById(draggedItemId);

                    if (draggedElement) {
                        const initialDraggableItemsPool = quiz.querySelector('.draggable-items');

                        if (initialDraggableItemsPool && initialDraggableItemsPool.contains(draggedElement)) {
                            initialDraggableItemsPool.removeChild(draggedElement);
                        } else if (draggedElement.parentElement && draggedElement.parentElement.classList.contains('drop-area')) {
                            draggedElement.parentElement.removeChild(draggedElement);
                        }

                        const dropArea = zone.querySelector('.drop-area');
                        if (dropArea) {
                            dropArea.appendChild(draggedElement);
                        }
                    }
                });
            });
        });
        
        if (config.debugMode) {
            console.log('カテゴリ分けクイズシステム初期化完了');
        }
    }
    
    function initMultipleChoiceQuizzes() {
        // 複数選択クイズは外部のcheckMultipleChoice関数に依存
        if (config.debugMode) {
            console.log('複数選択クイズシステム初期化完了');
        }
    }
    
    function loadUserProgress() {
        try {
            const saved = localStorage.getItem('learning_progress');
            if (saved) {
                const data = JSON.parse(saved);
                window.LearningMaterial.completedChapters = new Set(data.completedChapters || []);
                window.LearningMaterial.settings = Object.assign(
                    window.LearningMaterial.settings, 
                    data.settings || {}
                );
                
                if (config.debugMode) {
                    console.log('学習進度を読み込みました:', data);
                }
            }
        } catch (e) {
            console.warn('学習進度の読み込みに失敗:', e);
        }
    }
    
    function saveUserProgress() {
        try {
            const data = {
                completedChapters: Array.from(window.LearningMaterial.completedChapters),
                settings: window.LearningMaterial.settings,
                lastAccess: new Date().toISOString()
            };
            
            localStorage.setItem('learning_progress', JSON.stringify(data));
            
            if (config.debugMode) {
                console.log('学習進度を保存しました:', data);
            }
        } catch (e) {
            console.warn('学習進度の保存に失敗:', e);
        }
    }
    
    function setupEventListeners() {
        // 設定変更の監視
        document.addEventListener('change', function(e) {
            if (e.target.matches('.learning-setting')) {
                const setting = e.target.dataset.setting;
                const value = e.target.type === 'checkbox' ? e.target.checked : e.target.value;
                
                window.LearningMaterial.settings[setting] = value;
                
                if (window.LearningMaterial.settings.autoSave) {
                    saveUserProgress();
                }
                
                if (config.debugMode) {
                    console.log('設定変更:', setting, value);
                }
            }
        });
    }
    
    // CSSアニメーション定義を追加
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideInRight {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        @keyframes slideOutRight {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(100%);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
    
    // 公開API
    window.LearningMaterial.api = {
        markChapterComplete: markChapterComplete,
        saveProgress: saveUserProgress,
        loadProgress: loadUserProgress,
        resetProgress: function() {
            localStorage.removeItem('learning_progress');
            window.LearningMaterial.completedChapters.clear();
            if (config.debugMode) {
                console.log('学習進度をリセットしました');
            }
        },
        getProgress: function() {
            return {
                completedChapters: Array.from(window.LearningMaterial.completedChapters),
                settings: window.LearningMaterial.settings
            };
        }
    };
    
})();
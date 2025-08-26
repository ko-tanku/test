<<<<<<< HEAD
// インタラクティブ機能拡張

(function() {
    'use strict';
    
    // アコーディオン機能
    function initAccordions() {
        const accordions = document.querySelectorAll('.accordion-toggle');
        accordions.forEach(function(toggle) {
            toggle.addEventListener('click', function() {
                const content = this.nextElementSibling;
                const isOpen = content.style.display === 'block';
                
                content.style.display = isOpen ? 'none' : 'block';
                this.classList.toggle('active');
            });
        });
    }
    
    // タブ機能
    function initTabs() {
        const tabButtons = document.querySelectorAll('.tab-button');
        tabButtons.forEach(function(button) {
            button.addEventListener('click', function() {
                const tabGroup = this.closest('.tab-group');
                const targetTab = this.getAttribute('data-tab');
                
                // すべてのタブボタンとコンテンツを非アクティブ化
                tabGroup.querySelectorAll('.tab-button').forEach(b => b.classList.remove('active'));
                tabGroup.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
                
                // 選択されたタブをアクティブ化
                this.classList.add('active');
                tabGroup.querySelector(`[data-tab-content="${targetTab}"]`).classList.add('active');
            });
        });
    }
    
    // クイズ機能
    function initQuizzes() {
        if (!window.quizData || !window.quizData.quizzes) {
            console.warn("クイズデータが見つかりません。");
            return;
        }

        for (const quizId in window.quizData.quizzes) {
            const quiz = window.quizData.quizzes[quizId];
            const quizContainer = document.querySelector(`[data-quiz-id="${quizId}"]`);

            if (!quizContainer) {
                console.warn(`クイズコンテナが見つかりません: ${quizId}`);
                continue;
            }

            // 既存のコンテンツをクリア
            quizContainer.innerHTML = '';

            // クイズタイプに応じてコンテンツを生成
            switch (quiz.type) {
                case 'single-choice':
                    createSingleChoiceQuiz(quizContainer, quiz, quizId);
                    break;
                case 'multiple-choice':
                    createMultipleChoiceQuiz(quizContainer, quiz, quizId);
                    break;
                case 'categorization':
                    createCategorizationQuiz(quizContainer, quiz, quizId);
                    break;
                default:
                    console.warn(`不明なクイズタイプ: ${quiz.type}`);
            }
=======
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
>>>>>>> dbde2096846e5b4398413351225cc5f784d336f1
        }
    }
    
    function initCategorizationQuizzes() {
        const categorizationQuizzes = document.querySelectorAll('.categorization-quiz');
<<<<<<< HEAD
        
        categorizationQuizzes.forEach(quiz => {
            const draggableItems = quiz.querySelectorAll('.draggable-item');
            const dropZones = quiz.querySelectorAll('.drop-area');
            
            // ドラッグ可能なアイテムのイベントリスナー
            draggableItems.forEach(item => {
                item.addEventListener('dragstart', function(e) {
                    e.dataTransfer.setData('text/plain', item.dataset.item);
                    e.dataTransfer.setData('text/html', item.outerHTML);
                    item.classList.add('dragging');
                });
                
=======

        categorizationQuizzes.forEach(quiz => {
            const draggableItems = quiz.querySelectorAll('.draggable-item');
            const dropZones = quiz.querySelectorAll('.drop-zone');

            // ドラッグ可能なアイテムのイベントリスナー
            draggableItems.forEach(item => {
                item.addEventListener('dragstart', function(e) {
                    e.dataTransfer.setData('text/plain', item.id);
                    item.classList.add('dragging');
                });

>>>>>>> dbde2096846e5b4398413351225cc5f784d336f1
                item.addEventListener('dragend', function() {
                    item.classList.remove('dragging');
                });
            });
<<<<<<< HEAD
            
=======

>>>>>>> dbde2096846e5b4398413351225cc5f784d336f1
            // ドロップゾーンのイベントリスナー
            dropZones.forEach(zone => {
                zone.addEventListener('dragover', function(e) {
                    e.preventDefault();
                    zone.classList.add('drag-over');
                });
<<<<<<< HEAD
                
=======

>>>>>>> dbde2096846e5b4398413351225cc5f784d336f1
                zone.addEventListener('dragleave', function(e) {
                    if (!zone.contains(e.relatedTarget)) {
                        zone.classList.remove('drag-over');
                    }
                });
<<<<<<< HEAD
                
                zone.addEventListener('drop', function(e) {
                    e.preventDefault();
                    zone.classList.remove('drag-over');
                    
                    const itemIndex = e.dataTransfer.getData('text/plain');
                    const itemHTML = e.dataTransfer.getData('text/html');
                    
                    // 既存のアイテムを削除（他の場所から移動された場合）
                    const existingItem = document.querySelector(`[data-item="${itemIndex}"]`);
                    if (existingItem) {
                        existingItem.remove();
                    }
                    
                    // 新しいアイテムを追加（上書きではなく追加）
                    const tempDiv = document.createElement('div');
                    tempDiv.innerHTML = itemHTML;
                    const newItem = tempDiv.firstElementChild;
                    
                    // 「ここにドロップしてください」のテキストがある場合は削除
                    if (zone.textContent.trim() === 'ここにドロップしてください') {
                        zone.textContent = '';
                    }
                    
                    zone.appendChild(newItem);
                    
                    // イベントリスナーを再設定
                    if (newItem) {
                        newItem.addEventListener('dragstart', function(e) {
                            e.dataTransfer.setData('text/plain', newItem.dataset.item);
                            e.dataTransfer.setData('text/html', newItem.outerHTML);
                            newItem.classList.add('dragging');
                        });
                        
                        newItem.addEventListener('dragend', function() {
                            newItem.classList.remove('dragging');
                        });
=======

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
>>>>>>> dbde2096846e5b4398413351225cc5f784d336f1
                    }
                });
            });
        });
<<<<<<< HEAD
    }
    
    // ツールチップ機能（クリックベース、自動位置調整付き）
    function initClickableTooltips() {
        const HIDE_ALL_EVENT = 'hide-all-tooltips';

        function hideAllTooltips() {
            document.querySelectorAll('.tooltip-popup.visible').forEach(popup => {
                popup.remove();
            });
        }

        // カスタムイベントで非表示にする
        document.addEventListener(HIDE_ALL_EVENT, hideAllTooltips);
        // ドキュメントのどこかをクリックしても非表示にする
        document.addEventListener('click', () => {
             document.dispatchEvent(new CustomEvent(HIDE_ALL_EVENT));
        });

        document.querySelectorAll('.custom-tooltip').forEach(tooltipAnchor => {
            tooltipAnchor.addEventListener('click', function(event) {
                event.stopPropagation();

                const tooltipText = this.getAttribute('data-tooltip');
                if (!tooltipText) return;

                // 既に表示されているポップアップがあれば削除（トグル動作）
                const existingPopup = document.querySelector(`.tooltip-popup[data-owner="${this.textContent}"]`);
                if (existingPopup) {
                    existingPopup.remove();
                    return;
                }

                // 他のツールチップを非表示にする
                document.dispatchEvent(new CustomEvent(HIDE_ALL_EVENT));

                // 新しいツールチップポップアップを作成
                const popup = document.createElement('div');
                popup.className = 'tooltip-popup';
                popup.textContent = tooltipText;
                popup.dataset.owner = this.textContent; // オーナーを識別
                document.body.appendChild(popup);

                // 位置調整
                const anchorRect = this.getBoundingClientRect();
                const popupRect = popup.getBoundingClientRect();
                const margin = 8; // アンカーとのマージン

                let top = anchorRect.top - popupRect.height - margin;
                let left = anchorRect.left + (anchorRect.width / 2) - (popupRect.width / 2);

                // 上下左右が画面外に出ないように調整
                if (top < 0) { // 上にはみ出る場合
                    top = anchorRect.bottom + margin;
                }
                if (left < 0) { // 左にはみ出る場合
                    left = margin;
                }
                if (left + popupRect.width > window.innerWidth) { // 右にはみ出る場合
                    left = window.innerWidth - popupRect.width - margin;
                }

                popup.style.top = `${top}px`;
                popup.style.left = `${left}px`;

                // 表示
                setTimeout(() => popup.classList.add('visible'), 10);
            });
        });
    }

    // 初期化
    document.addEventListener('DOMContentLoaded', function() {
        initAccordions();
        initTabs();
        initQuizzes();
        initClickableTooltips(); // 新しいツールチップ初期化関数を呼び出し
    });
    
    // グローバル関数として公開
    window.checkCategorization = function(quizId) {
        const quizContainer = document.querySelector(`[data-quiz-id="${quizId}"]`);
        if (!quizContainer) return;

        const dropZones = quizContainer.querySelectorAll('.drop-area');
        const result = quizContainer.querySelector('.categorization-result');
        const quiz = window.quizData ? window.quizData.quizzes[quizId] : null;
        
        if (!quiz) {
            result.innerHTML = '<div class="error">クイズデータが見つかりません</div>';
            return;
        }

        let userAnswers = [];
        let allItemsPlaced = true;

        // 各ドロップゾーンから回答を収集
        dropZones.forEach((zone, categoryIndex) => {
            const items = zone.querySelectorAll('.draggable-item');
            items.forEach(item => {
                const itemIndex = parseInt(item.dataset.item);
                userAnswers[itemIndex] = categoryIndex;
            });
        });

        // 全てのアイテムが配置されているかチェック
        for (let i = 0; i < quiz.items.length; i++) {
            if (userAnswers[i] === undefined) {
                allItemsPlaced = false;
                break;
            }
        }

        if (!allItemsPlaced) {
            result.innerHTML = '<div class="warning">全ての項目を分類してください</div>';
            return;
        }

        // 正解数をカウント
        let correctCount = 0;
        for (let i = 0; i < quiz.items.length; i++) {
            if (userAnswers[i] === quiz.items[i].correct_category) {
                correctCount++;
            }
        }

        // 結果表示
        const percentage = Math.round((correctCount / quiz.items.length) * 100);
        let resultClass = percentage >= 80 ? 'success' : percentage >= 60 ? 'warning' : 'error';
        
        result.innerHTML = `
            <div class="${resultClass}">
                <strong>結果: ${correctCount}/${quiz.items.length}問正解 (${percentage}%)</strong>
            </div>
        `;
    };
    
    window.checkMultipleChoice = function(quizId) {
        const quizContainer = document.querySelector(`[data-quiz-id="${quizId}"]`);
        if (!quizContainer) return;

        const checkboxes = quizContainer.querySelectorAll(`input[name="${quizId}"]`);
        const result = quizContainer.querySelector('.multiple-choice-result');
        const quiz = window.quizData ? window.quizData.quizzes[quizId] : null;
        
        if (!quiz) {
            result.innerHTML = '<div class="error">クイズデータが見つかりません</div>';
            return;
        }

        // ユーザーの選択を収集
        let selectedIndices = [];
        checkboxes.forEach((checkbox, index) => {
            if (checkbox.checked) {
                selectedIndices.push(index);
            }
        });

        // 正解数をチェック
        const correctIndices = quiz.correct;
        let isFullyCorrect = true;
        
        correctIndices.forEach(correctIndex => {
            if (!selectedIndices.includes(correctIndex)) {
                isFullyCorrect = false;
            }
        });
        
        selectedIndices.forEach(selectedIndex => {
            if (!correctIndices.includes(selectedIndex)) {
                isFullyCorrect = false;
            }
        });

        // 結果表示
        let resultHTML = '';
        if (isFullyCorrect) {
            resultHTML = `
                <div class="success">
                    <strong>正解！</strong><br>
                    ${quiz.explanation}
                </div>
            `;
        } else {
            const correctCount = selectedIndices.filter(idx => correctIndices.includes(idx)).length;
            const incorrectCount = selectedIndices.filter(idx => !correctIndices.includes(idx)).length;
            const missedCount = correctIndices.filter(idx => !selectedIndices.includes(idx)).length;
            
            resultHTML = `
                <div class="warning">
                    <strong>部分的に正解</strong><br>
                    正しく選択: ${correctCount}個<br>
                    誤って選択: ${incorrectCount}個<br>
                    選択漏れ: ${missedCount}個<br><br>
                    <strong>正解:</strong> ${correctIndices.map(i => i + 1).join(', ')}番<br>
                    ${quiz.explanation}
                </div>
            `;
        }
        
        result.innerHTML = resultHTML;
    };

    window.checkSingleChoice = function(quizId) {
        const quizContainer = document.querySelector(`[data-quiz-id="${quizId}"]`);
        if (!quizContainer) return;

        const radioButtons = quizContainer.querySelectorAll(`input[name="${quizId}"]`);
        const result = quizContainer.querySelector('.single-choice-result');
        const quiz = window.quizData ? window.quizData.quizzes[quizId] : null;

        if (!quiz) {
            result.innerHTML = '<div class="error">クイズデータが見つかりません</div>';
            return;
        }

        let selectedIndex = -1;
        radioButtons.forEach((radio, index) => {
            if (radio.checked) {
                selectedIndex = index;
            }
        });

        if (selectedIndex === -1) {
            result.innerHTML = '<div class="warning">選択肢を選んでください</div>';
            return;
        }

        let isCorrect = (selectedIndex === quiz.correct);

        let resultHTML = '';
        if (isCorrect) {
            resultHTML = `
                <div class="success">
                    <strong>正解！</strong><br>
                    ${quiz.explanation || ''}
                </div>
            `;
        } else {
            resultHTML = `
                <div class="incorrect">
                    <strong>不正解</strong><br>
                    正解は ${quiz.correct + 1} 番です。<br>
                    ${quiz.explanation || ''}
                </div>
            `;
        }
        result.innerHTML = resultHTML;
    };

    // 分類クイズ生成関数
    function createCategorizationQuiz(quizContainer, quiz, quizId) {
        const questionHTML = `
            <div class="quiz-question">
                <h4>${quiz.question}</h4>
            </div>
        `;

        // アイテムエリア（ドラッグ元）
        const itemsHTML = quiz.items.map((item, index) => `
            <div class="draggable-item" draggable="true" data-item="${index}">
                ${item.name}
            </div>
        `).join('');

        // カテゴリエリア（ドロップ先）
        const categoriesHTML = quiz.categories.map((category, index) => `
            <div class="drop-zone">
                <h4>${category}</h4>
                <div class="drop-area" data-category="${index}">
                    ここにドロップしてください
                </div>
            </div>
        `).join('');

        const quizHTML = `
            ${questionHTML}
            <div class="categorization-quiz">
                <div class="items-pool">
                    <h5>分類対象の項目:</h5>
                    <div class="draggable-items">
                        ${itemsHTML}
                    </div>
                </div>
                <div class="categories-container">
                    ${categoriesHTML}
                </div>
                <button class="check-categorization" onclick="checkCategorization('${quizId}')">
                    解答をチェック
                </button>
                <div class="categorization-result"></div>
            </div>
        `;

        quizContainer.innerHTML = quizHTML;

        // ドラッグ&ドロップイベントの設定
        initCategorizationDragDrop(quizContainer);
    }

    // 単一選択クイズ生成関数
    function createSingleChoiceQuiz(quizContainer, quiz, quizId) {
        const optionsHTML = quiz.options.map((option, index) => `
            <label class="option-label">
                <input type="radio" name="${quizId}" value="${index}">
                <span class="option-text">${option}</span>
            </label>
        `).join('');

        const quizHTML = `
            <div class="single-choice-quiz">
                <div class="quiz-question">
                    <h4>${quiz.question}</h4>
                </div>
                <div class="quiz-options">
                    ${optionsHTML}
                </div>
                <button class="check-single-choice" onclick="checkSingleChoice('${quizId}')">
                    答えを確認
                </button>
                <div class="single-choice-result"></div>
            </div>
        `;

        quizContainer.innerHTML = quizHTML;
    }

    // 複数選択クイズ生成関数
    function createMultipleChoiceQuiz(quizContainer, quiz, quizId) {
        const optionsHTML = quiz.options.map((option, index) => `
            <label class="option-label">
                <input type="checkbox" name="${quizId}" value="${index}">
                <span class="option-text">${option}</span>
            </label>
        `).join('');

        const quizHTML = `
            <div class="multiple-choice-quiz">
                <div class="quiz-question">
                    <h4>${quiz.question}</h4>
                </div>
                <div class="quiz-options">
                    ${optionsHTML}
                </div>
                <button class="check-multiple-choice" onclick="checkMultipleChoice('${quizId}')">
                    回答をチェック
                </button>
                <div class="multiple-choice-result"></div>
            </div>
        `;

        quizContainer.innerHTML = quizHTML;
    }

    // 分類クイズのドラッグ&ドロップ初期化
    function initCategorizationDragDrop(quizContainer) {
        const draggableItems = quizContainer.querySelectorAll('.draggable-item');
        const dropAreas = quizContainer.querySelectorAll('.drop-area');

        // ドラッグ可能アイテムのイベント
        draggableItems.forEach(item => {
            item.addEventListener('dragstart', function(e) {
                e.dataTransfer.setData('text/plain', item.dataset.item);
                e.dataTransfer.setData('text/html', item.outerHTML);
                item.classList.add('dragging');
            });

            item.addEventListener('dragend', function() {
                item.classList.remove('dragging');
            });
        });

        // ドロップエリアのイベント
        dropAreas.forEach(area => {
            area.addEventListener('dragover', function(e) {
                e.preventDefault();
                area.classList.add('drag-over');
            });

            area.addEventListener('dragleave', function(e) {
                if (!area.contains(e.relatedTarget)) {
                    area.classList.remove('drag-over');
                }
            });

            area.addEventListener('drop', function(e) {
                e.preventDefault();
                area.classList.remove('drag-over');

                const itemIndex = e.dataTransfer.getData('text/plain');
                
                if (!itemIndex) {
                    console.warn('ドラッグデータが不完全です');
                    return;
                }

                // 既存のアイテムを探して移動
                const existingItem = quizContainer.querySelector(`[data-item="${itemIndex}"]`);
                if (!existingItem) {
                    console.warn('ドラッグされた要素が見つかりません');
                    return;
                }

                // プレースホルダーテキストをクリア（子要素がある場合のみ）
                if (area.children.length === 0 && area.textContent.trim() === 'ここにドロップしてください') {
                    area.textContent = '';
                }

                // 要素を移動（コピーではなく移動）
                area.appendChild(existingItem);

                // ドラッグイベントを再設定
                initDragEvents(existingItem, quizContainer);
            });
        });
    }

    // 個別アイテムのドラッグイベント初期化
    function initDragEvents(item, quizContainer) {
        item.addEventListener('dragstart', function(e) {
            e.dataTransfer.setData('text/plain', item.dataset.item);
            e.dataTransfer.setData('text/html', item.outerHTML);
            item.classList.add('dragging');
        });

        item.addEventListener('dragend', function() {
            item.classList.remove('dragging');
        });
    }
    
=======
        
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
    
>>>>>>> dbde2096846e5b4398413351225cc5f784d336f1
})();
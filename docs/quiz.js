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
        }
    }
    
    function initCategorizationQuizzes() {
        const categorizationQuizzes = document.querySelectorAll('.categorization-quiz');
        
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
                    }
                });
            });
        });
    }
    
    // 初期化
    document.addEventListener('DOMContentLoaded', function() {
        initAccordions();
        initTabs();
        initQuizzes();
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
    
})();
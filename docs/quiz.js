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
        // 基本クイズ初期化
        const quizContainers = document.querySelectorAll('.quiz-container');
        quizContainers.forEach(function(container) {
            const options = container.querySelectorAll('.quiz-option');
            const correctIndex = parseInt(container.dataset.correct);
            
            options.forEach(function(option, index) {
                option.addEventListener('click', function() {
                    options.forEach(opt => opt.style.pointerEvents = 'none');
                    
                    if (index === correctIndex) {
                        this.classList.add('correct');
                    } else {
                        this.classList.add('incorrect');
                        options[correctIndex].classList.add('correct');
                    }
                    
                    const explanation = container.querySelector('.quiz-explanation');
                    if (explanation) {
                        explanation.style.display = 'block';
                    }
                });
            });
        });
        
        // ドラッグ&ドロップクイズ初期化
        initCategorizationQuizzes();
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
                    zone.parentElement.classList.add('drag-over');
                });
                
                zone.addEventListener('dragleave', function(e) {
                    if (!zone.contains(e.relatedTarget)) {
                        zone.parentElement.classList.remove('drag-over');
                    }
                });
                
                zone.addEventListener('drop', function(e) {
                    e.preventDefault();
                    zone.parentElement.classList.remove('drag-over');
                    
                    const itemIndex = e.dataTransfer.getData('text/plain');
                    const itemHTML = e.dataTransfer.getData('text/html');
                    
                    // 既存のアイテムを削除（他の場所から移動された場合）
                    const existingItem = document.querySelector(`[data-item="${itemIndex}"]`);
                    if (existingItem && existingItem.parentElement.classList.contains('drop-area')) {
                        existingItem.remove();
                    }
                    
                    // 新しいアイテムを追加
                    zone.innerHTML = itemHTML;
                    
                    // イベントリスナーを再設定
                    const newItem = zone.querySelector('.draggable-item');
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

        const dropZones = quizContainer.querySelectorAll('.drop-zone');
        const result = quizContainer.querySelector('.categorization-result');
        const correctData = window.categorizationData ? window.categorizationData[quizId] : null;
        
        if (!correctData) {
            result.innerHTML = '<div class="error">正解データが見つかりません</div>';
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
        for (let i = 0; i < correctData.length; i++) {
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
        for (let i = 0; i < correctData.length; i++) {
            if (userAnswers[i] === correctData[i]) {
                correctCount++;
            }
        }

        // 結果表示
        const percentage = Math.round((correctCount / correctData.length) * 100);
        let resultClass = percentage >= 80 ? 'success' : percentage >= 60 ? 'warning' : 'error';
        
        result.innerHTML = `
            <div class="${resultClass}">
                <strong>結果: ${correctCount}/${correctData.length}問正解 (${percentage}%)</strong>
            </div>
        `;
    };
    
    window.checkMultipleChoice = function(quizId) {
        const quizContainer = document.querySelector(`[data-quiz-id="${quizId}"]`);
        if (!quizContainer) return;

        const checkboxes = quizContainer.querySelectorAll(`input[name="${quizId}"]`);
        const result = quizContainer.querySelector('.multiple-choice-result');
        const quizData = window.multipleChoiceData ? window.multipleChoiceData[quizId] : null;
        
        if (!quizData) {
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
        const correctIndices = quizData.correct;
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
                    ${quizData.explanation}
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
                    ${quizData.explanation}
                </div>
            `;
        }
        
        result.innerHTML = resultHTML;
    };
})();

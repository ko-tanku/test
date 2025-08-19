// クイズシステム - 自動生成

(function() {
    'use strict';
    
    function initQuizSystem() {
        const quizContainers = document.querySelectorAll('.quiz-container');
        
        quizContainers.forEach(function(container) {
            const options = container.querySelectorAll('.quiz-option');
            const correctIndex = parseInt(container.dataset.correct);
            
            options.forEach(function(option, index) {
                option.addEventListener('click', function() {
                    // 全てのオプションを無効化
                    options.forEach(opt => opt.style.pointerEvents = 'none');
                    
                    // 正解/不正解の表示
                    if (index === correctIndex) {
                        this.classList.add('correct');
                    } else {
                        this.classList.add('incorrect');
                        options[correctIndex].classList.add('correct');
                    }
                    
                    // 説明を表示
                    const explanation = container.querySelector('.quiz-explanation');
                    if (explanation) {
                        explanation.style.display = 'block';
                    }
                });
            });
        });
    }
    
    // 自動初期化
    document.addEventListener('DOMContentLoaded', initQuizSystem);
    
    // 公開API
    window.initQuizSystem = initQuizSystem;
    
})();

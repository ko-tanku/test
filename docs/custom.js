// docs/custom.js - 自動生成ファイル（完全修正版）

// MkDocs Material互換のカスタムスクリプト
document.addEventListener('DOMContentLoaded', function() {
    console.log('カスタムスクリプト初期化開始');
    
    // ツールチップの初期化（MkDocs Materialのレンダリング後に実行）
    setTimeout(function() {
        initCustomTooltips();
        initQuizComponents();
        initMermaidFallback();
    }, 100);
});

function initCustomTooltips() {
    const tooltips = document.querySelectorAll('.custom-tooltip');
    console.log('ツールチップ要素数:', tooltips.length);
    
    tooltips.forEach(function(tooltip) {
        // data-tooltip属性の内容を取得
        const tooltipText = tooltip.getAttribute('data-tooltip');
        if (!tooltipText) return;
        
        // ツールチップのスタイルを動的に適用
        tooltip.style.position = 'relative';
        tooltip.style.cursor = 'help';
        tooltip.style.borderBottom = '1px dotted #1976D2';
        
        // ホバーイベントの処理
        tooltip.addEventListener('mouseenter', function() {
            showTooltip(this, tooltipText);
        });
        
        tooltip.addEventListener('mouseleave', function() {
            hideTooltip(this);
        });
    });
}

function showTooltip(element, text) {
    // 既存のツールチップを削除
    hideTooltip(element);
    
    // 新しいツールチップを作成
    const tooltipEl = document.createElement('div');
    tooltipEl.className = 'custom-tooltip-popup';
    tooltipEl.textContent = text;
    tooltipEl.style.cssText = `
        position: absolute;
        bottom: 100%;
        left: 50%;
        transform: translateX(-50%);
        background: #263238;
        color: white;
        padding: 8px 12px;
        border-radius: 4px;
        font-size: 14px;
        white-space: nowrap;
        z-index: 9999;
        margin-bottom: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    `;
    
    element.appendChild(tooltipEl);
}

function hideTooltip(element) {
    const existing = element.querySelector('.custom-tooltip-popup');
    if (existing) {
        existing.remove();
    }
}

function initQuizComponents() {
    // クイズコンポーネントの初期化
    console.log('クイズコンポーネント初期化');
    
    // カテゴリ分けクイズ
    const categorizationQuizzes = document.querySelectorAll('.categorization-quiz');
    categorizationQuizzes.forEach(initDragAndDrop);
    
    // 複数選択クイズ
    const multipleChoiceQuizzes = document.querySelectorAll('.multiple-choice-quiz');
    multipleChoiceQuizzes.forEach(initMultipleChoice);
}

function initDragAndDrop(quiz) {
    const draggables = quiz.querySelectorAll('.draggable-item');
    const dropZones = quiz.querySelectorAll('.drop-area');
    
    draggables.forEach(item => {
        item.draggable = true;
        item.addEventListener('dragstart', handleDragStart);
        item.addEventListener('dragend', handleDragEnd);
    });
    
    dropZones.forEach(zone => {
        zone.addEventListener('dragover', handleDragOver);
        zone.addEventListener('drop', handleDrop);
        zone.addEventListener('dragleave', handleDragLeave);
    });
}

function handleDragStart(e) {
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/html', this.innerHTML);
    this.classList.add('dragging');
}

function handleDragEnd(e) {
    this.classList.remove('dragging');
}

function handleDragOver(e) {
    if (e.preventDefault) {
        e.preventDefault();
    }
    e.dataTransfer.dropEffect = 'move';
    this.classList.add('drag-over');
    return false;
}

function handleDragLeave(e) {
    this.classList.remove('drag-over');
}

function handleDrop(e) {
    if (e.stopPropagation) {
        e.stopPropagation();
    }
    this.classList.remove('drag-over');
    
    const draggedItem = document.querySelector('.dragging');
    if (draggedItem && this !== draggedItem) {
        this.appendChild(draggedItem);
    }
    return false;
}

function initMultipleChoice(quiz) {
    // 複数選択クイズの初期化
    console.log('複数選択クイズ初期化');
}

function initMermaidFallback() {
    // Mermaid初期化の強化版
    setTimeout(function() {
        if (typeof mermaid !== 'undefined') {
            console.log('Mermaid.jsが利用可能です。再初期化を実行します。');
            mermaid.initialize({ 
                startOnLoad: true,
                theme: 'default',
                securityLevel: 'loose'
            });
            mermaid.init();
        } else {
            console.log('Mermaid.jsが読み込まれていません。手動で初期化を試みます。');
            
            // Mermaid.jsを動的に読み込む
            const script = document.createElement('script');
            script.src = 'https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js';
            script.onload = function() {
                mermaid.initialize({ 
                    startOnLoad: true,
                    theme: 'default',
                    securityLevel: 'loose'
                });
                mermaid.init();
            };
            document.head.appendChild(script);
        }
    }, 500);
}

// レスポンシブ要素の初期化
function initResponsiveElements() {
    const iframes = document.querySelectorAll('iframe.auto-height-iframe');
    iframes.forEach(function(iframe) {
        iframe.onload = function() {
            try {
                const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
                const height = iframeDoc.body.scrollHeight;
                iframe.style.height = height + 'px';
            } catch (e) {
                console.warn('iframe高さ調整に失敗:', e);
            }
        };
    });
}

// グローバル関数として公開（quiz.jsから呼び出し用）
window.checkCategorization = function(quizId) {
    console.log('カテゴリ分けクイズチェック:', quizId);
    // クイズの答え合わせロジック
};

window.checkMultipleChoice = function(quizId) {
    console.log('複数選択クイズチェック:', quizId);
    // クイズの答え合わせロジック
};

// MkDocsUtils の提供
window.MkDocsUtils = {
    refreshTooltips: initCustomTooltips,
    refreshIframes: initResponsiveElements,
    refreshQuizzes: initQuizComponents
};

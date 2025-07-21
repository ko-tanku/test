// docs/custom.js - 自動生成ファイル

(function() {
    'use strict';
    
    // DOM読み込み完了時の初期化
    document.addEventListener('DOMContentLoaded', function() {
        console.log('カスタムスクリプト初期化完了');
        initializeComponents();
    });
    
    function initializeComponents() {
        // 各種コンポーネントの初期化
        initTooltips();
        initResponsiveElements();
    }
    
    function initTooltips() {
        const tooltips = document.querySelectorAll('.custom-tooltip');
        tooltips.forEach(function(tooltip) {
            tooltip.addEventListener('click', function(e) {
                e.preventDefault();
                this.classList.toggle('is-clicked');
            });
        });
    }
    
    function initResponsiveElements() {
        // レスポンシブ要素の初期化
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
    
    // グローバルユーティリティ関数
    window.MkDocsUtils = {
        refreshTooltips: function() {
            initTooltips();
        },
        
        refreshIframes: function() {
            initResponsiveElements();
        }
    };
})();


/* 追加コンテンツ */

// 学習材料追加機能

// テーマ切り替え機能
function switchTheme(theme) {
    const links = document.querySelectorAll('link[href*="custom"]');
    links.forEach(link => {
        if (link.href.includes('custom')) {
            const newHref = theme === 'default' ? 'custom.css' : `custom_${theme}.css`;
            link.href = link.href.replace(/custom[^.]*\.css/, newHref);
        }
    });
    
    // テーマ保存
    localStorage.setItem('preferred_theme', theme);
    console.log(`テーマを${theme}に切り替えました`);
}

// 学習進度追跡
function markChapterComplete(chapterNum) {
    const key = `chapter_${chapterNum}_completed`;
    localStorage.setItem(key, 'true');
    console.log(`第${chapterNum}章を完了としてマークしました`);
}

function getCompletedChapters() {
    const completed = [];
    for (let i = 1; i <= 6; i++) {
        if (localStorage.getItem(`chapter_${i}_completed`)) {
            completed.push(i);
        }
    }
    return completed;
}

// ページ読み込み時にテーマを復元
document.addEventListener('DOMContentLoaded', function() {
    const savedTheme = localStorage.getItem('preferred_theme');
    if (savedTheme && savedTheme !== 'default') {
        switchTheme(savedTheme);
    }
});

console.log('学習材料システム初期化完了');

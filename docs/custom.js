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

"""
CSS・JavaScript・その他アセットファイルを動的に生成する機能
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from .config import PATHS, MATERIAL_ICONS

logger = logging.getLogger(__name__)


class AssetGenerator:
    """CSS・JavaScript・その他アセットファイルの生成を管理"""
    
    def __init__(self, docs_dir: Path):
        """
        初期化
        
        Args:
            docs_dir: docsディレクトリのパス
        """
        self.docs_dir = docs_dir
        self.css_components = {}
        self.js_components = {}
        
    def generate_custom_css(self, additional_styles: Optional[Dict[str, str]] = None) -> Path:
        """
        custom.cssファイルを生成
        
        Args:
            additional_styles: 追加のCSSスタイル辞書 {"セレクタ": "スタイル"}
            
        Returns:
            生成されたCSSファイルのパス
        """
        css_content = self._build_base_css()
        
        # 追加スタイルの統合
        if additional_styles:
            css_content += "\n/* 追加カスタムスタイル */\n"
            for selector, styles in additional_styles.items():
                css_content += f"{selector} {{\n{styles}\n}}\n\n"
        
        # ファイル保存
        css_path = self.docs_dir / "custom.css"
        css_path.write_text(css_content, encoding='utf-8')
        
        logger.info(f"custom.css生成完了: {css_path}")
        return css_path
    
    def generate_custom_js(self, additional_scripts: Optional[List[str]] = None) -> Path:
        """
        custom.jsファイルを生成
        
        Args:
            additional_scripts: 追加のJavaScriptコードのリスト
            
        Returns:
            生成されたJSファイルのパス
        """
        js_content = self._build_base_js()
        
        # 追加スクリプトの統合
        if additional_scripts:
            js_content += "\n// 追加カスタムスクリプト\n"
            for script in additional_scripts:
                js_content += f"{script}\n\n"
        
        # ファイル保存
        js_path = self.docs_dir / "custom.js"
        js_path.write_text(js_content, encoding='utf-8')
        
        logger.info(f"custom.js生成完了: {js_path}")
        return js_path
    
    def _build_base_css(self) -> str:
        """ベースとなるCSSコンテンツを構築"""
        return """/* docs/custom.css - 自動生成ファイル */

/* ============================================
   ツールチップ関連スタイル
   ============================================ */
.custom-tooltip {
    position: relative;
    cursor: pointer;
    color: var(--md-typeset-a-color);
    text-decoration: underline;
    text-decoration-style: dotted;
}

.custom-tooltip:hover {
    color: var(--md-typeset-a-color--hover);
}

.custom-tooltip::before {
    content: attr(data-tooltip);
    background-color: #333;
    color: #fff;
    padding: 8px 12px;
    border-radius: 4px;
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    bottom: 125%;
    white-space: nowrap;
    z-index: 1000;
    visibility: hidden;
    opacity: 0;
    transition: opacity 0.2s ease-in-out, visibility 0.2s ease-in-out;
}

.custom-tooltip::after {
    content: '';
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    bottom: 120%;
    border-top: 5px solid #333;
    border-right: 5px solid transparent;
    border-left: 5px solid transparent;
    z-index: 1000;
    visibility: hidden;
    opacity: 0;
    transition: opacity 0.2s ease-in-out, visibility 0.2s ease-in-out;
}

.custom-tooltip.is-clicked::before,
.custom-tooltip.is-clicked::after {
    visibility: visible;
    opacity: 1;
}

/* ============================================
   iframeコンテナ関連スタイル
   ============================================ */
.auto-height-iframe {
    border: 1px solid #ddd;
    border-radius: 4px;
    width: 100%;
    transition: height 0.3s ease;
}

/* ============================================
   レスポンシブ対応
   ============================================ */
@media (max-width: 768px) {
    .custom-tooltip::before {
        white-space: normal;
        max-width: 250px;
        word-wrap: break-word;
    }
}

/* ============================================
   印刷用スタイル
   ============================================ */
@media print {
    .custom-tooltip::before,
    .custom-tooltip::after {
        display: none !important;
    }
    
    .auto-height-iframe {
        border: none;
        box-shadow: none;
    }
}

/* ============================================
   アクセシビリティ改善
   ============================================ */
.custom-tooltip:focus {
    outline: 2px solid var(--md-accent-fg-color);
    outline-offset: 2px;
}

/* ============================================
   カスタムアニメーション
   ============================================ */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.fade-in-up {
    animation: fadeInUp 0.3s ease-out;
}
"""
    
    def _build_base_js(self) -> str:
        """ベースとなるJavaScriptコンテンツを構築"""
        return """// docs/custom.js - 自動生成ファイル

document.addEventListener('DOMContentLoaded', function () {
    
    // ============================================
    // iframe自動高さ調整機能
    // ============================================
    const iframes = document.querySelectorAll('iframe.auto-height-iframe');
    
    iframes.forEach(iframe => {
        iframe.onload = function () {
            try {
                const innerDoc = iframe.contentWindow.document.body;
                if (innerDoc) {
                    const height = innerDoc.scrollHeight + 20;
                    iframe.style.height = height + 'px';
                }
            } catch (e) {
                console.warn('Cannot access iframe content due to same-origin policy:', e);
                iframe.style.height = '400px';
            }
        };
        
        if (iframe.contentWindow && iframe.contentWindow.document.readyState === 'complete') {
            iframe.onload();
        }
    });
    
    // ============================================
    // ツールチップ機能
    // ============================================
    const tooltips = document.querySelectorAll('.custom-tooltip');
    
    tooltips.forEach(tooltip => {
        tooltip.addEventListener('click', function (event) {
            event.stopPropagation();
            
            if (this.classList.contains('is-clicked')) {
                this.classList.remove('is-clicked');
            } else {
                tooltips.forEach(otherTooltip => {
                    if (otherTooltip !== this) {
                        otherTooltip.classList.remove('is-clicked');
                    }
                });
                this.classList.add('is-clicked');
            }
        });
        
        // キーボードアクセシビリティ対応
        tooltip.addEventListener('keydown', function (event) {
            if (event.key === 'Enter' || event.key === ' ') {
                event.preventDefault();
                this.click();
            }
        });
        
        // tabindex設定でキーボードフォーカス可能にする
        tooltip.setAttribute('tabindex', '0');
    });
    
    // ツールチップ以外をクリックで閉じる
    document.addEventListener('click', function (event) {
        tooltips.forEach(tooltip => {
            if (tooltip.classList.contains('is-clicked') && !tooltip.contains(event.target)) {
                tooltip.classList.remove('is-clicked');
            }
        });
    });
    
    // ============================================
    // ページ読み込み時のアニメーション
    // ============================================
    const animateElements = document.querySelectorAll('.admonition, .tabbed-set');
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    animateElements.forEach(element => {
        observer.observe(element);
    });
    
    // ============================================
    // スムーススクロール
    // ============================================
    const smoothScrollLinks = document.querySelectorAll('a[href^="#"]');
    
    smoothScrollLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                e.preventDefault();
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
});

// ============================================
// ユーティリティ関数
// ============================================
window.MkDocsUtils = {
    /**
     * 要素にフェードインアニメーションを適用
     */
    fadeIn: function(element) {
        element.classList.add('fade-in-up');
    },
    
    /**
     * すべてのツールチップを閉じる
     */
    closeAllTooltips: function() {
        const tooltips = document.querySelectorAll('.custom-tooltip.is-clicked');
        tooltips.forEach(tooltip => {
            tooltip.classList.remove('is-clicked');
        });
    },
    
    /**
     * iframe高さを手動で再調整
     */
    refreshIframeHeights: function() {
        const iframes = document.querySelectorAll('iframe.auto-height-iframe');
        iframes.forEach(iframe => {
            if (iframe.onload) {
                iframe.onload();
            }
        });
    }
};
"""
    
    def add_css_component(self, name: str, css_content: str):
        """CSSコンポーネントを追加"""
        self.css_components[name] = css_content
        
    def add_js_component(self, name: str, js_content: str):
        """JavaScriptコンポーネントを追加"""
        self.js_components[name] = js_content
        
    def generate_theme_variations(self) -> Dict[str, Path]:
        """
        複数のテーマバリエーションのCSSを生成
        
        Returns:
            テーマ名とファイルパスの辞書
        """
        themes = {
            "default": {},
            "dark": {
                ".custom-tooltip::before": """
                    background-color: #1a1a1a;
                    color: #ffffff;
                    border: 1px solid #404040;
                """,
                ".custom-tooltip::after": """
                    border-top-color: #1a1a1a;
                """
            },
            "high_contrast": {
                ".custom-tooltip": """
                    color: #000000;
                    font-weight: bold;
                """,
                ".custom-tooltip::before": """
                    background-color: #000000;
                    color: #ffffff;
                    border: 2px solid #ffffff;
                    font-size: 1.1em;
                """
            }
        }
        
        generated_files = {}
        for theme_name, additional_styles in themes.items():
            css_filename = f"custom_{theme_name}.css" if theme_name != "default" else "custom.css"
            css_path = self.generate_custom_css(additional_styles)
            if theme_name != "default":
                # デフォルト以外はリネーム
                new_path = self.docs_dir / css_filename
                css_path.rename(new_path)
                generated_files[theme_name] = new_path
            else:
                generated_files[theme_name] = css_path
                
        return generated_files
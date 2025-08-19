"""
AssetGeneratorとMkDocsManagerの機能テスト
"""

import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

# プロジェクトルートをsys.pathに追加
project_root = Path(__file__).resolve().parents[3]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.core.asset_generator import AssetGenerator, AssetType
from src.core.mkdocs_manager import MkDocsManager, NavItem

logger = logging.getLogger(__name__)


class TestMaterialAssetTester:
    """テスト資料用のアセット機能統合テスト"""
    
    def __init__(self, docs_dir: Path, project_root: Path):
        """
        初期化
        
        Args:
            docs_dir: docsディレクトリのパス
            project_root: プロジェクトルートのパス
        """
        self.docs_dir = docs_dir
        self.project_root = project_root
        self.asset_generator = AssetGenerator(docs_dir)
        self.mkdocs_manager = MkDocsManager(project_root)
        self.generated_assets = {}
        
    def test_css_generation(self) -> Dict[str, Path]:
        """CSSファイル生成機能のテスト"""
        logger.info("CSS生成機能のテスト開始")
        
        # カスタムテーマテンプレートの作成
        self.asset_generator.create_custom_template(
            AssetType.CSS,
            "learning_material_theme",
            self._get_learning_css_template(),
            variables={
                'primary_color': '#1976D2',
                'secondary_color': '#FFC107',
                'background_color': '#ffffff',
                'text_color': '#333333',
                'code_background': '#f5f5f5',
                'tooltip_bg': '#263238',
                'tooltip_text': '#ffffff',
                'quiz_correct': '#4CAF50',
                'quiz_incorrect': '#F44336',
                'admonition_info': '#2196F3',
                'admonition_warning': '#FF9800',
                'admonition_danger': '#F44336'
            }
        )
        
        # 基本CSSファイルの生成
        css_files = {}
        
        # デフォルトテーマ
        css_files['default'] = self.asset_generator.generate_asset(
            AssetType.CSS,
            'learning_material_theme',
            'custom.css'
        )
        
        # ダークテーマ
        css_files['dark'] = self.asset_generator.generate_asset(
            AssetType.CSS,
            'learning_material_theme',
            'custom_dark.css',
            variables={
                'primary_color': '#1565C0',
                'background_color': '#1a1a1a',
                'text_color': '#e0e0e0',
                'code_background': '#2d2d2d',
                'tooltip_bg': '#424242',
                'tooltip_text': '#ffffff'
            }
        )
        
        # 高コントラストテーマ
        css_files['high_contrast'] = self.asset_generator.generate_asset(
            AssetType.CSS,
            'learning_material_theme',
            'custom_high_contrast.css',
            variables={
                'primary_color': '#000000',
                'background_color': '#ffffff',
                'text_color': '#000000',
                'code_background': '#f0f0f0',
                'tooltip_bg': '#000000',
                'tooltip_text': '#ffffff'
            }
        )
        
        # 学習用アニメーションCSS
        css_files['animations'] = self.asset_generator.generate_asset(
            AssetType.CSS,
            'animations',
            'animations.css'
        )
        
        self.generated_assets.update(css_files)
        logger.info(f"CSS生成完了: {len(css_files)}個のファイル")
        return css_files
    
    def test_js_generation(self) -> Dict[str, Path]:
        """JavaScript生成機能のテスト"""
        logger.info("JavaScript生成機能のテスト開始")
        
        # 学習用JSテンプレートの作成
        self.asset_generator.create_custom_template(
            AssetType.JAVASCRIPT,
            "learning_interactive",
            self._get_learning_js_template()
        )
        
        # クイズシステムJSテンプレート
        self.asset_generator.create_custom_template(
            AssetType.JAVASCRIPT,
            "quiz_system",
            self._get_quiz_js_template()
        )
        
        # アニメーション制御JSテンプレート  
        self.asset_generator.create_custom_template(
            AssetType.JAVASCRIPT,
            "animations_control",
            self._get_animation_js_template()
        )
        
        js_files = {}
        
        # 基本インタラクティブ機能
        js_files['interactive'] = self.asset_generator.generate_asset(
            AssetType.JAVASCRIPT,
            'learning_interactive',
            'interactive.js'
        )
        
        # クイズシステム
        js_files['quiz'] = self.asset_generator.generate_asset(
            AssetType.JAVASCRIPT,
            'quiz_system',
            'quiz.js'
        )
        
        # アニメーション制御
        js_files['animations'] = self.asset_generator.generate_asset(
            AssetType.JAVASCRIPT,
            'animations_control',
            'animations.js'
        )
        
        # 統合カスタムJS（全機能含む）
        js_files['custom'] = self.asset_generator.generate_asset(
            AssetType.JAVASCRIPT,
            'base',
            'custom.js',
            additional_content="""
// 学習材料特化の追加機能
console.log('学習材料インタラクティブ機能が読み込まれました');

// ページ読み込み完了時の初期化
document.addEventListener('DOMContentLoaded', function() {
    initLearningFeatures();
});

function initLearningFeatures() {
    // 全ての学習機能を初期化
    if (typeof initQuizSystem === 'function') initQuizSystem();
    if (typeof initAnimationControls === 'function') initAnimationControls();
    if (typeof initTooltipEnhancements === 'function') initTooltipEnhancements();
}
            """
        )
        
        self.generated_assets.update(js_files)
        logger.info(f"JavaScript生成完了: {len(js_files)}個のファイル")
        return js_files
    
    def test_mkdocs_management(self) -> Path:
        """MkDocs設定管理機能のテスト"""
        logger.info("MkDocs設定管理機能のテスト開始")
        
        # 構造化ナビゲーションの作成
        nav_structure = [
            NavItem(
                title="IT・組み込み技術入門",
                children=[
                    NavItem(title="ホーム", path="test_material/index.md"),
                    NavItem(title="第1章: 基本要素", path="test_material/documents/chapter01.md"),
                    NavItem(title="第2章: ツールチップ", path="test_material/documents/chapter02.md"),
                    NavItem(title="第3章: 図表", path="test_material/documents/chapter03.md"),
                    NavItem(title="第4章: 演習", path="test_material/documents/chapter04.md"),
                    NavItem(title="第5章: 統合テスト", path="test_material/documents/chapter05.md"),
                    NavItem(title="第6章: アセット機能テスト", path="test_material/documents/chapter06.md"),
                    NavItem(title="用語集", path="test_material/glossary.md"),
                    NavItem(title="FAQ", path="test_material/faq.md"),
                    NavItem(title="TIPS", path="test_material/tips.md")
                ]
            )
        ]
        
        # カスタム設定
        custom_config = {
            "theme": {
                "name": "material",
                "palette": [
                    {
                        "media": "(prefers-color-scheme: light)",
                        "scheme": "default",
                        "primary": "blue",
                        "accent": "cyan",
                        "toggle": {
                            "icon": "material/brightness-7",
                            "name": "ダークモードに切り替え"
                        }
                    },
                    {
                        "media": "(prefers-color-scheme: dark)",
                        "scheme": "slate",
                        "primary": "blue",
                        "accent": "cyan",
                        "toggle": {
                            "icon": "material/brightness-4",
                            "name": "ライトモードに切り替え"
                        }
                    }
                ],
                "features": [
                    "navigation.tabs",
                    "navigation.sections",
                    "navigation.expand",
                    "navigation.top",
                    "search.suggest",
                    "search.highlight",
                    "toc.integrate",
                    "header.autohide",
                    "content.tooltips",
                    "content.code.copy",
                    "content.code.annotate"
                ]
            },
            "plugins": [
                "search",
                {
                    "minify": {
                        "minify_html": True,
                        "minify_js": True,
                        "minify_css": True
                    }
                }
            ],
            "markdown_extensions": [
                "admonition",
                "pymdownx.details",
                "pymdownx.superfences",
                "pymdownx.highlight",
                "pymdownx.tabbed",
                "pymdownx.tasklist",
                "attr_list",
                "md_in_html",
                "footnotes",
                "tables",
                "fenced_code",
                "abbr",
                "pymdownx.snippets",
                "pymdownx.emoji",
                "pymdownx.keys",
                "pymdownx.mark"
            ]
        }
        
        # MkDocs設定ファイル生成
        mkdocs_path = self.mkdocs_manager.generate_mkdocs_yml(
            nav_structure=nav_structure,
            custom_config=custom_config,
            backup=True
        )
        
        # 生成されたアセットファイルを設定に追加
        css_files = [
            "custom.css",
            "custom_dark.css", 
            "custom_high_contrast.css",
            "animations.css"
        ]
        
        js_files = [
            "custom.js",
            "interactive.js",
            "quiz.js",
            "animations.js"
        ]
        
        self.mkdocs_manager.add_asset_files(css_files, js_files)
        
        logger.info(f"MkDocs設定管理完了: {mkdocs_path}")
        return mkdocs_path
    
    def test_asset_updates(self) -> Dict[str, Path]:
        """アセット更新機能のテスト"""
        logger.info("アセット更新機能のテスト開始")
        
        updated_files = {}
        
        # CSSファイルの更新テスト（追記モード）
        additional_css = """
/* 追加スタイル - 学習進度表示 */
.progress-indicator {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background: linear-gradient(90deg, #4CAF50 var(--progress, 0%), #e0e0e0 var(--progress, 0%));
    z-index: 9999;
}

.chapter-completion {
    display: inline-block;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: #e0e0e0;
    margin-right: 8px;
    transition: background 0.3s;
}

.chapter-completion.completed {
    background: #4CAF50;
    color: white;
}
"""
        
        updated_files['css_append'] = self.asset_generator.update_asset(
            'custom.css',
            additional_content=additional_css,
            append_mode=True
        )
        
        # JSファイルの更新テスト（変数置換）
        updated_files['js_variables'] = self.asset_generator.update_asset(
            'interactive.js',
            variables={'debug_mode': 'true'},
            additional_content="""
// デバッグ機能追加
if (window.DEBUG_MODE) {
    console.log('デバッグモードが有効です');
    
    // 学習進度追跡
    window.trackLearningProgress = function(chapterId) {
        localStorage.setItem('chapter_' + chapterId + '_completed', 'true');
        updateProgressIndicator();
    };
    
    window.updateProgressIndicator = function() {
        const totalChapters = 6;
        let completedChapters = 0;
        
        for (let i = 1; i <= totalChapters; i++) {
            if (localStorage.getItem('chapter_' + i + '_completed')) {
                completedChapters++;
            }
        }
        
        const progress = (completedChapters / totalChapters) * 100;
        document.documentElement.style.setProperty('--progress', progress + '%');
    };
}
"""
        )
        
        logger.info(f"アセット更新完了: {len(updated_files)}個のファイル")
        return updated_files
    
    def test_config_validation(self) -> Dict[str, Any]:
        """設定検証機能のテスト"""
        logger.info("設定検証機能のテスト開始")
        
        # 設定検証の実行
        validation_results = self.mkdocs_manager.validate_config()
        
        # 設定情報のエクスポート
        config_info = self.mkdocs_manager.export_config_info()
        
        # アセットマニフェストの出力
        manifest_path = self.asset_generator.export_asset_manifest()
        
        logger.info("設定検証完了")
        
        return {
            'validation_results': validation_results,
            'config_info': config_info,
            'manifest_path': str(manifest_path)
        }
    
    def run_all_tests(self) -> Dict[str, Any]:
        """全てのテストを実行"""
        logger.info("=== アセット機能統合テスト開始 ===")
        
        results = {}
        
        try:
            # CSS生成テスト
            results['css_files'] = self.test_css_generation()
            
            # JavaScript生成テスト  
            results['js_files'] = self.test_js_generation()
            
            # MkDocs管理テスト
            results['mkdocs_config'] = self.test_mkdocs_management()
            
            # アセット更新テスト
            results['updated_assets'] = self.test_asset_updates()
            
            # 検証テスト
            results['validation'] = self.test_config_validation()
            
            logger.info("=== 全てのテストが完了しました ===")
            
        except Exception as e:
            logger.error(f"テスト実行中にエラーが発生: {e}")
            results['error'] = str(e)
            raise
            
        return results
    
    def _get_learning_css_template(self) -> str:
        """学習材料用CSSテンプレート"""
        return """/* 学習材料専用CSS - 自動生成 */

:root {
    --primary-color: {primary_color};
    --secondary-color: {secondary_color};
    --background-color: {background_color};
    --text-color: {text_color};
    --code-background: {code_background};
    --tooltip-bg: {tooltip_bg};
    --tooltip-text: {tooltip_text};
    --quiz-correct: {quiz_correct};
    --quiz-incorrect: {quiz_incorrect};
    --admonition-info: {admonition_info};
    --admonition-warning: {admonition_warning};
    --admonition-danger: {admonition_danger};
}

/* 基本レイアウト */
body {
    font-family: 'Roboto', 'Noto Sans JP', sans-serif;
    background-color: var(--background-color);
    color: var(--text-color);
}

/* ツールチップ拡張 */
.custom-tooltip {
    position: relative;
    cursor: help;
    border-bottom: 1px dotted var(--primary-color);
    transition: all 0.3s ease;
}

.custom-tooltip:hover {
    border-bottom-color: var(--secondary-color);
}

.custom-tooltip::before {
    content: attr(data-tooltip);
    position: absolute;
    bottom: 125%;
    left: 50%;
    transform: translateX(-50%);
    background: var(--tooltip-bg);
    color: var(--tooltip-text);
    padding: 12px 16px;
    border-radius: 6px;
    font-size: 14px;
    line-height: 1.4;
    white-space: nowrap;
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s ease;
    z-index: 1000;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    max-width: 300px;
    white-space: normal;
}

.custom-tooltip:hover::before {
    opacity: 1;
    visibility: visible;
    transform: translateX(-50%) translateY(-5px);
}

/* クイズスタイル */
.quiz-container {
    border: 2px solid var(--primary-color);
    border-radius: 12px;
    padding: 24px;
    margin: 24px 0;
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    position: relative;
    overflow: hidden;
}

.quiz-container::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
}

.quiz-question {
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 16px;
    color: var(--text-color);
}

.quiz-options {
    display: grid;
    gap: 12px;
    margin: 16px 0;
}

.quiz-option {
    padding: 12px 16px;
    border: 2px solid #ddd;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
    background: white;
}

.quiz-option:hover {
    border-color: var(--primary-color);
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.quiz-option.correct {
    background: var(--quiz-correct);
    color: white;
    border-color: var(--quiz-correct);
}

.quiz-option.incorrect {
    background: var(--quiz-incorrect);
    color: white;
    border-color: var(--quiz-incorrect);
}

/* コードブロック拡張 */
.highlight {
    background: var(--code-background);
    border-radius: 8px;
    border-left: 4px solid var(--primary-color);
    margin: 16px 0;
    overflow: hidden;
}

/* アニメーション要素 */
.learning-animation {
    border: 2px solid var(--secondary-color);
    border-radius: 12px;
    padding: 20px;
    margin: 20px 0;
    background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
    position: relative;
}

.fade-in {
    animation: fadeIn 0.8s ease-in;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

/* 進度表示 */
.chapter-progress {
    display: flex;
    align-items: center;
    margin: 20px 0;
    padding: 16px;
    background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
    border-radius: 8px;
}

.progress-circle {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: var(--primary-color);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    margin-right: 16px;
}
"""
    
    def _get_learning_js_template(self) -> str:
        """学習用JavaScriptテンプレート"""
        return """// 学習材料インタラクティブ機能

(function() {
    'use strict';
    
    // グローバル変数
    window.LearningMaterial = {
        initialized: false,
        currentChapter: 1,
        completedChapters: new Set(),
        settings: {
            autoSave: true,
            showHints: true,
            animationSpeed: 'normal'
        }
    };
    
    // 初期化
    document.addEventListener('DOMContentLoaded', function() {
        initLearningFeatures();
        loadUserProgress();
        setupEventListeners();
        
        window.LearningMaterial.initialized = true;
        console.log('学習材料システム初期化完了');
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
        
        // 詳細モーダルの表示（実装は省略）
        console.log('詳細表示:', term, tooltip);
    }
    
    function initProgressTracking() {
        // スクロール進度の追跡
        let ticking = false;
        
        function updateScrollProgress() {
            const scrolled = window.pageYOffset;
            const maxHeight = document.body.scrollHeight - window.innerHeight;
            const progress = (scrolled / maxHeight) * 100;
            
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
        const chapterMatch = currentPath.match(/chapter(\\d+)/);
        
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
        notification.innerHTML = `
            <div class="notification-content">
                <span class="notification-icon">✅</span>
                <span class="notification-text">第${chapterNum}章を完了しました！</span>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // アニメーション後に削除
        setTimeout(() => {
            notification.remove();
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
            }
        });
    }
    
    // 公開API
    window.LearningMaterial.api = {
        markChapterComplete: markChapterComplete,
        saveProgress: saveUserProgress,
        loadProgress: loadUserProgress,
        resetProgress: function() {
            localStorage.removeItem('learning_progress');
            window.LearningMaterial.completedChapters.clear();
        }
    };
    
})();
"""
    
    def _get_quiz_js_template(self) -> str:
        """クイズシステムJavaScriptテンプレート"""
        return """// クイズシステム

(function() {
    'use strict';
    
    function initQuizSystem() {
        const quizContainers = document.querySelectorAll('.quiz-container');
        
        quizContainers.forEach(function(container) {
            setupQuizContainer(container);
        });
    }
    
    function setupQuizContainer(container) {
        const options = container.querySelectorAll('.quiz-option');
        const question = container.querySelector('.quiz-question');
        const hintButton = container.querySelector('.quiz-hint-button');
        const explanationDiv = container.querySelector('.quiz-explanation');
        
        let answered = false;
        let correctAnswer = parseInt(container.dataset.correct);
        
        options.forEach(function(option, index) {
            option.addEventListener('click', function() {
                if (answered) return;
                
                handleQuizAnswer(container, index, correctAnswer, options);
                answered = true;
            });
        });
        
        if (hintButton) {
            hintButton.addEventListener('click', function() {
                toggleHint(container);
            });
        }
    }
    
    function handleQuizAnswer(container, selectedIndex, correctIndex, options) {
        options.forEach(function(option, index) {
            if (index === correctIndex) {
                option.classList.add('correct');
            } else if (index === selectedIndex && index !== correctIndex) {
                option.classList.add('incorrect');
            } else {
                option.classList.add('disabled');
            }
        });
        
        // 説明を表示
        const explanation = container.querySelector('.quiz-explanation');
        if (explanation) {
            explanation.style.display = 'block';
            explanation.classList.add('fade-in');
        }
        
        // 結果をトラッキング
        trackQuizResult(container, selectedIndex === correctIndex);
    }
    
    function toggleHint(container) {
        const hint = container.querySelector('.quiz-hint');
        if (hint) {
            hint.style.display = hint.style.display === 'none' ? 'block' : 'none';
        }
    }
    
    function trackQuizResult(container, isCorrect) {
        const quizId = container.dataset.quizId || 'unknown';
        
        // 学習進度に記録
        if (window.LearningMaterial && window.LearningMaterial.api) {
            const progress = JSON.parse(localStorage.getItem('learning_progress') || '{}');
            if (!progress.quizResults) progress.quizResults = {};
            
            progress.quizResults[quizId] = {
                correct: isCorrect,
                timestamp: new Date().toISOString()
            };
            
            localStorage.setItem('learning_progress', JSON.stringify(progress));
        }
    }
    
    // 公開API
    window.initQuizSystem = initQuizSystem;
    
    // DOMContentLoaded時に自動初期化
    document.addEventListener('DOMContentLoaded', initQuizSystem);
    
    })();
    """
    
    def _get_animation_js_template(self) -> str:
        """アニメーション制御JavaScriptテンプレート"""
        return """// アニメーション制御システム

    (function() {
    'use strict';
    
    function initAnimationControls() {
        setupIntersectionObserver();
        setupAnimationTriggers();
        setupAnimationControls();
    }
    
    function setupIntersectionObserver() {
        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    triggerAnimation(entry.target);
                }
            });
        }, {
            threshold: 0.3,
            rootMargin: '0px 0px -100px 0px'
        });
        
        // アニメーション対象要素を監視
        const animatedElements = document.querySelectorAll('.learning-animation, .fade-in-element');
        animatedElements.forEach(function(element) {
            observer.observe(element);
        });
    }
    
    function triggerAnimation(element) {
        element.classList.add('fade-in');
        
        // 連鎖アニメーション
        const children = element.querySelectorAll('.animate-child');
        children.forEach(function(child, index) {
            setTimeout(function() {
                child.classList.add('fade-in');
            }, index * 200);
        });
    }
    
    function setupAnimationTriggers() {
        // ボタンクリックでアニメーション
        const triggerButtons = document.querySelectorAll('.animation-trigger');
        
        triggerButtons.forEach(function(button) {
            button.addEventListener('click', function() {
                const targetId = this.dataset.target;
                const target = document.getElementById(targetId);
                
                if (target) {
                    playAnimation(target, this.dataset.animation || 'fade-in');
                }
            });
        });
    }
    
    function setupAnimationControls() {
        // アニメーション設定パネル
        const controlsHTML = `
            <div class="animation-controls" style="
                position: fixed;
                bottom: 20px;
                right: 20px;
                background: white;
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 16px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                z-index: 1000;
                display: none;
            ">
                <h4>アニメーション設定</h4>
                <label>
                    <input type="checkbox" class="learning-setting" data-setting="animationsEnabled" checked>
                    アニメーションを有効にする
                </label>
                <br>
                <label>
                    速度:
                    <select class="learning-setting" data-setting="animationSpeed">
                        <option value="slow">遅い</option>
                        <option value="normal" selected>普通</option>
                        <option value="fast">速い</option>
                    </select>
                </label>
                <br>
                <button onclick="this.parentElement.style.display='none'">閉じる</button>
            </div>
        `;
        
        // 設定ボタン
        const settingsButton = document.createElement('button');
        settingsButton.innerHTML = '⚙️';
        settingsButton.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            border: none;
            background: #2196F3;
            color: white;
            font-size: 20px;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            z-index: 999;
        `;
        
        settingsButton.addEventListener('click', function() {
            const controls = document.querySelector('.animation-controls');
            if (controls) {
                controls.style.display = controls.style.display === 'none' ? 'block' : 'none';
            }
        });
        
        document.body.insertAdjacentHTML('beforeend', controlsHTML);
        document.body.appendChild(settingsButton);
    }
    
    function playAnimation(element, animationType) {
        element.classList.remove('fade-in', 'slide-in', 'bounce-in');
        
        // 強制的にリフロー
        element.offsetHeight;
        
        element.classList.add(animationType);
    }
    
    // 公開API
    window.initAnimationControls = initAnimationControls;
    
    // DOMContentLoaded時に自動初期化
    document.addEventListener('DOMContentLoaded', initAnimationControls);
    
    })();
    """
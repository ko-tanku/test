"""
テスト資料生成のメインエントリポイント（アセット機能統合版）
このファイルを実行すると、テスト資料が自動生成される
"""

import sys
import logging
from pathlib import Path
import yaml
from typing import Dict, Any

# プロジェクトルートをsys.pathに追加
project_root = Path(__file__).resolve().parents[3]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.core.config import PATHS, MKDOCS_SITE_CONFIG
from src.core.asset_generator import AssetGenerator, AssetType
from src.core.mkdocs_manager import MkDocsManager, NavItem
from src.materials.test_material.test_material_config import (
    MATERIAL_CONFIG, MKDOCS_MATERIAL_OVERRIDE
)
from src.materials.test_material.test_material_contents import TestMaterialContentManager

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def update_mkdocs_config(material_config: Dict[str, Any]) -> None:
    """
    アセット機能を使ってmkdocs.ymlとアセットファイルを更新
    
    Args:
        material_config: 資料の設定情報
    """
    docs_dir = PATHS["DOCS_DIR"]
    
    # アセット機能の初期化
    asset_generator = AssetGenerator(docs_dir)
    mkdocs_manager = MkDocsManager(project_root)
    
    logger.info("=== アセットファイル生成開始 ===")
    
    try:
        # 1. CSSファイル生成
        logger.info("CSSファイルを生成中...")
        
        # 学習材料用CSSテンプレート作成
        asset_generator.create_custom_template(
            AssetType.CSS,
            "learning_theme",
            _get_learning_css_template(),
            variables={
                'primary_color': '#1976D2',
                'secondary_color': '#FFC107',
                'background_color': '#ffffff',
                'text_color': '#333333',
                'tooltip_bg': '#263238',
                'tooltip_text': '#ffffff',
                'quiz_correct': '#4CAF50',
                'quiz_incorrect': '#F44336'
            }
        )
        
        # 複数テーマのCSS生成
        css_files = []
        themes = {
            'default': {},
            'dark': {
                'background_color': '#1a1a1a',
                'text_color': '#e0e0e0',
                'tooltip_bg': '#424242'
            },
            'high_contrast': {
                'primary_color': '#000000',
                'background_color': '#ffffff',
                'text_color': '#000000'
            }
        }
        
        for theme_name, theme_vars in themes.items():
            filename = f"custom_{theme_name}.css" if theme_name != 'default' else "custom.css"
            css_path = asset_generator.generate_asset(
                AssetType.CSS,
                'learning_theme',
                filename,
                variables=theme_vars
            )
            css_files.append(filename)
        
        # 2. JavaScriptファイル生成
        logger.info("JavaScriptファイルを生成中...")
        
        # クイズシステムJSテンプレート作成
        asset_generator.create_custom_template(
            AssetType.JAVASCRIPT,
            "quiz_system",
            _get_quiz_js_template()
        )
        
        # JSファイル生成
        js_files = []
        
        # 基本カスタムJS
        js_path = asset_generator.generate_asset(
            AssetType.JAVASCRIPT,
            'base',
            'custom.js',
            additional_content=_get_additional_js_content()
        )
        js_files.append('custom.js')
        
        # クイズシステムJS
        quiz_js_path = asset_generator.generate_asset(
            AssetType.JAVASCRIPT,
            'quiz_system',
            'quiz.js'
        )
        js_files.append('quiz.js')
        
        # 3. MkDocs設定生成・更新
        logger.info("MkDocs設定を更新中...")
        
        # 構造化ナビゲーション作成（第6章追加）
        nav_structure = [
            NavItem(
                title=material_config["title"],
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
        
        # カスタム設定（Material Design改良版）
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
            "plugins": ["search"],
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
                "pymdownx.keys"
            ]
        }
        
        # MkDocs設定ファイル生成
        mkdocs_path = mkdocs_manager.generate_mkdocs_yml(
            nav_structure=nav_structure,
            custom_config=custom_config,
            backup=True
        )
        
        # 生成されたアセットファイルを設定に追加
        mkdocs_manager.add_asset_files(css_files, js_files)
        
        # 4. 設定検証
        logger.info("設定を検証中...")
        validation_results = mkdocs_manager.validate_config()
        
        if validation_results['errors']:
            logger.warning("設定エラーが見つかりました:")
            for error in validation_results['errors']:
                logger.warning(f"  ❌ {error}")
        
        if validation_results['warnings']:
            logger.info("設定警告:")
            for warning in validation_results['warnings']:
                logger.info(f"  ⚠️ {warning}")
        
        # 5. アセットマニフェスト出力
        manifest_path = asset_generator.export_asset_manifest()
        
        logger.info("=== アセットファイル生成完了 ===")
        logger.info(f"CSS files: {len(css_files)}")
        logger.info(f"JS files: {len(js_files)}")
        logger.info(f"MkDocs config: {mkdocs_path}")
        logger.info(f"Asset manifest: {manifest_path}")
        
    except Exception as e:
        logger.error(f"アセット生成中にエラーが発生しました: {e}")
        raise


def create_test_material() -> None:
    """
    テスト資料を生成するメイン関数
    """
    logger.info("テスト資料の生成を開始します...")
    
    try:
        # 出力ディレクトリの設定
        output_dir = PATHS["TEST_MATERIAL_DIR"]
        logger.info(f"出力ディレクトリ: {output_dir}")
        
        # コンテンツマネージャーの初期化
        content_manager = TestMaterialContentManager(
            material_name="test_material",
            output_base_dir=output_dir
        )
        
        # コンテンツの生成
        logger.info("コンテンツを生成中...")
        generated_files = content_manager.generate_content()
        
        logger.info(f"生成されたファイル数: {len(generated_files)}")
        for file_path in generated_files:
            logger.info(f"  - {file_path}")
        
        # アセット機能を使ったmkdocs.yml更新
        logger.info("アセット機能を使ってmkdocs.ymlを更新中...")
        update_mkdocs_config(MATERIAL_CONFIG)
        
        logger.info("テスト資料の生成が完了しました！")
        logger.info("\n実行方法:")
        logger.info("  1. プロジェクトルートで: mkdocs serve")
        logger.info("  2. ブラウザで: http://127.0.0.1:8000")
        logger.info("  3. 新機能（第6章）でアセット機能をテスト")
        
    except Exception as e:
        logger.error(f"テスト資料生成中にエラーが発生しました: {e}")
        logger.exception("詳細なエラー情報:")
        raise


def _get_learning_css_template() -> str:
    """学習材料用CSSテンプレート"""
    return """/* 学習材料専用CSS - 自動生成 */

:root {
    --primary-color: {primary_color};
    --secondary-color: {secondary_color};
    --background-color: {background_color};
    --text-color: {text_color};
    --tooltip-bg: {tooltip_bg};
    --tooltip-text: {tooltip_text};
    --quiz-correct: {quiz_correct};
    --quiz-incorrect: {quiz_incorrect};
}

/* ツールチップ拡張 */
.custom-tooltip {
    position: relative;
    cursor: help;
    border-bottom: 1px dotted var(--primary-color);
    transition: all 0.3s ease;
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
    white-space: nowrap;
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s ease;
    z-index: 1000;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}

.custom-tooltip:hover::before {
    opacity: 1;
    visibility: visible;
}

/* クイズスタイル */
.quiz-container {
    border: 2px solid var(--primary-color);
    border-radius: 12px;
    padding: 24px;
    margin: 24px 0;
    background: var(--background-color);
}

.quiz-option {
    padding: 12px 16px;
    border: 2px solid #ddd;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
    margin: 8px 0;
}

.quiz-option:hover {
    border-color: var(--primary-color);
}

.quiz-option.correct {
    background: var(--quiz-correct);
    color: white;
}

.quiz-option.incorrect {
    background: var(--quiz-incorrect);
    color: white;
}

/* テーマ切り替えボタン */
.theme-switcher {
    margin: 20px 0;
    text-align: center;
}

.theme-switcher button {
    margin: 5px;
    padding: 8px 16px;
    border: 1px solid var(--primary-color);
    background: var(--background-color);
    color: var(--text-color);
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.theme-switcher button:hover {
    background: var(--primary-color);
    color: white;
}
"""


def _get_quiz_js_template() -> str:
    """クイズシステムJavaScriptテンプレート"""
    return """// クイズシステム - 自動生成

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

// カテゴリ分けクイズ機能
function checkCategorization(quizId) {
    const quizContainer = document.querySelector(`[data-quiz-id="${quizId}"]`);
    if (!quizContainer) return;

    const dropZones = quizContainer.querySelectorAll('.drop-zone');
    const result = quizContainer.querySelector('.categorization-result');
    const correctData = window.categorizationData[quizId];
    
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
}

// 複数選択クイズ機能
function checkMultipleChoice(quizId) {
    const quizContainer = document.querySelector(`[data-quiz-id="${quizId}"]`);
    if (!quizContainer) return;

    const checkboxes = quizContainer.querySelectorAll(`input[name="${quizId}"]`);
    const result = quizContainer.querySelector('.multiple-choice-result');
    const quizData = window.multipleChoiceData[quizId];
    
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
    
    // 正解の選択肢が全て選ばれているかチェック
    correctIndices.forEach(correctIndex => {
        if (!selectedIndices.includes(correctIndex)) {
            isFullyCorrect = false;
        }
    });
    
    // 間違った選択肢が選ばれていないかチェック
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
}

// ドラッグ&ドロップ機能の初期化
document.addEventListener('DOMContentLoaded', function() {
    // カテゴリ分けクイズの初期化
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
            
            zone.addEventListener('dragleave', function() {
                zone.classList.remove('drag-over');
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
});
"""


def _get_additional_js_content() -> str:
    """追加JavaScript機能"""
    return """
// 学習材料追加機能

// テーマ切り替え機能
function switchTheme(theme) {
    const links = document.querySelectorAll('link[href*="custom"]');
    links.forEach(link => {
        if (link.href.includes('custom')) {
            const newHref = theme === 'default' ? 'custom.css' : `custom_${theme}.css`;
            link.href = link.href.replace(/custom[^.]*\\.css/, newHref);
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
"""


if __name__ == "__main__":
    """
    直接実行時のエントリポイント
    """
    try:
        create_test_material()
    except KeyboardInterrupt:
        logger.info("\n処理が中断されました")
        sys.exit(1)
    except Exception as e:
        logger.error(f"予期しないエラーが発生しました: {e}")
        sys.exit(1)
"""
CSS・JavaScript・その他アセットファイルを動的に生成・更新する機能
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from enum import Enum
import json
from .config import PATHS, MATERIAL_ICONS

logger = logging.getLogger(__name__)


class AssetType(Enum):
    """アセットタイプの列挙"""
    CSS = "css"
    JAVASCRIPT = "js"
    YAML = "yml"


@dataclass
class AssetTemplate:
    """アセットテンプレートの定義"""
    name: str
    content: str
    dependencies: List[str] = None
    variables: Dict[str, Any] = None


class AssetGenerator:
    """CSS・JavaScript・その他アセットファイルの生成・更新を管理"""
    
    def __init__(self, docs_dir: Path):
        """
        初期化
        
        Args:
            docs_dir: docsディレクトリのパス
        """
        self.docs_dir = docs_dir
        self.css_templates = {}
        self.js_templates = {}
        self.yml_templates = {}
        self.generated_assets = {}
        
        # 基本テンプレートの初期化
        self._initialize_base_templates()
        
    def _initialize_base_templates(self):
        """基本テンプレートを初期化"""
        # CSSベーステンプレート
        self.css_templates['base'] = AssetTemplate(
            name="base",
            content=self._get_base_css_template()
        )
        
        self.css_templates['tooltip'] = AssetTemplate(
            name="tooltip", 
            content=self._get_tooltip_css_template(),
            variables={'primary_color': '#2196F3', 'background_color': '#ffffff'}
        )
        
        # 学習材料専用CSSテンプレート
        self.css_templates['learning_material'] = AssetTemplate(
            name="learning_material",
            content=self._get_learning_material_css_template(),
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
        
        # JSベーステンプレート
        self.js_templates['base'] = AssetTemplate(
            name="base",
            content=self._get_base_js_template()
        )
        
        self.js_templates['interactive'] = AssetTemplate(
            name="interactive",
            content=self._get_interactive_js_template(),
            dependencies=['base']
        )

    def generate_asset(
        self, 
        asset_type: AssetType, 
        template_name: str, 
        filename: Optional[str] = None,
        variables: Optional[Dict[str, Any]] = None,
        additional_content: Optional[str] = None
    ) -> Path:
        """
        指定されたテンプレートからアセットファイルを生成
        
        Args:
            asset_type: アセットタイプ（CSS, JS, YAML）
            template_name: テンプレート名
            filename: 出力ファイル名（省略時は自動生成）
            variables: テンプレート変数
            additional_content: 追加コンテンツ
            
        Returns:
            生成されたファイルのパス
        """
        # テンプレート取得
        template = self._get_template(asset_type, template_name)
        if not template:
            raise ValueError(f"テンプレート '{template_name}' が見つかりません")
        
        # コンテンツ生成
        content = self._build_content(template, variables, additional_content)
        
        # ファイル名決定
        if not filename:
            filename = f"{template_name}.{asset_type.value}"
        
        # ファイル保存
        file_path = self.docs_dir / filename
        file_path.write_text(content, encoding='utf-8')
        
        # 生成記録
        self.generated_assets[filename] = {
            'type': asset_type,
            'template': template_name,
            'path': file_path,
            'variables': variables or {}
        }
        
        logger.info(f"{asset_type.value.upper()}ファイル生成完了: {file_path}")
        return file_path

    def write_raw_asset(self, asset_type: AssetType, filename: str, content: str) -> Path:
        """
        テンプレートを使用せず、生のコンテンツを直接アセットファイルに書き込む。

        Args:
            asset_type: アセットタイプ（CSS, JS, YAML）
            filename: 出力ファイル名
            content: 書き込む生のコンテンツ

        Returns:
            生成されたファイルのパス
        """
        file_path = self.docs_dir / filename
        file_path.write_text(content, encoding='utf-8')
        
        # 生成記録
        self.generated_assets[filename] = {
            'type': asset_type,
            'template': 'raw', # テンプレートはrawとして記録
            'path': file_path,
            'variables': {}
        }
        
        logger.info(f"RAW {asset_type.value.upper()}ファイル生成完了: {file_path}")
        return file_path

    def update_asset(
        self, 
        filename: str, 
        variables: Optional[Dict[str, Any]] = None,
        additional_content: Optional[str] = None,
        append_mode: bool = False
    ) -> Path:
        """
        既存のアセットファイルを更新
        
        Args:
            filename: 更新対象ファイル名
            variables: 更新する変数
            additional_content: 追加コンテンツ
            append_mode: 追記モード（True）か置換モード（False）
            
        Returns:
            更新されたファイルのパス
        """
        if filename not in self.generated_assets:
            raise ValueError(f"ファイル '{filename}' は管理されていません")
        
        asset_info = self.generated_assets[filename]
        file_path = asset_info['path']
        
        if append_mode and additional_content:
            # 追記モード
            current_content = file_path.read_text(encoding='utf-8')
            new_content = current_content + "\n" + additional_content
        else:
            # 置換モード - テンプレートから再生成
            template = self._get_template(asset_info['type'], asset_info['template'])
            merged_variables = asset_info['variables'].copy()
            if variables:
                merged_variables.update(variables)
            new_content = self._build_content(template, merged_variables, additional_content)
        
        file_path.write_text(new_content, encoding='utf-8')
        
        # 記録更新
        if variables:
            asset_info['variables'].update(variables)
        
        logger.info(f"アセットファイル更新完了: {file_path}")
        return file_path

    def generate_theme_variations(self, base_template: str = 'base') -> Dict[str, Path]:
        """
        複数のテーマバリエーションを生成
        
        Args:
            base_template: ベーステンプレート名
            
        Returns:
            テーマ名とファイルパスの辞書
        """
        themes = {
            "default": {},
            "dark": {
                'primary_color': '#1a1a1a',
                'text_color': '#ffffff',
                'background_color': '#2d2d2d'
            },
            "high_contrast": {
                'primary_color': '#000000', 
                'text_color': '#000000',
                'background_color': '#ffffff',
                'font_weight': 'bold'
            }
        }
        
        generated_files = {}
        for theme_name, theme_vars in themes.items():
            filename = f"custom_{theme_name}.css" if theme_name != "default" else "custom.css"
            file_path = self.generate_asset(
                AssetType.CSS, 
                base_template, 
                filename, 
                variables=theme_vars
            )
            generated_files[theme_name] = file_path
            
        return generated_files

    def create_custom_template(
        self, 
        asset_type: AssetType, 
        name: str, 
        content: str,
        variables: Optional[Dict[str, Any]] = None,
        dependencies: Optional[List[str]] = None
    ):
        """
        カスタムテンプレートを作成・登録
        
        Args:
            asset_type: アセットタイプ
            name: テンプレート名
            content: テンプレートコンテンツ
            variables: デフォルト変数
            dependencies: 依存テンプレート
        """
        template = AssetTemplate(
            name=name,
            content=content,
            variables=variables or {},
            dependencies=dependencies or []
        )
        
        template_dict = self._get_template_dict(asset_type)
        template_dict[name] = template
        
        logger.info(f"カスタムテンプレート '{name}' を登録しました")

    def export_asset_manifest(self) -> Path:
        """
        生成されたアセットの情報をJSONファイルにエクスポート
        
        Returns:
            マニフェストファイルのパス
        """
        manifest_data = {}
        for filename, info in self.generated_assets.items():
            manifest_data[filename] = {
                'type': info['type'].value,
                'template': info['template'],
                'path': str(info['path']),
                'variables': info['variables']
            }
        
        manifest_path = self.docs_dir / 'asset_manifest.json'
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"アセットマニフェストを出力: {manifest_path}")
        return manifest_path

    def _get_template(self, asset_type: AssetType, name: str) -> Optional[AssetTemplate]:
        """テンプレートを取得"""
        template_dict = self._get_template_dict(asset_type)
        return template_dict.get(name)

    def _get_template_dict(self, asset_type: AssetType) -> Dict[str, AssetTemplate]:
        """アセットタイプに応じたテンプレート辞書を取得"""
        if asset_type == AssetType.CSS:
            return self.css_templates
        elif asset_type == AssetType.JAVASCRIPT:
            return self.js_templates
        elif asset_type == AssetType.YAML:
            return self.yml_templates
        else:
            raise ValueError(f"サポートされていないアセットタイプ: {asset_type}")

    def _build_content(
        self, 
        template: AssetTemplate, 
        variables: Optional[Dict[str, Any]] = None,
        additional_content: Optional[str] = None
    ) -> str:
        """テンプレートからコンテンツを構築"""
        content = template.content
        
        # 変数置換
        all_variables = template.variables.copy() if template.variables else {}
        if variables:
            all_variables.update(variables)
        
        for key, value in all_variables.items():
            content = content.replace(f"{{{key}}}", str(value))
        
        # 追加コンテンツの結合
        if additional_content:
            content += f"\n\n/* 追加コンテンツ */\n{additional_content}"
        
        return content

    def _get_base_css_template(self) -> str:
        """ベースCSSテンプレート"""
        return """/* docs/custom.css - 自動生成ファイル */

:root {
    --primary-color: {primary_color};
    --text-color: {text_color}; 
    --background-color: {background_color};
    --font-weight: {font_weight};
}

/* ============================================
   基本スタイル
   ============================================ */
body {{
    font-family: 'Roboto', 'Noto Sans JP', sans-serif;
    background-color: var(--background-color);
    color: var(--text-color);
}

/* ============================================
   カスタムクラス
   ============================================ */
.highlight { background-color: var(--primary-color);
    color: white;
    padding: 2px 4px;
    border-radius: 3px;
}

/* ============================================
   ツールチップスタイル
   ============================================ */
.custom-tooltip { position: relative;
    cursor: help;
    border-bottom: 1px dotted var(--primary-color);
    transition: all 0.3s ease;
    color: var(--primary-color);
    font-weight: 500;
}

.custom-tooltip:hover { border-bottom-color: transparent;
}

/* CSSベースのツールチップ（フォールバック） */
.custom-tooltip::before { content: attr(data-tooltip);
    position: absolute;
    bottom: 125%;
    left: 50%;
    transform: translateX(-50%);
    background: #263238;
    color: white;
    padding: 8px 12px;
    border-radius: 4px;
    font-size: 14px;
    white-space: nowrap;
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s ease;
    z-index: 9999;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    pointer-events: none;
}

.custom-tooltip:hover::before { opacity: 1;
    visibility: visible;
}

/* ============================================
   クイズ関連スタイル
   ============================================ */
:root {
    --quiz-correct: #4CAF50;
    --quiz-incorrect: #F44336;
    --quiz-warning: #FF9800;
}

.quiz-container { border: 2px solid var(--primary-color);
    border-radius: 12px;
    padding: 24px;
    margin: 24px 0;
    background: var(--background-color);
}

.quiz-option { padding: 12px 16px;
    border: 2px solid #ddd;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
    margin: 8px 0;
}

.quiz-option:hover { border-color: var(--primary-color);
}

.quiz-option.correct { background: var(--quiz-correct);
    color: white;
}

.quiz-option.incorrect { background: var(--quiz-incorrect);
    color: white;
}

/* カテゴリ分けクイズスタイル */
.categorization-quiz { border: 2px solid var(--primary-color);
    border-radius: 12px;
    padding: 24px;
    margin: 24px 0;
    background: var(--background-color);
}

.quiz-items { margin-bottom: 24px;
}

.draggable-items { display: flex;
    flex-wrap: wrap;
    gap: 12px;
    margin: 16px 0;
    padding: 16px;
    background: #f5f5f5;
    border-radius: 8px;
    min-height: 60px;
}

.draggable-item { background: #FFC107;
    color: #333;
    padding: 8px 16px;
    border-radius: 20px;
    cursor: move;
    user-select: none;
    transition: all 0.3s ease;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.draggable-item:hover { transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.draggable-item.dragging { opacity: 0.5;
    transform: rotate(5deg);
}

.drop-zones { display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
    margin: 16px 0;
}

.drop-zone { border: 2px dashed #ddd;
    border-radius: 8px;
    background: #fafafa;
    transition: all 0.3s ease;
}

.drop-zone.drag-over { border-color: var(--primary-color);
    background: rgba(25, 118, 210, 0.1);
}

.drop-zone h4 { margin: 0;
    padding: 12px;
    background: var(--primary-color);
    color: white;
    border-radius: 6px 6px 0 0;
    text-align: center;
    font-size: 14px;
}

.drop-area { min-height: 80px;
    padding: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #666;
    font-style: italic;
}

.drop-area .draggable-item { font-style: normal;
    margin: 0;
}

/* 複数選択クイズスタイル */
.multiple-choice-quiz { border: 2px solid var(--primary-color);
    border-radius: 12px;
    padding: 24px;
    margin: 24px 0;
    background: var(--background-color);
}

.quiz-options { margin: 16px 0;
}

.option-label { display: block;
    padding: 12px 16px;
    margin: 8px 0;
    border: 2px solid #ddd;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
    background: var(--background-color);
}

.option-label:hover { border-color: var(--primary-color);
    background: rgba(25, 118, 210, 0.05);
}

.option-label input[type="checkbox"] { margin-right: 12px;
    transform: scale(1.2);
}

.option-text { font-size: 14px;
}

.check-categorization, .check-multiple-choice { background: var(--primary-color);
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 16px;
    margin-top: 16px;
    transition: all 0.3s ease;
}

.check-categorization:hover, .check-multiple-choice:hover { background: #1565C0;
    transform: translateY(-1px);
}

.categorization-result, .multiple-choice-result { margin-top: 16px;
    padding: 16px;
    border-radius: 8px;
    font-weight: bold;
}

.categorization-result .success, .multiple-choice-result .success { background: #E8F5E8;
    color: var(--quiz-correct);
    border: 1px solid var(--quiz-correct);
}

.categorization-result .warning, .multiple-choice-result .warning { background: #FFF8E1;
    color: var(--quiz-warning);
    border: 1px solid #FFB74D;
}

.categorization-result .error, .multiple-choice-result .error { background: #FFEBEE;
    color: var(--quiz-incorrect);
    border: 1px solid var(--quiz-incorrect);
}
"""

    def _get_tooltip_css_template(self) -> str:
        """ツールチップCSSテンプレート"""
        return """/* ツールチップ専用スタイル */
.custom-tooltip { position: relative;
    cursor: help;
    border-bottom: 1px dotted {primary_color};
}

.custom-tooltip::before { content: attr(data-tooltip);
    position: absolute;
    bottom: 125%;
    left: 50%;
    transform: translateX(-50%);
    background-color: {background_color};
    color: {text_color};
    padding: 8px 12px;
    border-radius: 4px;
    font-size: 14px;
    white-space: nowrap;
    opacity: 0;
    visibility: hidden;
    transition: opacity 0.3s;
    z-index: 1000;
}

.custom-tooltip:hover::before { opacity: 1;
    visibility: visible;
}
"""

    def _get_learning_material_css_template(self) -> str:
        """学習材料専用CSSテンプレート（完全版）"""
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
.custom-tooltip { position: relative;
    cursor: help;
    border-bottom: 1px dotted var(--primary-color);
    transition: all 0.3s ease;
}

.custom-tooltip::before { content: attr(data-tooltip);
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

.custom-tooltip:hover::before { opacity: 1;
    visibility: visible;
}

/* クイズスタイル */
.quiz-container { border: 2px solid var(--primary-color);
    border-radius: 12px;
    padding: 24px;
    margin: 24px 0;
    background: var(--background-color);
}

.quiz-option { padding: 12px 16px;
    border: 2px solid #ddd;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
    margin: 8px 0;
}

.quiz-option:hover { border-color: var(--primary-color);
}

.quiz-option.correct { background: var(--quiz-correct);
    color: white;
}

.quiz-option.incorrect { background: var(--quiz-incorrect);
    color: white;
}

/* カテゴリ分けクイズスタイル */
.categorization-quiz { border: 2px solid var(--primary-color);
    border-radius: 12px;
    padding: 24px;
    margin: 24px 0;
    background: var(--background-color);
}

.quiz-items { margin-bottom: 24px;
}

.draggable-items { display: flex;
    flex-wrap: wrap;
    gap: 12px;
    margin: 16px 0;
    padding: 16px;
    background: #f5f5f5;
    border-radius: 8px;
    min-height: 60px;
}

.draggable-item { background: var(--secondary-color);
    color: #333;
    padding: 8px 16px;
    border-radius: 20px;
    cursor: move;
    user-select: none;
    transition: all 0.3s ease;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.draggable-item:hover { transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.draggable-item.dragging { opacity: 0.5;
    transform: rotate(5deg);
}

.drop-zones { display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
    margin: 16px 0;
}

.drop-zone { border: 2px dashed #ddd;
    border-radius: 8px;
    background: #fafafa;
    transition: all 0.3s ease;
}

.drop-zone.drag-over { border-color: var(--primary-color);
    background: rgba(25, 118, 210, 0.1);
}

.drop-zone h4 { margin: 0;
    padding: 12px;
    background: var(--primary-color);
    color: white;
    border-radius: 6px 6px 0 0;
    text-align: center;
    font-size: 14px;
}

.drop-area { min-height: 80px;
    padding: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #666;
    font-style: italic;
}

.drop-area .draggable-item { font-style: normal;
    margin: 0;
}

/* 複数選択クイズスタイル */
.multiple-choice-quiz { border: 2px solid var(--primary-color);
    border-radius: 12px;
    padding: 24px;
    margin: 24px 0;
    background: var(--background-color);
}

.quiz-options { margin: 16px 0;
}

.option-label { display: block;
    padding: 12px 16px;
    margin: 8px 0;
    border: 2px solid #ddd;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
    background: var(--background-color);
}

.option-label:hover { border-color: var(--primary-color);
    background: rgba(25, 118, 210, 0.05);
}

.option-label input[type="checkbox"] { margin-right: 12px;
    transform: scale(1.2);
}

.option-text { font-size: 14px;
}

.check-categorization, .check-multiple-choice { background: var(--primary-color);
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 16px;
    margin-top: 16px;
    transition: all 0.3s ease;
}

.check-categorization:hover, .check-multiple-choice:hover { background: #1565C0;
    transform: translateY(-1px);
}

.categorization-result, .multiple-choice-result { margin-top: 16px;
    padding: 16px;
    border-radius: 8px;
    font-weight: bold;
}

.categorization-result .success, .multiple-choice-result .success { background: #E8F5E8;
    color: var(--quiz-correct);
    border: 1px solid var(--quiz-correct);
}

.categorization-result .warning, .multiple-choice-result .warning { background: #FFF8E1;
    color: #FF9800;
    border: 1px solid #FFB74D;
}

.categorization-result .error, .multiple-choice-result .error { background: #FFEBEE;
    color: var(--quiz-incorrect);
    border: 1px solid var(--quiz-incorrect);
}

/* テーマ切り替えボタン */
.theme-switcher { margin: 20px 0;
    text-align: center;
}

.theme-switcher button { margin: 5px;
    padding: 8px 16px;
    border: 1px solid var(--primary-color);
    background: var(--background-color);
    color: var(--text-color);
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.theme-switcher button:hover { background: var(--primary-color);
    color: white;
}
"""

    def _get_base_js_template(self) -> str:
        """ベースJavaScriptテンプレート"""
        return """// docs/custom.js - 自動生成ファイル（完全修正版）

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
"""

    def _get_interactive_js_template(self) -> str:
        """インタラクティブ機能JavaScriptテンプレート"""
        return """// インタラクティブ機能拡張

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
    
})();"""
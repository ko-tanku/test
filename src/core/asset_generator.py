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

:root {{
    --primary-color: {primary_color};
    --text-color: {text_color}; 
    --background-color: {background_color};
    --font-weight: {font_weight};
}}

/* ============================================
   基本スタイル
   ============================================ */
body {{
    font-family: 'Roboto', 'Noto Sans JP', sans-serif;
    background-color: var(--background-color);
    color: var(--text-color);
}}

/* ============================================
   カスタムクラス
   ============================================ */
.highlight {{
    background-color: var(--primary-color);
    color: white;
    padding: 2px 4px;
    border-radius: 3px;
}}
"""

    def _get_tooltip_css_template(self) -> str:
        """ツールチップCSSテンプレート"""
        return """/* ツールチップ専用スタイル */
.custom-tooltip {{
    position: relative;
    cursor: help;
    border-bottom: 1px dotted {primary_color};
}}

.custom-tooltip::before {{
    content: attr(data-tooltip);
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
}}

.custom-tooltip:hover::before {{
    opacity: 1;
    visibility: visible;
}}
"""

    def _get_base_js_template(self) -> str:
        """ベースJavaScriptテンプレート"""
        return """// docs/custom.js - 自動生成ファイル

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
    
    // 初期化
    document.addEventListener('DOMContentLoaded', function() {
        initAccordions();
        initTabs();
    });
})();
"""
"""
テスト資料生成のメインエントリポイント（改善版）
YAML データ駆動型、テンプレート外部化対応
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

from src.core.config import PATHS
from src.core.asset_generator import AssetGenerator, AssetType
from src.core.mkdocs_manager import MkDocsManager, NavItem
from src.materials.test_material.test_material_contents import TestMaterialContentManager
from src.core.utils import load_yaml_to_json

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_material_config() -> Dict[str, Any]:
    """資料設定をYAMLから読み込み"""
    config_path = Path(__file__).parent / "content" / "config.yml"
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = yaml.safe_load(f)
            return config_data.get('material_config', {}), config_data.get('template_variables', {})
    return {}, {}


def update_mkdocs_config(material_config: Dict[str, Any], template_vars: Dict[str, Any]) -> None:
    """
    アセット機能を使ってmkdocs.ymlとアセットファイルを更新（テンプレート外部化対応）
    
    Args:
        material_config: 資料の設定情報
        template_vars: テンプレート変数
    """
    docs_dir = PATHS["DOCS_DIR"]
    
    # アセット機能の初期化
    asset_generator = AssetGenerator(docs_dir)
    mkdocs_manager = MkDocsManager(project_root)
    
    logger.info("=== アセットファイル生成開始 ===")
    
    try:
        # 1. CSSファイル生成
        logger.info("CSSファイルを生成中...")
        
        # テンプレートファイルを外部から読み込み、カスタムテンプレートとして登録
        templates_dir = Path(__file__).parent / "templates"
        
        # CSSテンプレートを読み込み
        css_template_path = templates_dir / "custom.css.jinja"
        if css_template_path.exists():
            with open(css_template_path, 'r', encoding='utf-8') as f:
                css_template = f.read()
            
            asset_generator.create_custom_template(
                AssetType.CSS,
                'test_material_custom',
                css_template
            )
        
        # 複数テーマのCSS生成
        css_files = []
        css_vars = template_vars.get('css', {})
        
        themes = {
            'default': css_vars,
            'dark': {
                **css_vars,
                'background_color': '#1a1a1a',
                'text_color': '#e0e0e0',
                'tooltip_bg': '#424242',
                'theme': 'dark'
            },
            'high_contrast': {
                **css_vars,
                'primary_color': '#000000',
                'background_color': '#ffffff',
                'text_color': '#000000',
                'theme': 'high_contrast'
            }
        }
        
        for theme_name, theme_vars_merged in themes.items():
            filename = f"custom_{theme_name}.css" if theme_name != 'default' else "custom.css"
            css_path = asset_generator.generate_asset(
                AssetType.CSS,
                'test_material_custom',
                filename,
                variables=theme_vars_merged
            )
            css_files.append(filename)
        
        # 2. JavaScriptファイル生成
        logger.info("JavaScriptファイルを生成中...")
        
        # JavaScriptテンプレートを読み込み
        js_template_path = templates_dir / "interactive.js.jinja"
        if js_template_path.exists():
            with open(js_template_path, 'r', encoding='utf-8') as f:
                js_template = f.read()
            
            asset_generator.create_custom_template(
                AssetType.JAVASCRIPT,
                'test_material_interactive',
                js_template
            )
        
        # JSファイル生成
        js_files = []
        js_vars = template_vars.get('js', {})
        
        # 基本カスタムJS
        js_path = asset_generator.generate_asset(
            AssetType.JAVASCRIPT,
            'base',
            'custom.js'
        )
        js_files.append('custom.js')
        
        # インタラクティブJS（カスタムテンプレート使用）
        interactive_js_path = asset_generator.generate_asset(
            AssetType.JAVASCRIPT,
            'test_material_interactive',
            'interactive.js',
            variables=js_vars
        )
        js_files.append('interactive.js')
        
        # クイズシステムJS
        quiz_js_path = asset_generator.generate_asset(
            AssetType.JAVASCRIPT,
            'interactive',
            'quiz.js'
        )
        js_files.append('quiz.js')
        
        # 3. クイズデータJSファイル生成
        logger.info("クイズデータJSファイルを生成中...")
        quiz_yaml_path = Path(__file__).parent / "content" / "quizzes.yml"
        
        if quiz_yaml_path.exists():
            # load_yaml_to_json を使ってYAMLをJSON文字列として読み込む
            quiz_json_content = load_yaml_to_json(str(quiz_yaml_path))
            
            # JavaScriptの変数として埋め込む形式
            quiz_data_js_content = f"window.quizData = {quiz_json_content}"
            
            # write_raw_asset を使ってquizzes_data.jsを生成
            quiz_data_js_path = asset_generator.write_raw_asset(
                AssetType.JAVASCRIPT,
                'quizzes_data.js',
                quiz_data_js_content
            )
            js_files.append('quizzes_data.js')

        # 4. MkDocs設定生成・更新
        logger.info("MkDocs設定を更新中...")
        
        # 構造化ナビゲーション作成（YAML設定から自動生成）
        nav_children = [NavItem(title="ホーム", path="test_material/index.md")]
        
        # 章リストを設定から生成
        for chapter in material_config.get('chapters', []):
            chapter_title = chapter['title']
            chapter_id = chapter['id']
            nav_children.append(NavItem(
                title=chapter_title,
                path=f"test_material/documents/{chapter_id}.md"
            ))
        
        # 参考資料を追加
        nav_children.extend([
            NavItem(title="用語集", path="test_material/glossary.md"),
            NavItem(title="FAQ", path="test_material/faq.md"),
            NavItem(title="TIPS", path="test_material/tips.md")
        ])
        
        nav_structure = [
            NavItem(
                title=material_config.get("title", "学習教材"),
                children=nav_children
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
            "plugins": [
                "search",
                {
                    "mermaid2": {
                        "version": "10.6.1"
                    }
                }
            ],
            "markdown_extensions": [
                "admonition",
                "pymdownx.details",
                {
                    "pymdownx.superfences": {
                        "custom_fences": [
                            {
                                "name": "mermaid",
                                "class": "mermaid",
                                "format": "!!python/name:mermaid2.fence_mermaid_custom"
                            }
                        ]
                    }
                },
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
        
        # 5. 設定検証
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
        
        # 6. アセットマニフェスト出力
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
    テスト資料を生成するメイン関数（改善版）
    """
    logger.info("テスト資料の生成を開始します（YAML駆動型）...")
    
    try:
        # YAML設定を読み込み
        material_config, template_vars = load_material_config()
        
        # 出力ディレクトリの設定
        output_dir = PATHS["DOCS_DIR"] / "test_material"
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
        update_mkdocs_config(material_config, template_vars)
        
        logger.info("テスト資料の生成が完了しました！")
        logger.info("\n実行方法:")
        logger.info("  1. プロジェクトルートで: mkdocs serve")
        logger.info("  2. ブラウザで: http://127.0.0.1:8000")
        logger.info("  3. 新機能（第6章・第7章）でCore機能と拡張機能をテスト")
        
    except Exception as e:
        logger.error(f"テスト資料生成中にエラーが発生しました: {e}")
        logger.exception("詳細なエラー情報:")
        raise


# テンプレートはtemplates/ディレクトリで外部ファイル化し、Core機能で一元管理

if __name__ == "__main__":
    try:
        create_test_material()
    except KeyboardInterrupt:
        logger.info("\n処理が中断されました")
        sys.exit(1)
    except Exception as e:
        logger.error(f"予期しないエラーが発生しました: {e}")
        sys.exit(1)
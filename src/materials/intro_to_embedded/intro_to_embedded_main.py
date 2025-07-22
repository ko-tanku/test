"""
組込制御入門生成のメインエントリポイント
"""

import sys
import logging
from pathlib import Path
import yaml

# プロジェクトルートをsys.pathに追加
project_root = Path(__file__).resolve().parents[3]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.core.config import PATHS
from src.materials.intro_to_embedded.intro_to_embedded_config import MATERIAL_CONFIG
from src.materials.intro_to_embedded.intro_to_embedded_contents import IntroToEmbeddedContentManager

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def update_mkdocs_config(material_config: dict) -> None:
    """
    mkdocs.ymlにintro_to_embeddedのナビゲーション構造を追加

    Args:
        material_config: 教材の設定情報
    """
    mkdocs_path = project_root / "mkdocs.yml"

    try:
        # 既存のmkdocs.ymlを読み込み
        if mkdocs_path.exists():
            with open(mkdocs_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f) or {}
        else:
            config = {
                'site_name': 'MkDocs Learning Material Generator',
                'theme': {
                    'name': 'material',
                    'palette': {
                        'primary': 'teal',
                        'accent': 'orange'
                    },
                    'features': [
                        'navigation.tabs',
                        'search.suggest',
                        'toc.integrate',
                        'content.tooltips'
                    ]
                }
            }

        # ナビゲーション構造を定義
        intro_nav = {
            material_config["title"]: [
                {'ホーム': 'intro_to_embedded/index.md'},
                {'第1章: 組込制御ってなんだろう？': 'intro_to_embedded/documents/chapter01.md'},
                {'第2章: ITと組み込み技術': 'intro_to_embedded/documents/chapter02.md'},
                {'第3章: 技術者を目指す意義': 'intro_to_embedded/documents/chapter03.md'},
                {'演習問題': 'intro_to_embedded/exercises.md'},
                {'用語集': 'intro_to_embedded/glossary.md'},
                {'FAQ': 'intro_to_embedded/faq.md'},
                {'学習TIPS': 'intro_to_embedded/tips.md'}
            ]
        }

        # 既存のnavがない場合は新規作成
        if 'nav' not in config:
            config['nav'] = []

        # intro_to_embeddedが既にある場合は削除
        config['nav'] = [item for item in config['nav']
                        if not any(material_config["title"] in str(item) for item in [item])]

        # 新しいナビゲーション構造を追加
        config['nav'].append(intro_nav)

        # プラグインの設定
        if 'plugins' not in config:
            config['plugins'] = []
        if 'search' not in config['plugins']:
            config['plugins'].append('search')

        # Markdown拡張の設定
        if 'markdown_extensions' not in config:
            config['markdown_extensions'] = []

        required_extensions = [
            'admonition',
            'pymdownx.details',
            'pymdownx.superfences',
            'attr_list',
            'md_in_html',
            'abbr',
            'footnotes',
            'tables'
        ]

        for ext in required_extensions:
            if ext not in config['markdown_extensions']:
                config['markdown_extensions'].append(ext)

        # CSSとJSの設定
        if 'extra_css' not in config:
            config['extra_css'] = []
        if 'custom.css' not in config['extra_css']:
            config['extra_css'].append('custom.css')

        if 'extra_javascript' not in config:
            config['extra_javascript'] = []
        if 'custom.js' not in config['extra_javascript']:
            config['extra_javascript'].append('custom.js')

        # mkdocs.ymlを保存
        with open(mkdocs_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

        logger.info(f"mkdocs.yml を更新しました: {mkdocs_path}")

    except Exception as e:
        logger.error(f"mkdocs.yml の更新中にエラーが発生しました: {e}")
        raise


def create_intro_to_embedded_material() -> None:
    """
    組込制御入門資料を生成するメイン関数
    """
    logger.info("組込制御入門資料の生成を開始します...")

    try:
        # 出力ディレクトリの設定
        output_dir = PATHS["DOCS_DIR"] / "intro_to_embedded"
        logger.info(f"出力ディレクトリ: {output_dir}")

        # コンテンツマネージャーの初期化
        content_manager = IntroToEmbeddedContentManager(
            material_name="intro_to_embedded",
            output_base_dir=output_dir
        )

        # コンテンツの生成
        logger.info("コンテンツを生成中...")
        generated_files = content_manager.generate_content()

        logger.info(f"生成されたファイル数: {len(generated_files)}")
        for file_path in generated_files:
            logger.info(f"  - {file_path}")

        # mkdocs.ymlの更新
        logger.info("mkdocs.ymlを更新中...")
        update_mkdocs_config(MATERIAL_CONFIG)

        logger.info("組込制御入門資料の生成が完了しました！")
        logger.info("\n実行方法:")
        logger.info("  1. プロジェクトルートで: mkdocs serve")
        logger.info("  2. ブラウザで: http://127.0.0.1:8000")
        logger.info("  3. サイドバーから「組込制御入門」を選択")

    except Exception as e:
        logger.error(f"資料生成中にエラーが発生しました: {e}")
        logger.exception("詳細なエラー情報:")
        raise


if __name__ == "__main__":
    """
    直接実行時のエントリポイント
    """
    try:
        create_intro_to_embedded_material()
    except KeyboardInterrupt:
        logger.info("\n処理が中断されました")
        sys.exit(1)
    except Exception as e:
        logger.error(f"予期しないエラーが発生しました: {e}")
        sys.exit(1)
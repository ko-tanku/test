"""
Test Material Main
テスト資料生成のメインスクリプト
"""

import sys
from pathlib import Path
import logging
import traceback
from datetime import datetime

# プロジェクトルートをsys.pathに追加
project_root = Path(__file__).resolve().parents[3]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.core.config import PATHS, SYSTEM_CONFIG
from src.core.utils import ensure_directory_exists
from test_material_contents import TestMaterialContentManager
from test_material_config import get_execution_config

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('test_material_generation.log', encoding='utf-8')
    ]
)

logger = logging.getLogger(__name__)


def update_mkdocs_yml():
    """
    mkdocs.ymlファイルを更新（テスト資料のnavを追加）
    """
    import yaml

    mkdocs_yml_path = project_root / "mkdocs.yml"

    try:
        # 既存のmkdocs.ymlを読み込む（存在する場合）
        if mkdocs_yml_path.exists():
            with open(mkdocs_yml_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f) or {}
        else:
            # 新規作成
            config = {
                'site_name': 'MkDocs Materials Generator',
                'site_description': 'MkDocs Materials Generator で生成された学習資料',
                'docs_dir': 'docs',
                'site_dir': 'site'
            }

        # Material テーマの設定
        config['theme'] = {
            'name': 'material',
            'language': 'ja',
            'palette': {
                'scheme': 'default',
                'primary': 'blue',
                'accent': 'amber'
            },
            'features': [
                'navigation.tabs',
                'navigation.top',
                'navigation.tracking',
                'search.suggest',
                'search.highlight',
                'content.tooltips'
            ]
        }

        # Markdown拡張の設定
        config['markdown_extensions'] = [
            'admonition',
            'pymdownx.details',
            'pymdownx.superfences',
            'pymdownx.highlight',
            'pymdownx.tabbed:',
            {'alternate_style': True},
            'attr_list',
            'md_in_html',
            'footnotes',
            'tables',
            'toc:',
            {'permalink': True}
        ]

        # プラグインの設定
        config['plugins'] = [
            'search',
            {'search': {'lang': 'ja'}}
        ]

        # ナビゲーションの設定（テスト資料）
        config['nav'] = [
            {'Home': 'index.md'},
            {
                'テスト資料': [
                    {'目次': 'assets/test_material/index.md'},
                    {'第1章: システムテスト概要': 'assets/test_material/chapter_01_system_test_overview.md'},
                    {'第2章: 図表生成テスト': 'assets/test_material/chapter_02_chart_generation_test.md'},
                    {'第3章: 表生成テスト': 'assets/test_material/chapter_03_table_generation_test.md'},
                    {'第4章: 用語管理テスト': 'assets/test_material/chapter_04_knowledge_management_test.md'},
                    {'第5章: 統合テスト': 'assets/test_material/chapter_05_integration_test.md'},
                    {'用語集': 'assets/test_material/glossary.md'}
                ]
            }
        ]

        # CSSの追加設定
        config['extra_css'] = [
            'css/custom.css'
        ]

        # mkdocs.ymlを保存
        with open(mkdocs_yml_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

        logger.info(f"mkdocs.yml updated: {mkdocs_yml_path}")

        # カスタムCSSファイルを作成
        css_dir = project_root / "docs" / "css"
        ensure_directory_exists(css_dir)

        custom_css_path = css_dir / "custom.css"
        custom_css_content = """
/* カスタムCSS for MkDocs Materials Generator */

/* ツールチップのスタイル */
[data-md-tooltip] {
    border-bottom: 1px dotted #666;
    cursor: help;
}

/* iframeのスタイル調整 */
iframe {
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    margin: 1em 0;
}

/* テーブルのレスポンシブ対応 */
.md-typeset table {
    display: block;
    overflow-x: auto;
}

/* コードブロックの調整 */
.md-typeset pre {
    max-height: 400px;
    overflow-y: auto;
}

/* 注記ブロックの調整 */
.md-typeset .admonition {
    font-size: 0.9rem;
}
"""

        with open(custom_css_path, 'w', encoding='utf-8') as f:
            f.write(custom_css_content)

        logger.info(f"Custom CSS created: {custom_css_path}")

    except Exception as e:
        logger.error(f"Failed to update mkdocs.yml: {e}")
        raise


def create_docs_index():
    """
    docs/index.mdを作成（メインのトップページ）
    """
    docs_dir = project_root / "docs"
    ensure_directory_exists(docs_dir)

    index_path = docs_dir / "index.md"

    index_content = f"""# MkDocs Materials Generator

このサイトは、MkDocs Materials Generator によって自動生成された学習資料のデモサイトです。

## システム情報

- **バージョン**: {SYSTEM_CONFIG['version']}
- **最終更新**: {SYSTEM_CONFIG['last_updated']}
- **作者**: {SYSTEM_CONFIG['author']}

## 利用可能な資料

### 📚 テスト資料

MkDocs Materials Generator の全機能をテストするための資料です。

- [テスト資料を見る](assets/test_material/index.md)

## 機能一覧

このシステムは以下の機能を提供します：

1. **Markdownコンテンツ生成**
   - 見出し、段落、リスト、コードブロック
   - Material for MkDocsの拡張機能（Admonition、Tabs）
   - 専門用語のツールチップ

2. **図表生成**
   - Matplotlib/Seabornによる静的図表
   - Plotlyによるインタラクティブ図表
   - カスタム描画関数のサポート

3. **表生成**
   - 基本的なHTMLテーブル
   - スタイル付きテーブル
   - 検索・ソート機能付きテーブル

4. **用語管理**
   - 専門用語の一元管理
   - 自動用語集生成
   - ツールチップ機能

## 使い方

### 1. プレビューサーバーの起動

```bash
mkdocs serve
'''
### 2. 静的サイトのビルド
```bash
mkdocs build
'''

### 3. 新しい資料の追加
src/materials/ディレクトリに新しいモジュールを作成し、BaseContentManagerを継承してください。

!!! info "お問い合わせ"
このシステムに関するお問い合わせは、GitHubのIssueでお願いします。
"""
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_content)

    logger.info(f"Main index.md created: {index_path}")

def main():
    """
    メイン実行関数
    """
    start_time = datetime.now()
    print("=" * 60)
    print("MkDocs Materials Generator - Test Material Generation")
    print("=" * 60)
    print(f"Started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Project root: {project_root}")
    print()

    try:
        # 実行設定を取得
        exec_config = get_execution_config()

        # 1. 必要なディレクトリを作成
        logger.info("Creating necessary directories...")
        directories = [
            PATHS['docs_dir'],
            PATHS['assets_dir'],
            PATHS['test_material_dir'],
            PATHS['test_material_assets_dir'],
            PATHS['test_material_charts_dir'],
            PATHS['test_material_tables_dir']
        ]

        for directory in directories:
            ensure_directory_exists(directory)
            logger.info(f"Directory ensured: {directory}")

        # 2. メインのindex.mdを作成
        logger.info("Creating main index.md...")
        create_docs_index()

        # 3. テスト資料のコンテンツを生成
        logger.info("Generating test material content...")
        content_manager = TestMaterialContentManager()

        generated_files = content_manager.generate_content()

        print(f"\n✅ Generated {len(generated_files)} files:")
        for file_path in generated_files:
            print(f"   - {file_path.relative_to(project_root)}")

        # 4. mkdocs.ymlを更新
        logger.info("Updating mkdocs.yml...")
        update_mkdocs_yml()

        # 5. 統計情報を表示
        stats = content_manager.get_material_statistics()

        print("\n📊 Generation Statistics:")
        print(f"   - Material name: {stats['material_name']}")
        print(f"   - Total terms: {stats['knowledge_stats']['total_terms']}")
        print(f"   - Categories: {len(stats['knowledge_stats']['categories'])}")
        print(f"   - Chapters: {len(stats['knowledge_stats']['chapters'])}")

        # 6. 実行時間を計算
        end_time = datetime.now()
        duration = end_time - start_time

        print(f"\n⏱️  Total execution time: {duration.total_seconds():.2f} seconds")

        # 7. 次のステップを表示
        print("\n📝 Next steps:")
        print("   1. Run 'mkdocs serve' to preview the site")
        print("   2. Open http://127.0.0.1:8000 in your browser")
        print("   3. Run 'mkdocs build' to build the static site")

        print("\n✨ Test material generation completed successfully!")

        return 0

    except Exception as e:
        logger.error(f"Test material generation failed: {e}")
        logger.error(traceback.format_exc())

        print(f"\n❌ Error: {e}")
        print("\nCheck 'test_material_generation.log' for details.")

        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

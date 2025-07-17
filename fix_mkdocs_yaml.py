"""
Final mkdocs.yml fix script
"""
import yaml
from pathlib import Path

def create_correct_mkdocs_config():
    """
    正しいmkdocs.yml設定を作成
    """
    config = {
        'site_name': 'テスト資料',
        'site_description': 'MkDocs Materials Generator の動作確認用テスト資料',
        'site_author': 'MkDocs Materials Generator',
        'docs_dir': 'docs',
        'site_dir': 'site',
        'theme': {
            'name': 'material',
            'language': 'ja',
            'palette': {
                'scheme': 'default',
                'primary': 'green',
                'accent': 'orange'
            },
            'features': [
                'navigation.tabs',
                'navigation.top',
                'navigation.tracking',
                'search.suggest',
                'search.highlight',
                'search.share',
                'toc.integrate',
                'content.code.annotate',
                'content.tooltips'
            ]
        },
        'markdown_extensions': [
            'admonition',
            'pymdownx.details',
            'pymdownx.superfences',
            'pymdownx.highlight',
            'pymdownx.tabbed',
            'attr_list',
            'md_in_html',
            'footnotes',
            'tables',
            'toc',
            'abbr',
            'pymdownx.snippets'
        ],
        'plugins': [
            'search'
        ],
        'nav': [
            {'ホーム': 'assets/test_material/index.md'},
            {'第1章 システムテスト概要': 'assets/test_material/chapter_01_system_test_overview.md'},
            {'第2章 図表生成テスト': 'assets/test_material/chapter_02_chart_generation_test.md'},
            {'第3章 表生成テスト': 'assets/test_material/chapter_03_table_generation_test.md'},
            {'第4章 用語管理テスト': 'assets/test_material/chapter_04_knowledge_management_test.md'},
            {'第5章 統合テスト': 'assets/test_material/chapter_05_integration_test.md'},
            {'用語集': 'assets/test_material/glossary.md'}
        ],
        'extra_css': [
            'assets/custom.css'
        ]
    }
    
    return config

def fix_mkdocs_config():
    """
    mkdocs.ymlを修正
    """
    mkdocs_path = Path('mkdocs.yml')
    
    # バックアップを作成
    if mkdocs_path.exists():
        backup_path = Path('mkdocs.yml.backup')
        mkdocs_path.rename(backup_path)
        print(f"✅ Backup created: {backup_path}")
    
    # 正しい設定を作成
    config = create_correct_mkdocs_config()
    
    # YAML形式で保存（正しい形式で）
    with open(mkdocs_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    print("✅ mkdocs.yml fixed with correct navigation format!")
    
    # 設定を確認表示
    print("\n📝 Navigation configuration:")
    for item in config['nav']:
        for title, path in item.items():
            print(f"  - {title}: {path}")

if __name__ == "__main__":
    fix_mkdocs_config()
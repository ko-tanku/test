"""
Fix all path-related issues
"""
import sys
import re
from pathlib import Path

# プロジェクトルートをsys.pathに追加
project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

def fix_markdown_files():
    """
    生成されたMarkdownファイルのパスを修正
    """
    test_material_dir = project_root / "docs" / "assets" / "test_material"
    
    if not test_material_dir.exists():
        print("❌ test_material directory not found")
        return
    
    # 修正対象のMarkdownファイル
    md_files = list(test_material_dir.glob("chapter_*.md"))
    
    for md_file in md_files:
        print(f"🔧 Fixing {md_file.name}...")
        
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # iframeのsrcパスを修正
            # assets/charts/file.html → /assets/charts/file.html
            content = re.sub(
                r'<iframe src="assets/charts/([^"]+)"',
                r'<iframe src="/assets/charts/\1"',
                content
            )
            
            # assets/tables/file.html → /assets/tables/file.html
            content = re.sub(
                r'<iframe src="assets/tables/([^"]+)"',
                r'<iframe src="/assets/tables/\1"',
                content
            )
            
            # 相対リンクを修正
            # [text](assets/charts/file.html) → [text](/assets/charts/file.html)
            content = re.sub(
                r'\[([^\]]+)\]\(assets/(charts|tables)/([^)]+)\)',
                r'[\1](/assets/\2/\3)',
                content
            )
            
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Fixed {md_file.name}")
            
        except Exception as e:
            print(f"❌ Error fixing {md_file.name}: {e}")

def fix_mkdocs_config():
    """
    mkdocs.ymlの設定を最適化
    """
    mkdocs_file = project_root / "mkdocs.yml"
    
    # 追加のMarkdown拡張を設定
    additional_config = """
# 追加設定をmkdocs.ymlに手動で追加
markdown_extensions:
  - admonition
  - pymdownx.details
  - pymdownx.superfences
  - pymdownx.highlight
  - pymdownx.tabbed
  - attr_list
  - md_in_html
  - footnotes
  - tables
  - toc
  - abbr
  - pymdownx.snippets
  - pymdownx.caret
  - pymdownx.mark
  - pymdownx.tilde

extra_css:
  - https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500&display=swap

extra_javascript:
  - https://unpkg.com/mermaid@8.8.0/dist/mermaid.min.js
"""
    print("📝 mkdocs.yml optimization notes:")
    print(additional_config)

if __name__ == "__main__":
    print("🔧 Fixing all path issues...")
    print("=" * 50)
    
    fix_markdown_files()
    fix_mkdocs_config()
    
    print("=" * 50)
    print("✅ Path fixes completed!")
    print("\n💡 Next steps:")
    print("1. Run: mkdocs serve")
    print("2. Check: http://127.0.0.1:8000")
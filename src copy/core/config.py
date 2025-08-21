"""
システム全体の設定を集約
base_configの設定を統合し、上位のメタデータを定義
"""

from datetime import datetime
from pathlib import Path

# base_configから設定をインポート
from .base_config import (
    PROJECT_ROOT, DOCS_DIR, ASSETS_DIR_NAME, CHARTS_DIR_NAME, TABLES_DIR_NAME,
    MEANING_COLORS, BASE_CHART_STYLES, BASE_TABLE_STYLES, MKDOCS_SITE_CONFIG,
    GLOSSARY_BASE_PATH, MATERIAL_ICONS
)

# システム設定
SYSTEM_CONFIG = {
    "system_name": "MkDocs Learning Material Generator",
    "version": "1.0.0",
    "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "default_language": "ja",
    "author": "AI Learning Material Creator",
    "output_encoding": "utf-8"
}

# ファイル命名規則
FILE_NAMING_PATTERNS = {
    "md_chapter_index": "{chapter_num:02d}/index.md",
    "md_document_page": "{page_slug}.md",
    "md_site_index": "index.md",
    "md_glossary": "glossary.md",
    "html_chart": "{chart_name_slug}.html",
    "html_table": "{table_name_slug}.html",
    "gif_animation": "{animation_name_slug}.gif"
}

# グローバルカラー設定（MEANING_COLORSを含む）
GLOBAL_COLORS = MEANING_COLORS.copy()

# 主要パスの定義
PATHS = {
    "PROJECT_ROOT": PROJECT_ROOT,
    "DOCS_DIR": DOCS_DIR,
    "ASSETS_DIR": DOCS_DIR / ASSETS_DIR_NAME,
    "TEST_MATERIAL_SRC_DIR": PROJECT_ROOT / "src" / "materials" / "test_material",
    "TEST_MATERIAL_OUTPUT_DIR": DOCS_DIR / "test_material"
}

# 外部公開する要素
__all__ = [
    'SYSTEM_CONFIG',
    'FILE_NAMING_PATTERNS',
    'GLOBAL_COLORS',
    'PATHS',
    'MKDOCS_SITE_CONFIG',
    'BASE_CHART_STYLES',
    'BASE_TABLE_STYLES',
    'GLOSSARY_BASE_PATH',
    'MATERIAL_ICONS'
]
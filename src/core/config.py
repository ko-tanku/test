"""
Configuration module for MkDocs Materials Generator
base_config.pyの設定を集約し、上位メタデータを定義
"""

import datetime
from pathlib import Path
from typing import Dict, Any

from . import base_config

# システムメタデータ
SYSTEM_CONFIG: Dict[str, Any] = {
    "system_name": "MkDocs Materials Generator",
    "version": "1.0.0",
    "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "default_language": "ja",
    "author": "MkDocs Materials Generator",
    "output_encoding": "utf-8",
    "markdown_encoding": "utf-8"
}

# ファイル命名規則テンプレート
FILE_NAMING_PATTERNS: Dict[str, str] = {
    "md_chapter": "chapter_{chapter_num:02d}_{chapter_slug}.md",
    "md_index": "index.md",
    "md_glossary": "glossary.md",
    "html_chart": "chart_{chart_slug}.html",
    "html_table": "table_{table_slug}.html",
    "png_chart": "chart_{chart_slug}.png"
}

# 統合カラーパレット
GLOBAL_COLORS: Dict[str, str] = {
    **base_config.MEANING_COLORS,
    "text_primary": "#212121",
    "text_secondary": "#757575",
    "background_primary": "#ffffff",
    "background_secondary": "#fafafa",
    "divider": "#e0e0e0"
}

# 統合パス設定
PATHS: Dict[str, Path] = {
    "project_root": base_config.PROJECT_ROOT,
    "docs_dir": base_config.DOCS_DIR,
    "assets_dir": base_config.DOCS_DIR / base_config.ASSETS_DIR_NAME,
    "charts_dir": base_config.DOCS_DIR / base_config.ASSETS_DIR_NAME / base_config.CHARTS_DIR_NAME,
    "tables_dir": base_config.DOCS_DIR / base_config.ASSETS_DIR_NAME / base_config.TABLES_DIR_NAME,
    "test_material_dir": base_config.DOCS_DIR / base_config.ASSETS_DIR_NAME / "test_material",
    "test_material_assets_dir": base_config.DOCS_DIR / base_config.ASSETS_DIR_NAME / "test_material" / "assets",
    "test_material_charts_dir": base_config.DOCS_DIR / base_config.ASSETS_DIR_NAME / "test_material" / "assets" / base_config.CHARTS_DIR_NAME,
    "test_material_tables_dir": base_config.DOCS_DIR / base_config.ASSETS_DIR_NAME / "test_material" / "assets" / base_config.TABLES_DIR_NAME
}

# 外部モジュールが参照する主要設定
__all__ = [
    "SYSTEM_CONFIG",
    "FILE_NAMING_PATTERNS", 
    "GLOBAL_COLORS",
    "PATHS",
    "base_config"
]
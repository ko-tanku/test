"""
Base configuration module for MkDocs Materials Generator
システム全体の絶対的な基盤設定と色の定義
"""

from pathlib import Path
from typing import Dict, List, Any

# プロジェクトの基本パス設定を修正
# __file__ は base_config.py のパス
# parents[0] = core/
# parents[1] = src/
# parents[2] = my-project/ (プロジェクトルート)
PROJECT_ROOT = Path(__file__).resolve().parents[2]  # my-project/ フォルダ
DOCS_DIR = PROJECT_ROOT / "docs"
ASSETS_DIR_NAME = "assets"
CHARTS_DIR_NAME = "charts"
TABLES_DIR_NAME = "tables"

# 意味合いを持つ色定義（MaterialテーマのPalette色とは独立）
MEANING_COLORS: Dict[str, str] = {
    "danger": "#ff5252",      # 危険・エラー
    "warning": "#ff9800",     # 警告・注意
    "success": "#4caf50",     # 成功・正常
    "info": "#2196f3",        # 情報・参考
    "primary": "#1976d2",     # 主要・重要
    "secondary": "#424242",   # 副次的・補助
    "accent": "#ff4081",      # アクセント・強調
    "neutral": "#9e9e9e"      # 中立・標準
}


# Matplotlib等で利用するデフォルト図表スタイル
BASE_CHART_STYLES: Dict[str, Any] = {
    "font_family": ["Meiryo", "Yu Gothic", "Hiragino Sans", "Noto Sans CJK JP", "sans-serif"],
    "font_size_title": 14,
    "font_size_axis": 10,
    "font_size_legend": 9,
    "figure_dpi": 100,
    "figsize": (10, 6),
    "transparent_bg": True,
    "grid_alpha": 0.3,
    "line_width": 2,
    "marker_size": 6,
    "colors": [
        MEANING_COLORS["primary"],
        MEANING_COLORS["success"],
        MEANING_COLORS["warning"],
        MEANING_COLORS["danger"],
        MEANING_COLORS["info"],
        MEANING_COLORS["accent"]
    ]
}

# HTMLテーブルのデフォルトスタイル
BASE_TABLE_STYLES: Dict[str, Any] = {
    "class_name": "mkdocs-table",
    "header_bg_color": MEANING_COLORS["primary"],
    "header_text_color": "#ffffff",
    "row_even_bg_color": "#f5f5f5",
    "row_odd_bg_color": "#ffffff",
    "border_color": "#e0e0e0",
    "border_width": "1px",
    "cell_padding": "8px 12px",
    "font_size": "14px",
    "font_family": '"Roboto", "Helvetica", "Arial", sans-serif',
    "border_radius": "4px",
    "box_shadow": "0 2px 4px rgba(0,0,0,0.1)"
}

# mkdocs.ymlのベース設定
MKDOCS_SITE_CONFIG: Dict[str, Any] = {
    "site_name": "学習資料",
    "site_description": "MkDocs Materials Generator で生成された学習資料",
    "site_author": "MkDocs Materials Generator",
    "docs_dir": "docs",
    "site_dir": "site",
    "theme": {
        "name": "material",
        "language": "ja",
        "palette": {
            "scheme": "default",
            "primary": "blue",
            "accent": "amber"
        },
        "features": [
            "navigation.tabs",
            "navigation.top",
            "navigation.tracking",
            "search.suggest",
            "search.highlight",
            "search.share",
            "toc.integrate",
            "content.code.annotate",
            "content.tooltips"
        ],
        "icon": {
            "repo": "fontawesome/brands/github"
        }
    },
    "markdown_extensions": [
        "admonition",
        "pymdownx.details",
        "pymdownx.superfences",
        "pymdownx.highlight",
        "pymdownx.tabbed",
        "attr_list",
        "md_in_html",
        "footnotes",
        "tables",
        "toc",
        "abbr",
        "pymdownx.snippets",
        "pymdownx.emoji",
        "pymdownx.arithmatex",
        "pymdownx.keys",
        "pymdownx.mark",
        "pymdownx.critic",
        "pymdownx.caret",
        "pymdownx.tilde"
    ],
    "plugins": [
        "search",
        "minify"
    ],
    "extra": {
        "social": []
    }
}

# 用語集への基本パス
GLOSSARY_BASE_PATH: str = "glossary.md"
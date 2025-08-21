"""
システム全体の基盤となる設定と色定義
MkDocs Materialテーマのパレット設定とは独立した内部ロジック用の設定
"""

from pathlib import Path
from datetime import datetime

# プロジェクトルートディレクトリ（相対パスで設定）
PROJECT_ROOT = Path(__file__).resolve().parents[2]  # Embedded_control/

# 主要ディレクトリ（相対パスで設定）  
DOCS_DIR = Path("docs")
ASSETS_DIR_NAME = "assets"
CHARTS_DIR_NAME = "charts"
TABLES_DIR_NAME = "tables"

# 意味合いを持つHEXカラーコード（Material Design準拠）
MEANING_COLORS = {
    "danger": "#F44336",   # Material Design Red 500
    "warning": "#FF9800",  # Material Design Orange 500
    "success": "#4CAF50",  # Material Design Green 500
    "info": "#00BCD4"      # Material Design Cyan 500
}

# Material Design Icons辞書（確実に表示されるアイコンのみ）
MATERIAL_ICONS = {
    # システム・ハードウェア関連
    "memory": "memory",
    "speed": "speed",
    "cpu": "developer_board",
    "storage": "storage",
    "device": "devices",
    "hardware": "build",
    "circuit": "cable",
    
    # 学習・情報関連
    "help": "help",
    "info": "info",
    "question": "help_outline",
    "tip": "lightbulb_outline",
    "warning": "warning",
    "error": "error",
    "success": "check_circle",
    
    # ナビゲーション・UI関連
    "home": "home",
    "menu": "menu",
    "settings": "settings",
    "search": "search",
    "bookmark": "bookmark",
    "favorite": "favorite",
    
    # 学習コンテンツ関連
    "book": "book",
    "school": "school",
    "quiz": "quiz",
    "assignment": "assignment",
    "grade": "grade",
    "library": "local_library",
    
    # 技術・開発関連
    "code": "code",
    "bug": "bug_report",
    "terminal": "terminal",
    "api": "api",
    "database": "storage",
    "cloud": "cloud",
    
    # 組み込み・IoT関連
    "sensor": "sensors",
    "microchip": "memory",
    "robot": "precision_manufacturing",
    "automation": "autorenew",
    "control": "tune",
    "signal": "graphic_eq"
}

# 汎用的な図表スタイル設定
BASE_CHART_STYLES = {
    "font_family": ['Meiryo', 'Yu Gothic', 'Meiryo', 'TakaoGothic', 'IPAexGothic', 'IPA Gothic', 'sans-serif'],
    "font_size_title": 16,
    "font_size_label": 12,
    "line_width": 2,
    "marker_size": 6,
    "grid_alpha": 0.5,
    "figure_dpi": 150,      # A4想定
    "figsize": (7, 5),      # A4想定
    "transparent_bg": False
}

# HTMLテーブルのデフォルトスタイル
BASE_TABLE_STYLES = {
    "class_name": "mkdocs-table",
    "header_bg_color": MEANING_COLORS["info"],
    "header_text_color": "#FFFFFF",
    "row_even_bg_color": "#FAFAFA",
    "row_odd_bg_color": "#F0F0F0",
    "border_color": "#CCCCCC",
    "border_width": "1px",
    "cell_padding": "8px 12px",
    "font_size": "0.9em"
}

# MkDocs設定のベース
MKDOCS_SITE_CONFIG = {
    "site_name": "MkDocs Learning Material Generator",
    "site_description": "インタラクティブな学習資料を自動生成するシステム",
    "repo_url": "https://github.com/example/mkdocs-learning-material",
    "repo_name": "mkdocs-learning-material",
    "theme": {
        "name": "material",
        "palette": {
            "primary": "blue",
            "accent": "amber"
        },
        "features": [
            "navigation.tabs",
            "search.suggest",
            "toc.integrate",
            "header.autohide",
            "announce.dismiss",
            "content.tooltips"
        ],
        "locale": "ja"
    },
    "markdown_extensions": [
        "admonition",
        "pymdownx.details",
        {
            "pymdownx.superfences": {
                "custom_fences": [
                    {
                        "name": "mermaid",
                        "class": "mermaid",
                        "format": "!!python/name:pymdownx.superfences.fence_code_format"
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
    ],
    "plugins": [
        "search",
        {
            "mermaid2": {
                "version": "10.6.1",
                "arguments": {
                    "theme": "default",
                    "themeVariables": {
                        "primaryColor": "#1976D2",
                        "primaryTextColor": "#fff",
                        "primaryBorderColor": "#1976D2",
                        "lineColor": "#000000",
                        "secondaryColor": "#FFC107",
                        "tertiaryColor": "#fff"
                    }
                }
            }
        }
    ],
    "extra_javascript": [
        "custom.js",
        "quiz.js"
    ],
    "extra_css": [
        "custom.css",
        "custom_dark.css", 
        "custom_high_contrast.css"
    ],
    "extra": {
        # "analytics": {
        #     "provider": "google",
        #     "property": "G-XXXXXXXXXX"
        # }
    }
}

# 用語集のベースパス
GLOSSARY_BASE_PATH = "glossary.md"
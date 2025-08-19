"""
テスト資料固有の設定
IT・組み込み技術入門テーマ
"""

from src.core.base_config import MKDOCS_SITE_CONFIG
from src.core.config import GLOBAL_COLORS

# テスト資料のメタデータ
MATERIAL_CONFIG = {
    "title": "IT・組み込み技術入門",
    "material_id": "test_material",
    "version": "1.0.0",
    "author": "AI Learning Material Creator",
    "target_audience": "プログラミング初心者・組み込みエンジニア志望者",
    "purpose": "ITと組み込み技術の基礎を学びながら、学習システムの全機能を確認",
    "description": "プログラミングの基礎から組み込みシステムまで、実践的に学べる入門資料",
    "prerequisites": ["基本的なPC操作"],
    "learning_objectives": [
        "プログラミングの基本概念を理解する",
        "組み込みシステムの特徴を理解する",
        "ハードウェアとソフトウェアの関係を理解する",
        "リアルタイムシステムの基礎を理解する"
    ]
}

# MkDocs設定のオーバーライド
MKDOCS_MATERIAL_OVERRIDE = {
    "theme": {
        "palette": {
            "primary": "blue-grey",
            "accent": "cyan"
        }
    }
}

# テスト資料用のカスタムカラー
TEST_MATERIAL_COLORS = GLOBAL_COLORS.copy()
TEST_MATERIAL_COLORS.update({
    "embedded": "#607D8B",  # Blue Grey
    "hardware": "#00BCD4",  # Cyan
    "software": "#4CAF50"   # Green
})
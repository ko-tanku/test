"""
テスト資料固有の設定
coreの全機能を試すための設定を含む
"""

from src.core.base_config import MKDOCS_SITE_CONFIG
from src.core.config import GLOBAL_COLORS

# テスト資料のメタデータ
MATERIAL_CONFIG = {
    "title": "Core機能検証テスト資料",
    "material_id": "test_material",
    "version": "1.0.0",
    "author": "AI Learning Material Creator",
    "target_audience": "開発者",
    "purpose": "Coreモジュールの機能確認",
    "description": "MkDocs学習資料生成システムの全機能を網羅的にテストするための資料",
    "prerequisites": [],
    "learning_objectives": [
        "MkDocsの基本機能を理解する",
        "ツールチップ機能の動作を確認する",
        "インタラクティブな図表の生成を確認する",
        "用語集・FAQ・TIPSの自動生成を確認する"
    ]
}

# MkDocs設定のオーバーライド（テスト資料用）
MKDOCS_MATERIAL_OVERRIDE = {
    "theme": {
        "palette": {
            "primary": "indigo",
            "accent": "orange"
        }
    }
}

# テスト資料用のカスタムカラー
TEST_MATERIAL_COLORS = GLOBAL_COLORS.copy()
TEST_MATERIAL_COLORS.update({
    "test_primary": "#3F51B5",  # Indigo
    "test_secondary": "#FF9800"  # Orange
})
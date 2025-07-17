"""
Test Material Configuration
テスト資料固有の設定とカスタマイズ
"""

from pathlib import Path
from typing import Dict, List, Any

# テスト資料固有の設定
TEST_MATERIAL_CONFIG: Dict[str, Any] = {
    "material_name": "テスト資料",
    "material_slug": "test_material",
    "version": "1.0.0",
    "description": "MkDocs Materials Generator の動作確認用テスト資料",
    "author": "MkDocs Materials Generator",
    "language": "ja",
    "estimated_duration": "1時間",
    "difficulty": "テスト用",
    "target_audience": ["開発者", "テスター", "システム管理者"]
}

# テスト資料のカスタムカラーパレット
TEST_MATERIAL_COLORS: Dict[str, str] = {
    "primary": "#2E7D32",      # 深緑（テスト成功）
    "secondary": "#FFA726",    # オレンジ（警告）
    "success": "#388E3C",      # 緑（成功）
    "warning": "#F57C00",      # 濃いオレンジ（警告）
    "danger": "#D32F2F",       # 赤（エラー）
    "info": "#1976D2",         # 青（情報）
    "test_pass": "#4CAF50",    # 明るい緑（テスト通過）
    "test_fail": "#F44336",    # 明るい赤（テスト失敗）
    "test_pending": "#FF9800", # オレンジ（テスト保留）
    "neutral": "#757575"       # グレー（中立）
}

# テスト資料の章構成
TEST_MATERIAL_CHAPTERS: List[Dict[str, Any]] = [
    {
        "number": 1,
        "title": "システムテスト概要",
        "slug": "system_test_overview",
        "description": "MkDocs Materials Generator の概要と基本機能のテスト",
        "estimated_time": "15分",
        "difficulty": "基本",
        "topics": [
            "システム構成の確認",
            "基本機能の動作確認",
            "設定の妥当性検証"
        ],
        "introduction_template": """
このテスト資料は、MkDocs Materials Generator の動作確認を行うためのサンプルです。
システムの各コンポーネントが正常に動作することを確認します。

!!! info "テストの目的"
    - システムの基本動作を確認する
    - 各モジュールの連携を検証する
    - 出力品質を評価する
""",
        "conclusion_template": """
!!! success "第1章完了"
    システムテスト概要の確認が完了しました。
    次章では図表生成機能のテストを行います。
"""
    },
    {
        "number": 2,
        "title": "図表生成テスト",
        "slug": "chart_generation_test",
        "description": "ChartGeneratorクラスの機能テストとサンプル図表の生成",
        "estimated_time": "20分",
        "difficulty": "基本",
        "topics": [
            "折れ線グラフの生成",
            "棒グラフの生成",
            "円グラフの生成",
            "インタラクティブ図表の生成"
        ],
        "introduction_template": """
この章では、ChartGeneratorクラスの機能をテストし、
様々な種類の図表を生成して動作確認を行います。

!!! tip "図表生成のポイント"
    - Matplotlib/Seaborn と Plotly の両方をサポート
    - 日本語フォント対応
    - レスポンシブデザイン対応
""",
        "conclusion_template": """
!!! success "第2章完了"
    図表生成機能のテストが完了しました。
    次章では表生成機能のテストを行います。
"""
    },
    {
        "number": 3,
        "title": "表生成テスト",
        "slug": "table_generation_test",
        "description": "TableGeneratorクラスの機能テストとサンプル表の生成",
        "estimated_time": "15分",
        "difficulty": "基本",
        "topics": [
            "基本テーブルの生成",
            "比較テーブルの生成",
            "スタイル付きテーブルの生成",
            "レスポンシブテーブルの生成"
        ],
        "introduction_template": """
この章では、TableGeneratorクラスの機能をテストし、
様々な形式の表を生成して動作確認を行います。

!!! tip "表生成のポイント"
    - HTMLテーブルとして出力
    - カスタムスタイル対応
    - レスポンシブデザイン対応
""",
        "conclusion_template": """
!!! success "第3章完了"
    表生成機能のテストが完了しました。
    次章では用語管理機能のテストを行います。
"""
    },
    {
        "number": 4,
        "title": "用語管理テスト",
        "slug": "knowledge_management_test",
        "description": "KnowledgeManagerクラスの機能テストと用語集の生成",
        "estimated_time": "10分",
        "difficulty": "基本",
        "topics": [
            "用語の登録と管理",
            "カテゴリ別分類",
            "用語集の生成",
            "ツールチップ機能"
        ],
        "introduction_template": """
この章では、KnowledgeManagerクラスの機能をテストし、
専門用語の管理と用語集生成の動作確認を行います。

!!! tip "用語管理のポイント"
    - 用語の一元管理
    - カテゴリ別の整理
    - 自動ツールチップ生成
""",
        "conclusion_template": """
!!! success "第4章完了"
    用語管理機能のテストが完了しました。
    次章では統合テストを行います。
"""
    },
    {
        "number": 5,
        "title": "統合テスト",
        "slug": "integration_test",
        "description": "全機能の統合テストと最終確認",
        "estimated_time": "10分",
        "difficulty": "基本",
        "topics": [
            "全機能の統合動作確認",
            "パフォーマンステスト",
            "出力品質の評価",
            "エラーハンドリングの確認"
        ],
        "introduction_template": """
この章では、システム全体の統合テストを行い、
各機能が連携して正常に動作することを確認します。

!!! warning "統合テストの注意点"
    - 全機能を組み合わせた動作確認
    - エラー発生時の対応確認
    - 出力品質の最終評価
""",
        "conclusion_template": """
!!! success "統合テスト完了"
    全機能の統合テストが正常に完了しました。
    システムは正常に動作しています。
"""
    }
]

# テスト資料のカスタム図表スタイル
TEST_CHART_STYLES: Dict[str, Any] = {
    "font_family": ["Meiryo", "Yu Gothic", "Hiragino Sans", "sans-serif"],
    "font_size_title": 16,
    "font_size_axis": 12,
    "font_size_legend": 10,
    "figure_dpi": 100,
    "figsize": (10, 6),
    "transparent_bg": True,
    "grid_alpha": 0.3,
    "line_width": 2.5,
    "marker_size": 8,
    "colors": [
        TEST_MATERIAL_COLORS["test_pass"],
        TEST_MATERIAL_COLORS["test_fail"],
        TEST_MATERIAL_COLORS["test_pending"],
        TEST_MATERIAL_COLORS["info"],
        TEST_MATERIAL_COLORS["warning"],
        TEST_MATERIAL_COLORS["neutral"]
    ]
}

# テスト資料のカスタム表スタイル
TEST_TABLE_STYLES: Dict[str, Any] = {
    "class_name": "test-table",
    "header_bg_color": TEST_MATERIAL_COLORS["primary"],
    "header_text_color": "#ffffff",
    "row_even_bg_color": "#f8f9fa",
    "row_odd_bg_color": "#ffffff",
    "border_color": "#dee2e6",
    "border_width": "1px",
    "cell_padding": "10px 15px",
    "font_size": "14px",
    "font_family": '"Roboto", "Helvetica", "Arial", sans-serif',
    "border_radius": "6px",
    "box_shadow": "0 2px 8px rgba(0,0,0,0.1)"
}

# テスト用サンプルデータ
TEST_SAMPLE_DATA: Dict[str, Any] = {
    "line_chart_data": {
        "x": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "y": [2, 4, 6, 8, 10, 12, 14, 16, 18, 20],
        "title": "線形関数のテスト",
        "xlabel": "X軸",
        "ylabel": "Y軸"
    },
    "bar_chart_data": {
        "categories": ["テスト1", "テスト2", "テスト3", "テスト4", "テスト5"],
        "values": [85, 92, 78, 96, 89],
        "title": "テスト結果の比較",
        "xlabel": "テスト項目",
        "ylabel": "スコア"
    },
    "pie_chart_data": {
        "labels": ["成功", "失敗", "保留", "スキップ"],
        "values": [75, 15, 8, 2],
        "title": "テスト結果の分布"
    },
    "table_data": {
        "headers": ["機能", "テスト結果", "実行時間", "備考"],
        "rows": [
            ["図表生成", "✅ 成功", "0.5秒", "正常動作"],
            ["表生成", "✅ 成功", "0.3秒", "正常動作"],
            ["用語管理", "✅ 成功", "0.2秒", "正常動作"],
            ["文書生成", "✅ 成功", "0.4秒", "正常動作"],
            ["統合テスト", "✅ 成功", "1.2秒", "全機能正常"]
        ]
    },
    "comparison_data": {
        "categories": ["処理速度", "メモリ使用量", "出力品質", "安定性"],
        "items": ["Ver 1.0", "Ver 1.1", "Ver 1.2"],
        "data": [
            [85, 78, 92, 88],  # Ver 1.0
            [90, 82, 94, 91],  # Ver 1.1
            [95, 88, 96, 93]   # Ver 1.2
        ]
    }
}

# テスト実行設定
TEST_EXECUTION_CONFIG: Dict[str, Any] = {
    "run_chart_tests": True,
    "run_table_tests": True,
    "run_knowledge_tests": True,
    "run_integration_tests": True,
    "generate_performance_report": True,
    "cleanup_after_test": False,
    "verbose_output": True
}

def get_test_config() -> Dict[str, Any]:
    """
    テスト設定を取得
    
    Returns:
        テスト設定辞書
    """
    return TEST_MATERIAL_CONFIG

def get_test_colors() -> Dict[str, str]:
    """
    テスト用カラーパレットを取得
    
    Returns:
        カラー辞書
    """
    return TEST_MATERIAL_COLORS

def get_test_chart_styles() -> Dict[str, Any]:
    """
    テスト用図表スタイルを取得
    
    Returns:
        図表スタイル辞書
    """
    return TEST_CHART_STYLES

def get_test_table_styles() -> Dict[str, Any]:
    """
    テスト用表スタイルを取得
    
    Returns:
        表スタイル辞書
    """
    return TEST_TABLE_STYLES

def get_test_chapters() -> List[Dict[str, Any]]:
    """
    テスト資料の章構成を取得
    
    Returns:
        章構成リスト
    """
    return TEST_MATERIAL_CHAPTERS

def get_sample_data() -> Dict[str, Any]:
    """
    テスト用サンプルデータを取得
    
    Returns:
        サンプルデータ辞書
    """
    return TEST_SAMPLE_DATA

def get_execution_config() -> Dict[str, Any]:
    """
    テスト実行設定を取得
    
    Returns:
        実行設定辞書
    """
    return TEST_EXECUTION_CONFIG
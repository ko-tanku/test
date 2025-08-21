"""
テスト資料用の表生成ロジック
core.table_generatorの機能を網羅的にテスト
"""

from pathlib import Path
from typing import Dict

from src.core.table_generator import TableGenerator


def create_all_test_tables(table_gen: TableGenerator, output_base_path: Path) -> Dict[str, Path]:
    """
    テスト用の全表を生成
    
    Args:
        table_gen: TableGeneratorインスタンス
        output_base_path: 出力先ベースパス
        
    Returns:
        生成されたファイルパスの辞書
    """
    generated_files = {}
    
    # 出力ディレクトリの作成
    tables_dir = output_base_path
    tables_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. 基本的な表
    headers = ["項目", "説明", "重要度"]
    rows = [
        ["MkDocs", "静的サイトジェネレータ", "高"],
        ["Markdown", "軽量マークアップ言語", "高"],
        ["Python", "プログラミング言語", "中"],
        ["HTML", "ウェブページ記述言語", "低"]
    ]
    
    file_path = tables_dir / table_gen.create_basic_table(
        headers, rows,
        "基本的なツール一覧",
        "basic_tools_table.html",
        output_dir=tables_dir
    )
    generated_files["basic_table"] = file_path
    
    # 2. 比較表
    categories = ["MkDocs", "Sphinx", "Jekyll"]
    items = ["言語", "設定の簡単さ", "テーマの豊富さ", "拡張性", "学習曲線"]
    data = [
        ["Python", "Python", "Ruby"],
        ["★★★★★", "★★★", "★★★★"],
        ["★★★★", "★★★★★", "★★★★★"],
        ["★★★", "★★★★★", "★★★★"],
        ["緩やか", "急", "中程度"]
    ]
    
    file_path = tables_dir / table_gen.create_comparison_table(
        categories, items, data,
        "静的サイトジェネレータ比較",
        "ssg_comparison_table.html",
        output_dir=tables_dir
    )
    generated_files["comparison_table"] = file_path
    
    # 3. カスタムスタイルの表（セル背景色）
    headers = ["ステータス", "タスク", "担当者", "期限"]
    rows = [
        ["完了", "ドキュメント作成", "田中", "2024/01/15"],
        ["進行中", "レビュー", "佐藤", "2024/01/20"],
        ["未着手", "テスト実装", "鈴木", "2024/01/25"],
        ["遅延", "デプロイ準備", "山田", "2024/01/10"]
    ]
    
    # カスタムスタイル（ステータスに応じた色分け）
    custom_styles = {
        "header_bg_color": "#2196F3",
        "row_even_bg_color": "#F5F5F5",
        "row_odd_bg_color": "#FAFAFA"
    }
    
    file_path = tables_dir / table_gen.create_basic_table(
        headers, rows,
        "プロジェクトタスク管理表",
        "project_tasks_table.html",
        custom_styles,
        output_dir=tables_dir
    )
    generated_files["styled_table"] = file_path
    
    # 4. 幅の広い表（横スクロール対応）
    wide_headers = ["ID"] + [f"列{i+1}" for i in range(20)]
    wide_rows = []
    for i in range(10):
        row = [f"行{i+1}"] + [f"データ{i+1}-{j+1}" for j in range(20)]
        wide_rows.append(row)
    
    file_path = tables_dir / table_gen.create_basic_table(
        wide_headers, wide_rows,
        "横スクロール対応の幅広表",
        "wide_scrollable_table.html",
        output_dir=tables_dir
    )
    generated_files["wide_table"] = file_path
    
    # 5. 数値データの表（右寄せスタイル）
    headers = ["月", "売上（万円）", "前年比（%）", "累計（万円）"]
    rows = [
        ["1月", "1,234", "+5.2", "1,234"],
        ["2月", "1,456", "+8.7", "2,690"],
        ["3月", "1,789", "+12.3", "4,479"],
        ["4月", "1,567", "-2.1", "6,046"],
        ["5月", "1,890", "+15.6", "7,936"],
        ["6月", "2,123", "+18.9", "10,059"]
    ]
    
    custom_styles = {
        "font_family": "monospace"
    }
    
    file_path = tables_dir / table_gen.create_basic_table(
        headers, rows,
        "月次売上データ",
        "monthly_sales_table.html",
        custom_styles,
        output_dir=tables_dir
    )
    generated_files["numeric_table"] = file_path
    
    # 6. アイコンを含む表（HTMLエンティティ使用）
    headers = ["機能", "説明", "ステータス"]
    rows = [
        ["✅ Markdown対応", "Markdownファイルから自動生成", "実装済み"],
        ["⚡ 高速ビルド", "インクリメンタルビルドに対応", "実装済み"],
        ["🎨 テーマ対応", "Material Designテーマを使用", "実装済み"],
        ["🔍 検索機能", "全文検索に対応", "計画中"],
        ["📱 レスポンシブ", "モバイル端末に最適化", "テスト中"]
    ]
    
    file_path = tables_dir / table_gen.create_basic_table(
        headers, rows,
        "機能一覧（アイコン付き）",
        "features_with_icons_table.html",
        output_dir=tables_dir
    )
    generated_files["icon_table"] = file_path
    
    return generated_files
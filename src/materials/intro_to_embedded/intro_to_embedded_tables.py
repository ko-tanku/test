"""
組込制御入門の表データ定義
"""

from pathlib import Path
from typing import Dict

from src.core.table_generator import TableGenerator


def create_all_intro_tables(table_gen: TableGenerator, output_base_path: Path) -> Dict[str, Path]:
    """
    組込制御入門用の全表を生成

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

    # ITシステムと組み込みシステムの比較表
    categories = ["ITシステム", "組み込みシステム"]
    items = ["目的", "汎用性/特定用途", "リアルタイム性", "主な開発環境", "代表例"]
    data = [
        ["情報処理・データ管理", "特定機能の制御"],
        ["汎用的（様々な用途）", "特定用途に特化"],
        ["必須ではない", "多くの場合必須"],
        ["PC、クラウド環境", "専用開発ボード、実機"],
        ["PC、スマホ、Webサービス", "家電、自動車、医療機器"]
    ]

    file_path = tables_dir / table_gen.create_comparison_table(
        categories, items, data,
        "ITシステムと組み込みシステムの比較",
        "it_embedded_comparison.html",
        output_dir=tables_dir
    )
    generated_files["it_embedded_comparison"] = file_path

    return generated_files
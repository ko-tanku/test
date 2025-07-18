"""
Test Material Tables
テスト資料で使用する表の生成
"""

import sys
from pathlib import Path
import logging
from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np

# プロジェクトルートをsys.pathに追加
project_root = Path(__file__).resolve().parents[3]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.core.table_generator import TableGenerator
from src.core.config import PATHS
from test_material_config import get_test_colors, get_test_table_styles

logger = logging.getLogger(__name__)


class TestMaterialTables:
    """
    テスト資料用の表生成クラス
    """

    def __init__(self):
        """
        初期化
        """
        # テスト用の設定を取得
        self.colors = get_test_colors()
        self.table_styles = get_test_table_styles()

        # 出力ディレクトリを設定
        self.output_dir = PATHS["test_material_tables_dir"]

        # TableGeneratorを初期化
        self.table_generator = TableGenerator(self.colors, self.table_styles)

        # 出力先を変更
        self.table_generator.output_dir = self.output_dir

        self.logger = logging.getLogger(__name__ + ".TestMaterialTables")

    def generate_basic_table_test(self) -> Path:
        """
        基本テーブルのテストを生成

        Returns:
            生成されたファイルのパス
        """
        try:
            headers = ["機能", "テスト結果", "実行時間", "備考"]
            rows = [
                ["図表生成", "✅ 成功", "0.5秒", "正常動作"],
                ["表生成", "✅ 成功", "0.3秒", "正常動作"],
                ["用語管理", "✅ 成功", "0.2秒", "正常動作"],
                ["文書生成", "✅ 成功", "0.4秒", "正常動作"],
                ["統合テスト", "✅ 成功", "1.2秒", "全機能正常"]
            ]

            output_path = self.table_generator.create_basic_table(
                headers=headers,
                rows=rows,
                title="基本機能テスト結果",
                output_filename="test_basic_table.html"
            )

            self.logger.info(f"Basic table test generated: {output_path}")

            return output_path

        except Exception as e:
            self.logger.error(f"Failed to generate basic table test: {e}")
            raise

    def generate_comparison_table_test(self) -> Path:
        """
        比較テーブルのテストを生成

        Returns:
            生成されたファイルのパス
        """
        try:
            categories = ["処理速度", "メモリ使用量", "出力品質", "安定性"]
            items = ["Ver 1.0", "Ver 1.1", "Ver 1.2"]
            data = [
                [85, 78, 92, 88],  # Ver 1.0
                [90, 82, 94, 91],  # Ver 1.1
                [95, 88, 96, 93]   # Ver 1.2
            ]

            output_path = self.table_generator.create_comparison_table(
                categories=categories,
                items=items,
                data=data,
                title="バージョン別性能比較",
                output_filename="test_comparison_table.html"
            )

            self.logger.info(f"Comparison table test generated: {output_path}")

            return output_path

        except Exception as e:
            self.logger.error(f"Failed to generate comparison table test: {e}")
            raise

    def generate_styled_table_test(self) -> Path:
        """
        スタイル付きテーブルのテストを生成

        Returns:
            生成されたファイルのパス
        """
        try:
            # テストデータを作成
            data = {
                "テスト項目": ["単体テスト", "統合テスト", "性能テスト", "セキュリティテスト", "負荷テスト"],
                "実行数": [150, 45, 20, 15, 10],
                "成功": [145, 42, 18, 15, 9],
                "失敗": [5, 3, 2, 0, 1],
                "成功率": ["96.7%", "93.3%", "90.0%", "100.0%", "90.0%"]
            }

            df = pd.DataFrame(data)

            # スタイル設定
            style_config = {
                "highlight_rows": [3],  # セキュリティテストをハイライト
                "highlight_cols": ["成功率"],
                "cell_colors": {
                    (1, "失敗"): self.colors.get("test_fail", "#ff5252"),
                    (3, "成功率"): self.colors.get("test_pass", "#4caf50")
                }
            }

            output_path = self.table_generator.create_styled_table(
                df=df,
                title="テスト結果サマリー（スタイル付き）",
                output_filename="test_styled_table.html",
                style_config=style_config
            )

            self.logger.info(f"Styled table test generated: {output_path}")

            return output_path

        except Exception as e:
            self.logger.error(f"Failed to generate styled table test: {e}")
            raise

    def generate_data_table_test(self) -> Path:
        """
        データテーブル（検索・ソート機能付き）のテストを生成

        Returns:
            生成されたファイルのパス
        """
        try:
            # 大量データのサンプルを作成
            np.random.seed(42)

            modules = ["core.base_config", "core.config", "core.utils", "core.document_builder",
                      "core.chart_generator", "core.table_generator", "core.knowledge_manager",
                      "core.content_manager", "materials.test_material"]

            data = []
            for i in range(50):
                module = np.random.choice(modules)
                test_type = np.random.choice(["Unit", "Integration", "Performance", "Security"])
                status = np.random.choice(["Pass", "Fail", "Skip"], p=[0.8, 0.15, 0.05])
                duration = round(np.random.uniform(0.1, 5.0), 2)

                data.append({
                    "ID": f"T{i+1:03d}",
                    "モジュール": module,
                    "テスト種類": test_type,
                    "ステータス": status,
                    "実行時間": f"{duration}s",
                    "実行日時": pd.Timestamp.now() - pd.Timedelta(hours=np.random.randint(0, 24))
                })

            output_path = self.table_generator.create_data_table(
                data=data,
                title="テスト実行履歴（検索・ソート機能付き）",
                output_filename="test_data_table.html",
                sortable=True,
                searchable=True
            )

            self.logger.info(f"Data table test generated: {output_path}")

            return output_path

        except Exception as e:
            self.logger.error(f"Failed to generate data table test: {e}")
            raise

    def generate_responsive_table_test(self) -> Path:
        """
        レスポンシブテーブルのテストを生成

        Returns:
            生成されたファイルのパス
        """
        try:
            # モバイル対応を想定したテーブルデータ
            headers = ["項目", "説明", "状態"]
            rows = [
                ["レスポンシブ対応", "画面サイズに応じて表示を最適化", "✅"],
                ["タッチ操作", "タッチデバイスでの操作に対応", "✅"],
                ["横スクロール", "必要に応じて横スクロール可能", "✅"],
                ["フォントサイズ", "小画面でも読みやすいサイズに調整", "✅"],
                ["パフォーマンス", "モバイルでも高速に動作", "✅"]
            ]

            output_path = self.table_generator.create_basic_table(
                headers=headers,
                rows=rows,
                title="レスポンシブデザイン対応状況",
                output_filename="test_responsive_table.html",
                custom_styles={
                    "font_size": "16px",  # モバイル向けに大きめ
                    "cell_padding": "12px 16px"
                }
            )

            self.logger.info(f"Responsive table test generated: {output_path}")

            return output_path

        except Exception as e:
            self.logger.error(f"Failed to generate responsive table test: {e}")
            raise

    def generate_all_table_tests(self) -> List[Path]:
        """
        全ての表テストを生成

        Returns:
            生成されたファイルのパスリスト
        """
        generated_files = []

        try:
            # 各種テーブルを生成
            generated_files.append(self.generate_basic_table_test())
            generated_files.append(self.generate_comparison_table_test())
            generated_files.append(self.generate_styled_table_test())
            generated_files.append(self.generate_data_table_test())
            generated_files.append(self.generate_responsive_table_test())

            self.logger.info(f"All table tests generated: {len(generated_files)} files")

            return generated_files

        except Exception as e:
            self.logger.error(f"Failed to generate all table tests: {e}")
            raise
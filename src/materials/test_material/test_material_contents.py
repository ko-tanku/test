"""
Test Material Contents
テスト資料のコンテンツ生成とテスト
"""

import sys
from pathlib import Path
import logging
from typing import Dict, List, Any, Optional
import pandas as pd

# プロジェクトルートをsys.pathに追加
project_root = Path(__file__).resolve().parents[3]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.core.content_manager import BaseContentManager
from src.core.config import PATHS
from test_material_config import (
    get_test_config, get_test_colors, get_test_chart_styles,
    get_test_table_styles, get_test_chapters
)
from test_material_terms import get_test_terms
from test_material_charts import TestMaterialCharts
from test_material_tables import TestMaterialTables

logger = logging.getLogger(__name__)


class TestMaterialContentManager(BaseContentManager):
    """
    テスト資料のコンテンツ生成を管理するクラス
    """

    def __init__(self):
        """
        初期化
        """
        # 設定を取得
        config = get_test_config()
        colors = get_test_colors()
        chart_styles = get_test_chart_styles()
        table_styles = get_test_table_styles()

        # 基底クラスを初期化
        super().__init__(
            material_name=config["material_name"],
            output_base_dir=PATHS["test_material_dir"],
            colors=colors,
            chart_styles=chart_styles,
            table_styles=table_styles
        )

        # テスト用のコンポーネントを初期化
        self.test_charts = TestMaterialCharts()
        self.test_tables = TestMaterialTables()

        # 章構成を取得
        self.chapters = get_test_chapters()

        # 専門用語を登録
        self._register_material_terms(get_test_terms())

        self.logger = logging.getLogger(__name__ + ".TestMaterialContentManager")

    def _generate_chapter_1_content(self, doc_builder, chapter_info: Dict[str, Any], context: Dict[str, Any]) -> None:
        """
        第1章「システムテスト概要」のコンテンツを生成

        Args:
            doc_builder: DocumentBuilderインスタンス
            chapter_info: 章情報
            context: テンプレートコンテキスト
        """
        try:
            # システム概要の説明
            doc_builder.add_heading("システム構成", 2)

            system_overview = """
MkDocs Materials Generator は以下のコンポーネントで構成されています：

- **DocumentBuilder**: Markdownコンテンツの構築
- **ChartGenerator**: 図表の生成とHTML出力
- **TableGenerator**: 表データの生成とHTML出力
- **KnowledgeManager**: 専門用語の管理と用語集生成
- **ContentManager**: コンテンツ生成の統合管理
"""

            doc_builder.add_paragraph_with_tooltips(system_overview, context["terms"])

            # 基本機能のテスト
            doc_builder.add_heading("基本機能テスト", 2)

            # システム情報テーブル
            system_info = [
                ["項目", "値"],
                ["システム名", "MkDocs Materials Generator"],
                ["バージョン", "1.0.0"],
                ["言語", "Python 3.8+"],
                ["ライセンス", "MIT"],
                ["作者", "MkDocs Materials Generator Team"]
            ]

            doc_builder.add_table(system_info[0], system_info[1:])

            # 設定の妥当性確認
            doc_builder.add_heading("設定確認", 2)

            doc_builder.add_admonition(
                "info",
                "設定状態",
                f"""
**プロジェクトルート**: {PATHS['project_root']}
**ドキュメントディレクトリ**: {PATHS['docs_dir']}
**アセットディレクトリ**: {PATHS['assets_dir']}
**テスト資料ディレクトリ**: {PATHS['test_material_dir']}
"""
            )

            # 依存関係の確認
            doc_builder.add_heading("依存関係確認", 2)

            dependencies = [
                "MkDocs", "Material for MkDocs", "pandas", "numpy",
                "matplotlib", "seaborn", "plotly", "PyYAML"
            ]

            doc_builder.add_paragraph("システムは以下の外部ライブラリに依存しています：")
            doc_builder.add_unordered_list(dependencies)

        except Exception as e:
            self.logger.error(f"Failed to generate chapter 1 content: {e}")
            raise

    def _generate_chapter_2_content(self, doc_builder, chapter_info: Dict[str, Any], context: Dict[str, Any]) -> None:
        """
        第2章「図表生成テスト」のコンテンツを生成

        Args:
            doc_builder: DocumentBuilderインスタンス
            chapter_info: 章情報
            context: テンプレートコンテキスト
        """
        try:
            # 図表生成機能の説明
            doc_builder.add_heading("図表生成機能", 2)

            chart_description = """
ChartGenerator クラスは以下の機能を提供します：

- **折れ線グラフ**: 時系列データの可視化に適用
- **棒グラフ**: カテゴリ別データの比較に適用
- **円グラフ**: 全体に対する割合の表示に適用
- **カスタム図表**: 独自の描画ロジックによる図表生成
- **インタラクティブ図表**: Plotlyによる動的な図表生成
"""

            doc_builder.add_paragraph_with_tooltips(chart_description, context["terms"])

            # 図表生成テストの実行
            doc_builder.add_heading("図表生成テスト実行", 2)

            doc_builder.add_paragraph("以下の図表を生成してテストを実行します：")

            # テスト図表を生成
            try:
                # 折れ線グラフ
                doc_builder.add_heading("折れ線グラフテスト", 3)
                line_chart_path = self.test_charts.generate_line_chart_test()
                doc_builder.add_html_component_reference(line_chart_path)

                # 棒グラフ
                doc_builder.add_heading("棒グラフテスト", 3)
                bar_chart_path = self.test_charts.generate_bar_chart_test()
                doc_builder.add_html_component_reference(bar_chart_path)

                # 円グラフ
                doc_builder.add_heading("円グラフテスト", 3)
                pie_chart_path = self.test_charts.generate_pie_chart_test()
                doc_builder.add_html_component_reference(pie_chart_path)

                # インタラクティブ図表
                doc_builder.add_heading("インタラクティブ図表テスト", 3)
                interactive_chart_path = self.test_charts.generate_interactive_chart_test()
                doc_builder.add_html_component_reference(interactive_chart_path, height="500px")

                # カスタム図表
                doc_builder.add_heading("カスタム図表テスト", 3)
                custom_chart_path = self.test_charts.generate_custom_figure_test()
                doc_builder.add_html_component_reference(custom_chart_path)

            except Exception as e:
                self.logger.error(f"Chart generation failed: {e}")
                doc_builder.add_admonition(
                    "danger",
                    "エラー",
                    f"図表生成中にエラーが発生しました: {e}"
                )

        except Exception as e:
            self.logger.error(f"Failed to generate chapter 2 content: {e}")
            raise

    def _generate_chapter_3_content(self, doc_builder, chapter_info: Dict[str, Any], context: Dict[str, Any]) -> None:
        """
        第3章「表生成テスト」のコンテンツを生成

        Args:
            doc_builder: DocumentBuilderインスタンス
            chapter_info: 章情報
            context: テンプレートコンテキスト
        """
        try:
            # 表生成機能の説明
            doc_builder.add_heading("表生成機能", 2)

            table_description = """
TableGenerator クラスは以下の機能を提供します：

- **基本テーブル**: シンプルなデータ表示
- **比較テーブル**: 複数項目の比較表示
- **スタイル付きテーブル**: カスタムスタイルの適用
- **データテーブル**: 検索・ソート機能付き
- **レスポンシブテーブル**: モバイル対応表示
"""

            doc_builder.add_paragraph_with_tooltips(table_description, context["terms"])

            # 表生成テストの実行
            doc_builder.add_heading("表生成テスト実行", 2)

            # テスト表を生成
            try:
                # 基本テーブル
                doc_builder.add_heading("基本テーブルテスト", 3)
                basic_table_path = self.test_tables.generate_basic_table_test()
                doc_builder.add_html_component_reference(basic_table_path, height="300px")

                # 比較テーブル
                doc_builder.add_heading("比較テーブルテスト", 3)
                comparison_table_path = self.test_tables.generate_comparison_table_test()
                doc_builder.add_html_component_reference(comparison_table_path, height="300px")

                # スタイル付きテーブル
                doc_builder.add_heading("スタイル付きテーブルテスト", 3)
                styled_table_path = self.test_tables.generate_styled_table_test()
                doc_builder.add_html_component_reference(styled_table_path, height="350px")

                # データテーブル
                doc_builder.add_heading("データテーブルテスト", 3)
                data_table_path = self.test_tables.generate_data_table_test()
                doc_builder.add_html_component_reference(data_table_path, height="600px")

            except Exception as e:
                self.logger.error(f"Table generation failed: {e}")
                doc_builder.add_admonition(
                    "danger",
                    "エラー",
                    f"表生成中にエラーが発生しました: {e}"
                )

        except Exception as e:
            self.logger.error(f"Failed to generate chapter 3 content: {e}")
            raise

    def _generate_chapter_4_content(self, doc_builder, chapter_info: Dict[str, Any], context: Dict[str, Any]) -> None:
        """
        第4章「用語管理テスト」のコンテンツを生成

        Args:
            doc_builder: DocumentBuilderインスタンス
            chapter_info: 章情報
            context: テンプレートコンテキスト
        """
        try:
            # 用語管理機能の説明
            doc_builder.add_heading("用語管理機能", 2)

            knowledge_description = """
KnowledgeManager クラスは以下の機能を提供します：

- **用語の登録**: 専門用語とその定義の管理
- **カテゴリ分類**: 用語をカテゴリ別に整理
- **関連用語**: 用語間の関連性を定義
- **用語集生成**: 自動的に用語集を生成
- **ツールチップ**: 本文中の用語にツールチップを付与
"""

            doc_builder.add_paragraph_with_tooltips(knowledge_description, context["terms"])

            # 登録済み用語の統計
            doc_builder.add_heading("用語統計", 2)

            stats = self.knowledge_manager.get_term_statistics()

            stats_table = [
                ["項目", "値"],
                ["総用語数", f"{stats['total_terms']}語"],
                ["カテゴリ数", f"{len(stats['categories'])}カテゴリ"],
                ["平均定義長", f"{stats['average_definition_length']:.1f}文字"],
                ["関連用語あり", f"{stats['terms_with_related']}語"]
            ]

            doc_builder.add_table(stats_table[0], stats_table[1:])

            # カテゴリ別用語数
            doc_builder.add_heading("カテゴリ別用語数", 3)

            category_data = []
            for category, count in stats['categories'].items():
                category_data.append([category, f"{count}語"])

            if category_data:
                doc_builder.add_table(["カテゴリ", "用語数"], category_data)

            # 用語の検証
            doc_builder.add_heading("用語検証", 2)

            validation_errors = self.knowledge_manager.validate_terms()

            if validation_errors:
                doc_builder.add_admonition(
                    "warning",
                    "検証エラー",
                    "\n".join(f"- {error}" for error in validation_errors)
                )
            else:
                doc_builder.add_admonition(
                    "success",
                    "検証成功",
                    "すべての用語が正しく登録されています。"
                )

        except Exception as e:
            self.logger.error(f"Failed to generate chapter 4 content: {e}")
            raise

    def _generate_chapter_5_content(self, doc_builder, chapter_info: Dict[str, Any], context: Dict[str, Any]) -> None:
        """
        第5章「統合テスト」のコンテンツを生成

        Args:
            doc_builder: DocumentBuilderインスタンス
            chapter_info: 章情報
            context: テンプレートコンテキスト
        """
        try:
            # 統合テストの説明
            doc_builder.add_heading("統合テスト概要", 2)

            integration_description = """
                統合テストでは、すべてのコンポーネントが協調して動作することを確認します：

                - **コンテンツ生成**: 各章のMarkdownファイルが正しく生成される
                - **図表埋め込み**: 生成された図表が正しく表示される
                - **表埋め込み**: 生成された表が正しく表示される
                - **用語ツールチップ**: 専門用語のツールチップが機能する
                - **ナビゲーション**: 章間のリンクが正しく機能する
                """

            doc_builder.add_paragraph_with_tooltips(integration_description, context["terms"])

            # 統合テスト結果
            doc_builder.add_heading("テスト結果サマリー", 2)

            # タブ形式でテスト結果を表示
            test_results = {
                "成功したテスト": """
                - ✅ Markdownファイル生成
                - ✅ 図表HTML生成
                - ✅ 表HTML生成
                - ✅ 用語集生成
                - ✅ ツールチップ機能
                - ✅ ナビゲーションリンク
                """,
                                "注意が必要な項目": """
                - ⚠️ 日本語フォントの設定（環境依存）
                - ⚠️ 大量データの処理速度
                - ⚠️ ブラウザ互換性（IE非対応）
                """,
                                "今後の改善点": """
                - 📌 PDF出力機能の追加
                - 📌 テーマカスタマイズ機能
                - 📌 多言語対応
                - 📌 バージョン管理機能
                """
            }

            doc_builder.add_tabbed_block(test_results)

            # パフォーマンステスト結果
            doc_builder.add_heading("パフォーマンステスト", 2)

            perf_data = [
                ["処理内容", "実行時間", "メモリ使用量"],
                ["Markdown生成", "0.2秒", "15MB"],
                ["図表生成（6種類）", "3.5秒", "120MB"],
                ["表生成（5種類）", "1.8秒", "45MB"],
                ["用語集生成", "0.5秒", "20MB"],
                ["全体処理", "6.0秒", "200MB"]
            ]

            doc_builder.add_table(perf_data[0], perf_data[1:])

            # 最終確認
            doc_builder.add_heading("最終確認", 2)

            doc_builder.add_admonition(
                "success",
                "テスト完了",
                """
                すべての統合テストが正常に完了しました。
                MkDocs Materials Generator は正常に動作しています。

                生成された資料は以下のコマンドでプレビューできます：
                ```bash
                mkdocs serve
                """
                )
        except Exception as e:
            self.logger.error(f"Failed to generate chapter 5 content: {e}")
            raise

    def generate_content(self) -> List[Path]:
        """
        テスト資料全体のコンテンツを生成

        Returns:
            生成されたファイルのパスリスト
        """
        generated_files = []

        try:
            self.logger.info("Starting test material content generation...")

            # 出力ディレクトリをクリーンアップ
            self.cleanup_output_directory()

            # 各章のコンテンツを生成
            chapter_functions = {
                1: self._generate_chapter_1_content,
                2: self._generate_chapter_2_content,
                3: self._generate_chapter_3_content,
                4: self._generate_chapter_4_content,
                5: self._generate_chapter_5_content
            }

            # 章ごとに処理
            for i, chapter_info in enumerate(self.chapters):
                chapter_num = chapter_info.get("number", i + 1)

                # 次章の情報を追加
                if i < len(self.chapters) - 1:
                    chapter_info['next_chapter'] = self.chapters[i + 1]

                # 章生成関数を取得
                chapter_func = chapter_functions.get(chapter_num)

                if chapter_func:
                    try:
                        # 章を生成
                        chapter_path = self._create_chapter_template(
                            chapter_info,
                            chapter_func
                        )
                        generated_files.append(chapter_path)

                    except Exception as e:
                        self.logger.error(f"Failed to generate chapter {chapter_num}: {e}")
                        raise
                else:
                    self.logger.warning(f"No generation function for chapter {chapter_num}")

            # 目次ページを生成
            index_path = self.create_index_page(self.chapters)
            generated_files.append(index_path)

            # 用語集を生成
            glossary_path = self.generate_glossary()
            generated_files.append(glossary_path)

            # コンテンツの検証
            validation_errors = self.validate_content()
            if validation_errors:
                self.logger.warning(f"Validation errors: {validation_errors}")

            self.logger.info(f"Test material generation completed. Generated {len(generated_files)} files.")

            return generated_files

        except Exception as e:
            self.logger.error(f"Failed to generate test material content: {e}")
            raise
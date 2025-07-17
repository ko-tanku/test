"""
Test Material Tables
テスト資料で使用する表の生成とテスト
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
from .test_material_config import (
    get_test_colors, get_test_table_styles, get_sample_data
)

logger = logging.getLogger(__name__)


class TestMaterialTables:
    """
    テスト資料用の表生成とテストを行うクラス
    """
    
    def __init__(self):
        """
        初期化
        """
        # テスト用の設定を取得
        self.colors = get_test_colors()
        self.styles = get_test_table_styles()
        self.sample_data = get_sample_data()
        
        # TableGeneratorを初期化
        self.table_generator = TableGenerator(self.colors, self.styles)
        
        # 出力ディレクトリを設定
        self.output_dir = PATHS["test_material_tables_dir"]
        
        self.logger = logging.getLogger(__name__ + ".TestMaterialTables")
    
    def generate_basic_table_test(self) -> Path:
        """
        基本テーブルのテストを生成
        
        Returns:
            生成されたファイルのパス
        """
        try:
            data = self.sample_data["table_data"]
            
            output_path = self.table_generator.create_basic_table(
                headers=data["headers"],
                rows=data["rows"],
                title="基本テーブルテスト",
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
            data = self.sample_data["comparison_data"]
            
            # データの次元を確認してログ出力
            self.logger.info(f"Categories: {len(data['categories'])}")
            self.logger.info(f"Items: {len(data['items'])}")
            self.logger.info(f"Data shape: {len(data['data'])} x {len(data['data'][0]) if data['data'] else 0}")
            
            # データを転置して正しい形式にする
            transposed_data = []
            for i, category in enumerate(data["categories"]):
                row = [category]
                for item_data in data["data"]:
                    row.append(item_data[i])
                transposed_data.append(row)
            
            # ヘッダーを作成
            headers = ["項目"] + data["items"]
            
            output_path = self.table_generator.create_basic_table(
                headers=headers,
                rows=transposed_data,
                title="バージョン比較テーブル",
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
            # テスト結果データを作成
            test_results = {
                "テスト名": ["単体テスト", "統合テスト", "パフォーマンステスト", "セキュリティテスト", "ユーザビリティテスト"],
                "実行数": [150, 45, 20, 35, 25],
                "成功数": [148, 43, 18, 33, 24],
                "失敗数": [2, 2, 2, 2, 1],
                "成功率": ["98.7%", "95.6%", "90.0%", "94.3%", "96.0%"]
            }
            
            df = pd.DataFrame(test_results)
            
            # スタイル設定
            style_config = {
                "font_size": "16px",
                "header_bg_color": self.colors.get('primary', '#2E7D32'),
                "cell_colors": {
                    # 成功率に応じた色分け（将来的に実装予定）
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
            # モバイル表示を考慮したテーブルデータ
            mobile_data = {
                "機能名": ["ドキュメント生成", "図表生成", "表生成", "用語管理", "テンプレート", "設定管理"],
                "ステータス": ["✅ 完了", "✅ 完了", "✅ 完了", "✅ 完了", "🔄 進行中", "📋 計画中"],
                "優先度": ["高", "高", "中", "中", "低", "低"],
                "担当者": ["田中", "佐藤", "鈴木", "田中", "佐藤", "鈴木"],
                "期限": ["2024-01-15", "2024-01-20", "2024-01-25", "2024-01-30", "2024-02-05", "2024-02-10"],
                "進捗": ["100%", "100%", "100%", "100%", "60%", "0%"]
            }
            
            df = pd.DataFrame(mobile_data)
            
            # モバイル表示時は最初の3列のみ表示
            mobile_columns = ["機能名", "ステータス", "優先度"]
            
            output_path = self.table_generator.create_responsive_table(
                df=df,
                title="プロジェクト進捗管理（レスポンシブ対応）",
                output_filename="test_responsive_table.html",
                mobile_columns=mobile_columns
            )
            
            self.logger.info(f"Responsive table test generated: {output_path}")
            
            return output_path
            
        except Exception as e:
            self.logger.error(f"Failed to generate responsive table test: {e}")
            raise
    
    def generate_pivot_table_test(self) -> Path:
        """
        ピボットテーブルのテストを生成
        
        Returns:
            生成されたファイルのパス
        """
        try:
            # ピボットテーブル用のデータを作成
            np.random.seed(42)
            
            data = []
            modules = ["DocumentBuilder", "ChartGenerator", "TableGenerator", "KnowledgeManager"]
            test_types = ["Unit", "Integration", "Performance"]
            
            for module in modules:
                for test_type in test_types:
                    for _ in range(10):
                        execution_time = round(np.random.uniform(0.1, 3.0), 2)
                        data.append({
                            "モジュール": module,
                            "テスト種類": test_type,
                            "実行時間": execution_time
                        })
            
            df = pd.DataFrame(data)
            
            output_path = self.table_generator.create_pivot_table(
                df=df,
                index="モジュール",
                columns="テスト種類", 
                values="実行時間",
                title="モジュール別テスト実行時間（平均）",
                output_filename="test_pivot_table.html",
                aggfunc='mean'
           )
           
            self.logger.info(f"Pivot table test generated: {output_path}")
            
            return output_path
            
        except Exception as e:
            self.logger.error(f"Failed to generate pivot table test: {e}")
            raise
    
    def generate_complex_table_test(self) -> Path:
        """
        複雑なテーブルのテストを生成
        
        Returns:
            生成されたファイルのパス
        """
        try:
            # 複雑なテストレポートデータ
            complex_data = {
                "テストケース": [
                    "TC001: 基本機能テスト",
                    "TC002: エラーハンドリング",
                    "TC003: パフォーマンステスト",
                    "TC004: セキュリティテスト",
                    "TC005: 統合テスト",
                    "TC006: UIテスト",
                    "TC007: APIテスト",
                    "TC008: データベーステスト"
                ],
                "実行結果": [
                    "✅ PASS",
                    "❌ FAIL",
                    "⚠️ WARNING",
                    "✅ PASS",
                    "✅ PASS",
                    "🔄 RUNNING",
                    "✅ PASS",
                    "⏸️ SKIPPED"
                ],
                "実行時間": ["0.5s", "1.2s", "15.3s", "3.7s", "8.9s", "2.1s", "0.8s", "N/A"],
                "CPU使用率": ["12%", "45%", "89%", "23%", "67%", "34%", "18%", "N/A"],
                "メモリ使用量": ["1.2MB", "3.5MB", "15.7MB", "2.1MB", "8.9MB", "4.3MB", "1.8MB", "N/A"],
                "カバレッジ": ["95%", "78%", "N/A", "85%", "92%", "88%", "91%", "N/A"],
                "エラーメッセージ": [
                    "",
                    "Assertion failed: expected 'test' but got 'prod'",
                    "Performance degradation detected",
                    "",
                    "",
                    "Test in progress...",
                    "",
                    "Test skipped due to dependency failure"
                ]
            }
            
            df = pd.DataFrame(complex_data)
            
            # カスタムスタイル設定
            custom_styles = {
                "font_size": "13px",
                "cell_padding": "12px 8px",
                "header_bg_color": self.colors.get('primary', '#2E7D32'),
                "row_even_bg_color": "#f8f9fa",
                "row_odd_bg_color": "#ffffff"
            }
            
            output_path = self.table_generator.create_styled_table(
                df=df,
                title="詳細テストレポート",
                output_filename="test_complex_table.html",
                style_config=custom_styles
            )
            
            self.logger.info(f"Complex table test generated: {output_path}")
            
            return output_path
            
        except Exception as e:
            self.logger.error(f"Failed to generate complex table test: {e}")
            raise
    
    def generate_performance_table_test(self) -> Path:
        """
        パフォーマンステーブルのテストを生成
        
        Returns:
            生成されたファイルのパス
        """
        try:
            # パフォーマンステストデータ
            performance_data = []
            
            functions = [
                "document_builder.add_heading",
                "document_builder.add_paragraph",
                "chart_generator.create_line_chart",
                "chart_generator.create_bar_chart",
                "table_generator.create_basic_table",
                "table_generator.create_comparison_table",
                "knowledge_manager.register_term",
                "knowledge_manager.generate_glossary",
                "content_manager.generate_content"
            ]
            
            for func in functions:
                # 複数回実行した結果をシミュレート
                times = np.random.normal(0.5, 0.1, 10)  # 平均0.5秒、標準偏差0.1秒
                times = np.clip(times, 0.1, 2.0)  # 0.1秒から2.0秒の範囲に制限
                
                performance_data.append({
                    "関数名": func,
                    "平均実行時間": f"{np.mean(times):.3f}s",
                    "最小実行時間": f"{np.min(times):.3f}s",
                    "最大実行時間": f"{np.max(times):.3f}s",
                    "標準偏差": f"{np.std(times):.3f}s",
                    "実行回数": "10回",
                    "成功率": f"{np.random.uniform(95, 100):.1f}%"
                })
            
            df = pd.DataFrame(performance_data)
            
            output_path = self.table_generator.create_data_table(
                data=df.to_dict('records'),
                title="関数別パフォーマンス測定結果",
                output_filename="test_performance_table.html",
                sortable=True,
                searchable=True
            )
            
            self.logger.info(f"Performance table test generated: {output_path}")
            
            return output_path
            
        except Exception as e:
            self.logger.error(f"Failed to generate performance table test: {e}")
            raise
    
    def generate_all_table_tests(self) -> List[Path]:
        """
        全ての表テストを生成
        
        Returns:
            生成されたファイルのパスリスト
        """
        try:
            generated_files = []
            
            self.logger.info("Starting table generation tests...")
            
            # 各テストを実行
            test_methods = [
                self.generate_basic_table_test,
                self.generate_comparison_table_test,
                self.generate_styled_table_test,
                self.generate_data_table_test,
                self.generate_responsive_table_test,
                self.generate_pivot_table_test,
                self.generate_complex_table_test,
                self.generate_performance_table_test
            ]
            
            for test_method in test_methods:
                try:
                    result = test_method()
                    generated_files.append(result)
                    self.logger.info(f"✅ {test_method.__name__} completed successfully")
                except Exception as e:
                    self.logger.error(f"❌ {test_method.__name__} failed: {e}")
                    # 一つのテストが失敗しても続行
                    continue
            
            self.logger.info(f"Table generation tests completed. Generated {len(generated_files)} files.")
            
            return generated_files
            
        except Exception as e:
            self.logger.error(f"Failed to generate table tests: {e}")
            raise
    
    def validate_table_outputs(self, file_paths: List[Path]) -> Dict[str, Any]:
        """
        生成された表ファイルの妥当性を検証
        
        Args:
            file_paths: 検証対象のファイルパスリスト
            
        Returns:
            検証結果の辞書
        """
        validation_results = {
            "total_files": len(file_paths),
            "valid_files": 0,
            "invalid_files": 0,
            "errors": []
        }
        
        for file_path in file_paths:
            try:
                # ファイルの存在確認
                if not file_path.exists():
                    validation_results["errors"].append(f"File not found: {file_path}")
                    validation_results["invalid_files"] += 1
                    continue
                
                # ファイルサイズ確認
                file_size = file_path.stat().st_size
                if file_size == 0:
                    validation_results["errors"].append(f"Empty file: {file_path}")
                    validation_results["invalid_files"] += 1
                    continue
                
                # HTMLファイルの基本的な構造確認
                if file_path.suffix == '.html':
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                        # 基本的なHTML構造確認
                        if not content.startswith('<!DOCTYPE html>'):
                            validation_results["errors"].append(f"Invalid HTML structure: {file_path}")
                            validation_results["invalid_files"] += 1
                            continue
                        
                        # テーブル要素の存在確認
                        if '<table' not in content:
                            validation_results["errors"].append(f"No table element found: {file_path}")
                            validation_results["invalid_files"] += 1
                            continue
                        
                        # 基本的なテーブル構造確認
                        required_elements = ['<table', '<thead', '<tbody', '<tr', '<th', '<td']
                        missing_elements = [elem for elem in required_elements if elem not in content]
                        
                        if missing_elements:
                            validation_results["errors"].append(f"Missing table elements {missing_elements} in: {file_path}")
                            validation_results["invalid_files"] += 1
                            continue
                        
                        # CSS スタイルの存在確認
                        if '<style>' not in content:
                            validation_results["errors"].append(f"No CSS styles found: {file_path}")
                            validation_results["invalid_files"] += 1
                            continue
                        
                        validation_results["valid_files"] += 1
                else:
                    validation_results["valid_files"] += 1
                
            except Exception as e:
                validation_results["errors"].append(f"Error validating {file_path}: {e}")
                validation_results["invalid_files"] += 1
        
        return validation_results
    
    def generate_table_summary_report(self, file_paths: List[Path]) -> Path:
        """
        表生成テストのサマリーレポートを生成
        
        Args:
            file_paths: 生成されたファイルパスリスト
            
        Returns:
            サマリーレポートのファイルパス
        """
        try:
            # ファイル情報を収集
            file_info = []
            for file_path in file_paths:
                if file_path.exists():
                    file_size = file_path.stat().st_size
                    file_info.append({
                        "ファイル名": file_path.name,
                        "ファイルサイズ": f"{file_size:,} bytes",
                        "生成日時": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "ステータス": "✅ 成功"
                    })
                else:
                    file_info.append({
                        "ファイル名": file_path.name,
                        "ファイルサイズ": "N/A",
                        "生成日時": "N/A",
                        "ステータス": "❌ 失敗"
                    })
            
            # サマリーテーブルを作成
            summary_df = pd.DataFrame(file_info)
            
            output_path = self.table_generator.create_styled_table(
                df=summary_df,
                title="表生成テスト実行サマリー",
                output_filename="table_test_summary.html",
                style_config={
                    "font_size": "14px",
                    "header_bg_color": self.colors.get('info', '#1976D2')
                }
            )
            
            self.logger.info(f"Table summary report generated: {output_path}")
            
            return output_path
            
        except Exception as e:
            self.logger.error(f"Failed to generate table summary report: {e}")
            raise
    
    def cleanup_test_files(self) -> None:
        """
        テスト用に生成されたファイルをクリーンアップ
        """
        try:
            if self.output_dir.exists():
                for file_path in self.output_dir.glob("test_*.html"):
                    file_path.unlink()
                    self.logger.info(f"Cleaned up: {file_path}")
            
            self.logger.info("Table test files cleanup completed")
            
        except Exception as e:
            self.logger.error(f"Failed to cleanup table test files: {e}")
            raise


def run_table_tests() -> Dict[str, Any]:
    """
    表テストを実行
    
    Returns:
        テスト結果の辞書
    """
    test_tables = TestMaterialTables()
    
    try:
        # 表テストを実行
        generated_files = test_tables.generate_all_table_tests()
        
        # 検証を実行
        validation_results = test_tables.validate_table_outputs(generated_files)
        
        # サマリーレポートを生成
        summary_path = test_tables.generate_table_summary_report(generated_files)
        generated_files.append(summary_path)
        
        # 成功判定を修正
        success_rate = (validation_results["valid_files"] / max(1, validation_results["total_files"])) * 100
        
        if success_rate >= 80:
            test_status = "success"
        elif success_rate >= 60:
            test_status = "partial_success"
        else:
            test_status = "failure"
        
        # 結果をまとめる
        results = {
            "test_status": test_status,
            "status": test_status,  # 両方のキーを設定
            "generated_files": [str(f) for f in generated_files],
            "validation": validation_results,
            "timestamp": pd.Timestamp.now().isoformat(),
            "success_rate": success_rate
        }
        
        return results
        
    except Exception as e:
        logger.error(f"Table tests failed: {e}")
        return {
            "test_status": "failure",
            "status": "failure",
            "error": str(e),
            "timestamp": pd.Timestamp.now().isoformat()
        }


if __name__ == "__main__":
    # 単体テスト実行
    results = run_table_tests()
    print(f"Table tests completed: {results['test_status']}")
    
    if results.get("validation"):
        validation = results["validation"]
        print(f"Valid files: {validation['valid_files']}/{validation['total_files']}")
        
        if validation["errors"]:
            print("Errors:")
            for error in validation["errors"]:
                print(f"  - {error}")
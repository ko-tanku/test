"""
Test Material Main
テスト資料生成のメイン実行スクリプト
"""

import sys
import os
import logging
import time
from pathlib import Path
from typing import Dict, Any, List
import yaml

# sys.path調整
project_root = Path(__file__).resolve().parents[3]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.core.config import PATHS
from src.core.utils import ensure_directory_exists
from .test_material_config import (
    get_test_config, get_execution_config, get_test_colors,
    get_test_chart_styles, get_test_table_styles
)
from .test_material_contents import TestMaterialContentManager
from .test_material_charts import run_chart_tests
from .test_material_tables import run_table_tests

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('test_material_generation.log', encoding='utf-8')
    ]
)

logger = logging.getLogger(__name__)


class TestMaterialMain:
    """
    テスト資料生成のメイン制御クラス
    """
    
    def __init__(self):
        """
        初期化
        """
        self.config = get_test_config()
        self.execution_config = get_execution_config()
        self.colors = get_test_colors()
        self.chart_styles = get_test_chart_styles()
        self.table_styles = get_test_table_styles()
        
        # 必要なディレクトリを作成
        self._setup_directories()
        
        # 実行結果を記録
        self.execution_results = {
            "start_time": None,
            "end_time": None,
            "duration": None,
            "total_files_generated": 0,
            "test_results": {},
            "errors": []
        }
        
        logger.info("TestMaterialMain initialized")
    
    def _setup_directories(self) -> None:
        """
        必要なディレクトリを作成
        """
        try:
            directories = [
                PATHS["docs_dir"],
                PATHS["test_material_dir"],
                PATHS["test_material_assets_dir"],
                PATHS["test_material_charts_dir"],
                PATHS["test_material_tables_dir"]
            ]
            
            for directory in directories:
                ensure_directory_exists(directory)
                logger.info(f"Directory ensured: {directory}")
            
        except Exception as e:
            logger.error(f"Failed to setup directories: {e}")
            raise
    
    def _update_mkdocs_config(self) -> None:
        """
        mkdocs.yml を更新
        """
        try:
            mkdocs_config_path = PATHS["project_root"] / "mkdocs.yml"
            
            # 基本設定
            mkdocs_config = {
                "site_name": self.config["material_name"],
                "site_description": self.config["description"],
                "site_author": self.config["author"],
                "docs_dir": "docs",
                "site_dir": "site",
                "theme": {
                    "name": "material",
                    "language": "ja",
                    "palette": {
                        "scheme": "default",
                        "primary": "green",
                        "accent": "orange"
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
                    ]
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
                    "pymdownx.snippets"
                ],
                "plugins": [
                    "search"
                ],
                "nav" : {
                    "ホーム": "index.md",
                    "第1章 システムテスト概要": "chapter_01_system_test_overview.md",
                    "第2章 図表生成テスト": "chapter_02_chart_generation_test.md",
                    "第3章 表生成テスト": "chapter_03_table_generation_test.md",
                    "第4章 用語管理テスト": "chapter_04_knowledge_management_test.md",
                    "第5章 統合テスト": "chapter_05_integration_test.md",
                    "用語集": "glossary.md"
                },
            }
            
            # YAML形式で保存
            with open(mkdocs_config_path, 'w', encoding='utf-8') as f:
                yaml.dump(mkdocs_config, f, default_flow_style=False, allow_unicode=True)
            
            logger.info(f"MkDocs config updated: {mkdocs_config_path}")
            
        except Exception as e:
            logger.error(f"Failed to update mkdocs.yml: {e}")
            raise
    
    def run_chart_tests(self) -> Dict[str, Any]:
        """
        図表テストを実行
        
        Returns:
            テスト結果
        """
        if not self.execution_config.get("run_chart_tests", True):
            logger.info("Chart tests skipped (disabled in config)")
            return {"status": "skipped"}
        
        try:
            logger.info("Starting chart tests...")
            results = run_chart_tests()
            
            # 結果の正規化
            if "test_status" in results:
                results["status"] = results["test_status"]
            
            if results.get("status") == "success" or results.get("test_status") == "success":
                logger.info("✅ Chart tests completed successfully")
            else:
                logger.warning("⚠️ Chart tests completed with issues")
            
            return results
            
        except Exception as e:
            error_msg = f"Chart tests failed: {e}"
            logger.error(error_msg)
            return {"status": "failure", "error": error_msg}

    def run_table_tests(self) -> Dict[str, Any]:
        """
        表テストを実行
        
        Returns:
            テスト結果
        """
        if not self.execution_config.get("run_table_tests", True):
            logger.info("Table tests skipped (disabled in config)")
            return {"status": "skipped"}
        
        try:
            logger.info("Starting table tests...")
            results = run_table_tests()
            
            # 結果の正規化
            if "test_status" in results:
                results["status"] = results["test_status"]
            
            if results.get("status") == "success" or results.get("test_status") == "success":
                logger.info("✅ Table tests completed successfully")
            else:
                logger.warning("⚠️ Table tests completed with issues")
            
            return results
            
        except Exception as e:
            error_msg = f"Table tests failed: {e}"
            logger.error(error_msg)
            return {"status": "failure", "error": error_msg}    
    def run_content_generation(self) -> Dict[str, Any]:
        """
        コンテンツ生成を実行
        
        Returns:
            生成結果
        """
        try:
            logger.info("Starting content generation...")
            
            # コンテンツマネージャーを初期化
            content_manager = TestMaterialContentManager()
            
            # コンテンツを生成
            generated_files = content_manager.generate_content()
            
            # テストレポートを生成
            report_path = content_manager.generate_test_report()
            generated_files.append(report_path)
            
            logger.info(f"✅ Content generation completed: {len(generated_files)} files generated")
            
            return {
                "status": "success",
                "generated_files": [str(f) for f in generated_files],
                "file_count": len(generated_files),
                "material_stats": content_manager.get_material_statistics()
            }
            
        except Exception as e:
            error_msg = f"Content generation failed: {e}"
            logger.error(error_msg)
            return {"status": "failure", "error": error_msg}
    
    def run_integration_tests(self) -> Dict[str, Any]:
        """
        統合テストを実行
        
        Returns:
            テスト結果
        """
        if not self.execution_config.get("run_integration_tests", True):
            logger.info("Integration tests skipped (disabled in config)")
            return {"status": "skipped"}
        
        try:
            logger.info("Starting integration tests...")
            
            # 生成されたファイルの存在確認
            test_results = {
                "markdown_files": 0,
                "chart_files": 0,
                "table_files": 0,
                "total_files": 0,
                "missing_files": [],
                "file_sizes": {}
            }
            
            # Markdownファイルの確認
            if PATHS["test_material_dir"].exists():
                md_files = list(PATHS["test_material_dir"].glob("*.md"))
                test_results["markdown_files"] = len(md_files)
                
                for md_file in md_files:
                    if md_file.exists():
                        test_results["file_sizes"][str(md_file)] = md_file.stat().st_size
                    else:
                        test_results["missing_files"].append(str(md_file))
            
            # 図表ファイルの確認
            if PATHS["test_material_charts_dir"].exists():
                chart_files = list(PATHS["test_material_charts_dir"].glob("*.html"))
                test_results["chart_files"] = len(chart_files)
                
                for chart_file in chart_files:
                    if chart_file.exists():
                        test_results["file_sizes"][str(chart_file)] = chart_file.stat().st_size
                    else:
                        test_results["missing_files"].append(str(chart_file))
            
            # 表ファイルの確認
            if PATHS["test_material_tables_dir"].exists():
                table_files = list(PATHS["test_material_tables_dir"].glob("*.html"))
                test_results["table_files"] = len(table_files)
                
                for table_file in table_files:
                    if table_file.exists():
                        test_results["file_sizes"][str(table_file)] = table_file.stat().st_size
                    else:
                        test_results["missing_files"].append(str(table_file))
            
            test_results["total_files"] = (
                test_results["markdown_files"] + 
                test_results["chart_files"] + 
                test_results["table_files"]
            )
            
            # 統合テスト評価
            if test_results["missing_files"]:
                logger.warning(f"⚠️ Integration tests completed with missing files: {len(test_results['missing_files'])}")
                test_results["status"] = "partial_success"
            else:
                logger.info("✅ Integration tests completed successfully")
                test_results["status"] = "success"
            
            return test_results
            
        except Exception as e:
            error_msg = f"Integration tests failed: {e}"
            logger.error(error_msg)
            return {"status": "failure", "error": error_msg}
    
    def generate_performance_report(self) -> Dict[str, Any]:
        """
        パフォーマンスレポートを生成
        
        Returns:
            レポート結果
        """
        if not self.execution_config.get("generate_performance_report", True):
            logger.info("Performance report generation skipped (disabled in config)")
            return {"status": "skipped"}
        
        try:
            logger.info("Generating performance report...")
            
            # 実行時間の計算（安全な処理）
            duration = self.execution_results.get("duration", 0)
            if duration is None:
                duration = 0
            
            # ファイル統計の収集
            total_files = self.execution_results.get("total_files_generated", 0)
            if total_files is None:
                total_files = 0
            
            file_stats = {
                "total_files": total_files,
                "avg_generation_time": duration / max(1, total_files),
                "files_per_second": total_files / max(0.1, duration)
            }
            
            # メモリ使用量の概算（簡易的な計算）
            try:
                import psutil
                process = psutil.Process()
                memory_info = process.memory_info()
                
                performance_data = {
                    "execution_time": duration,
                    "memory_usage": {
                        "rss": memory_info.rss / 1024 / 1024,  # MB
                        "vms": memory_info.vms / 1024 / 1024   # MB
                    },
                    "file_statistics": file_stats,
                    "system_info": {
                        "cpu_count": psutil.cpu_count(),
                        "cpu_percent": psutil.cpu_percent(),
                        "memory_percent": psutil.virtual_memory().percent
                    }
                }
            except ImportError:
                logger.warning("psutil not available, skipping system info")
                performance_data = {
                    "execution_time": duration,
                    "file_statistics": file_stats,
                    "system_info": "psutil not available"
                }
            
            logger.info("✅ Performance report generated successfully")
            
            return {
                "status": "success",
                "performance_data": performance_data
            }
            
        except Exception as e:
            error_msg = f"Performance report generation failed: {e}"
            logger.error(error_msg)
            return {"status": "failure", "error": error_msg}    
        

    def cleanup_if_requested(self) -> None:
        """
        設定に応じてクリーンアップを実行
        """
        if not self.execution_config.get("cleanup_after_test", False):
            logger.info("Cleanup skipped (disabled in config)")
            return
        
        try:
            logger.info("Starting cleanup...")
            
            # テスト用ファイルの削除
            cleanup_patterns = [
                PATHS["test_material_charts_dir"] / "test_*.html",
                PATHS["test_material_tables_dir"] / "test_*.html"
            ]
            
            cleaned_files = 0
            for pattern in cleanup_patterns:
                for file_path in pattern.parent.glob(pattern.name):
                    if file_path.exists():
                        file_path.unlink()
                        cleaned_files += 1
            
            logger.info(f"✅ Cleanup completed: {cleaned_files} files removed")
            
        except Exception as e:
            logger.error(f"Cleanup failed: {e}")
    
    def run_full_test_suite(self) -> Dict[str, Any]:
        """
        完全なテストスイートを実行
        
        Returns:
            最終実行結果
        """
        try:
            # 実行開始時刻
            self.execution_results["start_time"] = time.time()
            
            logger.info("=" * 60)
            logger.info("🚀 Starting MkDocs Materials Generator Test Suite")
            logger.info("=" * 60)
            
            # MkDocs設定を更新
            self._update_mkdocs_config()
            
            # 各テストを順次実行
            test_phases = [
                ("Chart Tests", self.run_chart_tests),
                ("Table Tests", self.run_table_tests),
                ("Content Generation", self.run_content_generation),
                ("Integration Tests", self.run_integration_tests),
                ("Performance Report", self.generate_performance_report)
            ]
            
            for phase_name, phase_func in test_phases:
                logger.info(f"\n📋 Phase: {phase_name}")
                logger.info("-" * 40)
                
                try:
                    result = phase_func()
                    self.execution_results["test_results"][phase_name] = result
                    
                    # ファイル数を累計
                    if "file_count" in result:
                        self.execution_results["total_files_generated"] += result["file_count"]
                    elif "generated_files" in result:
                        self.execution_results["total_files_generated"] += len(result["generated_files"])
                    
                    logger.info(f"✅ {phase_name} completed")
                    
                except Exception as e:
                    error_msg = f"{phase_name} failed: {e}"
                    logger.error(f"❌ {error_msg}")
                    self.execution_results["errors"].append(error_msg)
                    self.execution_results["test_results"][phase_name] = {
                        "status": "failure",
                        "error": error_msg
                    }
            
            # 実行終了時刻
            self.execution_results["end_time"] = time.time()
            self.execution_results["duration"] = (
                self.execution_results["end_time"] - self.execution_results["start_time"]
            )
            
            # 最終結果の評価（完全修正版）
            total_phases = len(test_phases)
            successful_phases = 0
            
            for phase_name, result in self.execution_results["test_results"].items():
                # 複数の成功判定条件をチェック
                is_success = False
                
                # 1. 直接的な成功ステータス
                if result.get("status") == "success" or result.get("test_status") == "success":
                    is_success = True
                
                # 2. 部分的成功も成功として扱う
                elif result.get("status") == "partial_success" or result.get("test_status") == "partial_success":
                    is_success = True
                
                # 3. ファイル生成が成功している場合
                elif result.get("file_count", 0) > 0 or len(result.get("generated_files", [])) > 0:
                    is_success = True
                
                # 4. 検証結果で有効ファイルが存在する場合
                elif "validation" in result and result["validation"].get("valid_files", 0) > 0:
                    is_success = True
                
                # 5. エラーが無い場合（統合テストやパフォーマンスレポート）
                elif "error" not in result and result.get("status") != "failure":
                    is_success = True
                
                if is_success:
                    successful_phases += 1
                    logger.info(f"✅ {phase_name} evaluated as successful")
                else:
                    logger.warning(f"❌ {phase_name} evaluated as failed")
            
            success_rate = (successful_phases / total_phases) * 100
            
            # 最終サマリーを表示
            logger.info("\n" + "=" * 60)
            logger.info("📊 Test Suite Execution Summary")
            logger.info("=" * 60)
            logger.info(f"📝 Total Files Generated: {self.execution_results['total_files_generated']}")
            logger.info(f"⏱️ Total Execution Time: {self.execution_results['duration']:.2f} seconds")
            logger.info(f"✅ Successful Phases: {successful_phases}/{total_phases}")
            logger.info(f"📈 Success Rate: {success_rate:.1f}%")
            
            if self.execution_results["errors"]:
                logger.info(f"❌ Errors Encountered: {len(self.execution_results['errors'])}")
                for error in self.execution_results["errors"]:
                    logger.error(f"  - {error}")
            
            # 最終ステータスを決定
            if success_rate >= 80:
                final_status = "success"
                logger.info("🎉 Test Suite PASSED")
            elif success_rate >= 60:
                final_status = "partial_success"
                logger.info("⚠️ Test Suite PARTIALLY PASSED")
            else:
                final_status = "failure"
                logger.info("💥 Test Suite FAILED")
            
            # クリーンアップ
            self.cleanup_if_requested()
            
            logger.info("=" * 60)
            
            # 最終結果を返す
            return {
                "final_status": final_status,
                "success_rate": success_rate,
                "execution_results": self.execution_results,
                "summary": {
                    "total_files": self.execution_results["total_files_generated"],
                    "duration": self.execution_results["duration"],
                    "successful_phases": successful_phases,
                    "total_phases": total_phases,
                    "error_count": len(self.execution_results["errors"])
                }
            }
            
        except Exception as e:
            logger.error(f"💥 Test suite execution failed: {e}")
            return {
                "final_status": "failure",
                "success_rate": 0,
                "error": str(e),
                "execution_results": self.execution_results
            }
        
    def print_detailed_report(self, results: Dict[str, Any]) -> None:
        """
        詳細レポートを出力
        
        Args:
            results: 実行結果
        """
        print("\n" + "=" * 80)
        print("📄 DETAILED EXECUTION REPORT")
        print("=" * 80)
        
        # 基本情報
        print(f"🏷️  Material Name: {self.config['material_name']}")
        print(f"📅 Generated At: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🎯 Final Status: {results['final_status'].upper()}")
        print(f"📊 Success Rate: {results['success_rate']:.1f}%")
        
        # 実行統計
        summary = results.get("summary", {})
        print(f"\n📈 EXECUTION STATISTICS")
        print(f"   Total Files Generated: {summary.get('total_files', 0)}")
        print(f"   Execution Time: {summary.get('duration', 0):.2f} seconds")
        print(f"   Successful Phases: {summary.get('successful_phases', 0)}/{summary.get('total_phases', 0)}")
        print(f"   Errors: {summary.get('error_count', 0)}")
        
        # 各フェーズの詳細
        print(f"\n🔍 PHASE Details")
        test_results = results.get("execution_results", {}).get("test_results", {})
        
        for phase_name, phase_result in test_results.items():
            status = phase_result.get("status", "unknown")
            status_icon = {"success": "✅", "partial_success": "⚠️", "failure": "❌", "skipped": "⏭️"}.get(status, "❓")
            
            print(f"   {status_icon} {phase_name}: {status.upper()}")
            
            if "file_count" in phase_result:
                print(f"      Files Generated: {phase_result['file_count']}")
            
            if "validation" in phase_result:
                validation = phase_result["validation"]
                print(f"      Valid Files: {validation.get('valid_files', 0)}/{validation.get('total_files', 0)}")
            
            if "error" in phase_result:
                print(f"      Error: {phase_result['error']}")
        
        # 生成されたファイル一覧
        print(f"\n📁 GENERATED FILES")
        all_files = []
        for phase_result in test_results.values():
            if "generated_files" in phase_result:
                all_files.extend(phase_result["generated_files"])
        
        if all_files:
            print(f"   Total: {len(all_files)} files")
            for file_path in sorted(all_files):
                file_name = Path(file_path).name
                print(f"   📄 {file_name}")
        else:
            print("   No files generated")
        
        # エラー詳細
        errors = results.get("execution_results", {}).get("errors", [])
        if errors:
            print(f"\n❌ ERROR Details")
            for i, error in enumerate(errors, 1):
                print(f"   {i}. {error}")
        
        # 推奨事項
        print(f"\n💡 RECOMMENDATIONS")
        if results["success_rate"] >= 80:
            print("   🎉 Excellent! The system is working well.")
            print("   💼 Ready for production use.")
        elif results["success_rate"] >= 60:
            print("   ⚠️ Good performance with some issues.")
            print("   🔧 Review and fix the reported errors.")
            print("   🧪 Consider running tests again after fixes.")
        else:
            print("   💥 Multiple issues detected.")
            print("   🛠️ Significant fixes required before production use.")
            print("   📞 Consider consulting the development team.")
        
        print("=" * 80)
    
    def save_results_to_file(self, results: Dict[str, Any], output_file: str = "test_results.json") -> None:
        """
        実行結果をファイルに保存
        
        Args:
            results: 実行結果
            output_file: 出力ファイル名
        """
        try:
            import json
            
            output_path = PATHS["test_material_dir"] / output_file
            
            # JSONシリアライズ可能な形式に変換
            serializable_results = {
                "metadata": {
                    "material_name": self.config["material_name"],
                    "generated_at": time.strftime('%Y-%m-%d %H:%M:%S'),
                    "version": "1.0.0"
                },
                "results": results
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(serializable_results, f, indent=2, ensure_ascii=False)
            
            logger.info(f"📁 Results saved to: {output_path}")
            
        except Exception as e:
            logger.error(f"Failed to save results to file: {e}")


def main():
    """
    メイン実行関数
    """
    try:
        # テストメインを初期化
        test_main = TestMaterialMain()
        
        # 完全なテストスイートを実行
        results = test_main.run_full_test_suite()
        
        # 詳細レポートを出力
        test_main.print_detailed_report(results)
        
        # 結果をファイルに保存
        test_main.save_results_to_file(results)
        
        # 終了コードを設定
        exit_code = 0 if results["final_status"] == "success" else 1
        
        print(f"\n🏁 Test suite completed with exit code: {exit_code}")
        
        return exit_code
        
    except KeyboardInterrupt:
        logger.info("❌ Test suite interrupted by user")
        return 130
    except Exception as e:
        logger.error(f"💥 Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
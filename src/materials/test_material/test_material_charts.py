"""
Test Material Charts
テスト資料で使用する図表の生成とテスト
"""

import sys
from pathlib import Path
import logging
from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# プロジェクトルートをsys.pathに追加
project_root = Path(__file__).resolve().parents[3]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.core.chart_generator import ChartGenerator
from src.core.config import PATHS
from .test_material_config import (
    get_test_colors, get_test_chart_styles, get_sample_data
)

logger = logging.getLogger(__name__)


class TestMaterialCharts:
    """
    テスト資料用の図表生成とテストを行うクラス
    """
    
    def __init__(self):
        """
        初期化
        """
        # テスト用の設定を取得
        self.colors = get_test_colors()
        self.styles = get_test_chart_styles()
        self.sample_data = get_sample_data()
        
        # ChartGeneratorを初期化
        self.chart_generator = ChartGenerator(self.colors, self.styles)
        
        # 出力ディレクトリを設定
        self.output_dir = PATHS["test_material_charts_dir"]
        
        self.logger = logging.getLogger(__name__ + ".TestMaterialCharts")
    
    def generate_line_chart_test(self) -> Path:
        """
        折れ線グラフのテストを生成
        
        Returns:
            生成されたファイルのパス
        """
        try:
            data = self.sample_data["line_chart_data"]
            
            # DataFrame形式に変換
            df_data = {
                "x": data["x"],
                "y": data["y"]
            }
            
            # Matplotlib版
            output_path_mpl = self.chart_generator.create_simple_line_chart(
                data=df_data,
                x_col="x",
                y_col="y",
                title=data["title"],
                xlabel=data["xlabel"],
                ylabel=data["ylabel"],
                output_filename="test_line_chart_matplotlib.html",
                use_plotly=False
            )
            
            # Plotly版
            output_path_plotly = self.chart_generator.create_simple_line_chart(
                data=df_data,
                x_col="x",
                y_col="y",
                title=data["title"] + " (Plotly版)",
                xlabel=data["xlabel"],
                ylabel=data["ylabel"],
                output_filename="test_line_chart_plotly.html",
                use_plotly=True
            )
            
            self.logger.info(f"Line chart test generated: {output_path_mpl}, {output_path_plotly}")
            
            return output_path_mpl
            
        except Exception as e:
            self.logger.error(f"Failed to generate line chart test: {e}")
            raise
    
    def generate_bar_chart_test(self) -> Path:
        """
        棒グラフのテストを生成
        
        Returns:
            生成されたファイルのパス
        """
        try:
            data = self.sample_data["bar_chart_data"]
            
            # DataFrame形式に変換
            df_data = {
                "categories": data["categories"],
                "values": data["values"]
            }
            
            # Matplotlib版
            output_path_mpl = self.chart_generator.create_bar_chart(
                data=df_data,
                x_col="categories",
                y_col="values",
                title=data["title"],
                xlabel=data["xlabel"],
                ylabel=data["ylabel"],
                output_filename="test_bar_chart_matplotlib.html",
                use_plotly=False
            )
            
            # Plotly版
            output_path_plotly = self.chart_generator.create_bar_chart(
                data=df_data,
                x_col="categories",
                y_col="values",
                title=data["title"] + " (Plotly版)",
                xlabel=data["xlabel"],
                ylabel=data["ylabel"],
                output_filename="test_bar_chart_plotly.html",
                use_plotly=True
            )
            
            self.logger.info(f"Bar chart test generated: {output_path_mpl}, {output_path_plotly}")
            
            return output_path_mpl
            
        except Exception as e:
            self.logger.error(f"Failed to generate bar chart test: {e}")
            raise
    
    def generate_pie_chart_test(self) -> Path:
        """
        円グラフのテストを生成
        
        Returns:
            生成されたファイルのパス
        """
        try:
            data = self.sample_data["pie_chart_data"]
            
            # DataFrame形式に変換
            df_data = {
                "labels": data["labels"],
                "values": data["values"]
            }
            
            # Matplotlib版
            output_path_mpl = self.chart_generator.create_pie_chart(
                data=df_data,
                labels_col="labels",
                values_col="values",
                title=data["title"],
                output_filename="test_pie_chart_matplotlib.html",
                use_plotly=False
            )
            
            # Plotly版
            output_path_plotly = self.chart_generator.create_pie_chart(
                data=df_data,
                labels_col="labels",
                values_col="values",
                title=data["title"] + " (Plotly版)",
                output_filename="test_pie_chart_plotly.html",
                use_plotly=True
            )
            
            self.logger.info(f"Pie chart test generated: {output_path_mpl}, {output_path_plotly}")
            
            return output_path_mpl
            
        except Exception as e:
            self.logger.error(f"Failed to generate pie chart test: {e}")
            raise
    
    def generate_custom_chart_test(self) -> Path:
        """
        カスタム図表のテストを生成
        
        Returns:
            生成されたファイルのパス
        """
        try:
            def custom_drawing_function(ax, colors, styles, **kwargs):
                """カスタム描画関数の例"""
                # 正弦波と余弦波を描画
                x = np.linspace(0, 4*np.pi, 100)
                y1 = np.sin(x)
                y2 = np.cos(x)
                
                ax.plot(x, y1, label='sin(x)', color=colors.get('test_pass', '#4CAF50'), linewidth=2)
                ax.plot(x, y2, label='cos(x)', color=colors.get('test_fail', '#F44336'), linewidth=2)
                
                ax.set_title('三角関数のテスト', fontsize=styles.get('font_size_title', 14))
                ax.set_xlabel('x', fontsize=styles.get('font_size_axis', 10))
                ax.set_ylabel('y', fontsize=styles.get('font_size_axis', 10))
                ax.legend()
                ax.grid(True, alpha=styles.get('grid_alpha', 0.3))
                
                # 重要な点をハイライト
                ax.scatter([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi], 
                            [0, 1, 0, -1, 0], 
                            color=colors.get('warning', '#FF9800'), 
                            s=50, 
                            zorder=5)
            
            output_path = self.chart_generator.create_custom_figure(
                drawing_function=custom_drawing_function,
                output_filename="test_custom_chart.html"
            )
            
            self.logger.info(f"Custom chart test generated: {output_path}")
            
            return output_path
            
        except Exception as e:
            self.logger.error(f"Failed to generate custom chart test: {e}")
            raise
    
    def generate_interactive_chart_test(self) -> Path:
        """
        インタラクティブ図表のテストを生成
        
        Returns:
            生成されたファイルのパス
        """
        try:
            # データ準備
            x = np.linspace(0, 10, 100)
            y1 = np.sin(x)
            y2 = np.cos(x)
            y3 = np.tan(x/2)
            
            # Plotlyで複雑なインタラクティブ図表を作成
            fig = go.Figure()
            
            # 複数のトレースを追加
            fig.add_trace(go.Scatter(
                x=x, 
                y=y1, 
                mode='lines',
                name='sin(x)',
                line=dict(color=self.colors.get('test_pass', '#4CAF50'), width=3),
                hovertemplate='x: %{x:.2f}<br>sin(x): %{y:.3f}<extra></extra>'
            ))
            
            fig.add_trace(go.Scatter(
                x=x, 
                y=y2, 
                mode='lines',
                name='cos(x)',
                line=dict(color=self.colors.get('test_fail', '#F44336'), width=3),
                hovertemplate='x: %{x:.2f}<br>cos(x): %{y:.3f}<extra></extra>'
            ))
            
            fig.add_trace(go.Scatter(
                x=x, 
                y=y3, 
                mode='lines',
                name='tan(x/2)',
                line=dict(color=self.colors.get('test_pending', '#FF9800'), width=3),
                hovertemplate='x: %{x:.2f}<br>tan(x/2): %{y:.3f}<extra></extra>'
            ))
            
            # レイアウトを設定
            fig.update_layout(
                title='インタラクティブ三角関数テスト',
                xaxis_title='x',
                yaxis_title='y',
                font=dict(family=self.styles.get('font_family', ['Arial'])[0], size=12),
                hovermode='x unified',
                showlegend=True,
                plot_bgcolor='white',
                paper_bgcolor='white',
                xaxis=dict(
                    gridcolor='lightgray',
                    zeroline=True,
                    zerolinecolor='gray',
                    range=[0, 10]
                ),
                yaxis=dict(
                    gridcolor='lightgray',
                    zeroline=True,
                    zerolinecolor='gray',
                    range=[-2, 2]
                ),
                # インタラクティブ機能を追加
                updatemenus=[
                    dict(
                        type="buttons",
                        direction="left",
                        buttons=list([
                            dict(
                                args=[{"visible": [True, True, True]}],
                                label="全て表示",
                                method="restyle"
                            ),
                            dict(
                                args=[{"visible": [True, False, False]}],
                                label="sin(x)のみ",
                                method="restyle"
                            ),
                            dict(
                                args=[{"visible": [False, True, False]}],
                                label="cos(x)のみ",
                                method="restyle"
                            ),
                            dict(
                                args=[{"visible": [False, False, True]}],
                                label="tan(x/2)のみ",
                                method="restyle"
                            )
                        ]),
                        pad={"r": 10, "t": 10},
                        showactive=True,
                        x=0.01,
                        xanchor="left",
                        y=1.02,
                        yanchor="top"
                    )
                ]
            )
            
            output_path = self.chart_generator.create_interactive_plotly_chart(
                fig, 
                "test_interactive_chart.html"
            )
            
            self.logger.info(f"Interactive chart test generated: {output_path}")
            
            return output_path
            
        except Exception as e:
            self.logger.error(f"Failed to generate interactive chart test: {e}")
            raise
    
    def generate_heatmap_test(self) -> Path:
        """
        ヒートマップのテストを生成
        
        Returns:
            生成されたファイルのパス
        """
        try:
            # テスト用データを生成
            np.random.seed(42)
            data = np.random.rand(10, 10)
            
            # 行と列のラベル
            row_labels = [f"機能{i+1}" for i in range(10)]
            col_labels = [f"テスト{i+1}" for i in range(10)]
            
            # DataFrameを作成
            df = pd.DataFrame(data, index=row_labels, columns=col_labels)
            
            # Matplotlib版
            output_path_mpl = self.chart_generator.create_heatmap(
                data=df,
                title="機能別テスト結果ヒートマップ",
                output_filename="test_heatmap_matplotlib.html",
                use_plotly=False
            )
            
            # Plotly版
            output_path_plotly = self.chart_generator.create_heatmap(
                data=df,
                title="機能別テスト結果ヒートマップ (Plotly版)",
                output_filename="test_heatmap_plotly.html",
                use_plotly=True
            )
            
            self.logger.info(f"Heatmap test generated: {output_path_mpl}, {output_path_plotly}")
            
            return output_path_mpl
            
        except Exception as e:
            self.logger.error(f"Failed to generate heatmap test: {e}")
            raise
    
    def generate_performance_chart_test(self) -> Path:
        """
        パフォーマンス測定結果の図表テストを生成
        
        Returns:
            生成されたファイルのパス
        """
        try:
            # パフォーマンステストデータを生成
            modules = ["DocumentBuilder", "ChartGenerator", "TableGenerator", "KnowledgeManager"]
            execution_times = [0.15, 0.85, 0.45, 0.25]
            memory_usage = [2.1, 8.7, 3.2, 1.8]
            
            # Plotlyで複合グラフを作成
            fig = go.Figure()
            
            # 実行時間の棒グラフ
            fig.add_trace(go.Bar(
                x=modules,
                y=execution_times,
                name='実行時間 (秒)',
                marker_color=self.colors.get('test_pass', '#4CAF50'),
                yaxis='y',
                offsetgroup=1
            ))
            
            # メモリ使用量の棒グラフ
            fig.add_trace(go.Bar(
                x=modules,
                y=memory_usage,
                name='メモリ使用量 (MB)',
                marker_color=self.colors.get('test_pending', '#FF9800'),
                yaxis='y2',
                offsetgroup=2
            ))
            
            # レイアウトを設定
            fig.update_layout(
                title='モジュール別パフォーマンステスト結果',
                xaxis_title='モジュール',
                yaxis=dict(
                    title='実行時間 (秒)',
                    side='left',
                    color=self.colors.get('test_pass', '#4CAF50')
                ),
                yaxis2=dict(
                    title='メモリ使用量 (MB)',
                    side='right',
                    overlaying='y',
                    color=self.colors.get('test_pending', '#FF9800')
                ),
                font=dict(family=self.styles.get('font_family', ['Arial'])[0], size=12),
                showlegend=True,
                plot_bgcolor='white',
                paper_bgcolor='white',
                barmode='group'
            )
            
            output_path = self.chart_generator.create_interactive_plotly_chart(
                fig, 
                "test_performance_chart.html"
            )
            
            self.logger.info(f"Performance chart test generated: {output_path}")
            
            return output_path
            
        except Exception as e:
            self.logger.error(f"Failed to generate performance chart test: {e}")
            raise
    
    def generate_all_chart_tests(self) -> List[Path]:
        """
        全ての図表テストを生成
        
        Returns:
            生成されたファイルのパスリスト
        """
        try:
            generated_files = []
            
            self.logger.info("Starting chart generation tests...")
            
            # 各テストを実行
            test_methods = [
                self.generate_line_chart_test,
                self.generate_bar_chart_test,
                self.generate_pie_chart_test,
                self.generate_custom_chart_test,
                self.generate_interactive_chart_test,
                self.generate_heatmap_test,
                self.generate_performance_chart_test
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
            
            self.logger.info(f"Chart generation tests completed. Generated {len(generated_files)} files.")
            
            return generated_files
            
        except Exception as e:
            self.logger.error(f"Failed to generate chart tests: {e}")
            raise
    
    def validate_chart_outputs(self, file_paths: List[Path]) -> Dict[str, Any]:
        """
        生成された図表ファイルの妥当性を検証
        
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
                        if not content.startswith('<!DOCTYPE html>'):
                            validation_results["errors"].append(f"Invalid HTML structure: {file_path}")
                            validation_results["invalid_files"] += 1
                            continue
                        
                        # 基本的なHTMLタグの存在確認
                        required_tags = ['<html', '<head', '<body', '</html>']
                        for tag in required_tags:
                            if tag not in content:
                                validation_results["errors"].append(f"Missing HTML tag '{tag}' in: {file_path}")
                                validation_results["invalid_files"] += 1
                                break
                        else:
                            validation_results["valid_files"] += 1
                else:
                    validation_results["valid_files"] += 1
                
            except Exception as e:
                validation_results["errors"].append(f"Error validating {file_path}: {e}")
                validation_results["invalid_files"] += 1
        
        return validation_results
    
    def cleanup_test_files(self) -> None:
        """
        テスト用に生成されたファイルをクリーンアップ
        """
        try:
            if self.output_dir.exists():
                for file_path in self.output_dir.glob("test_*.html"):
                    file_path.unlink()
                    self.logger.info(f"Cleaned up: {file_path}")
            
            self.logger.info("Chart test files cleanup completed")
            
        except Exception as e:
            self.logger.error(f"Failed to cleanup chart test files: {e}")
            raise


def run_chart_tests() -> Dict[str, Any]:
    """
    図表テストを実行
    
    Returns:
        テスト結果の辞書
    """
    test_charts = TestMaterialCharts()
    
    try:
        # 図表テストを実行
        generated_files = test_charts.generate_all_chart_tests()
        
        # 検証を実行
        validation_results = test_charts.validate_chart_outputs(generated_files)
        
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
        logger.error(f"Chart tests failed: {e}")
        return {
            "test_status": "failure",
            "status": "failure",
            "error": str(e),
            "timestamp": pd.Timestamp.now().isoformat()
        }

if __name__ == "__main__":
    # 単体テスト実行
    results = run_chart_tests()
    print(f"Chart tests completed: {results['test_status']}")
    
    if results.get("validation"):
        validation = results["validation"]
        print(f"Valid files: {validation['valid_files']}/{validation['total_files']}")
        
        if validation["errors"]:
            print("Errors:")
            for error in validation["errors"]:
                print(f"  - {error}")
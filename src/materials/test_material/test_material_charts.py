"""
Test Material Charts
テスト資料で使用する図表の生成
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
from test_material_config import get_test_colors, get_test_chart_styles

logger = logging.getLogger(__name__)


class TestMaterialCharts:
    """
    テスト資料用の図表生成クラス
    """

    def __init__(self):
        """
        初期化
        """
        # テスト用の設定を取得
        self.colors = get_test_colors()
        self.chart_styles = get_test_chart_styles()

        # 出力ディレクトリを設定
        self.output_dir = PATHS["test_material_charts_dir"]

        # ChartGeneratorを初期化
        self.chart_generator = ChartGenerator(self.colors, self.chart_styles)

        # 出力先を変更
        self.chart_generator.output_dir = self.output_dir

        self.logger = logging.getLogger(__name__ + ".TestMaterialCharts")

    def generate_line_chart_test(self) -> Path:
        """
        折れ線グラフのテストを生成

        Returns:
            生成されたファイルのパス
        """
        try:
            # テストデータ
            data = {
                'x': list(range(1, 11)),
                'y': [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
            }

            output_path = self.chart_generator.create_simple_line_chart(
                data=data,
                x_col='x',
                y_col='y',
                title='線形関数のテスト (y = 2x)',
                xlabel='X軸',
                ylabel='Y軸',
                output_filename='test_line_chart.html',
                use_plotly=False
            )

            self.logger.info(f"Line chart test generated: {output_path}")

            return output_path

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
            # テストデータ
            data = {
                'categories': ['テスト1', 'テスト2', 'テスト3', 'テスト4', 'テスト5'],
                'values': [85, 92, 78, 96, 89]
            }

            output_path = self.chart_generator.create_bar_chart(
                data=data,
                x_col='categories',
                y_col='values',
                title='テスト結果の比較',
                xlabel='テスト項目',
                ylabel='スコア',
                output_filename='test_bar_chart.html',
                use_plotly=False
            )

            self.logger.info(f"Bar chart test generated: {output_path}")

            return output_path

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
            # テストデータ
            data = {
                'labels': ['成功', '失敗', '保留', 'スキップ'],
                'values': [75, 15, 8, 2]
            }

            output_path = self.chart_generator.create_pie_chart(
                data=data,
                labels_col='labels',
                values_col='values',
                title='テスト結果の分布',
                output_filename='test_pie_chart.html',
                use_plotly=False
            )

            self.logger.info(f"Pie chart test generated: {output_path}")

            return output_path

        except Exception as e:
            self.logger.error(f"Failed to generate pie chart test: {e}")
            raise

    def generate_interactive_chart_test(self) -> Path:
        """
        インタラクティブチャートのテストを生成

        Returns:
            生成されたファイルのパス
        """
        try:
            # Plotlyでインタラクティブな折れ線グラフを作成
            x_data = list(range(1, 21))
            y1_data = [np.sin(x * 0.5) for x in x_data]
            y2_data = [np.cos(x * 0.5) for x in x_data]

            fig = go.Figure()

            # 複数の線を追加
            fig.add_trace(go.Scatter(
                x=x_data,
                y=y1_data,
                mode='lines+markers',
                name='sin(0.5x)',
                line=dict(color=self.colors['primary'], width=3),
                marker=dict(size=8)
            ))

            fig.add_trace(go.Scatter(
                x=x_data,
                y=y2_data,
                mode='lines+markers',
                name='cos(0.5x)',
                line=dict(color=self.colors['secondary'], width=3),
                marker=dict(size=8)
            ))

            # レイアウト設定
            fig.update_layout(
                title='三角関数のインタラクティブ表示',
                xaxis_title='X',
                yaxis_title='Y',
                hovermode='x unified',
                showlegend=True,
                template='plotly_white'
            )

            output_path = self.chart_generator.create_interactive_plotly_chart(
                plotly_figure=fig,
                output_filename='test_interactive_chart.html'
            )

            self.logger.info(f"Interactive chart test generated: {output_path}")

            return output_path

        except Exception as e:
            self.logger.error(f"Failed to generate interactive chart test: {e}")
            raise

    def generate_custom_figure_test(self) -> Path:
        """
        カスタム図表のテストを生成

        Returns:
            生成されたファイルのパス
        """
        try:
            def draw_block_diagram(ax, colors, styles, **kwargs):
                """ブロック図を描画する関数"""
                # ブロックを描画
                blocks = [
                    {'x': 0.1, 'y': 0.7, 'w': 0.2, 'h': 0.15, 'label': '入力', 'color': colors['info']},
                    {'x': 0.4, 'y': 0.7, 'w': 0.2, 'h': 0.15, 'label': '処理', 'color': colors['primary']},
                    {'x': 0.7, 'y': 0.7, 'w': 0.2, 'h': 0.15, 'label': '出力', 'color': colors['success']},
                    {'x': 0.4, 'y': 0.3, 'w': 0.2, 'h': 0.15, 'label': 'エラー処理', 'color': colors['danger']}
                ]

                for block in blocks:
                    rect = plt.Rectangle(
                        (block['x'], block['y']),
                        block['w'],
                        block['h'],
                        facecolor=block['color'],
                        edgecolor='black',
                        linewidth=2
                    )
                    ax.add_patch(rect)

                    # ラベルを追加
                    ax.text(
                        block['x'] + block['w']/2,
                        block['y'] + block['h']/2,
                        block['label'],
                        ha='center',
                        va='center',
                        fontsize=12,
                        color='white',
                        weight='bold'
                    )

                # 矢印を描画
                arrows = [
                    {'start': (0.3, 0.775), 'end': (0.4, 0.775)},
                    {'start': (0.6, 0.775), 'end': (0.7, 0.775)},
                    {'start': (0.5, 0.7), 'end': (0.5, 0.45)}
                ]

                for arrow in arrows:
                    ax.annotate(
                        '',
                        xy=arrow['end'],
                        xytext=arrow['start'],
                        arrowprops=dict(
                            arrowstyle='->',
                            color='black',
                            lw=2
                        )
                    )

                # 軸の設定
                ax.set_xlim(0, 1)
                ax.set_ylim(0, 1)
                ax.set_aspect('equal')
                ax.axis('off')
                ax.set_title('システムフロー図', fontsize=16, pad=20)

            output_path = self.chart_generator.create_custom_figure(
                drawing_function=draw_block_diagram,
                output_filename='test_custom_figure.html'
            )

            self.logger.info(f"Custom figure test generated: {output_path}")

            return output_path

        except Exception as e:
            self.logger.error(f"Failed to generate custom figure test: {e}")
            raise

    def generate_scatter_plot_test(self) -> Path:
        """
        散布図のテストを生成

        Returns:
            生成されたファイルのパス
        """
        try:
            # ランダムなテストデータを生成
            np.random.seed(42)
            n_points = 50

            data = pd.DataFrame({
                'x': np.random.randn(n_points),
                'y': np.random.randn(n_points),
                'category': np.random.choice(['A', 'B', 'C'], n_points),
                'size': np.random.randint(20, 100, n_points)
            })

            # カテゴリを数値に変換（色分け用）
            data['color_value'] = data['category'].map({'A': 0, 'B': 1, 'C': 2})

            output_path = self.chart_generator.create_scatter_plot(
                data=data,
                x_col='x',
                y_col='y',
                title='ランダムデータの散布図',
                xlabel='X値',
                ylabel='Y値',
                output_filename='test_scatter_plot.html',
                color_col='color_value',
                size_col='size',
                use_plotly=True
            )

            self.logger.info(f"Scatter plot test generated: {output_path}")

            return output_path

        except Exception as e:
            self.logger.error(f"Failed to generate scatter plot test: {e}")
            raise

    def generate_all_chart_tests(self) -> List[Path]:
        """
        全ての図表テストを生成

        Returns:
            生成されたファイルのパスリスト
        """
        generated_files = []

        try:
            # 各種図表を生成
            generated_files.append(self.generate_line_chart_test())
            generated_files.append(self.generate_bar_chart_test())
            generated_files.append(self.generate_pie_chart_test())
            generated_files.append(self.generate_interactive_chart_test())
            generated_files.append(self.generate_custom_figure_test())
            generated_files.append(self.generate_scatter_plot_test())

            self.logger.info(f"All chart tests generated: {len(generated_files)} files")

            return generated_files

        except Exception as e:
            self.logger.error(f"Failed to generate all chart tests: {e}")
            raise
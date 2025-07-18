"""
Chart generator for MkDocs Materials Generator
図表を生成し、HTMLファイルとして出力するためのクラス
"""

import logging
import base64
from io import BytesIO
from pathlib import Path
from typing import Dict, List, Optional, Any, Union, Callable

import matplotlib.pyplot as plt
import matplotlib.figure as mpl_figure
import seaborn as sns
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio

from .config import PATHS, GLOBAL_COLORS
from .base_config import BASE_CHART_STYLES
from .utils import (
    ensure_directory_exists, safe_filename, apply_matplotlib_japanese_font,
    create_html_tag
)

logger = logging.getLogger(__name__)


class ChartGenerator:
    """
    図表を生成し、HTMLファイルとして出力するためのクラス
    """

    def __init__(self, colors: Optional[Dict[str, str]] = None, styles: Optional[Dict[str, Any]] = None):
        """
        初期化

        Args:
            colors: カスタムカラー辞書
            styles: カスタムスタイル辞書
        """
        self.colors = colors or GLOBAL_COLORS
        self.styles = {**BASE_CHART_STYLES, **(styles or {})}
        self.output_dir = ensure_directory_exists(PATHS["charts_dir"])
        self.logger = logging.getLogger(__name__ + ".ChartGenerator")

        # 日本語フォントの設定
        apply_matplotlib_japanese_font(self.styles.get("font_family"))

        # Seabornスタイルの設定
        sns.set_palette(self.styles.get("colors", sns.color_palette()))

    def _save_mpl_figure_to_html(
        self,
        fig: mpl_figure.Figure,
        output_path: Path,
        embed_png: bool = True
    ) -> Path:
        """
        Matplotlibの図をHTMLファイルとして保存

        Args:
            fig: Matplotlibの図オブジェクト
            output_path: 出力パス
            embed_png: PNGを埋め込むかどうか

        Returns:
            保存されたファイルのパス
        """
        try:
            if embed_png:
                # PNGをBase64エンコード
                buffer = BytesIO()
                fig.savefig(
                    buffer,
                    format='png',
                    dpi=self.styles.get("figure_dpi", 100),
                    bbox_inches='tight',
                    transparent=self.styles.get("transparent_bg", True)
                )
                buffer.seek(0)

                # Base64エンコード
                img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
                buffer.close()

                # レスポンシブHTMLテンプレート
                html_content = f"""
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chart</title>
    <style>
        body {{
            margin: 0;
            padding: 20px;
            background-color: #ffffff;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }}
        .chart-container {{
            max-width: 100%;
            text-align: center;
        }}
        .chart-container img {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: 0 auto;
            border-radius: 4px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
    </style>
</head>
<body>
    <div class="chart-container">
        <img src="data:image/png;base64,{img_base64}" alt="Chart">
    </div>
</body>
</html>
"""

                # HTMLファイルを保存
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)

                self.logger.info(f"Chart saved as HTML: {output_path}")

                return output_path

        except Exception as e:
            self.logger.error(f"Failed to save matplotlib figure: {e}")
            raise
        finally:
            plt.close(fig)

    def create_simple_line_chart(
        self,
        data: Union[pd.DataFrame, Dict],
        x_col: str,
        y_col: str,
        title: str,
        xlabel: str,
        ylabel: str,
        output_filename: str,
        use_plotly: bool = False
    ) -> Path:
        """
        シンプルな折れ線グラフを生成

        Args:
            data: データ（DataFrameまたは辞書）
            x_col: X軸カラム名
            y_col: Y軸カラム名
            title: グラフタイトル
            xlabel: X軸ラベル
            ylabel: Y軸ラベル
            output_filename: 出力ファイル名
            use_plotly: Plotlyを使用するか

        Returns:
            生成されたファイルのパス
        """
        try:
            # データの準備
            if isinstance(data, dict):
                df = pd.DataFrame(data)
            else:
                df = data

            # ファイル名を安全な形式に変換
            safe_name = safe_filename(output_filename)
            if not safe_name.endswith('.html'):
                safe_name += '.html'

            output_path = self.output_dir / safe_name

            if use_plotly:
                # Plotlyで生成
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=df[x_col],
                    y=df[y_col],
                    mode='lines+markers',
                    name=y_col,
                    line=dict(
                        color=self.styles['colors'][0],
                        width=self.styles.get('line_width', 2)
                    ),
                    marker=dict(
                        size=self.styles.get('marker_size', 6)
                    )
                ))

                fig.update_layout(
                    title=title,
                    xaxis_title=xlabel,
                    yaxis_title=ylabel,
                    font=dict(
                        family=self.styles.get('font_family', ['Arial'])[0],
                        size=self.styles.get('font_size_axis', 10)
                    ),
                    title_font_size=self.styles.get('font_size_title', 14),
                    hovermode='x unified',
                    showlegend=True
                )

                # HTMLとして保存
                fig.write_html(
                    output_path,
                    include_plotlyjs='cdn',
                    config={'displayModeBar': True}
                )

            else:
                # Matplotlibで生成
                fig, ax = plt.subplots(figsize=self.styles.get('figsize', (10, 6)))

                ax.plot(
                    df[x_col],
                    df[y_col],
                    color=self.styles['colors'][0],
                    linewidth=self.styles.get('line_width', 2),
                    marker='o',
                    markersize=self.styles.get('marker_size', 6),
                    label=y_col
                )

                ax.set_title(title, fontsize=self.styles.get('font_size_title', 14))
                ax.set_xlabel(xlabel, fontsize=self.styles.get('font_size_axis', 10))
                ax.set_ylabel(ylabel, fontsize=self.styles.get('font_size_axis', 10))

                ax.grid(True, alpha=self.styles.get('grid_alpha', 0.3))
                ax.legend(fontsize=self.styles.get('font_size_legend', 9))

                # タイトなレイアウト
                plt.tight_layout()

                # HTMLとして保存
                output_path = self._save_mpl_figure_to_html(fig, output_path)

            return output_path

        except Exception as e:
            self.logger.error(f"Failed to create line chart: {e}")
            raise

    def create_bar_chart(
        self,
        data: Union[pd.DataFrame, Dict],
        x_col: str,
        y_col: str,
        title: str,
        xlabel: str,
        ylabel: str,
        output_filename: str,
        use_plotly: bool = False
    ) -> Path:
        """
        棒グラフを生成

        Args:
            data: データ（DataFrameまたは辞書）
            x_col: X軸カラム名
            y_col: Y軸カラム名
            title: グラフタイトル
            xlabel: X軸ラベル
            ylabel: Y軸ラベル
            output_filename: 出力ファイル名
            use_plotly: Plotlyを使用するか

        Returns:
            生成されたファイルのパス
        """
        try:
            # データの準備
            if isinstance(data, dict):
                df = pd.DataFrame(data)
            else:
                df = data

            # ファイル名を安全な形式に変換
            safe_name = safe_filename(output_filename)
            if not safe_name.endswith('.html'):
                safe_name += '.html'

            output_path = self.output_dir / safe_name

            if use_plotly:
                # Plotlyで生成
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=df[x_col],
                    y=df[y_col],
                    name=y_col,
                    marker_color=self.styles['colors'][0],
                    text=df[y_col],
                    textposition='auto'
                ))

                fig.update_layout(
                    title=title,
                    xaxis_title=xlabel,
                    yaxis_title=ylabel,
                    font=dict(
                        family=self.styles.get('font_family', ['Arial'])[0],
                        size=self.styles.get('font_size_axis', 10)
                    ),
                    title_font_size=self.styles.get('font_size_title', 14),
                    showlegend=False
                )

                # HTMLとして保存
                fig.write_html(
                    output_path,
                    include_plotlyjs='cdn',
                    config={'displayModeBar': True}
                )

            else:
                # Matplotlibで生成
                fig, ax = plt.subplots(figsize=self.styles.get('figsize', (10, 6)))

                bars = ax.bar(
                    df[x_col],
                    df[y_col],
                    color=self.styles['colors'][0],
                    alpha=0.8
                )

                # 値をバーの上に表示
                for bar in bars:
                    height = bar.get_height()
                    ax.text(
                        bar.get_x() + bar.get_width()/2.,
                        height,
                        f'{height:.1f}',
                        ha='center',
                        va='bottom',
                        fontsize=self.styles.get('font_size_legend', 9)
                    )

                ax.set_title(title, fontsize=self.styles.get('font_size_title', 14))
                ax.set_xlabel(xlabel, fontsize=self.styles.get('font_size_axis', 10))
                ax.set_ylabel(ylabel, fontsize=self.styles.get('font_size_axis', 10))

                ax.grid(True, alpha=self.styles.get('grid_alpha', 0.3), axis='y')

                # X軸ラベルの回転（必要に応じて）
                plt.xticks(rotation=45, ha='right')

                # タイトなレイアウト
                plt.tight_layout()

                # HTMLとして保存
                output_path = self._save_mpl_figure_to_html(fig, output_path)

            return output_path

        except Exception as e:
            self.logger.error(f"Failed to create bar chart: {e}")
            raise

    def create_custom_figure(
        self,
        drawing_function: Callable,
        output_filename: str,
        **kwargs: Any
    ) -> Path:
        """
        カスタム描画関数を使用して図を生成

        Args:
            drawing_function: 描画関数（ax, colors, styles, **kwargs を受け取る）
            output_filename: 出力ファイル名
            **kwargs: 描画関数に渡す追加の引数

        Returns:
            生成されたファイルのパス
        """
        try:
            # ファイル名を安全な形式に変換
            safe_name = safe_filename(output_filename)
            if not safe_name.endswith('.html'):
                safe_name += '.html'

            output_path = self.output_dir / safe_name

            # 図を作成
            fig, ax = plt.subplots(figsize=self.styles.get('figsize', (10, 6)))

            # カスタム描画関数を実行
            try:
                drawing_function(ax, self.colors, self.styles, **kwargs)
            except Exception as e:
                self.logger.error(f"Error in custom drawing function: {e}")
                raise

            # タイトなレイアウト
            plt.tight_layout()

            # HTMLとして保存
            output_path = self._save_mpl_figure_to_html(fig, output_path)

            return output_path

        except Exception as e:
            self.logger.error(f"Failed to create custom figure: {e}")
            raise

    def create_interactive_plotly_chart(
        self,
        plotly_figure: go.Figure,
        output_filename: str
    ) -> Path:
        """
        PlotlyのFigureオブジェクトをHTMLとして保存

        Args:
            plotly_figure: PlotlyのFigureオブジェクト
            output_filename: 出力ファイル名

        Returns:
            生成されたファイルのパス
        """
        try:
            # ファイル名を安全な形式に変換
            safe_name = safe_filename(output_filename)
            if not safe_name.endswith('.html'):
                safe_name += '.html'

            output_path = self.output_dir / safe_name

            # デフォルトのレイアウト設定を適用
            plotly_figure.update_layout(
                font=dict(
                    family=self.styles.get('font_family', ['Arial'])[0],
                    size=self.styles.get('font_size_axis', 10)
                ),
                title_font_size=self.styles.get('font_size_title', 14)
            )

            # HTMLとして保存
            plotly_figure.write_html(
                output_path,
                include_plotlyjs='cdn',
                config={'displayModeBar': True}
            )

            self.logger.info(f"Interactive chart saved: {output_path}")

            return output_path

        except Exception as e:
            self.logger.error(f"Failed to save Plotly chart: {e}")
            raise

    def create_pie_chart(
        self,
        data: Union[pd.DataFrame, Dict],
        labels_col: str,
        values_col: str,
        title: str,
        output_filename: str,
        use_plotly: bool = False
    ) -> Path:
        """
        円グラフを生成

        Args:
            data: データ（DataFrameまたは辞書）
            labels_col: ラベルカラム名
            values_col: 値カラム名
            title: グラフタイトル
            output_filename: 出力ファイル名
            use_plotly: Plotlyを使用するか

        Returns:
            生成されたファイルのパス
        """
        try:
            # データの準備
            if isinstance(data, dict):
                df = pd.DataFrame(data)
            else:
                df = data

            # ファイル名を安全な形式に変換
            safe_name = safe_filename(output_filename)
            if not safe_name.endswith('.html'):
                safe_name += '.html'

            output_path = self.output_dir / safe_name

            if use_plotly:
                # Plotlyで生成
                fig = go.Figure(data=[go.Pie(
                    labels=df[labels_col],
                    values=df[values_col],
                    hole=.3,
                    marker=dict(colors=self.styles['colors'])
                )])

                fig.update_layout(
                    title=title,
                    font=dict(
                        family=self.styles.get('font_family', ['Arial'])[0],
                        size=self.styles.get('font_size_axis', 10)
                    ),
                    title_font_size=self.styles.get('font_size_title', 14)
                )

                # HTMLとして保存
                fig.write_html(
                    output_path,
                    include_plotlyjs='cdn',
                    config={'displayModeBar': True}
                )

            else:
                # Matplotlibで生成
                fig, ax = plt.subplots(figsize=(8, 8))

                wedges, texts, autotexts = ax.pie(
                    df[values_col],
                    labels=df[labels_col],
                    colors=self.styles['colors'][:len(df)],
                    autopct='%1.1f%%',
                    startangle=90
                )

                # テキストのフォントサイズ設定
                for text in texts:
                    text.set_fontsize(self.styles.get('font_size_legend', 9))
                for autotext in autotexts:
                    autotext.set_fontsize(self.styles.get('font_size_legend', 9))
                    autotext.set_color('white')
                    autotext.set_weight('bold')

                ax.set_title(title, fontsize=self.styles.get('font_size_title', 14))

                # HTMLとして保存
                output_path = self._save_mpl_figure_to_html(fig, output_path)

            return output_path

        except Exception as e:
            self.logger.error(f"Failed to create pie chart: {e}")
            raise

    def create_scatter_plot(
        self,
        data: Union[pd.DataFrame, Dict],
        x_col: str,
        y_col: str,
        title: str,
        xlabel: str,
        ylabel: str,
        output_filename: str,
        color_col: Optional[str] = None,
        size_col: Optional[str] = None,
        use_plotly: bool = False
    ) -> Path:
        """
        散布図を生成

        Args:
            data: データ（DataFrameまたは辞書）
            x_col: X軸カラム名
            y_col: Y軸カラム名
            title: グラフタイトル
            xlabel: X軸ラベル
            ylabel: Y軸ラベル
            output_filename: 出力ファイル名
            color_col: 色分けカラム名（オプション）
            size_col: サイズカラム名（オプション）
            use_plotly: Plotlyを使用するか

        Returns:
            生成されたファイルのパス
        """
        try:
            # データの準備
            if isinstance(data, dict):
                df = pd.DataFrame(data)
            else:
                df = data

            # ファイル名を安全な形式に変換
            safe_name = safe_filename(output_filename)
            if not safe_name.endswith('.html'):
                safe_name += '.html'

            output_path = self.output_dir / safe_name

            if use_plotly:
                # Plotlyで生成
                fig = go.Figure()

                fig.add_trace(go.Scatter(
                    x=df[x_col],
                    y=df[y_col],
                    mode='markers',
                    marker=dict(
                        size=df[size_col] if size_col else 8,
                        color=df[color_col] if color_col else self.styles['colors'][0],
                        colorscale='Viridis' if color_col else None,
                        showscale=True if color_col else False
                    ),
                    text=df.index,
                    hovertemplate='%{text}<br>X: %{x}<br>Y: %{y}<extra></extra>'
                ))

                fig.update_layout(
                    title=title,
                    xaxis_title=xlabel,
                    yaxis_title=ylabel,
                    font=dict(
                        family=self.styles.get('font_family', ['Arial'])[0],
                        size=self.styles.get('font_size_axis', 10)
                    ),
                    title_font_size=self.styles.get('font_size_title', 14)
                )

                # HTMLとして保存
                fig.write_html(
                    output_path,
                    include_plotlyjs='cdn',
                    config={'displayModeBar': True}
                )

            else:
                # Matplotlibで生成
                fig, ax = plt.subplots(figsize=self.styles.get('figsize', (10, 6)))

                scatter = ax.scatter(
                    df[x_col],
                    df[y_col],
                    c=df[color_col] if color_col else self.styles['colors'][0],
                    s=df[size_col] if size_col else 50,
                    alpha=0.6,
                    cmap='viridis' if color_col else None
                )

                if color_col:
                    cbar = plt.colorbar(scatter, ax=ax)
                    cbar.set_label(color_col, fontsize=self.styles.get('font_size_axis', 10))

                ax.set_title(title, fontsize=self.styles.get('font_size_title', 14))
                ax.set_xlabel(xlabel, fontsize=self.styles.get('font_size_axis', 10))
                ax.set_ylabel(ylabel, fontsize=self.styles.get('font_size_axis', 10))

                ax.grid(True, alpha=self.styles.get('grid_alpha', 0.3))

                # タイトなレイアウト
                plt.tight_layout()

                # HTMLとして保存
                output_path = self._save_mpl_figure_to_html(fig, output_path)

            return output_path

        except Exception as e:
            self.logger.error(f"Failed to create scatter plot: {e}")
            raise
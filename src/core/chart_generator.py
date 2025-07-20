"""
様々な種類の図表を生成し、HTMLファイルとして出力
Matplotlib/Seaborn、Plotlyをサポートし、インタラクティブ要素に対応
"""

import io
import base64
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.io as pio
from PIL import Image
import imageio

from .utils import apply_matplotlib_japanese_font, slugify
from .config import GLOBAL_COLORS, BASE_CHART_STYLES

logger = logging.getLogger(__name__)


class ChartGenerator:
    """図表生成クラス"""
    
    def __init__(self, colors: Dict[str, str] = None, styles: Dict[str, Any] = None):
        """
        初期化
        
        Args:
            colors: カスタムカラーパレット
            styles: カスタムスタイル設定
        """
        self.colors = colors or GLOBAL_COLORS
        self.styles = styles or BASE_CHART_STYLES
        
        # 日本語フォント設定を適用
        apply_matplotlib_japanese_font(self.styles.get("font_family"))
        
        # Seabornのスタイル設定
        sns.set_style("whitegrid")
        sns.set_palette("husl")
        
    def _save_mpl_figure_to_html(
        self, fig: plt.Figure, output_path: Path, embed_png: bool = True
    ) -> None:
        """
        MatplotlibのFigureをHTMLファイルとして保存
        
        Args:
            fig: Matplotlib Figureオブジェクト
            output_path: 出力先パス
            embed_png: PNG画像を埋め込むか
        """
        try:
            # PNGをBase64エンコード
            buffer = io.BytesIO()
            fig.savefig(
                buffer, 
                format='png', 
                dpi=self.styles.get("figure_dpi", 150),
                bbox_inches='tight',
                transparent=self.styles.get("transparent_bg", False)
            )
            buffer.seek(0)
            img_base64 = base64.b64encode(buffer.read()).decode()
            
            # HTML生成
            html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{
            margin: 0;
            padding: 20px;
            font-family: sans-serif;
            background-color: #f5f5f5;
        }}
        .chart-container {{
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
        }}
        img {{
            max-width: 100%;
            height: auto;
            display: inline-block;
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
            # ファイル保存
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(html_content, encoding='utf-8')
            
            logger.info(f"図表HTMLを保存しました: {output_path}")
            
        except Exception as e:
            logger.error(f"図表の保存中にエラーが発生しました: {e}")
            raise
        finally:
            plt.close(fig)
            
    def create_simple_line_chart(
        self,
        data: Dict[str, List[Any]],
        x_col: str,
        y_col: str,
        title: str,
        xlabel: str,
        ylabel: str,
        output_filename: str = "line_chart.html",
        use_plotly: bool = False
    ) -> Path:
        """
        シンプルな折れ線グラフを生成
        
        Args:
            data: データ辞書
            x_col: X軸のカラム名
            y_col: Y軸のカラム名
            title: グラフタイトル
            xlabel: X軸ラベル
            ylabel: Y軸ラベル
            output_filename: 出力ファイル名
            use_plotly: Plotlyを使用するか
            
        Returns:
            生成されたファイルのパス
        """
        # ファイル名をスラッグ化
        safe_filename = slugify(output_filename.replace('.html', '')) + '.html'
        output_path = Path(safe_filename)
        
        try:
            if use_plotly:
                # Plotlyで生成
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=data[x_col],
                    y=data[y_col],
                    mode='lines+markers',
                    name=y_col,
                    line=dict(width=self.styles["line_width"]),
                    marker=dict(size=self.styles["marker_size"])
                ))
                
                fig.update_layout(
                    title=title,
                    xaxis_title=xlabel,
                    yaxis_title=ylabel,
                    hovermode='x unified',
                    width=None,  # 相対幅を使用
                    height=500,
                    margin=dict(l=50, r=50, t=50, b=50),
                    plot_bgcolor='white',
                    paper_bgcolor='#f5f5f5'
                )
                
                # HTMLとして保存
                fig.write_html(
                    output_path,
                    include_plotlyjs='cdn',
                    config={'responsive': True}
                )
                
            else:
                # Matplotlibで生成
                fig, ax = plt.subplots(figsize=self.styles["figsize"])
                ax.plot(
                    data[x_col], 
                    data[y_col],
                    linewidth=self.styles["line_width"],
                    marker='o',
                    markersize=self.styles["marker_size"]
                )
                
                ax.set_title(title, fontsize=self.styles["font_size_title"])
                ax.set_xlabel(xlabel, fontsize=self.styles["font_size_label"])
                ax.set_ylabel(ylabel, fontsize=self.styles["font_size_label"])
                ax.grid(True, alpha=self.styles["grid_alpha"])
                
                plt.tight_layout()
                self._save_mpl_figure_to_html(fig, output_path)
                
            return output_path
            
        except Exception as e:
            logger.error(f"折れ線グラフの生成中にエラーが発生しました: {e}")
            raise
            
    def create_bar_chart(
        self,
        data: Dict[str, List[Any]],
        x_col: str,
        y_col: str,
        title: str,
        xlabel: str,
        ylabel: str,
        output_filename: str = "bar_chart.html",
        use_plotly: bool = False
    ) -> Path:
        """
        棒グラフを生成
        
        Args:
            data: データ辞書
            x_col: X軸のカラム名
            y_col: Y軸のカラム名
            title: グラフタイトル
            xlabel: X軸ラベル
            ylabel: Y軸ラベル
            output_filename: 出力ファイル名
            use_plotly: Plotlyを使用するか
            
        Returns:
            生成されたファイルのパス
        """
        # ファイル名をスラッグ化
        safe_filename = slugify(output_filename.replace('.html', '')) + '.html'
        output_path = Path(safe_filename)
        
        try:
            if use_plotly:
                # Plotlyで生成
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=data[x_col],
                    y=data[y_col],
                    name=y_col,
                    marker_color=self.colors["info"]
                ))
                
                fig.update_layout(
                    title=title,
                    xaxis_title=xlabel,
                    yaxis_title=ylabel,
                    showlegend=False,
                    width=None,
                    height=500,
                    margin=dict(l=50, r=50, t=50, b=50),
                    plot_bgcolor='white',
                    paper_bgcolor='#f5f5f5'
                )
                
                # HTMLとして保存
                fig.write_html(
                    output_path,
                    include_plotlyjs='cdn',
                    config={'responsive': True}
                )
                
            else:
                # Matplotlibで生成
                fig, ax = plt.subplots(figsize=self.styles["figsize"])
                ax.bar(
                    data[x_col], 
                    data[y_col],
                    color=self.colors["info"]
                )
                
                ax.set_title(title, fontsize=self.styles["font_size_title"])
                ax.set_xlabel(xlabel, fontsize=self.styles["font_size_label"])
                ax.set_ylabel(ylabel, fontsize=self.styles["font_size_label"])
                ax.grid(True, alpha=self.styles["grid_alpha"], axis='y')
                
                plt.tight_layout()
                self._save_mpl_figure_to_html(fig, output_path)
                
            return output_path
            
        except Exception as e:
            logger.error(f"棒グラフの生成中にエラーが発生しました: {e}")
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
            drawing_function: 描画関数 (ax, colors, styles, **kwargs) -> None
            output_filename: 出力ファイル名
            **kwargs: 描画関数に渡す追加引数
            
        Returns:
            生成されたファイルのパス
        """
        # ファイル名をスラッグ化
        safe_filename = slugify(output_filename.replace('.html', '')) + '.html'
        output_path = Path(safe_filename)
        
        try:
            fig, ax = plt.subplots(figsize=self.styles["figsize"])
            
            # カスタム描画関数を実行
            drawing_function(ax, self.colors, self.styles, **kwargs)
            
            plt.tight_layout()
            self._save_mpl_figure_to_html(fig, output_path)
            
            return output_path
            
        except Exception as e:
            logger.error(f"カスタム図の生成中にエラーが発生しました: {e}")
            raise
            
    def create_interactive_plotly_chart(
        self, plotly_figure: go.Figure, output_filename: str
    ) -> Path:
        """
        PlotlyのFigureオブジェクトをHTMLファイルとして保存
        
        Args:
            plotly_figure: Plotly Figureオブジェクト
            output_filename: 出力ファイル名
            
        Returns:
            生成されたファイルのパス
        """
        # ファイル名をスラッグ化
        safe_filename = slugify(output_filename.replace('.html', '')) + '.html'
        output_path = Path(safe_filename)
        
        try:
            # レスポンシブ設定
            plotly_figure.update_layout(
                width=None,
                height=600,
                margin=dict(l=50, r=50, t=50, b=50)
            )
            
            # HTMLとして保存
            plotly_figure.write_html(
                output_path,
                include_plotlyjs='cdn',
                config={'responsive': True}
            )
            
            logger.info(f"インタラクティブ図表を保存しました: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Plotly図表の保存中にエラーが発生しました: {e}")
            raise
            
    def create_animation_gif(
        self, frames: List[Any], output_filename: str, fps: int = 10
    ) -> Path:
        """
        アニメーションGIFを生成
        
        Args:
            frames: フレームのリスト（Matplotlib FigureまたはPIL Image）
            output_filename: 出力ファイル名
            fps: フレームレート
            
        Returns:
            生成されたファイルのパス
        """
        # ファイル名をスラッグ化
        safe_filename = slugify(output_filename.replace('.gif', '')) + '.gif'
        output_path = Path(safe_filename)
        
        try:
            images = []
            
            for frame in frames:
                if isinstance(frame, plt.Figure):
                    # MatplotlibのFigureをPIL Imageに変換
                    buffer = io.BytesIO()
                    frame.savefig(
                        buffer, 
                        format='png',
                        dpi=self.styles.get("figure_dpi", 150),
                        bbox_inches='tight'
                    )
                    buffer.seek(0)
                    img = Image.open(buffer)
                    images.append(img)
                    plt.close(frame)
                elif isinstance(frame, Image.Image):
                    images.append(frame)
                else:
                    logger.warning(f"未対応のフレームタイプ: {type(frame)}")
                    
            # GIFとして保存
            if images:
                imageio.mimsave(output_path, images, fps=fps)
                logger.info(f"アニメーションGIFを保存しました: {output_path}")
                
            return output_path
            
        except Exception as e:
            logger.error(f"アニメーションGIFの生成中にエラーが発生しました: {e}")
            raise
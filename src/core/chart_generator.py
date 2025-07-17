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
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            body {{
                font-family: {self.styles.get("font_family", ["Arial"])[0]};
                background-color: #ffffff;
                padding: 10px;
                height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }}
            .chart-container {{
                width: 100%;
                height: 100%;
                display: flex;
                align-items: center;
                justify-content: center;
                background: white;
            }}
            .chart-image {{
                max-width: 100%;
                max-height: 100%;
                width: auto;
                height: auto;
                object-fit: contain;
                border: none;
            }}
            @media (max-width: 768px) {{
                body {{
                    padding: 5px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="chart-container">
            <img src="data:image/png;base64,{img_base64}" alt="Chart" class="chart-image">
        </div>
    </body>
    </html>
    """
            
            # HTMLファイルに保存
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            self.logger.info(f"Chart saved as HTML: {output_path}")
            
            # 図を閉じる
            plt.close(fig)
            
            return output_path
            
        except Exception as e:
            self.logger.error(f"Failed to save chart as HTML: {e}")
            plt.close(fig)
            raise


    def create_simple_line_chart(
        self, 
        data: Union[pd.DataFrame, Dict[str, List]], 
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
            data: データ（DataFrame or Dict）
            x_col: X軸の列名
            y_col: Y軸の列名
            title: グラフタイトル
            xlabel: X軸ラベル
            ylabel: Y軸ラベル
            output_filename: 出力ファイル名
            use_plotly: Plotlyを使用するかどうか
            
        Returns:
            保存されたファイルのパス
        """
        try:
            # データの準備
            if isinstance(data, dict):
                df = pd.DataFrame(data)
            else:
                df = data
            
            # 安全なファイル名
            safe_name = safe_filename(output_filename)
            if not safe_name.endswith('.html'):
                safe_name += '.html'
            
            output_path = self.output_dir / safe_name
            
            if use_plotly:
                # Plotlyで作成
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=df[x_col],
                    y=df[y_col],
                    mode='lines+markers',
                    name=y_col,
                    line=dict(color=self.colors.get("primary", "#1976d2"), width=self.styles.get("line_width", 2)),
                    marker=dict(size=self.styles.get("marker_size", 6))
                ))
                
                fig.update_layout(
                    title=title,
                    xaxis_title=xlabel,
                    yaxis_title=ylabel,
                    font=dict(family=self.styles.get("font_family", ["Arial"])[0], size=self.styles.get("font_size_axis", 10)),
                    showlegend=True,
                    plot_bgcolor='white',
                    paper_bgcolor='white'
                )
                
                return self.create_interactive_plotly_chart(fig, safe_name)
            
            else:
                # Matplotlibで作成
                fig, ax = plt.subplots(figsize=self.styles.get("figsize", (10, 6)))
                
                ax.plot(
                    df[x_col], 
                    df[y_col], 
                    color=self.colors.get("primary", "#1976d2"),
                    linewidth=self.styles.get("line_width", 2),
                    marker='o',
                    markersize=self.styles.get("marker_size", 6)
                )
                
                ax.set_title(title, fontsize=self.styles.get("font_size_title", 14))
                ax.set_xlabel(xlabel, fontsize=self.styles.get("font_size_axis", 10))
                ax.set_ylabel(ylabel, fontsize=self.styles.get("font_size_axis", 10))
                ax.grid(True, alpha=self.styles.get("grid_alpha", 0.3))
                
                return self._save_mpl_figure_to_html(fig, output_path)
                
        except Exception as e:
            self.logger.error(f"Failed to create line chart: {e}")
            raise
    
    def create_bar_chart(
        self, 
        data: Union[pd.DataFrame, Dict[str, List]], 
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
            data: データ（DataFrame or Dict）
            x_col: X軸の列名
            y_col: Y軸の列名
            title: グラフタイトル
            xlabel: X軸ラベル
            ylabel: Y軸ラベル
            output_filename: 出力ファイル名
            use_plotly: Plotlyを使用するかどうか
            
        Returns:
            保存されたファイルのパス
        """
        try:
            # データの準備
            if isinstance(data, dict):
                df = pd.DataFrame(data)
            else:
                df = data
            
            # 安全なファイル名
            safe_name = safe_filename(output_filename)
            if not safe_name.endswith('.html'):
                safe_name += '.html'
            
            output_path = self.output_dir / safe_name
            
            if use_plotly:
                # Plotlyで作成
                fig = go.Figure()
                
                fig.add_trace(go.Bar(
                    x=df[x_col],
                    y=df[y_col],
                    name=y_col,
                    marker=dict(color=self.colors.get("primary", "#1976d2"))
                ))
                
                fig.update_layout(
                    title=title,
                    xaxis_title=xlabel,
                    yaxis_title=ylabel,
                    font=dict(family=self.styles.get("font_family", ["Arial"])[0], size=self.styles.get("font_size_axis", 10)),
                    showlegend=False,
                    plot_bgcolor='white',
                    paper_bgcolor='white'
                )
                
                return self.create_interactive_plotly_chart(fig, safe_name)
            
            else:
                # Matplotlibで作成
                fig, ax = plt.subplots(figsize=self.styles.get("figsize", (10, 6)))
                
                bars = ax.bar(
                    df[x_col], 
                    df[y_col], 
                    color=self.colors.get("primary", "#1976d2"),
                    alpha=0.7
                )
                
                ax.set_title(title, fontsize=self.styles.get("font_size_title", 14))
                ax.set_xlabel(xlabel, fontsize=self.styles.get("font_size_axis", 10))
                ax.set_ylabel(ylabel, fontsize=self.styles.get("font_size_axis", 10))
                ax.grid(True, alpha=self.styles.get("grid_alpha", 0.3))
                
                return self._save_mpl_figure_to_html(fig, output_path)
                
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
            **kwargs: 描画関数に渡す追加引数
            
        Returns:
            保存されたファイルのパス
        """
        try:
            # 安全なファイル名
            safe_name = safe_filename(output_filename)
            if not safe_name.endswith('.html'):
                safe_name += '.html'
            
            output_path = self.output_dir / safe_name
            
            # 図を作成
            fig, ax = plt.subplots(figsize=self.styles.get("figsize", (10, 6)))
            
            # 描画関数を呼び出し
            drawing_function(ax=ax, colors=self.colors, styles=self.styles, **kwargs)
            
            return self._save_mpl_figure_to_html(fig, output_path)
            
        except Exception as e:
            self.logger.error(f"Failed to create custom figure: {e}")
            raise
    
    def create_interactive_plotly_chart(
        self, 
        plotly_figure: go.Figure, 
        output_filename: str
    ) -> Path:
        """
        PlotlyのFigureオブジェクトをインタラクティブなHTMLファイルとして保存
        
        Args:
            plotly_figure: PlotlyのFigureオブジェクト
            output_filename: 出力ファイル名
            
        Returns:
            保存されたファイルのパス
        """
        try:
            # 安全なファイル名
            safe_name = safe_filename(output_filename)
            if not safe_name.endswith('.html'):
                safe_name += '.html'
            
            output_path = self.output_dir / safe_name
            
            # HTMLファイルとして保存
            pio.write_html(
                plotly_figure, 
                str(output_path),
                full_html=True,
                include_plotlyjs='cdn',
                config={'displayModeBar': True, 'responsive': True}
            )
            
            self.logger.info(f"Interactive chart saved: {output_path}")
            
            return output_path
            
        except Exception as e:
            self.logger.error(f"Failed to create interactive chart: {e}")
            raise
    
    def create_pie_chart(
        self, 
        data: Union[pd.DataFrame, Dict[str, List]], 
        labels_col: str, 
        values_col: str, 
        title: str, 
        output_filename: str,
        use_plotly: bool = False
    ) -> Path:
        """
        円グラフを生成
        
        Args:
            data: データ（DataFrame or Dict）
            labels_col: ラベル列名
            values_col: 値列名
            title: グラフタイトル
            output_filename: 出力ファイル名
            use_plotly: Plotlyを使用するかどうか
            
        Returns:
            保存されたファイルのパス
        """
        try:
            # データの準備
            if isinstance(data, dict):
                df = pd.DataFrame(data)
            else:
                df = data
            
            # 安全なファイル名
            safe_name = safe_filename(output_filename)
            if not safe_name.endswith('.html'):
                safe_name += '.html'
            
            output_path = self.output_dir / safe_name
            
            if use_plotly:
                # Plotlyで作成
                fig = go.Figure()
                
                fig.add_trace(go.Pie(
                    labels=df[labels_col],
                    values=df[values_col],
                    name=title
                ))
                
                fig.update_layout(
                    title=title,
                    font=dict(family=self.styles.get("font_family", ["Arial"])[0], size=self.styles.get("font_size_axis", 10)),
                    showlegend=True
                )
                
                return self.create_interactive_plotly_chart(fig, safe_name)
            
            else:
                # Matplotlibで作成
                fig, ax = plt.subplots(figsize=self.styles.get("figsize", (10, 6)))
                
                colors = self.styles.get("colors", ["#1976d2", "#4caf50", "#ff9800", "#f44336"])
                
                wedges, texts, autotexts = ax.pie(
                    df[values_col], 
                    labels=df[labels_col], 
                    colors=colors,
                    autopct='%1.1f%%',
                    startangle=90
                )
                
                ax.set_title(title, fontsize=self.styles.get("font_size_title", 14))
                
                return self._save_mpl_figure_to_html(fig, output_path)
                
        except Exception as e:
            self.logger.error(f"Failed to create pie chart: {e}")
            raise
    
    def create_heatmap(
        self, 
        data: Union[pd.DataFrame, np.ndarray], 
        title: str, 
        output_filename: str,
        use_plotly: bool = False
    ) -> Path:
        """
        ヒートマップを生成
        
        Args:
            data: データ（DataFrame or ndarray）
            title: グラフタイトル
            output_filename: 出力ファイル名
            use_plotly: Plotlyを使用するかどうか
            
        Returns:
            保存されたファイルのパス
        """
        try:
            # 安全なファイル名
            safe_name = safe_filename(output_filename)
            if not safe_name.endswith('.html'):
                safe_name += '.html'
            
            output_path = self.output_dir / safe_name
            
            if use_plotly:
                # Plotlyで作成
                fig = go.Figure()
                
                if isinstance(data, pd.DataFrame):
                    fig.add_trace(go.Heatmap(
                        z=data.values,
                        x=data.columns,
                        y=data.index,
                        colorscale='Viridis'
                    ))
                else:
                    fig.add_trace(go.Heatmap(
                        z=data,
                        colorscale='Viridis'
                    ))
                
                fig.update_layout(
                    title=title,
                    font=dict(family=self.styles.get("font_family", ["Arial"])[0], size=self.styles.get("font_size_axis", 10))
                )
                
                return self.create_interactive_plotly_chart(fig, safe_name)
            
            else:
                # Matplotlibで作成
                fig, ax = plt.subplots(figsize=self.styles.get("figsize", (10, 6)))
                
                if isinstance(data, pd.DataFrame):
                    sns.heatmap(data, ax=ax, cmap='viridis', annot=True, fmt='.2f')
                else:
                    sns.heatmap(data, ax=ax, cmap='viridis', annot=True, fmt='.2f')
                
                ax.set_title(title, fontsize=self.styles.get("font_size_title", 14))
                
                return self._save_mpl_figure_to_html(fig, output_path)
                
        except Exception as e:
            self.logger.error(f"Failed to create heatmap: {e}")
            raise
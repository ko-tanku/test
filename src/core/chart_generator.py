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
        
        # 日本語フォント設定を適用
        apply_matplotlib_japanese_font(self.styles.get("font_family"))
        
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
        use_plotly: bool = False,
        output_dir: Path = None  # この引数を追加
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
            output_dir: 出力ディレクトリ
            
        Returns:
            生成されたファイルのパス
        """
        # ファイル名をスラッグ化
        safe_filename = slugify(output_filename.replace('.html', '')) + '.html'
        
        if output_dir:
            output_path = output_dir / safe_filename
        else:
            output_path = Path(safe_filename)
        print(f"⭐{output_path}")
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
        use_plotly: bool = False,
        output_dir: Path = None  # この引数を追加
    ) -> Path:
    # 同様の修正
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
        
        if output_dir:
            output_path = output_dir / safe_filename
        else:
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
        output_dir: Path = None,  # この引数を追加
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
        
        if output_dir:
            output_path = output_dir / safe_filename
        else:
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
        self, plotly_figure: go.Figure, output_filename: str,
        output_dir: Path = None,
    ) -> Path:
        """
        PlotlyのFigureオブジェクトをHTMLファイルとして保存
        
        Args:
            plotly_figure: Plotly Figureオブジェクト
            output_filename: 出力ファイル名
            
        Returns:
            生成されたファイルのパス
        """
        safe_filename = slugify(output_filename.replace('.html', '')) + '.html'
        
        if output_dir:
            output_path = output_dir / safe_filename
        else:
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
        self, frames: List[Any], output_filename: str, fps: int = 10, output_dir: Path = None,
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
        safe_filename = slugify(output_filename.replace('.gif', '')) + '.gif'
        
        if output_dir:
            output_path = output_dir / safe_filename
        else:
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
# 既存のメソッドに加えて以下を追加

    def create_scatter_chart(
        self,
        data: Dict[str, List[Any]],
        x_col: str,
        y_col: str,
        title: str,
        xlabel: str,
        ylabel: str,
        output_filename: str = "scatter_chart.html",
        use_plotly: bool = False,
        output_dir: Path = None
    ) -> Path:
        """散布図を生成"""
        safe_filename = slugify(output_filename.replace('.html', '')) + '.html'
        
        if output_dir:
            output_path = output_dir / safe_filename
        else:
            output_path = Path(safe_filename)
        
        try:
            if use_plotly:
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=data[x_col],
                    y=data[y_col],
                    mode='markers',
                    marker=dict(
                        size=10,
                        color=self.colors["info"],
                        line=dict(width=1, color='DarkSlateGrey')
                    )
                ))
                
                fig.update_layout(
                    title=title,
                    xaxis_title=xlabel,
                    yaxis_title=ylabel,
                    width=None,
                    height=450,
                    margin=dict(l=50, r=50, t=50, b=50)
                )
                
                fig.write_html(
                    output_path,
                    include_plotlyjs='cdn',
                    config={'responsive': True}
                )
            else:
                fig, ax = plt.subplots(figsize=self.styles["figsize"])
                ax.scatter(
                    data[x_col], 
                    data[y_col],
                    s=50,
                    color=self.colors["info"],
                    alpha=0.6
                )
                
                ax.set_title(title, fontsize=self.styles["font_size_title"])
                ax.set_xlabel(xlabel, fontsize=self.styles["font_size_label"])
                ax.set_ylabel(ylabel, fontsize=self.styles["font_size_label"])
                ax.grid(True, alpha=self.styles["grid_alpha"])
                
                plt.tight_layout()
                self._save_mpl_figure_to_html(fig, output_path)
                
            return output_path
            
        except Exception as e:
            logger.error(f"散布図の生成中にエラーが発生しました: {e}")
            raise

    def create_pie_chart(
        self,
        data: Dict[str, List[Any]],
        values_col: str,
        labels_col: str,
        title: str,
        output_filename: str = "pie_chart.html",
        use_plotly: bool = False,
        output_dir: Path = None
    ) -> Path:
        """円グラフを生成"""
        safe_filename = slugify(output_filename.replace('.html', '')) + '.html'
        
        if output_dir:
            output_path = output_dir / safe_filename
        else:
            output_path = Path(safe_filename)
        
        try:
            if use_plotly:
                fig = go.Figure(data=[go.Pie(
                    labels=data[labels_col],
                    values=data[values_col],
                    hole=0.3  # ドーナツチャート
                )])
                
                fig.update_layout(
                    title=title,
                    width=None,
                    height=450,
                    margin=dict(l=50, r=50, t=50, b=50)
                )
                
                fig.write_html(
                    output_path,
                    include_plotlyjs='cdn',
                    config={'responsive': True}
                )
            else:
                fig, ax = plt.subplots(figsize=(6, 6))
                ax.pie(
                    data[values_col],
                    labels=data[labels_col],
                    autopct='%1.1f%%',
                    startangle=90
                )
                
                ax.set_title(title, fontsize=self.styles["font_size_title"])
                
                plt.tight_layout()
                self._save_mpl_figure_to_html(fig, output_path)
                
            return output_path
            
        except Exception as e:
            logger.error(f"円グラフの生成中にエラーが発生しました: {e}")
            raise

    def create_state_transition_chart(
        self, data: Dict, config: Dict, output_filename: str, output_dir: Path = None
    ) -> Path:
        """状態遷移インタラクティブチャート"""
        safe_filename = slugify(output_filename.replace('.html', '')) + '.html'
        
        if output_dir:
            output_path = output_dir / safe_filename
        else:
            output_path = Path(safe_filename)
        
        try:
            fig = go.Figure()
            
            # データから状態を抽出
            states = data.get('states', [])
            
            # 各状態のトレースを追加
            for i, state in enumerate(states):
                fig.add_trace(go.Bar(
                    x=state['x'],
                    y=state['y'],
                    name=state['name'],
                    visible=(i == 0)  # 最初の状態のみ表示
                ))
            
            # ボタンの作成
            buttons = []
            for i, state in enumerate(states):
                visible = [False] * len(states)
                visible[i] = True
                buttons.append(dict(
                    label=state['name'],
                    method="update",
                    args=[{"visible": visible}]
                ))
            
            fig.update_layout(
                title=config.get('title', '状態遷移デモ'),
                updatemenus=[dict(
                    buttons=buttons,
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.1,
                    xanchor="left",
                    y=1.15,
                    yanchor="top"
                )],
                xaxis_title=config.get('xlabel', ''),
                yaxis_title=config.get('ylabel', ''),
                width=None,
                height=450,
                margin=dict(l=50, r=50, t=80, b=50)
            )
            
            fig.write_html(
                output_path,
                include_plotlyjs='cdn',
                config={'responsive': True}
            )
            
            return output_path
            
        except Exception as e:
            logger.error(f"状態遷移チャートの生成中にエラーが発生しました: {e}")
            raise

    def create_dropdown_filter_chart(
        self, data: Dict, config: Dict, output_filename: str, output_dir: Path = None
    ) -> Path:
        """ドロップダウンフィルタ付きチャート"""
        safe_filename = slugify(output_filename.replace('.html', '')) + '.html'
        
        if output_dir:
            output_path = output_dir / safe_filename
        else:
            output_path = Path(safe_filename)
        
        try:
            fig = go.Figure()
            
            # データセットを取得
            datasets = data.get('datasets', {})
            
            # 全データセットのトレースを追加
            for i, (name, dataset) in enumerate(datasets.items()):
                fig.add_trace(go.Scatter(
                    x=dataset['x'],
                    y=dataset['y'],
                    mode='lines+markers',
                    name=name,
                    visible=(i == 0),
                    line=dict(width=3),
                    marker=dict(size=10)
                ))
            
            # ドロップダウンメニューの作成
            dropdown_buttons = []
            for i, name in enumerate(datasets.keys()):
                visible = [False] * len(datasets)
                visible[i] = True
                dropdown_buttons.append(dict(
                    label=name,
                    method="update",
                    args=[{"visible": visible}, {"title": f"{name}のデータ"}]
                ))
            
            fig.update_layout(
                title=list(datasets.keys())[0] + "のデータ",
                updatemenus=[dict(
                    buttons=dropdown_buttons,
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=1.0,
                    xanchor="right",
                    y=1.15,
                    yanchor="top"
                )],
                xaxis_title=config.get('xlabel', ''),
                yaxis_title=config.get('ylabel', ''),
                width=None,
                height=450,
                margin=dict(l=50, r=50, t=80, b=50)
            )
            
            fig.write_html(
                output_path,
                include_plotlyjs='cdn',
                config={'responsive': True}
            )
            
            return output_path
            
        except Exception as e:
            logger.error(f"ドロップダウンフィルタチャートの生成中にエラーが発生しました: {e}")
            raise

    def create_slider_chart(
        self, data: Dict, config: Dict, output_filename: str, output_dir: Path = None
    ) -> Path:
        """スライダー付きチャート"""
        safe_filename = slugify(output_filename.replace('.html', '')) + '.html'
        
        if output_dir:
            output_path = output_dir / safe_filename
        else:
            output_path = Path(safe_filename)
        
        try:
            fig = go.Figure()
            
            # パラメータとデータ
            x = np.array(data.get('x', []))
            parameters = data.get('parameters', [])
            
            # 各パラメータでのトレースを追加
            for i, param in enumerate(parameters):
                y = param['function'](x)
                fig.add_trace(go.Scatter(
                    x=x,
                    y=y,
                    mode='lines',
                    name=param['name'],
                    visible=(i == 0)
                ))
            
            # スライダーの作成
            steps = []
            for i, param in enumerate(parameters):
                visible = [False] * len(parameters)
                visible[i] = True
                step = dict(
                    method="update",
                    args=[{"visible": visible}],
                    label=param['label']
                )
                steps.append(step)
            
            sliders = [dict(
                active=0,
                currentvalue={"prefix": config.get('slider_prefix', 'パラメータ: ')},
                pad={"t": 50},
                steps=steps
            )]
            
            fig.update_layout(
                title=config.get('title', 'スライダーデモ'),
                sliders=sliders,
                xaxis_title=config.get('xlabel', ''),
                yaxis_title=config.get('ylabel', ''),
                width=None,
                height=450,
                margin=dict(l=50, r=50, t=50, b=100)
            )
            
            fig.write_html(
                output_path,
                include_plotlyjs='cdn',
                config={'responsive': True}
            )
            
            return output_path
            
        except Exception as e:
            logger.error(f"スライダーチャートの生成中にエラーが発生しました: {e}")
            raise

    def create_hover_details_chart(
        self, data: Dict, config: Dict, output_filename: str, output_dir: Path = None
    ) -> Path:
        """ホバー詳細表示チャート"""
        safe_filename = slugify(output_filename.replace('.html', '')) + '.html'
        
        if output_dir:
            output_path = output_dir / safe_filename
        else:
            output_path = Path(safe_filename)
        
        try:
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=data['x'],
                y=data['y'],
                mode='markers',
                marker=dict(
                    size=data.get('size', [10] * len(data['x'])),
                    color=data.get('color', data['y']),
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title=config.get('colorbar_title', '値'))
                ),
                text=data.get('labels', [f"Point {i+1}" for i in range(len(data['x']))]),
                hovertemplate='<b>%{text}</b><br>' +
                            f'{config.get("x_label", "X")}: %{{x:.2f}}<br>' +
                            f'{config.get("y_label", "Y")}: %{{y:.2f}}<br>' +
                            'サイズ: %{marker.size}<br>' +
                            '<extra></extra>'
            ))
            
            fig.update_layout(
                title=config.get('title', 'ホバー詳細表示'),
                xaxis_title=config.get('xlabel', ''),
                yaxis_title=config.get('ylabel', ''),
                hovermode='closest',
                width=None,
                height=450,
                margin=dict(l=50, r=50, t=50, b=50)
            )
            
            fig.write_html(
                output_path,
                include_plotlyjs='cdn',
                config={'responsive': True}
            )
            
            return output_path
            
        except Exception as e:
            logger.error(f"ホバー詳細チャートの生成中にエラーが発生しました: {e}")
            raise

    def create_animation_from_data(
        self, frames_data: List[Dict], config: Dict, output_filename: str, output_dir: Path = None
    ) -> Path:
        """データからアニメーションGIFを生成"""
        safe_filename = slugify(output_filename.replace('.gif', '')) + '.gif'
        
        if output_dir:
            output_path = output_dir / safe_filename
        else:
            output_path = Path(safe_filename)
        
        try:
            frames = []
            
            for frame_data in frames_data:
                fig, ax = plt.subplots(figsize=self.styles["figsize"])
                
                # フレームのタイプに応じて描画
                frame_type = frame_data.get('type', 'line')
                if frame_type == 'line':
                    ax.plot(frame_data['x'], frame_data['y'], 
                        linewidth=self.styles["line_width"])
                elif frame_type == 'scatter':
                    ax.scatter(frame_data['x'], frame_data['y'], 
                            s=50, alpha=0.6)
                
                ax.set_xlim(config.get('xlim', (None, None)))
                ax.set_ylim(config.get('ylim', (None, None)))
                ax.set_title(frame_data.get('title', config.get('title', '')))
                ax.set_xlabel(config.get('xlabel', ''))
                ax.set_ylabel(config.get('ylabel', ''))
                ax.grid(True, alpha=self.styles["grid_alpha"])
                
                frames.append(fig)
            
            # GIFとして保存
            self.create_animation_gif(
                frames, 
                output_filename, 
                fps=config.get('fps', 2),
                output_dir=output_dir
            )
            
            return output_path
            
        except Exception as e:
            logger.error(f"アニメーションGIFの生成中にエラーが発生しました: {e}")
            raise
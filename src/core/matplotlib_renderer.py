"""
Matplotlib描画エンジン

既存のChartGeneratorを統合し、宣言的コンポーネントシステムに適合させたレンダラー。
matplotlib/seabornを使用して、Shape、DataVisualization、MathFunction等のコンポーネントをサポートします。
"""

from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import io
import base64
import logging

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import seaborn as sns
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, Polygon

from .component_renderer import ComponentRenderer, BaseComponent
from .chart_generator import ChartGenerator  # 既存のChartGeneratorをインポート

logger = logging.getLogger(__name__)


class MatplotlibRenderer(ComponentRenderer):
    """Matplotlib描画エンジン"""
    
    engine_name = "matplotlib"
    file_extension = "html"
    supported_component_types = [
        "Shape", "Text", "DataVisualization", "MathFunction", 
        "Grid", "Axis", "Legend", "Annotation"
    ]
    
    def __init__(self, output_dir: Path, config: Optional[Dict] = None):
        """
        MatplotlibRendererを初期化
        
        Args:
            output_dir: 出力ディレクトリ
            config: 描画設定
        """
        super().__init__(output_dir, config)
        
        # 既存のChartGeneratorとの互換性を保持
        self.chart_generator = ChartGenerator(
            colors=config.get('colors'),
            styles=config.get('styles')
        )
        
        # matplotlib固有の設定
        self.fig = None
        self.ax = None
        self.figure_config = {
            'figsize': (10, 6),
            'dpi': 150,
            'facecolor': 'white',
            'edgecolor': 'none'
        }
        
        # 描画コンテキスト
        self.drawing_context = {
            'colors': self.chart_generator.colors,
            'styles': self.chart_generator.styles,
            'component_counter': 0
        }
    
    def _register_default_components(self):
        """デフォルトコンポーネントを登録"""
        self.component_registry.update({
            'Shape': ShapeComponent,
            'Text': TextComponent,
            'DataVisualization': DataVisualizationComponent,
            'MathFunction': MathFunctionComponent,
            'Grid': GridComponent,
            'Axis': AxisComponent,
            'Legend': LegendComponent,
            'Annotation': AnnotationComponent,
        })
    
    def _apply_global_config(self, config: Dict[str, Any]):
        """グローバル設定を適用してfigとaxを初期化"""
        # Figure設定を更新
        self.figure_config.update({
            'figsize': config.get('size', config.get('figsize', (10, 6))),
            'dpi': config.get('dpi', 150),
            'facecolor': config.get('facecolor', 'white'),
            'edgecolor': config.get('edgecolor', 'none')
        })
        
        # Figureとaxesを作成
        self.fig, self.ax = plt.subplots(
            figsize=self.figure_config['figsize']
        )
        
        self.fig.patch.set_facecolor(self.figure_config['facecolor'])
        self.fig.patch.set_edgecolor(self.figure_config['edgecolor'])
        
        # 軸設定
        if 'xlim' in config:
            self.ax.set_xlim(config['xlim'])
        if 'ylim' in config:
            self.ax.set_ylim(config['ylim'])
        if 'title' in config:
            self.ax.set_title(config['title'], fontsize=config.get('title_fontsize', 16))
        if 'xlabel' in config:
            self.ax.set_xlabel(config['xlabel'], fontsize=config.get('label_fontsize', 12))
        if 'ylabel' in config:
            self.ax.set_ylabel(config['ylabel'], fontsize=config.get('label_fontsize', 12))
        
        # グリッド設定
        if config.get('grid', False):
            self.ax.grid(True, alpha=config.get('grid_alpha', 0.3))
        
        # その他のスタイル設定
        if config.get('style'):
            plt.style.use(config['style'])
        
        # Seaborn設定
        if config.get('seaborn_style'):
            sns.set_style(config['seaborn_style'])
        if config.get('seaborn_palette'):
            sns.set_palette(config['seaborn_palette'])
        
        logger.info(f"matplotlib図を初期化: {self.figure_config}")
    
    def _save_rendered_content(self, content: Any, output_path: Path, config: Dict[str, Any]):
        """HTMLファイルとして保存"""
        try:
            # レイアウト調整
            self.fig.tight_layout()
            
            # PNGをBase64エンコード
            buffer = io.BytesIO()
            self.fig.savefig(
                buffer, 
                format='png',
                dpi=self.figure_config['dpi'],
                bbox_inches='tight',
                facecolor=self.figure_config['facecolor'],
                edgecolor=self.figure_config['edgecolor']
            )
            buffer.seek(0)
            img_base64 = base64.b64encode(buffer.read()).decode()
            
            # HTML生成
            title = config.get('title', 'Matplotlib Chart')
            html_content = self._generate_html_template(img_base64, title, config)
            
            # ファイル保存
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(html_content, encoding='utf-8')
            
            logger.info(f"matplotlib図をHTMLとして保存: {output_path}")
            
        except Exception as e:
            logger.error(f"matplotlib図の保存に失敗: {e}")
            raise
        finally:
            # リソース解放
            if self.fig:
                plt.close(self.fig)
                self.fig = None
                self.ax = None
    
    def _generate_html_template(self, img_base64: str, title: str, config: Dict[str, Any]) -> str:
        """HTMLテンプレートを生成"""
        return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            margin: 0;
            padding: 20px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: #f5f5f5;
        }}
        .chart-container {{
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
            max-width: 100%;
            margin: 0 auto;
        }}
        .chart-image {{
            max-width: 100%;
            height: auto;
            display: inline-block;
            border-radius: 4px;
        }}
        .chart-metadata {{
            margin-top: 10px;
            font-size: 12px;
            color: #666;
            text-align: right;
        }}
        @media (max-width: 768px) {{
            body {{ padding: 10px; }}
            .chart-container {{ padding: 15px; }}
        }}
    </style>
</head>
<body>
    <div class="chart-container">
        <img src="data:image/png;base64,{img_base64}" 
             alt="{title}" 
             class="chart-image">
        <div class="chart-metadata">
            Generated by Matplotlib Renderer
        </div>
    </div>
</body>
</html>"""


# ======== コンポーネント実装 ========

class ShapeComponent(BaseComponent):
    """図形描画コンポーネント"""
    
    type_name = "Shape"
    required_props = ['variant', 'position']
    optional_props = {
        'size': [1, 1],
        'style': {},
        'rotation': 0,
        'zorder': 1
    }
    
    @classmethod
    def render(cls, props: Dict[str, Any], renderer: MatplotlibRenderer):
        props = cls.validate_props(props)
        
        variant = props['variant']
        position = props['position']
        style = props.get('style', {})
        size = props.get('size', [1, 1])
        rotation = props.get('rotation', 0)
        zorder = props.get('zorder', 1)
        
        # 共通スタイル
        face_color = style.get('color', style.get('fillColor', 'blue'))
        edge_color = style.get('stroke', style.get('edgeColor', 'black'))
        line_width = style.get('strokeWidth', style.get('lineWidth', 1))
        alpha = style.get('opacity', style.get('alpha', 1.0))
        
        if variant == 'rectangle':
            width, height = size if len(size) == 2 else (size[0], size[0])
            rect = Rectangle(
                (position[0] - width/2, position[1] - height/2),
                width, height,
                linewidth=line_width,
                edgecolor=edge_color,
                facecolor=face_color,
                alpha=alpha,
                angle=rotation,
                zorder=zorder
            )
            renderer.ax.add_patch(rect)
            
        elif variant == 'circle':
            radius = size[0] if isinstance(size, list) else size
            circle = Circle(
                position, radius,
                linewidth=line_width,
                edgecolor=edge_color,
                facecolor=face_color,
                alpha=alpha,
                zorder=zorder
            )
            renderer.ax.add_patch(circle)
            
        elif variant == 'polygon':
            points = props.get('points', [])
            if points:
                polygon = Polygon(
                    points,
                    linewidth=line_width,
                    edgecolor=edge_color,
                    facecolor=face_color,
                    alpha=alpha,
                    zorder=zorder
                )
                renderer.ax.add_patch(polygon)
        
        elif variant in ['line', 'arrow']:
            end_position = props.get('endPosition', [position[0]+1, position[1]])
            arrow_style = '->' if variant == 'arrow' else '-'
            
            renderer.ax.annotate('',
                xy=end_position, 
                xytext=position,
                arrowprops=dict(
                    arrowstyle=arrow_style,
                    color=edge_color,
                    lw=line_width,
                    alpha=alpha
                ),
                zorder=zorder
            )


class TextComponent(BaseComponent):
    """テキスト描画コンポーネント"""
    
    type_name = "Text"
    required_props = ['content', 'position']
    optional_props = {
        'style': {},
        'rotation': 0,
        'zorder': 2
    }
    
    @classmethod
    def render(cls, props: Dict[str, Any], renderer: MatplotlibRenderer):
        props = cls.validate_props(props)
        
        content = props['content']
        position = props['position']
        style = props.get('style', {})
        rotation = props.get('rotation', 0)
        zorder = props.get('zorder', 2)
        
        renderer.ax.text(
            position[0], position[1], content,
            fontsize=style.get('fontSize', 12),
            color=style.get('color', 'black'),
            weight=style.get('fontWeight', 'normal'),
            ha=style.get('align', style.get('horizontalAlign', 'left')),
            va=style.get('verticalAlign', 'bottom'),
            rotation=rotation,
            zorder=zorder,
            alpha=style.get('opacity', 1.0)
        )


class DataVisualizationComponent(BaseComponent):
    """データ可視化コンポーネント"""
    
    type_name = "DataVisualization"
    required_props = ['variant', 'data']
    optional_props = {
        'style': {},
        'interactive': False
    }
    
    @classmethod
    def render(cls, props: Dict[str, Any], renderer: MatplotlibRenderer):
        props = cls.validate_props(props)
        
        variant = props['variant']
        data = props['data']
        style = props.get('style', {})
        
        if variant == 'line':
            renderer.ax.plot(
                data['x'], data['y'],
                color=style.get('color', 'blue'),
                linewidth=style.get('lineWidth', 2),
                linestyle=style.get('lineStyle', '-'),
                marker='o' if style.get('showMarkers', True) else None,
                markersize=style.get('markerSize', 6),
                alpha=style.get('opacity', 1.0),
                label=style.get('label')
            )
            
        elif variant == 'bar':
            colors = style.get('colors', [style.get('color', 'blue')])
            renderer.ax.bar(
                data['x'], data['y'],
                color=colors,
                alpha=style.get('opacity', 0.7),
                width=style.get('barWidth', 0.8),
                label=style.get('label')
            )
            
        elif variant == 'scatter':
            renderer.ax.scatter(
                data['x'], data['y'],
                c=style.get('colors', style.get('color', 'blue')),
                s=style.get('markerSize', 50),
                alpha=style.get('opacity', 0.6),
                marker=style.get('marker', 'o'),
                label=style.get('label')
            )
            
        elif variant == 'pie':
            labels = data.get('labels', data.get('x', []))
            values = data.get('values', data.get('y', []))
            colors = style.get('colors')
            
            renderer.ax.pie(
                values, labels=labels, colors=colors,
                autopct=style.get('autopct', '%1.1f%%'),
                startangle=style.get('startAngle', 90),
                explode=style.get('explode')
            )
        
        # 軸ラベル設定
        if style.get('xlabel'):
            renderer.ax.set_xlabel(style['xlabel'])
        if style.get('ylabel'):
            renderer.ax.set_ylabel(style['ylabel'])
        if style.get('title'):
            renderer.ax.set_title(style['title'])


class MathFunctionComponent(BaseComponent):
    """数学関数描画コンポーネント"""
    
    type_name = "MathFunction"
    required_props = ['function', 'domain']
    optional_props = {
        'parameters': {},
        'style': {},
        'resolution': 1000
    }
    
    @classmethod
    def render(cls, props: Dict[str, Any], renderer: MatplotlibRenderer):
        props = cls.validate_props(props)
        
        function = props['function']
        domain = props['domain']
        parameters = props.get('parameters', {})
        style = props.get('style', {})
        resolution = props.get('resolution', 1000)
        
        x = np.linspace(domain[0], domain[1], resolution)
        
        if function == 'sin':
            y = parameters.get('amplitude', 1) * np.sin(
                parameters.get('frequency', 1) * x + parameters.get('phase', 0)
            ) + parameters.get('offset', 0)
        elif function == 'cos':
            y = parameters.get('amplitude', 1) * np.cos(
                parameters.get('frequency', 1) * x + parameters.get('phase', 0)
            ) + parameters.get('offset', 0)
        elif function == 'linear':
            slope = parameters.get('slope', 1)
            intercept = parameters.get('intercept', 0)
            y = slope * x + intercept
        elif function == 'polynomial':
            coefficients = parameters.get('coefficients', [1])
            y = np.polyval(coefficients, x)
        elif function == 'exponential':
            base = parameters.get('base', np.e)
            scale = parameters.get('scale', 1)
            y = scale * np.power(base, x)
        else:
            raise ValueError(f"サポートされていない関数: {function}")
        
        renderer.ax.plot(x, y,
            color=style.get('color', 'blue'),
            linewidth=style.get('lineWidth', 2),
            linestyle=style.get('lineStyle', '-'),
            alpha=style.get('opacity', 1.0),
            label=style.get('label', function)
        )


class GridComponent(BaseComponent):
    """グリッド設定コンポーネント"""
    
    type_name = "Grid"
    optional_props = {
        'enabled': True,
        'alpha': 0.3,
        'color': 'gray',
        'linestyle': '-',
        'linewidth': 0.5
    }
    
    @classmethod
    def render(cls, props: Dict[str, Any], renderer: MatplotlibRenderer):
        props = cls.validate_props(props)
        
        if props.get('enabled', True):
            renderer.ax.grid(
                True,
                alpha=props.get('alpha', 0.3),
                color=props.get('color', 'gray'),
                linestyle=props.get('linestyle', '-'),
                linewidth=props.get('linewidth', 0.5)
            )


class AxisComponent(BaseComponent):
    """軸設定コンポーネント"""
    
    type_name = "Axis"
    optional_props = {
        'xlim': None,
        'ylim': None,
        'xlabel': '',
        'ylabel': '',
        'xscale': 'linear',
        'yscale': 'linear'
    }
    
    @classmethod
    def render(cls, props: Dict[str, Any], renderer: MatplotlibRenderer):
        props = cls.validate_props(props)
        
        if props.get('xlim'):
            renderer.ax.set_xlim(props['xlim'])
        if props.get('ylim'):
            renderer.ax.set_ylim(props['ylim'])
        if props.get('xlabel'):
            renderer.ax.set_xlabel(props['xlabel'])
        if props.get('ylabel'):
            renderer.ax.set_ylabel(props['ylabel'])
        if props.get('xscale'):
            renderer.ax.set_xscale(props['xscale'])
        if props.get('yscale'):
            renderer.ax.set_yscale(props['yscale'])


class LegendComponent(BaseComponent):
    """凡例コンポーネント"""
    
    type_name = "Legend"
    optional_props = {
        'location': 'best',
        'frameon': True,
        'shadow': False,
        'fontsize': 'medium'
    }
    
    @classmethod
    def render(cls, props: Dict[str, Any], renderer: MatplotlibRenderer):
        props = cls.validate_props(props)
        
        renderer.ax.legend(
            loc=props.get('location', 'best'),
            frameon=props.get('frameon', True),
            shadow=props.get('shadow', False),
            fontsize=props.get('fontsize', 'medium')
        )


class AnnotationComponent(BaseComponent):
    """注釈コンポーネント"""
    
    type_name = "Annotation"
    required_props = ['text', 'position']
    optional_props = {
        'arrow_position': None,
        'style': {},
        'arrow_style': '->',
        'bbox_style': None
    }
    
    @classmethod
    def render(cls, props: Dict[str, Any], renderer: MatplotlibRenderer):
        props = cls.validate_props(props)
        
        text = props['text']
        position = props['position']
        arrow_position = props.get('arrow_position')
        style = props.get('style', {})
        
        # 矢印プロパティ
        arrow_props = None
        if arrow_position:
            arrow_props = dict(
                arrowstyle=props.get('arrow_style', '->'),
                color=style.get('color', 'black'),
                lw=style.get('lineWidth', 1)
            )
        
        # バウンディングボックス
        bbox_props = None
        if props.get('bbox_style'):
            bbox_props = dict(
                boxstyle=props['bbox_style'],
                facecolor=style.get('backgroundColor', 'white'),
                alpha=style.get('backgroundOpacity', 0.8)
            )
        
        renderer.ax.annotate(
            text,
            xy=arrow_position if arrow_position else position,
            xytext=position,
            fontsize=style.get('fontSize', 12),
            color=style.get('color', 'black'),
            ha=style.get('horizontalAlign', 'center'),
            va=style.get('verticalAlign', 'center'),
            arrowprops=arrow_props,
            bbox=bbox_props
        )
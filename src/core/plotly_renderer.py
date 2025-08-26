"""
Plotly描画エンジン

MCPサーバから取得したPlotlyドキュメントを参考に、宣言的コンポーネントシステムに適合させた
インタラクティブなPlotlyレンダラー。高度なダッシュボード、アニメーション、インタラクティブ機能をサポートします。
"""

from typing import Dict, List, Any, Optional, Union, Callable
from pathlib import Path
import json
import logging
import numpy as np

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from plotly.offline import plot

from .component_renderer import ComponentRenderer, BaseComponent

logger = logging.getLogger(__name__)


class PlotlyRenderer(ComponentRenderer):
    """Plotly描画エンジン"""
    
    engine_name = "plotly"
    file_extension = "html"
    supported_component_types = [
        "DataVisualization", "Interactive", "Layout", "Animation",
        "Dashboard", "Subplot", "Shape", "Annotation", "Button", "Slider",
        "Dropdown", "UpdateMenu", "RangeSlider", "CustomTrace"
    ]
    
    def __init__(self, output_dir: Path, config: Optional[Dict] = None):
        """
        PlotlyRendererを初期化
        
        Args:
            output_dir: 出力ディレクトリ
            config: Plotly設定
        """
        super().__init__(output_dir, config)
        
        # Plotly固有の設定
        self.plotly_config = {
            'responsive': True,
            'displaylogo': False,
            'modeBarButtonsToRemove': [
                'zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 
                'zoomOut2d', 'autoScale2d', 'resetScale2d', 'toImage'
            ],
            'scrollZoom': False,
            'doubleClick': False
        }
        
        # 図とレイアウト
        self.figure = None
        self.subplots_specs = None
        self.animation_frames = []
        
        # インタラクティブコンポーネント追跡
        self.interactive_components = {
            'updatemenus': [],
            'sliders': [],
            'buttons': [],
            'annotations': []
        }
        
        # カラーパレット
        self.color_palettes = {
            'default': px.colors.qualitative.Plotly,
            'viridis': px.colors.sequential.Viridis,
            'plasma': px.colors.sequential.Plasma,
            'custom': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
        }
    
    def _register_default_components(self):
        """デフォルトコンポーネントを登録"""
        self.component_registry.update({
            'DataVisualization': PlotlyDataVisualizationComponent,
            'Interactive': PlotlyInteractiveComponent,
            'Layout': PlotlyLayoutComponent,
            'Animation': PlotlyAnimationComponent,
            'Dashboard': PlotlyDashboardComponent,
            'Subplot': PlotlySubplotComponent,
            'Shape': PlotlyShapeComponent,
            'Annotation': PlotlyAnnotationComponent,
            'Button': PlotlyButtonComponent,
            'Slider': PlotlySliderComponent,
            'Dropdown': PlotlyDropdownComponent,
            'UpdateMenu': PlotlyUpdateMenuComponent,
            'RangeSlider': PlotlyRangeSliderComponent,
            'CustomTrace': PlotlyCustomTraceComponent,
        })
    
    def _apply_global_config(self, config: Dict[str, Any]):
        """グローバル設定を適用してFigureを初期化"""
        # サブプロット設定
        subplot_config = config.get('subplots', {})
        if subplot_config:
            rows = subplot_config.get('rows', 1)
            cols = subplot_config.get('cols', 1)
            subplot_titles = subplot_config.get('titles', [])
            specs = subplot_config.get('specs')
            
            self.figure = make_subplots(
                rows=rows, cols=cols,
                subplot_titles=subplot_titles,
                specs=specs,
                shared_xaxes=subplot_config.get('shared_xaxes', False),
                shared_yaxes=subplot_config.get('shared_yaxes', False),
                vertical_spacing=subplot_config.get('vertical_spacing', 0.03),
                horizontal_spacing=subplot_config.get('horizontal_spacing', 0.03)
            )
            self.subplots_specs = {'rows': rows, 'cols': cols}
        else:
            # 単一プロット
            self.figure = go.Figure()
        
        # レイアウト設定
        layout_config = {
            'title': config.get('title', ''),
            'width': config.get('width'),
            'height': config.get('height', 600),
            'margin': config.get('margin', dict(l=50, r=50, t=50, b=50)),
            'plot_bgcolor': config.get('plot_bgcolor', 'white'),
            'paper_bgcolor': config.get('paper_bgcolor', '#f5f5f5'),
            'hovermode': config.get('hovermode', 'closest'),
            'showlegend': config.get('showlegend', True),
        }
        
        # テーマ設定
        theme = config.get('theme')
        if theme == 'dark':
            layout_config.update({
                'plot_bgcolor': '#2f3037',
                'paper_bgcolor': '#2f3037',
                'font': {'color': 'white'}
            })
        elif theme == 'minimal':
            layout_config.update({
                'plot_bgcolor': 'rgba(0,0,0,0)',
                'paper_bgcolor': 'rgba(0,0,0,0)',
            })
        
        self.figure.update_layout(**layout_config)
        
        # Plotly設定を更新
        if config.get('plotly_config'):
            self.plotly_config.update(config['plotly_config'])
        
        logger.info(f"Plotly図を初期化: {layout_config}")
    
    def _save_rendered_content(self, content: Any, output_path: Path, config: Dict[str, Any]):
        """HTMLファイルとして保存"""
        try:
            # インタラクティブコンポーネントを追加
            self._finalize_interactive_components()
            
            # HTMLとして保存
            plot(
                self.figure,
                filename=str(output_path),
                config=self.plotly_config,
                auto_open=False,
                include_plotlyjs='cdn'  # CDNから読み込み
            )
            
            logger.info(f"Plotly図をHTMLとして保存: {output_path}")
            
        except Exception as e:
            logger.error(f"Plotly図の保存に失敗: {e}")
            raise
    
    def _finalize_interactive_components(self):
        """インタラクティブコンポーネントをfigureに統合"""
        if self.interactive_components['updatemenus']:
            self.figure.update_layout(updatemenus=self.interactive_components['updatemenus'])
        
        if self.interactive_components['sliders']:
            self.figure.update_layout(sliders=self.interactive_components['sliders'])
        
        if self.interactive_components['annotations']:
            self.figure.update_layout(annotations=self.interactive_components['annotations'])
    
    def add_trace(self, trace, row=None, col=None):
        """トレースを追加（サブプロット対応）"""
        if self.subplots_specs and row and col:
            self.figure.add_trace(trace, row=row, col=col)
        else:
            self.figure.add_trace(trace)
    
    def get_color_palette(self, palette_name: str, count: int) -> List[str]:
        """カラーパレットを取得"""
        colors = self.color_palettes.get(palette_name, self.color_palettes['default'])
        if count <= len(colors):
            return colors[:count]
        else:
            # 色が不足している場合は繰り返し
            return (colors * ((count // len(colors)) + 1))[:count]


# ======== コンポーネント実装 ========

class PlotlyDataVisualizationComponent(BaseComponent):
    """Plotlyデータ可視化コンポーネント"""
    
    type_name = "DataVisualization"
    required_props = ['variant', 'data']
    optional_props = {
        'style': {},
        'subplot': None,
        'name': '',
        'showlegend': True
    }
    
    @classmethod
    def render(cls, props: Dict[str, Any], renderer: PlotlyRenderer):
        props = cls.validate_props(props)
        
        variant = props['variant']
        data = props['data']
        style = props.get('style', {})
        subplot = props.get('subplot')
        name = props.get('name', '')
        
        # サブプロット位置
        row = subplot.get('row', None) if subplot else None
        col = subplot.get('col', None) if subplot else None
        
        if variant == 'line':
            trace = go.Scatter(
                x=data['x'],
                y=data['y'],
                mode='lines+markers' if style.get('showMarkers', True) else 'lines',
                name=name or style.get('label', ''),
                line=dict(
                    color=style.get('color', '#1f77b4'),
                    width=style.get('lineWidth', 2),
                    dash=style.get('lineDash', 'solid')
                ),
                marker=dict(
                    size=style.get('markerSize', 6),
                    symbol=style.get('markerSymbol', 'circle')
                ),
                hovertemplate=style.get('hoverTemplate'),
                showlegend=props.get('showlegend', True)
            )
            
        elif variant == 'bar':
            trace = go.Bar(
                x=data['x'],
                y=data['y'],
                name=name or style.get('label', ''),
                marker=dict(
                    color=style.get('colors', style.get('color', '#1f77b4')),
                    opacity=style.get('opacity', 1.0),
                    line=dict(
                        color=style.get('borderColor', 'rgba(0,0,0,0)'),
                        width=style.get('borderWidth', 0)
                    )
                ),
                text=style.get('text'),
                textposition=style.get('textPosition', 'auto'),
                hovertemplate=style.get('hoverTemplate'),
                showlegend=props.get('showlegend', True)
            )
            
        elif variant == 'scatter':
            trace = go.Scatter(
                x=data['x'],
                y=data['y'],
                mode='markers',
                name=name or style.get('label', ''),
                marker=dict(
                    size=data.get('size', style.get('markerSize', [10]*len(data['x']))),
                    color=data.get('color', style.get('colors', style.get('color', '#1f77b4'))),
                    opacity=style.get('opacity', 0.7),
                    symbol=style.get('markerSymbol', 'circle'),
                    line=dict(
                        color=style.get('borderColor', 'rgba(0,0,0,0.3)'),
                        width=style.get('borderWidth', 1)
                    ),
                    colorscale=style.get('colorscale', 'Viridis') if isinstance(data.get('color'), list) else None,
                    showscale=style.get('showColorbar', False)
                ),
                text=data.get('text', data.get('labels')),
                hovertemplate=style.get('hoverTemplate'),
                showlegend=props.get('showlegend', True)
            )
            
        elif variant == 'pie':
            trace = go.Pie(
                labels=data.get('labels', data.get('x', [])),
                values=data.get('values', data.get('y', [])),
                name=name,
                hole=style.get('hole', 0),
                textinfo=style.get('textInfo', 'label+percent'),
                textposition=style.get('textPosition', 'auto'),
                marker=dict(
                    colors=style.get('colors'),
                    line=dict(
                        color=style.get('borderColor', 'white'),
                        width=style.get('borderWidth', 2)
                    )
                ),
                pull=style.get('pull'),
                rotation=style.get('rotation', 0),
                showlegend=props.get('showlegend', True)
            )
            
        elif variant == 'heatmap':
            trace = go.Heatmap(
                z=data['z'],
                x=data.get('x'),
                y=data.get('y'),
                colorscale=style.get('colorscale', 'Viridis'),
                showscale=style.get('showColorbar', True),
                hoverongaps=style.get('hoverOnGaps', True),
                name=name
            )
            
        elif variant == '3d_scatter':
            trace = go.Scatter3d(
                x=data['x'],
                y=data['y'],
                z=data['z'],
                mode='markers',
                name=name or style.get('label', ''),
                marker=dict(
                    size=data.get('size', style.get('markerSize', [5]*len(data['x']))),
                    color=data.get('color', style.get('colors', style.get('color', '#1f77b4'))),
                    opacity=style.get('opacity', 0.8),
                    colorscale=style.get('colorscale', 'Viridis') if isinstance(data.get('color'), list) else None
                ),
                text=data.get('text', data.get('labels')),
                showlegend=props.get('showlegend', True)
            )
            
        elif variant == 'box':
            trace = go.Box(
                y=data['y'],
                x=data.get('x'),
                name=name or style.get('label', ''),
                marker=dict(color=style.get('color', '#1f77b4')),
                line=dict(color=style.get('lineColor', '#1f77b4')),
                showlegend=props.get('showlegend', True)
            )
            
        elif variant == 'violin':
            trace = go.Violin(
                y=data['y'],
                x=data.get('x'),
                name=name or style.get('label', ''),
                marker=dict(color=style.get('color', '#1f77b4')),
                line=dict(color=style.get('lineColor', '#1f77b4')),
                showlegend=props.get('showlegend', True)
            )
            
        else:
            raise ValueError(f"サポートされていないPlotlyチャートタイプ: {variant}")
        
        renderer.add_trace(trace, row=row, col=col)


class PlotlyInteractiveComponent(BaseComponent):
    """インタラクティブコンポーネント（ボタン、スライダー等）"""
    
    type_name = "Interactive"
    required_props = ['variant']
    optional_props = {
        'position': {'x': 0.1, 'y': 1.02},
        'style': {},
        'actions': []
    }
    
    @classmethod
    def render(cls, props: Dict[str, Any], renderer: PlotlyRenderer):
        props = cls.validate_props(props)
        
        variant = props['variant']
        position = props.get('position', {'x': 0.1, 'y': 1.02})
        style = props.get('style', {})
        actions = props.get('actions', [])
        
        if variant == 'button':
            buttons = []
            for action in actions:
                button = dict(
                    label=action.get('label', 'Button'),
                    method=action.get('method', 'update'),
                    args=action.get('args', []),
                    visible=action.get('visible', True)
                )
                buttons.append(button)
            
            updatemenu = dict(
                type="buttons",
                direction=style.get('direction', 'left'),
                active=style.get('active', 0),
                x=position.get('x', 0.1),
                y=position.get('y', 1.02),
                buttons=buttons,
                pad=style.get('pad', {"r": 10, "t": 10}),
                showactive=style.get('showActive', True)
            )
            
            renderer.interactive_components['updatemenus'].append(updatemenu)
            
        elif variant == 'slider':
            steps = []
            for action in actions:
                step = dict(
                    method=action.get('method', 'animate'),
                    args=action.get('args', []),
                    label=action.get('label', str(len(steps)))
                )
                steps.append(step)
            
            slider = dict(
                active=style.get('active', 0),
                currentvalue=dict(
                    prefix=style.get('prefix', 'Step: '),
                    visible=style.get('showValue', True)
                ),
                pad=style.get('pad', {"b": 10, "t": 50}),
                len=style.get('length', 0.9),
                x=position.get('x', 0.1),
                y=position.get('y', 0),
                steps=steps,
                transition=dict(
                    duration=style.get('duration', 300),
                    easing=style.get('easing', 'cubic-in-out')
                )
            )
            
            renderer.interactive_components['sliders'].append(slider)
            
        elif variant == 'dropdown':
            dropdown_buttons = []
            for action in actions:
                button = dict(
                    label=action.get('label', 'Option'),
                    method=action.get('method', 'update'),
                    args=action.get('args', []),
                    visible=action.get('visible', True)
                )
                dropdown_buttons.append(button)
            
            updatemenu = dict(
                type="dropdown",
                active=style.get('active', 0),
                x=position.get('x', 1.0),
                y=position.get('y', 1.15),
                buttons=dropdown_buttons,
                direction="down",
                showactive=True
            )
            
            renderer.interactive_components['updatemenus'].append(updatemenu)


class PlotlyLayoutComponent(BaseComponent):
    """レイアウト設定コンポーネント"""
    
    type_name = "Layout"
    optional_props = {
        'title': '',
        'xaxis': {},
        'yaxis': {},
        'legend': {},
        'annotations': []
    }
    
    @classmethod
    def render(cls, props: Dict[str, Any], renderer: PlotlyRenderer):
        props = cls.validate_props(props)
        
        layout_updates = {}
        
        if props.get('title'):
            layout_updates['title'] = props['title']
        
        if props.get('xaxis'):
            layout_updates['xaxis'] = props['xaxis']
        
        if props.get('yaxis'):
            layout_updates['yaxis'] = props['yaxis']
        
        if props.get('legend'):
            layout_updates['legend'] = props['legend']
        
        if props.get('annotations'):
            renderer.interactive_components['annotations'].extend(props['annotations'])
        
        renderer.figure.update_layout(**layout_updates)


class PlotlyAnimationComponent(BaseComponent):
    """アニメーションコンポーネント"""
    
    type_name = "Animation"
    required_props = ['frames']
    optional_props = {
        'transition': {'duration': 500, 'easing': 'cubic-in-out'},
        'controls': True
    }
    
    @classmethod
    def render(cls, props: Dict[str, Any], renderer: PlotlyRenderer):
        props = cls.validate_props(props)
        
        frames_data = props['frames']
        transition = props.get('transition', {'duration': 500, 'easing': 'cubic-in-out'})
        show_controls = props.get('controls', True)
        
        frames = []
        for i, frame_data in enumerate(frames_data):
            frame_traces = []
            for trace_spec in frame_data.get('traces', []):
                # フレーム内のトレースを生成（簡略化）
                if trace_spec['type'] == 'scatter':
                    trace = go.Scatter(
                        x=trace_spec['data']['x'],
                        y=trace_spec['data']['y'],
                        mode='markers'
                    )
                    frame_traces.append(trace)
            
            frame = go.Frame(
                data=frame_traces,
                name=frame_data.get('name', str(i)),
                layout=frame_data.get('layout', {})
            )
            frames.append(frame)
        
        renderer.figure.frames = frames
        
        if show_controls:
            # アニメーション制御ボタンを追加
            updatemenus = [{
                'type': 'buttons',
                'buttons': [{
                    'label': 'Play',
                    'method': 'animate',
                    'args': [None, {'frame': {'duration': transition['duration']}, 
                                   'transition': transition}]
                }, {
                    'label': 'Pause',
                    'method': 'animate',
                    'args': [[None], {'frame': {'duration': 0}, 'mode': 'immediate'}]
                }],
                'direction': 'left',
                'pad': {'r': 10, 't': 87},
                'showactive': False,
                'x': 0.1,
                'y': 0
            }]
            
            renderer.interactive_components['updatemenus'].extend(updatemenus)


class PlotlyDashboardComponent(BaseComponent):
    """ダッシュボード合成コンポーネント"""
    
    type_name = "Dashboard"
    required_props = ['components']
    optional_props = {
        'layout': 'grid',
        'rows': 2,
        'cols': 2,
        'spacing': 0.05
    }
    
    @classmethod
    def render(cls, props: Dict[str, Any], renderer: PlotlyRenderer):
        props = cls.validate_props(props)
        
        components = props['components']
        layout_type = props.get('layout', 'grid')
        rows = props.get('rows', 2)
        cols = props.get('cols', 2)
        spacing = props.get('spacing', 0.05)
        
        if layout_type == 'grid' and not renderer.subplots_specs:
            # サブプロット仕様を後から設定
            renderer.figure = make_subplots(
                rows=rows, cols=cols,
                vertical_spacing=spacing,
                horizontal_spacing=spacing
            )
            renderer.subplots_specs = {'rows': rows, 'cols': cols}
        
        # 各コンポーネントを適切なサブプロットに配置
        for i, component_spec in enumerate(components):
            row = (i // cols) + 1
            col = (i % cols) + 1
            
            if row <= rows and col <= cols:
                # サブプロット位置を指定
                component_spec['props'] = component_spec.get('props', {})
                component_spec['props']['subplot'] = {'row': row, 'col': col}
                
                # コンポーネントをレンダリング
                component_type = component_spec['type']
                if component_type in renderer.component_registry:
                    component_class = renderer.component_registry[component_type]
                    component_class.render(component_spec['props'], renderer)


class PlotlySubplotComponent(BaseComponent):
    """サブプロットコンポーネント"""
    
    type_name = "Subplot"
    required_props = ['row', 'col', 'components']
    
    @classmethod
    def render(cls, props: Dict[str, Any], renderer: PlotlyRenderer):
        props = cls.validate_props(props)
        
        row = props['row']
        col = props['col']
        components = props['components']
        
        # サブプロット内の各コンポーネントをレンダリング
        for component_spec in components:
            component_spec['props'] = component_spec.get('props', {})
            component_spec['props']['subplot'] = {'row': row, 'col': col}
            
            component_type = component_spec['type']
            if component_type in renderer.component_registry:
                component_class = renderer.component_registry[component_type]
                component_class.render(component_spec['props'], renderer)


class PlotlyShapeComponent(BaseComponent):
    """図形・線描画コンポーネント"""
    
    type_name = "Shape"
    required_props = ['variant']
    optional_props = {
        'x0': 0, 'y0': 0, 'x1': 1, 'y1': 1,
        'style': {},
        'layer': 'below'
    }
    
    @classmethod
    def render(cls, props: Dict[str, Any], renderer: PlotlyRenderer):
        props = cls.validate_props(props)
        
        variant = props['variant']
        style = props.get('style', {})
        
        shape = dict(
            type=variant,  # 'line', 'circle', 'rect', etc.
            x0=props.get('x0', 0),
            y0=props.get('y0', 0),
            x1=props.get('x1', 1),
            y1=props.get('y1', 1),
            line=dict(
                color=style.get('color', 'rgba(128,0,128,1)'),
                width=style.get('width', 2),
                dash=style.get('dash', 'solid')
            ),
            fillcolor=style.get('fillColor', 'rgba(128,0,128,0.2)'),
            layer=props.get('layer', 'below')
        )
        
        renderer.figure.add_shape(shape)


class PlotlyAnnotationComponent(BaseComponent):
    """注釈コンポーネント"""
    
    type_name = "Annotation"
    required_props = ['text', 'x', 'y']
    optional_props = {
        'arrow': True,
        'style': {}
    }
    
    @classmethod
    def render(cls, props: Dict[str, Any], renderer: PlotlyRenderer):
        props = cls.validate_props(props)
        
        text = props['text']
        x = props['x']
        y = props['y']
        show_arrow = props.get('arrow', True)
        style = props.get('style', {})
        
        annotation = dict(
            text=text,
            x=x, y=y,
            showarrow=show_arrow,
            arrowhead=style.get('arrowhead', 2),
            arrowsize=style.get('arrowsize', 1),
            arrowwidth=style.get('arrowwidth', 2),
            arrowcolor=style.get('arrowcolor', '#636363'),
            ax=style.get('ax', 0),
            ay=style.get('ay', -30),
            bordercolor=style.get('bordercolor', '#c7c7c7'),
            borderwidth=style.get('borderwidth', 2),
            bgcolor=style.get('bgcolor', 'rgba(255,255,255,0.9)'),
            font=dict(
                color=style.get('color', 'black'),
                size=style.get('fontSize', 12)
            )
        )
        
        renderer.interactive_components['annotations'].append(annotation)


# 追加のコンポーネント（簡略版）
class PlotlyButtonComponent(PlotlyInteractiveComponent):
    type_name = "Button"
    
    @classmethod  
    def render(cls, props: Dict[str, Any], renderer: PlotlyRenderer):
        props['variant'] = 'button'
        super().render(props, renderer)


class PlotlySliderComponent(PlotlyInteractiveComponent):
    type_name = "Slider"
    
    @classmethod
    def render(cls, props: Dict[str, Any], renderer: PlotlyRenderer):
        props['variant'] = 'slider'
        super().render(props, renderer)


class PlotlyDropdownComponent(PlotlyInteractiveComponent):
    type_name = "Dropdown"
    
    @classmethod
    def render(cls, props: Dict[str, Any], renderer: PlotlyRenderer):
        props['variant'] = 'dropdown'
        super().render(props, renderer)


class PlotlyUpdateMenuComponent(PlotlyInteractiveComponent):
    type_name = "UpdateMenu"


class PlotlyRangeSliderComponent(BaseComponent):
    """範囲スライダーコンポーネント"""
    type_name = "RangeSlider"
    
    @classmethod
    def render(cls, props: Dict[str, Any], renderer: PlotlyRenderer):
        renderer.figure.update_layout(
            xaxis=dict(rangeslider=dict(visible=True))
        )


class PlotlyCustomTraceComponent(BaseComponent):
    """カスタムトレースコンポーネント"""
    
    type_name = "CustomTrace"
    required_props = ['trace_config']
    
    @classmethod
    def render(cls, props: Dict[str, Any], renderer: PlotlyRenderer):
        props = cls.validate_props(props)
        
        trace_config = props['trace_config']
        trace_type = trace_config.get('type', 'scatter')
        
        # 動的にトレースを生成
        if hasattr(go, trace_type.title()):
            TraceClass = getattr(go, trace_type.title())
            trace = TraceClass(**trace_config.get('params', {}))
            renderer.add_trace(trace)
        else:
            logger.warning(f"未サポートのトレースタイプ: {trace_type}")
# コンポーネント実装ガイド

## 1. 概要

本書は`UNIVERSAL_COMPONENT_DESIGN.md`で定義した超汎用的コンポーネント指向設計の具体的な実装方法を詳解します。

## 2. 基本実装パターン

### 2.1. ComponentRenderer基底クラス実装例

```python
from abc import ABC, abstractmethod
from typing import Dict, List, Any
from pathlib import Path
import yaml

class ComponentRenderer(ABC):
    """すべての描画エンジンの基底クラス"""
    
    def __init__(self, output_dir: Path, config: Dict = None):
        self.output_dir = Path(output_dir)
        self.config = config or {}
        self.component_registry = {}
        self._register_default_components()
    
    @abstractmethod
    def _register_default_components(self):
        """デフォルトコンポーネントを登録"""
        pass
    
    def render_spec(self, spec: Dict) -> Path:
        """YAML仕様を受け取ってレンダリング"""
        engine = spec.get('engine')
        if engine != self.engine_name:
            raise ValueError(f"Invalid engine: {engine}, expected {self.engine_name}")
        
        # 全体設定を適用
        config = spec.get('config', {})
        self._apply_global_config(config)
        
        # コンポーネントリストを処理
        components = spec.get('components', [])
        rendered_content = self._render_components(components)
        
        # ファイル保存
        filename = spec.get('filename', 'output')
        output_path = self.output_dir / f"{filename}.{self.file_extension}"
        self._save_rendered_content(rendered_content, output_path, config)
        
        return output_path
    
    def _render_components(self, components: List[Dict]) -> Any:
        """コンポーネントリストをレンダリング"""
        rendered_items = []
        for component in components:
            component_type = component.get('type')
            props = component.get('props', {})
            
            if component_type not in self.component_registry:
                raise ValueError(f"Unsupported component type: {component_type}")
            
            component_class = self.component_registry[component_type]
            rendered_item = component_class.render(props, self)
            rendered_items.append(rendered_item)
        
        return rendered_items
    
    @abstractmethod  
    def _apply_global_config(self, config: Dict):
        """全体設定を適用"""
        pass
    
    @abstractmethod
    def _save_rendered_content(self, content: Any, output_path: Path, config: Dict):
        """レンダリング結果をファイルに保存"""
        pass
    
    def register_component(self, component_class):
        """カスタムコンポーネントを登録"""
        self.component_registry[component_class.type_name] = component_class
```

### 2.2. コンポーネント基底クラス

```python
class BaseComponent(ABC):
    """個別コンポーネントの基底クラス"""
    type_name: str = None
    
    @classmethod
    @abstractmethod
    def render(cls, props: Dict, renderer: ComponentRenderer) -> Any:
        """プロパティを受け取ってレンダリング"""
        pass
    
    @classmethod
    def validate_props(cls, props: Dict) -> Dict:
        """プロパティの検証と正規化"""
        return props
```

### 2.3. matplotlib用の実装例

```python
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import numpy as np

class MatplotlibRenderer(ComponentRenderer):
    engine_name = "matplotlib" 
    file_extension = "html"
    
    def __init__(self, output_dir: Path, config: Dict = None):
        super().__init__(output_dir, config)
        self.fig = None
        self.ax = None
        
    def _register_default_components(self):
        self.component_registry.update({
            'Shape': ShapeComponent,
            'Text': TextComponent,
            'DataVisualization': DataVisualizationComponent,
            'MathFunction': MathFunctionComponent,
        })
    
    def _apply_global_config(self, config: Dict):
        """figとaxを初期化"""
        figsize = config.get('size', [10, 6])
        self.fig, self.ax = plt.subplots(figsize=figsize)
        
        # 軸設定
        if 'xlim' in config:
            self.ax.set_xlim(config['xlim'])
        if 'ylim' in config:
            self.ax.set_ylim(config['ylim'])
        if 'title' in config:
            self.ax.set_title(config['title'])
            
    def _save_rendered_content(self, content: Any, output_path: Path, config: Dict):
        """HTMLとして保存"""
        self.fig.tight_layout()
        
        # PNGをBase64エンコード
        buffer = io.BytesIO()
        self.fig.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.read()).decode()
        
        # HTML生成
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{config.get('title', 'Chart')}</title>
    <style>
        body {{ margin: 0; padding: 20px; font-family: sans-serif; }}
        .chart-container {{ text-align: center; }}
        img {{ max-width: 100%; height: auto; }}
    </style>
</head>
<body>
    <div class="chart-container">
        <img src="data:image/png;base64,{img_base64}" alt="Chart">
    </div>
</body>
</html>"""
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html_content, encoding='utf-8')
        plt.close(self.fig)

class ShapeComponent(BaseComponent):
    type_name = "Shape"
    
    @classmethod
    def render(cls, props: Dict, renderer: MatplotlibRenderer):
        props = cls.validate_props(props)
        
        variant = props['variant']
        position = props['position']
        style = props.get('style', {})
        
        if variant == 'rectangle':
            size = props['size']
            rect = patches.Rectangle(
                (position[0] - size[0]/2, position[1] - size[1]/2),
                size[0], size[1],
                linewidth=style.get('strokeWidth', 1),
                edgecolor=style.get('stroke', 'black'),
                facecolor=style.get('color', 'blue'),
                alpha=style.get('opacity', 1.0)
            )
            renderer.ax.add_patch(rect)
            
        elif variant == 'circle':
            radius = props.get('radius', props.get('size', 1))
            circle = patches.Circle(
                position, radius,
                linewidth=style.get('strokeWidth', 1),
                edgecolor=style.get('stroke', 'black'),
                facecolor=style.get('color', 'blue'),
                alpha=style.get('opacity', 1.0)
            )
            renderer.ax.add_patch(circle)
            
        elif variant == 'arrow':
            end_pos = props['endPosition']
            renderer.ax.annotate('',
                xy=end_pos, xytext=position,
                arrowprops=dict(
                    arrowstyle='->' if variant == 'arrow' else '-',
                    color=style.get('color', 'black'),
                    lw=style.get('strokeWidth', 1)
                )
            )

class TextComponent(BaseComponent):
    type_name = "Text"
    
    @classmethod 
    def render(cls, props: Dict, renderer: MatplotlibRenderer):
        props = cls.validate_props(props)
        
        content = props['content']
        position = props['position']
        style = props.get('style', {})
        
        renderer.ax.text(
            position[0], position[1], content,
            fontsize=style.get('fontSize', 12),
            color=style.get('color', 'black'),
            weight=style.get('fontWeight', 'normal'),
            ha=style.get('align', 'left'),
            va=style.get('verticalAlign', 'bottom')
        )

class DataVisualizationComponent(BaseComponent):
    type_name = "DataVisualization"
    
    @classmethod
    def render(cls, props: Dict, renderer: MatplotlibRenderer):
        props = cls.validate_props(props)
        
        variant = props['variant']
        data = props['data']
        style = props.get('style', {})
        
        if variant == 'line':
            renderer.ax.plot(
                data['x'], data['y'],
                color=style.get('color', 'blue'),
                linewidth=style.get('lineWidth', 2),
                marker='o' if style.get('showMarkers', True) else None,
                alpha=style.get('opacity', 1.0)
            )
            
        elif variant == 'bar':
            renderer.ax.bar(
                data['x'], data['y'],
                color=style.get('colors', style.get('color', 'blue')),
                alpha=style.get('opacity', 0.7)
            )
            
        elif variant == 'scatter':
            renderer.ax.scatter(
                data['x'], data['y'],
                c=style.get('colors', style.get('color', 'blue')),
                s=style.get('markerSize', 50),
                alpha=style.get('opacity', 0.6)
            )
        
        # 軸ラベル設定
        if style.get('title'):
            renderer.ax.set_title(style['title'])
        if style.get('xlabel'):
            renderer.ax.set_xlabel(style['xlabel'])
        if style.get('ylabel'):
            renderer.ax.set_ylabel(style['ylabel'])

class MathFunctionComponent(BaseComponent):
    type_name = "MathFunction"
    
    @classmethod
    def render(cls, props: Dict, renderer: MatplotlibRenderer):
        props = cls.validate_props(props)
        
        function = props['function']
        domain = props['domain']
        parameters = props.get('parameters', {})
        style = props.get('style', {})
        
        x = np.linspace(domain[0], domain[1], 1000)
        
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
        
        renderer.ax.plot(x, y,
            color=style.get('color', 'blue'),
            linewidth=style.get('lineWidth', 2),
            label=style.get('label', function)
        )
```

### 2.4. Markdown用の実装例

```python
class MarkdownRenderer(ComponentRenderer):
    engine_name = "markdown"
    file_extension = "md"
    
    def __init__(self, output_dir: Path, config: Dict = None):
        super().__init__(output_dir, config)
        self.content_buffer = []
    
    def _register_default_components(self):
        self.component_registry.update({
            'Heading': HeadingComponent,
            'Paragraph': ParagraphComponent,
            'List': ListComponent,
            'CodeBlock': CodeBlockComponent,
            'Admonition': AdmonitionComponent,
            'Tabs': TabsComponent,
            'Quiz': QuizComponent,
        })
        
    def _apply_global_config(self, config: Dict):
        if config.get('title'):
            self.content_buffer.append(f"# {config['title']}\n")
        if config.get('toc', False):
            self.content_buffer.append("[TOC]\n")
    
    def _render_components(self, components: List[Dict]) -> List[str]:
        for component in components:
            component_type = component.get('type')
            props = component.get('props', {})
            
            # ネストしたコンポーネントの処理
            if 'components' in props:
                nested_components = props.pop('components')
                # 現在のコンポーネントをレンダリング  
                if component_type in self.component_registry:
                    component_class = self.component_registry[component_type]
                    result = component_class.render(props, self)
                    if result:
                        self.content_buffer.append(result)
                
                # ネストしたコンポーネントを再帰処理
                self._render_components(nested_components)
            else:
                if component_type in self.component_registry:
                    component_class = self.component_registry[component_type] 
                    result = component_class.render(props, self)
                    if result:
                        self.content_buffer.append(result)
        
        return self.content_buffer
    
    def _save_rendered_content(self, content: List[str], output_path: Path, config: Dict):
        markdown_content = '\n'.join(content)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(markdown_content, encoding='utf-8')

class HeadingComponent(BaseComponent):
    type_name = "Heading"
    
    @classmethod
    def render(cls, props: Dict, renderer: MarkdownRenderer) -> str:
        level = props.get('level', 1)
        content = props.get('content', '')
        prefix = '#' * level
        return f"{prefix} {content}\n"

class ParagraphComponent(BaseComponent):
    type_name = "Paragraph"
    
    @classmethod
    def render(cls, props: Dict, renderer: MarkdownRenderer) -> str:
        content = props.get('content', '')
        terms = props.get('terms', {})
        enable_tooltips = props.get('enableTooltips', False)
        
        if enable_tooltips and terms:
            # 専門用語にツールチップを適用
            for term, definition in terms.items():
                tooltip_html = f'<span class="custom-tooltip" data-tooltip="{definition}">{term}</span>'
                content = content.replace(term, tooltip_html)
        
        return f"{content}\n"

class TabsComponent(BaseComponent):
    type_name = "Tabs"
    
    @classmethod
    def render(cls, props: Dict, renderer: MarkdownRenderer) -> str:
        tabs = props.get('tabs', {})
        
        markdown = "\n=== Tab Content\n\n"
        
        for tab_name, tab_content in tabs.items():
            markdown += f"=== \"{tab_name}\"\n\n"
            
            if isinstance(tab_content, list):
                # コンポーネントリストの場合
                for component in tab_content:
                    component_type = component.get('type')
                    component_props = component.get('props', {})
                    
                    if component_type in renderer.component_registry:
                        component_class = renderer.component_registry[component_type]
                        result = component_class.render(component_props, renderer)
                        if result:
                            markdown += f"    {result}"
            else:
                # 文字列の場合
                markdown += f"    {tab_content}\n\n"
        
        return markdown
```

## 3. 統合システム実装

### 3.1. RendererFactory

```python
class RendererFactory:
    """描画エンジンファクトリ"""
    
    _engines = {
        'matplotlib': MatplotlibRenderer,
        'plotly': PlotlyRenderer, 
        'markdown': MarkdownRenderer,
        'd3js': D3jsRenderer,
    }
    
    @classmethod
    def create_renderer(cls, engine: str, output_dir: Path, config: Dict = None) -> ComponentRenderer:
        if engine not in cls._engines:
            raise ValueError(f"Unsupported engine: {engine}")
        
        renderer_class = cls._engines[engine]
        return renderer_class(output_dir, config)
    
    @classmethod
    def register_engine(cls, name: str, renderer_class):
        """新しい描画エンジンを登録"""
        cls._engines[name] = renderer_class
```

### 3.2. 統一エントリーポイント

```python
class UniversalContentGenerator:
    """すべてのコンテンツ生成の統一エントリーポイント"""
    
    def __init__(self, output_dir: Path):
        self.output_dir = Path(output_dir)
    
    def generate_from_yaml(self, yaml_path: Path) -> Path:
        """YAMLファイルからコンテンツを生成"""
        with open(yaml_path, 'r', encoding='utf-8') as f:
            spec = yaml.safe_load(f)
        
        return self.generate_from_spec(spec)
    
    def generate_from_spec(self, spec: Dict) -> Path:
        """仕様辞書からコンテンツを生成"""
        engine = spec.get('engine')
        if not engine:
            raise ValueError("Engine not specified in spec")
        
        renderer = RendererFactory.create_renderer(
            engine, self.output_dir, spec.get('config', {})
        )
        
        return renderer.render_spec(spec)
    
    def generate_multiple(self, specs: List[Dict]) -> List[Path]:
        """複数の仕様を一括生成"""
        return [self.generate_from_spec(spec) for spec in specs]
```

## 4. 使用例

### 4.1. 基本的な使い方

```python
# YAMLファイルから生成
generator = UniversalContentGenerator(output_dir="./output")
result_path = generator.generate_from_yaml("./specs/dashboard.yml")

# プログラム内で仕様を定義して生成
spec = {
    "type": "content_block",
    "engine": "matplotlib",
    "filename": "sample_chart",
    "config": {
        "title": "サンプルグラフ",
        "size": [10, 6],
        "xlim": [0, 10],
        "ylim": [0, 10]
    },
    "components": [
        {
            "type": "DataVisualization",
            "props": {
                "variant": "line",
                "data": {
                    "x": [1, 2, 3, 4, 5],
                    "y": [2, 4, 3, 5, 4]
                },
                "style": {
                    "color": "#1f77b4",
                    "lineWidth": 3
                }
            }
        }
    ]
}

result_path = generator.generate_from_spec(spec)
```

### 4.2. カスタムコンポーネントの追加

```python
class CustomGaugeComponent(BaseComponent):
    type_name = "Gauge"
    
    @classmethod
    def render(cls, props: Dict, renderer: MatplotlibRenderer):
        value = props.get('value', 0)
        max_value = props.get('maxValue', 100)
        
        # ゲージチャートの描画ロジック
        theta = np.linspace(0, np.pi, 100)
        r = np.ones_like(theta)
        
        renderer.ax = plt.subplot(111, projection='polar')
        renderer.ax.plot(theta, r, 'k-', linewidth=8)
        
        # 現在値の針を描画
        value_theta = np.pi * (1 - value / max_value)
        renderer.ax.plot([value_theta, value_theta], [0, 1], 'r-', linewidth=4)
        
        return f"Gauge: {value}/{max_value}"

# カスタムコンポーネントを登録
renderer = RendererFactory.create_renderer('matplotlib', './output')
renderer.register_component(CustomGaugeComponent)
```

## 5. 移行ガイド

### 5.1. 既存コード変換例

**変更前（従来方式）:**
```python
chart_gen = ChartGenerator()
chart_gen.create_simple_line_chart(
    data={'x': [1,2,3], 'y': [4,5,6]},
    x_col='x', y_col='y', 
    title='Sample Chart',
    xlabel='X Axis', ylabel='Y Axis',
    output_filename='chart.html'
)
```

**変更後（新方式）:**
```python
generator = UniversalContentGenerator('./output')
spec = {
    "type": "content_block", 
    "engine": "matplotlib",
    "filename": "chart",
    "components": [{
        "type": "DataVisualization",
        "props": {
            "variant": "line",
            "data": {"x": [1,2,3], "y": [4,5,6]},
            "style": {
                "title": "Sample Chart",
                "xlabel": "X Axis", 
                "ylabel": "Y Axis"
            }
        }
    }]
}
generator.generate_from_spec(spec)
```

### 5.2. 段階的移行戦略

1. **Phase 1**: 既存APIをラッパーとして保持しつつ、内部で新システム使用
2. **Phase 2**: 新YAMLベース記法の並行サポート  
3. **Phase 3**: 既存API廃止予定の通知
4. **Phase 4**: 完全に新システムに移行

この実装により、PROJECT_BLUEPRINT.mdの理念を満たす、真にスケーラブルで保守性の高いコンテンツ生成プラットフォームが実現されます。
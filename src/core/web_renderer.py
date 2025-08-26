"""
Web描画エンジン（D3.js統合）

MCPサーバーから取得したD3.jsの知識とベストプラクティスを基に設計された
高度なWeb技術統合レンダラー。D3.js、SVG、Canvas、カスタムJavaScriptを使用して
最大限に柔軟でインタラクティブな可視化を生成します。
"""

from typing import Dict, List, Any, Optional, Union, Tuple
from pathlib import Path
import json
import logging
import hashlib
import base64
from datetime import datetime

from .component_renderer import ComponentRenderer, BaseComponent

logger = logging.getLogger(__name__)


class WebRenderer(ComponentRenderer):
    """Web技術統合描画エンジン（D3.js、SVG、Canvas）"""
    
    engine_name = "web"
    file_extension = "html"
    supported_component_types = [
        # 基本データ可視化
        "D3Chart", "CustomVisualization", "InteractiveChart",
        "NetworkGraph", "TreeVisualization", "HierarchicalData",
        
        # SVG/Canvas要素
        "SVGElement", "CanvasElement", "MixedVisualization",
        
        # 高度なインタラクション
        "Tooltip", "Brush", "Zoom", "Drag", "Animation", "Transition",
        
        # レイアウト
        "ForceLayout", "TreeLayout", "PackLayout", "PartitionLayout",
        "BundleLayout", "ChordLayout",
        
        # 特殊可視化
        "Wordcloud", "Treemap", "CircularPacking", "Sankey",
        "Parallel", "Radar", "Sunburst", "Icicle",
        
        # カスタム要素
        "CustomJS", "WebComponent", "ThirdPartyLib", "HTMLWidget"
    ]
    
    def __init__(self, output_dir: Path, config: Optional[Dict] = None):
        """
        WebRendererを初期化
        
        Args:
            output_dir: 出力ディレクトリ
            config: Web描画設定
        """
        super().__init__(output_dir, config)
        
        # D3.js設定
        self.d3_version = config.get('d3_version', 'v7') if config else 'v7'
        self.d3_modules = config.get('d3_modules', []) if config else []
        
        # レンダリング設定
        self.rendering_mode = config.get('rendering_mode', 'svg') if config else 'svg'  # svg, canvas, mixed
        self.enable_interactions = config.get('enable_interactions', True) if config else True
        self.responsive = config.get('responsive', True) if config else True
        
        # JavaScriptとCSS収集
        self.javascript_components = []
        self.css_styles = []
        self.external_libraries = set()
        
        # データ管理
        self.data_registry = {}
        self.component_instances = []
        
        # グローバル設定
        self.global_config = {
            'width': 800,
            'height': 600,
            'margin': {'top': 20, 'right': 20, 'bottom': 30, 'left': 40},
            'theme': 'default',  # default, dark, minimal, custom
            'animation_duration': 750,
            'transition_ease': 'd3.easeLinear',
            'color_scheme': 'd3.schemeCategory10'
        }
        
        if config:
            self.global_config.update(config.get('global', {}))
    
    def _register_default_components(self):
        """デフォルトコンポーネントを登録"""
        self.component_registry.update({
            # 基本チャート
            'D3Chart': D3ChartComponent,
            'CustomVisualization': CustomVisualizationComponent,
            'InteractiveChart': InteractiveChartComponent,
            
            # ネットワーク・階層
            'NetworkGraph': NetworkGraphComponent,
            'TreeVisualization': TreeVisualizationComponent,
            'HierarchicalData': HierarchicalDataComponent,
            
            # SVG/Canvas
            'SVGElement': SVGElementComponent,
            'CanvasElement': CanvasElementComponent,
            'MixedVisualization': MixedVisualizationComponent,
            
            # インタラクション
            'Tooltip': TooltipComponent,
            'Brush': BrushComponent,
            'Zoom': ZoomComponent,
            'Drag': DragComponent,
            'Animation': AnimationComponent,
            'Transition': TransitionComponent,
            
            # レイアウト
            'ForceLayout': ForceLayoutComponent,
            'TreeLayout': TreeLayoutComponent,
            'PackLayout': PackLayoutComponent,
            'PartitionLayout': PartitionLayoutComponent,
            'BundleLayout': BundleLayoutComponent,
            'ChordLayout': ChordLayoutComponent,
            
            # 特殊可視化
            'Wordcloud': WordcloudComponent,
            'Treemap': TreemapComponent,
            'CircularPacking': CircularPackingComponent,
            'Sankey': SankeyComponent,
            'Parallel': ParallelComponent,
            'Radar': RadarComponent,
            'Sunburst': SunburstComponent,
            'Icicle': IcicleComponent,
            
            # カスタム要素
            'CustomJS': CustomJSComponent,
            'WebComponent': WebComponentComponent,
            'ThirdPartyLib': ThirdPartyLibComponent,
            'HTMLWidget': HTMLWidgetComponent,
        })
    
    def _apply_global_config(self, config: Dict[str, Any]):
        """グローバル設定を適用"""
        if config.get('width'):
            self.global_config['width'] = config['width']
        if config.get('height'):
            self.global_config['height'] = config['height']
        if config.get('theme'):
            self.global_config['theme'] = config['theme']
            
        logger.info(f"Web描画設定を適用: {self.global_config}")
    
    def _save_rendered_content(self, content: Any, output_path: Path, config: Dict[str, Any]):
        """完全なHTMLファイルとして保存"""
        try:
            # D3.jsライブラリの取得
            d3_libraries = self._get_d3_libraries()
            
            # 外部ライブラリの取得
            external_libs = self._get_external_libraries()
            
            # CSS生成
            css_content = self._generate_css()
            
            # JavaScript生成
            js_content = self._generate_javascript()
            
            # データの埋め込み
            data_content = self._generate_data_scripts()
            
            # 完全なHTMLドキュメント生成
            html_content = self._generate_complete_html(
                d3_libraries, external_libs, css_content, js_content, data_content, config
            )
            
            # ファイル保存
            output_path.write_text(html_content, encoding='utf-8')
            
            logger.info(f"Web可視化HTMLを保存: {output_path}")
            
        except Exception as e:
            logger.error(f"Web描画の保存に失敗: {e}")
            raise
    
    def _get_d3_libraries(self) -> List[str]:
        """D3.jsライブラリのCDNリンクを生成"""
        base_url = f"https://d3js.org"
        
        # 基本D3.js
        libraries = [f"{base_url}/d3.{self.d3_version}.min.js"]
        
        # 追加モジュール
        for module in self.d3_modules:
            if module == 'geo-projection':
                libraries.append(f"{base_url}/d3-geo-projection.{self.d3_version}.min.js")
            elif module == 'sankey':
                libraries.append("https://unpkg.com/d3-sankey@0")
            elif module == 'cloud':
                libraries.append("https://cdn.jsdelivr.net/gh/holtzy/D3-graph-gallery@master/LIB/d3.layout.cloud.js")
        
        return libraries
    
    def _get_external_libraries(self) -> List[str]:
        """外部ライブラリのCDNリンクを取得"""
        libraries = []
        
        for lib in self.external_libraries:
            if lib == 'lodash':
                libraries.append("https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.21/lodash.min.js")
            elif lib == 'moment':
                libraries.append("https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.29.4/moment.min.js")
            elif lib == 'topojson':
                libraries.append("https://unpkg.com/topojson@3")
        
        return libraries
    
    def _generate_css(self) -> str:
        """CSSスタイルを生成"""
        # テーマに基づく基本スタイル
        theme_styles = self._get_theme_styles()
        
        css_content = f"""
        <style>
            /* WebRenderer基本スタイル */
            body {{
                margin: 0;
                padding: 20px;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background-color: {theme_styles['body_bg']};
                color: {theme_styles['text_color']};
            }}
            
            .web-viz-container {{
                max-width: 100%;
                margin: 0 auto;
                background: {theme_styles['container_bg']};
                border-radius: 8px;
                box-shadow: {theme_styles['shadow']};
                padding: 20px;
            }}
            
            .viz-title {{
                font-size: 24px;
                font-weight: 600;
                text-align: center;
                margin-bottom: 20px;
                color: {theme_styles['title_color']};
            }}
            
            /* SVG基本スタイル */
            svg {{
                display: block;
                margin: 0 auto;
            }}
            
            /* ツールチップスタイル */
            .d3-tooltip {{
                position: absolute;
                padding: 10px;
                background: rgba(0, 0, 0, 0.8);
                color: white;
                border-radius: 4px;
                font-size: 12px;
                pointer-events: none;
                opacity: 0;
                transition: opacity 0.2s;
            }}
            
            /* インタラクション要素 */
            .interactive-element:hover {{
                cursor: pointer;
                filter: brightness(1.1);
            }}
            
            /* アニメーション */
            .animated {{
                transition: all {self.global_config['animation_duration']}ms ease-in-out;
            }}
            
            /* レスポンシブ */
            @media (max-width: 768px) {{
                .web-viz-container {{
                    padding: 10px;
                }}
                
                .viz-title {{
                    font-size: 18px;
                }}
            }}
            
            /* カスタムスタイル */
            {chr(10).join(self.css_styles)}
        </style>
        """
        
        return css_content
    
    def _get_theme_styles(self) -> Dict[str, str]:
        """テーマに基づくスタイルを取得"""
        themes = {
            'default': {
                'body_bg': '#f8f9fa',
                'container_bg': '#ffffff',
                'text_color': '#212529',
                'title_color': '#495057',
                'shadow': '0 0.125rem 0.25rem rgba(0, 0, 0, 0.075)'
            },
            'dark': {
                'body_bg': '#121212',
                'container_bg': '#1e1e1e',
                'text_color': '#e0e0e0',
                'title_color': '#ffffff',
                'shadow': '0 0.125rem 0.25rem rgba(255, 255, 255, 0.075)'
            },
            'minimal': {
                'body_bg': '#ffffff',
                'container_bg': '#ffffff',
                'text_color': '#000000',
                'title_color': '#000000',
                'shadow': 'none'
            }
        }
        
        return themes.get(self.global_config['theme'], themes['default'])
    
    def _generate_javascript(self) -> str:
        """JavaScriptコードを生成"""
        js_content = f"""
        <script>
            // WebRendererグローバル設定
            const WebRenderer = {{
                config: {json.dumps(self.global_config, ensure_ascii=False, indent=2)},
                components: [],
                data: {{}},
                utils: {{}}
            }};
            
            // ユーティリティ関数
            WebRenderer.utils.createTooltip = function(container) {{
                return d3.select(container).append("div")
                    .attr("class", "d3-tooltip")
                    .style("opacity", 0);
            }};
            
            WebRenderer.utils.showTooltip = function(tooltip, content, event) {{
                tooltip
                    .html(content)
                    .style("left", (event.pageX + 10) + "px")
                    .style("top", (event.pageY - 10) + "px")
                    .style("opacity", 1);
            }};
            
            WebRenderer.utils.hideTooltip = function(tooltip) {{
                tooltip.style("opacity", 0);
            }};
            
            WebRenderer.utils.getColor = function(index, scheme) {{
                const colorScheme = scheme || WebRenderer.config.color_scheme;
                if (typeof colorScheme === 'string') {{
                    return d3.schemeCategory10[index % 10];
                }}
                return colorScheme[index % colorScheme.length];
            }};
            
            WebRenderer.utils.responsiveSVG = function(svg, aspectRatio) {{
                aspectRatio = aspectRatio || (WebRenderer.config.height / WebRenderer.config.width);
                
                svg
                    .attr("viewBox", `0 0 ${{WebRenderer.config.width}} ${{WebRenderer.config.height}}`)
                    .attr("preserveAspectRatio", "xMidYMid meet")
                    .style("width", "100%")
                    .style("height", "auto");
                
                if (WebRenderer.config.responsive) {{
                    const container = svg.node().parentNode;
                    d3.select(window).on("resize." + Math.random(), function() {{
                        const width = container.getBoundingClientRect().width;
                        svg.style("height", (width * aspectRatio) + "px");
                    }});
                }}
            }};
            
            // コンポーネント管理
            WebRenderer.registerComponent = function(name, instance) {{
                WebRenderer.components.push({{ name: name, instance: instance }});
            }};
            
            // データ管理
            WebRenderer.setData = function(key, data) {{
                WebRenderer.data[key] = data;
            }};
            
            WebRenderer.getData = function(key) {{
                return WebRenderer.data[key];
            }};
            
            // 初期化
            document.addEventListener('DOMContentLoaded', function() {{
                console.log('WebRenderer initialized with', WebRenderer.config);
                
                // カスタムコンポーネントの初期化
                {chr(10).join(self.javascript_components)}
            }});
        </script>
        """
        
        return js_content
    
    def _generate_data_scripts(self) -> str:
        """データ埋め込みスクリプトを生成"""
        data_scripts = []
        
        for key, data in self.data_registry.items():
            # データをJSONとしてシリアライズ
            try:
                json_data = json.dumps(data, ensure_ascii=False, indent=2)
                script = f"""
                <script>
                    WebRenderer.setData('{key}', {json_data});
                </script>
                """
                data_scripts.append(script)
            except Exception as e:
                logger.warning(f"データ '{key}' のシリアライズに失敗: {e}")
        
        return '\n'.join(data_scripts)
    
    def _generate_complete_html(
        self, 
        d3_libs: List[str], 
        external_libs: List[str],
        css_content: str, 
        js_content: str, 
        data_content: str,
        config: Dict[str, Any]
    ) -> str:
        """完全なHTMLドキュメントを生成"""
        
        title = config.get('title', 'Web可視化')
        meta_description = config.get('meta', {}).get('description', 'D3.js統合Web可視化')
        
        # ライブラリスクリプトタグ生成
        d3_script_tags = '\n    '.join([f'<script src="{lib}"></script>' for lib in d3_libs])
        external_script_tags = '\n    '.join([f'<script src="{lib}"></script>' for lib in external_libs])
        
        # メインコンテンツ領域
        main_content = '<div id="main-visualization" class="web-viz-container"></div>'
        if config.get('title'):
            main_content = f'<h1 class="viz-title">{config["title"]}</h1>\n    ' + main_content
        
        # 完全なHTMLテンプレート
        html_template = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{meta_description}">
    <title>{title}</title>
    
    <!-- External Libraries -->
    {external_script_tags}
    
    <!-- D3.js Libraries -->
    {d3_script_tags}
    
    {css_content}
</head>
<body>
    {main_content}
    
    <!-- Data Scripts -->
    {data_content}
    
    <!-- Main JavaScript -->
    {js_content}
</body>
</html>"""
        
        return html_template
    
    def add_data(self, key: str, data: Any):
        """データをレジストリに追加"""
        self.data_registry[key] = data
    
    def add_javascript(self, js_code: str):
        """カスタムJavaScriptを追加"""
        self.javascript_components.append(js_code)
    
    def add_css(self, css_code: str):
        """カスタムCSSを追加"""
        self.css_styles.append(css_code)
    
    def require_library(self, library_name: str):
        """外部ライブラリの依存関係を追加"""
        self.external_libraries.add(library_name)


# ======== 基本コンポーネント実装 ========

class D3ChartComponent(BaseComponent):
    """D3.js基本チャートコンポーネント"""
    
    type_name = "D3Chart"
    required_props = ['chart_type', 'data']
    optional_props = {
        'width': 800,
        'height': 600,
        'margin': {'top': 20, 'right': 20, 'bottom': 30, 'left': 40},
        'color_scheme': 'd3.schemeCategory10',
        'interactive': True,
        'animated': True
    }
    
    @classmethod
    def render(cls, props: Dict[str, Any], renderer: WebRenderer):
        props = cls.validate_props(props)
        
        chart_type = props['chart_type']
        data = props['data']
        width = props.get('width', renderer.global_config['width'])
        height = props.get('height', renderer.global_config['height'])
        margin = props.get('margin', renderer.global_config['margin'])
        
        # データをレジストリに登録
        data_key = f"chart_data_{id(props)}"
        renderer.add_data(data_key, data)
        
        # チャートタイプに応じたJavaScript生成
        if chart_type == 'bar':
            js_code = cls._generate_bar_chart_js(data_key, width, height, margin, props)
        elif chart_type == 'line':
            js_code = cls._generate_line_chart_js(data_key, width, height, margin, props)
        elif chart_type == 'scatter':
            js_code = cls._generate_scatter_chart_js(data_key, width, height, margin, props)
        elif chart_type == 'area':
            js_code = cls._generate_area_chart_js(data_key, width, height, margin, props)
        else:
            raise ValueError(f"未サポートのチャートタイプ: {chart_type}")
        
        renderer.add_javascript(js_code)
    
    @staticmethod
    def _generate_bar_chart_js(data_key: str, width: int, height: int, margin: Dict, props: Dict) -> str:
        return f"""
        // バーチャート生成
        (function() {{
            const data = WebRenderer.getData('{data_key}');
            const margin = {json.dumps(margin)};
            const width = {width} - margin.left - margin.right;
            const height = {height} - margin.top - margin.bottom;
            
            const svg = d3.select("#main-visualization")
                .append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom);
            
            WebRenderer.utils.responsiveSVG(svg);
            
            const g = svg.append("g")
                .attr("transform", `translate(${{margin.left}},${{margin.top}})`);
            
            // スケール設定
            const x = d3.scaleBand()
                .rangeRound([0, width])
                .padding(0.1)
                .domain(data.map(d => d.x));
            
            const y = d3.scaleLinear()
                .rangeRound([height, 0])
                .domain([0, d3.max(data, d => d.y)]);
            
            // 軸
            g.append("g")
                .attr("class", "axis axis--x")
                .attr("transform", `translate(0,${{height}})`)
                .call(d3.axisBottom(x));
            
            g.append("g")
                .attr("class", "axis axis--y")
                .call(d3.axisLeft(y).ticks(10));
            
            // ツールチップ
            const tooltip = WebRenderer.utils.createTooltip("#main-visualization");
            
            // バー
            g.selectAll(".bar")
                .data(data)
                .enter().append("rect")
                .attr("class", "bar interactive-element")
                .attr("x", d => x(d.x))
                .attr("y", d => y(d.y))
                .attr("width", x.bandwidth())
                .attr("height", d => height - y(d.y))
                .attr("fill", (d, i) => WebRenderer.utils.getColor(i))
                .on("mouseover", function(event, d) {{
                    WebRenderer.utils.showTooltip(tooltip, `値: ${{d.y}}`, event);
                }})
                .on("mouseout", function() {{
                    WebRenderer.utils.hideTooltip(tooltip);
                }});
            
            WebRenderer.registerComponent('BarChart', {{ svg: svg, data: data }});
        }})();
        """
    
    @staticmethod
    def _generate_line_chart_js(data_key: str, width: int, height: int, margin: Dict, props: Dict) -> str:
        return f"""
        // ラインチャート生成
        (function() {{
            const data = WebRenderer.getData('{data_key}');
            const margin = {json.dumps(margin)};
            const width = {width} - margin.left - margin.right;
            const height = {height} - margin.top - margin.bottom;
            
            const svg = d3.select("#main-visualization")
                .append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom);
            
            WebRenderer.utils.responsiveSVG(svg);
            
            const g = svg.append("g")
                .attr("transform", `translate(${{margin.left}},${{margin.top}})`);
            
            // スケール設定
            const x = d3.scaleLinear()
                .rangeRound([0, width])
                .domain(d3.extent(data, d => d.x));
            
            const y = d3.scaleLinear()
                .rangeRound([height, 0])
                .domain(d3.extent(data, d => d.y));
            
            // ライン生成器
            const line = d3.line()
                .x(d => x(d.x))
                .y(d => y(d.y))
                .curve(d3.curveMonotoneX);
            
            // 軸
            g.append("g")
                .attr("class", "axis axis--x")
                .attr("transform", `translate(0,${{height}})`)
                .call(d3.axisBottom(x));
            
            g.append("g")
                .attr("class", "axis axis--y")
                .call(d3.axisLeft(y));
            
            // ライン
            g.append("path")
                .datum(data)
                .attr("class", "line")
                .attr("fill", "none")
                .attr("stroke", WebRenderer.utils.getColor(0))
                .attr("stroke-width", 2)
                .attr("d", line);
            
            // ツールチップ付きドット
            const tooltip = WebRenderer.utils.createTooltip("#main-visualization");
            
            g.selectAll(".dot")
                .data(data)
                .enter().append("circle")
                .attr("class", "dot interactive-element")
                .attr("cx", d => x(d.x))
                .attr("cy", d => y(d.y))
                .attr("r", 4)
                .attr("fill", WebRenderer.utils.getColor(0))
                .on("mouseover", function(event, d) {{
                    WebRenderer.utils.showTooltip(tooltip, `X: ${{d.x}}, Y: ${{d.y}}`, event);
                }})
                .on("mouseout", function() {{
                    WebRenderer.utils.hideTooltip(tooltip);
                }});
            
            WebRenderer.registerComponent('LineChart', {{ svg: svg, data: data }});
        }})();
        """
    
    @staticmethod
    def _generate_scatter_chart_js(data_key: str, width: int, height: int, margin: Dict, props: Dict) -> str:
        return f"""
        // 散布図生成
        (function() {{
            const data = WebRenderer.getData('{data_key}');
            const margin = {json.dumps(margin)};
            const width = {width} - margin.left - margin.right;
            const height = {height} - margin.top - margin.bottom;
            
            const svg = d3.select("#main-visualization")
                .append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom);
            
            WebRenderer.utils.responsiveSVG(svg);
            
            const g = svg.append("g")
                .attr("transform", `translate(${{margin.left}},${{margin.top}})`);
            
            // スケール設定
            const x = d3.scaleLinear()
                .rangeRound([0, width])
                .domain(d3.extent(data, d => d.x));
            
            const y = d3.scaleLinear()
                .rangeRound([height, 0])
                .domain(d3.extent(data, d => d.y));
            
            // 軸
            g.append("g")
                .attr("class", "axis axis--x")
                .attr("transform", `translate(0,${{height}})`)
                .call(d3.axisBottom(x));
            
            g.append("g")
                .attr("class", "axis axis--y")
                .call(d3.axisLeft(y));
            
            // ツールチップ
            const tooltip = WebRenderer.utils.createTooltip("#main-visualization");
            
            // ドット
            g.selectAll(".dot")
                .data(data)
                .enter().append("circle")
                .attr("class", "dot interactive-element")
                .attr("cx", d => x(d.x))
                .attr("cy", d => y(d.y))
                .attr("r", d => d.r || 5)
                .attr("fill", (d, i) => WebRenderer.utils.getColor(i))
                .attr("opacity", 0.7)
                .on("mouseover", function(event, d) {{
                    d3.select(this).attr("r", (d.r || 5) * 1.5);
                    WebRenderer.utils.showTooltip(tooltip, `X: ${{d.x}}, Y: ${{d.y}}`, event);
                }})
                .on("mouseout", function(event, d) {{
                    d3.select(this).attr("r", d.r || 5);
                    WebRenderer.utils.hideTooltip(tooltip);
                }});
            
            WebRenderer.registerComponent('ScatterChart', {{ svg: svg, data: data }});
        }})();
        """
    
    @staticmethod
    def _generate_area_chart_js(data_key: str, width: int, height: int, margin: Dict, props: Dict) -> str:
        return f"""
        // エリアチャート生成
        (function() {{
            const data = WebRenderer.getData('{data_key}');
            const margin = {json.dumps(margin)};
            const width = {width} - margin.left - margin.right;
            const height = {height} - margin.top - margin.bottom;
            
            const svg = d3.select("#main-visualization")
                .append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom);
            
            WebRenderer.utils.responsiveSVG(svg);
            
            const g = svg.append("g")
                .attr("transform", `translate(${{margin.left}},${{margin.top}})`);
            
            // スケール設定
            const x = d3.scaleLinear()
                .rangeRound([0, width])
                .domain(d3.extent(data, d => d.x));
            
            const y = d3.scaleLinear()
                .rangeRound([height, 0])
                .domain([0, d3.max(data, d => d.y)]);
            
            // エリア生成器
            const area = d3.area()
                .x(d => x(d.x))
                .y0(height)
                .y1(d => y(d.y))
                .curve(d3.curveMonotoneX);
            
            // ライン生成器
            const line = d3.line()
                .x(d => x(d.x))
                .y(d => y(d.y))
                .curve(d3.curveMonotoneX);
            
            // 軸
            g.append("g")
                .attr("class", "axis axis--x")
                .attr("transform", `translate(0,${{height}})`)
                .call(d3.axisBottom(x));
            
            g.append("g")
                .attr("class", "axis axis--y")
                .call(d3.axisLeft(y));
            
            // エリア
            g.append("path")
                .datum(data)
                .attr("class", "area")
                .attr("fill", WebRenderer.utils.getColor(0))
                .attr("fill-opacity", 0.3)
                .attr("d", area);
            
            // ライン
            g.append("path")
                .datum(data)
                .attr("class", "line")
                .attr("fill", "none")
                .attr("stroke", WebRenderer.utils.getColor(0))
                .attr("stroke-width", 2)
                .attr("d", line);
            
            WebRenderer.registerComponent('AreaChart', {{ svg: svg, data: data }});
        }})();
        """


class CustomVisualizationComponent(BaseComponent):
    """カスタム可視化コンポーネント"""
    
    type_name = "CustomVisualization"
    required_props = ['javascript_code']
    optional_props = {
        'data': None,
        'css_code': '',
        'libraries': [],
        'dom_id': 'main-visualization'
    }
    
    @classmethod
    def render(cls, props: Dict[str, Any], renderer: WebRenderer):
        props = cls.validate_props(props)
        
        javascript_code = props['javascript_code']
        data = props.get('data')
        css_code = props.get('css_code', '')
        libraries = props.get('libraries', [])
        
        # 外部ライブラリの依存関係を追加
        for lib in libraries:
            renderer.require_library(lib)
        
        # データがある場合はレジストリに追加
        if data:
            data_key = f"custom_data_{id(props)}"
            renderer.add_data(data_key, data)
            
            # JavaScript内でデータキーを利用できるよう置換
            javascript_code = javascript_code.replace('{{DATA_KEY}}', data_key)
        
        # CSSがある場合は追加
        if css_code:
            renderer.add_css(css_code)
        
        # JavaScriptを追加
        renderer.add_javascript(javascript_code)


class NetworkGraphComponent(BaseComponent):
    """ネットワークグラフコンポーネント"""
    
    type_name = "NetworkGraph"
    required_props = ['nodes', 'links']
    optional_props = {
        'width': 800,
        'height': 600,
        'force_strength': -30,
        'link_distance': 30,
        'node_radius': 5,
        'charge': -120,
        'center_force': True,
        'collision_detection': True
    }
    
    @classmethod
    def render(cls, props: Dict[str, Any], renderer: WebRenderer):
        props = cls.validate_props(props)
        
        nodes = props['nodes']
        links = props['links']
        width = props.get('width', 800)
        height = props.get('height', 600)
        
        # ネットワークデータをレジストリに登録
        network_data = {'nodes': nodes, 'links': links}
        data_key = f"network_data_{id(props)}"
        renderer.add_data(data_key, network_data)
        
        # Force layoutのJavaScript生成
        js_code = f"""
        // ネットワークグラフ生成
        (function() {{
            const data = WebRenderer.getData('{data_key}');
            const width = {width};
            const height = {height};
            
            const svg = d3.select("#main-visualization")
                .append("svg")
                .attr("width", width)
                .attr("height", height);
            
            WebRenderer.utils.responsiveSVG(svg);
            
            // リンク
            const link = svg.append("g")
                .attr("class", "links")
                .selectAll("line")
                .data(data.links)
                .enter().append("line")
                .attr("stroke", "#aaa")
                .attr("stroke-width", d => Math.sqrt(d.value || 1));
            
            // ノード
            const node = svg.append("g")
                .attr("class", "nodes")
                .selectAll("circle")
                .data(data.nodes)
                .enter().append("circle")
                .attr("r", {props.get('node_radius', 5)})
                .attr("fill", (d, i) => WebRenderer.utils.getColor(i))
                .call(d3.drag()
                    .on("start", dragstarted)
                    .on("drag", dragged)
                    .on("end", dragended));
            
            // ツールチップ
            const tooltip = WebRenderer.utils.createTooltip("#main-visualization");
            
            node.on("mouseover", function(event, d) {{
                WebRenderer.utils.showTooltip(tooltip, d.id || d.name || "ノード", event);
            }})
            .on("mouseout", function() {{
                WebRenderer.utils.hideTooltip(tooltip);
            }});
            
            // フォースシミュレーション
            const simulation = d3.forceSimulation(data.nodes)
                .force("link", d3.forceLink(data.links).id(d => d.id).distance({props.get('link_distance', 30)}))
                .force("charge", d3.forceManyBody().strength({props.get('charge', -120)}))
                .force("center", d3.forceCenter(width / 2, height / 2))
                {"" if not props.get('collision_detection', True) else f".force('collision', d3.forceCollide().radius({props.get('node_radius', 5)} + 1))"};
            
            simulation.on("tick", function() {{
                link
                    .attr("x1", d => d.source.x)
                    .attr("y1", d => d.source.y)
                    .attr("x2", d => d.target.x)
                    .attr("y2", d => d.target.y);
                
                node
                    .attr("cx", d => d.x)
                    .attr("cy", d => d.y);
            }});
            
            function dragstarted(event) {{
                if (!event.active) simulation.alphaTarget(0.3).restart();
                event.subject.fx = event.subject.x;
                event.subject.fy = event.subject.y;
            }}
            
            function dragged(event) {{
                event.subject.fx = event.x;
                event.subject.fy = event.y;
            }}
            
            function dragended(event) {{
                if (!event.active) simulation.alphaTarget(0);
                event.subject.fx = null;
                event.subject.fy = null;
            }}
            
            WebRenderer.registerComponent('NetworkGraph', {{ 
                svg: svg, 
                simulation: simulation,
                nodes: data.nodes,
                links: data.links 
            }});
        }})();
        """
        
        renderer.add_javascript(js_code)


# 他のコンポーネント（簡略版）
class TreeVisualizationComponent(BaseComponent):
    type_name = "TreeVisualization"
    required_props = ['data']
    
    @classmethod
    def render(cls, props: Dict[str, Any], renderer: WebRenderer):
        # Tree layoutの実装（簡略化）
        renderer.add_javascript("// Tree visualization implementation")

class HierarchicalDataComponent(BaseComponent):
    type_name = "HierarchicalData"
    required_props = ['data']

class SVGElementComponent(BaseComponent):
    type_name = "SVGElement"
    required_props = ['element_type']

class CanvasElementComponent(BaseComponent):
    type_name = "CanvasElement"
    required_props = ['draw_function']

class MixedVisualizationComponent(BaseComponent):
    type_name = "MixedVisualization"
    required_props = ['svg_components', 'canvas_components']

# インタラクションコンポーネント
class TooltipComponent(BaseComponent):
    type_name = "Tooltip"

class BrushComponent(BaseComponent):
    type_name = "Brush"

class ZoomComponent(BaseComponent):
    type_name = "Zoom"

class DragComponent(BaseComponent):
    type_name = "Drag"

class AnimationComponent(BaseComponent):
    type_name = "Animation"

class TransitionComponent(BaseComponent):
    type_name = "Transition"

# レイアウトコンポーネント
class ForceLayoutComponent(BaseComponent):
    type_name = "ForceLayout"

class TreeLayoutComponent(BaseComponent):
    type_name = "TreeLayout"

class PackLayoutComponent(BaseComponent):
    type_name = "PackLayout"

class PartitionLayoutComponent(BaseComponent):
    type_name = "PartitionLayout"

class BundleLayoutComponent(BaseComponent):
    type_name = "BundleLayout"

class ChordLayoutComponent(BaseComponent):
    type_name = "ChordLayout"

# 特殊可視化コンポーネント
class WordcloudComponent(BaseComponent):
    type_name = "Wordcloud"
    required_props = ['words']
    
    @classmethod
    def render(cls, props: Dict[str, Any], renderer: WebRenderer):
        # WordcloudはD3-cloudライブラリが必要
        renderer.d3_modules.append('cloud')

class TreemapComponent(BaseComponent):
    type_name = "Treemap"
    required_props = ['data']

class CircularPackingComponent(BaseComponent):
    type_name = "CircularPacking"
    required_props = ['data']

class SankeyComponent(BaseComponent):
    type_name = "Sankey"
    required_props = ['nodes', 'links']
    
    @classmethod
    def render(cls, props: Dict[str, Any], renderer: WebRenderer):
        # SankeyはD3-sankeyライブラリが必要
        renderer.d3_modules.append('sankey')

class ParallelComponent(BaseComponent):
    type_name = "Parallel"

class RadarComponent(BaseComponent):
    type_name = "Radar"

class SunburstComponent(BaseComponent):
    type_name = "Sunburst"

class IcicleComponent(BaseComponent):
    type_name = "Icicle"

# カスタム要素コンポーネント
class CustomJSComponent(BaseComponent):
    type_name = "CustomJS"
    required_props = ['code']

class WebComponentComponent(BaseComponent):
    type_name = "WebComponent"

class ThirdPartyLibComponent(BaseComponent):
    type_name = "ThirdPartyLib"
    required_props = ['library_name']

class HTMLWidgetComponent(BaseComponent):
    type_name = "HTMLWidget"
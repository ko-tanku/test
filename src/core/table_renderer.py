"""
テーブル描画エンジン

既存のTableGeneratorを統合し、宣言的コンポーネントシステムに適合させた
高機能なテーブル・グリッドレンダラー。様々な表形式やインタラクティブ機能をサポートします。
"""

from typing import Dict, List, Any, Optional, Union
from pathlib import Path
import json
import logging
from html import escape

import pandas as pd

from .component_renderer import ComponentRenderer, BaseComponent
from .table_generator import TableGenerator
from .utils import slugify

logger = logging.getLogger(__name__)


class TableRenderer(ComponentRenderer):
    """テーブル描画エンジン"""
    
    engine_name = "table"
    file_extension = "html"
    supported_component_types = [
        "BasicTable", "ComparisonTable", "DataTable", "Grid",
        "InteractiveTable", "SortableTable", "FilterableTable",
        "PivotTable", "SummaryTable", "StatisticsTable"
    ]
    
    def __init__(self, output_dir: Path, config: Optional[Dict] = None):
        """
        TableRendererを初期化
        
        Args:
            output_dir: 出力ディレクトリ
            config: テーブル設定
        """
        super().__init__(output_dir, config)
        
        # 既存のTableGeneratorを統合
        self.table_generator = TableGenerator(
            colors=config.get('colors') if config else None,
            styles=config.get('styles') if config else None
        )
        
        # テーブルコンテンツを保存するリスト
        self.table_contents = []
        
        # グローバル設定
        self.global_config = {
            'title': '',
            'layout': 'single',  # single, multi, dashboard
            'theme': 'default',   # default, dark, minimal
            'responsive': True,
            'show_borders': True,
            'show_grid_lines': True,
            'font_family': 'sans-serif',
            'font_size': '14px'
        }
        
        if config:
            self.global_config.update(config.get('global', {}))
    
    def _register_default_components(self):
        """デフォルトコンポーネントを登録"""
        self.component_registry.update({
            'BasicTable': BasicTableComponent,
            'ComparisonTable': ComparisonTableComponent,
            'DataTable': DataTableComponent,
            'Grid': GridComponent,
            'InteractiveTable': InteractiveTableComponent,
            'SortableTable': SortableTableComponent,
            'FilterableTable': FilterableTableComponent,
            'PivotTable': PivotTableComponent,
            'SummaryTable': SummaryTableComponent,
            'StatisticsTable': StatisticsTableComponent,
        })
    
    def _apply_global_config(self, config: Dict[str, Any]):
        """グローバル設定を適用"""
        if config.get('title'):
            self.global_config['title'] = config['title']
        
        if config.get('theme'):
            self.global_config['theme'] = config['theme']
            
        if config.get('layout'):
            self.global_config['layout'] = config['layout']
            
        logger.info(f"テーブル設定を適用: {self.global_config}")
    
    def _save_rendered_content(self, content: Any, output_path: Path, config: Dict[str, Any]):
        """HTMLファイルとして保存"""
        try:
            # テーマに基づくスタイル設定
            theme_styles = self._get_theme_styles(self.global_config['theme'])
            
            # 完全なHTMLドキュメントを生成
            html_content = self._generate_complete_html(theme_styles)
            
            # ファイル保存
            output_path.write_text(html_content, encoding='utf-8')
            
            logger.info(f"テーブルHTMLを保存: {output_path}")
            
        except Exception as e:
            logger.error(f"テーブル保存に失敗: {e}")
            raise
    
    def _get_theme_styles(self, theme: str) -> Dict[str, str]:
        """テーマに基づくスタイルを取得"""
        themes = {
            'default': {
                'body_bg': '#f5f5f5',
                'content_bg': '#ffffff',
                'text_color': '#333333',
                'border_color': '#dddddd',
                'header_bg': '#00BCD4',
                'header_text': '#ffffff',
                'shadow': '0 2px 4px rgba(0,0,0,0.1)'
            },
            'dark': {
                'body_bg': '#1a1a1a',
                'content_bg': '#2d2d2d',
                'text_color': '#e0e0e0',
                'border_color': '#404040',
                'header_bg': '#0097a7',
                'header_text': '#ffffff',
                'shadow': '0 2px 8px rgba(0,0,0,0.3)'
            },
            'minimal': {
                'body_bg': '#ffffff',
                'content_bg': '#ffffff',
                'text_color': '#2c2c2c',
                'border_color': '#e8e8e8',
                'header_bg': '#f8f9fa',
                'header_text': '#495057',
                'shadow': '0 1px 2px rgba(0,0,0,0.05)'
            }
        }
        
        return themes.get(theme, themes['default'])
    
    def _generate_complete_html(self, theme_styles: Dict[str, str]) -> str:
        """完全なHTMLドキュメントを生成"""
        # すべてのテーブルコンテンツを結合
        tables_html = '\n'.join(self.table_contents)
        
        # レスポンシブ設定
        responsive_meta = '<meta name="viewport" content="width=device-width, initial-scale=1">' if self.global_config.get('responsive') else ''
        
        # グローバルタイトル
        title_html = f'<h1 style="color: {theme_styles["text_color"]; margin-bottom: 30px; text-align: center;">{escape(self.global_config["title"])}</h1>' if self.global_config['title'] else ''
        
        # CSS スタイル
        css_styles = f"""
        <style>
            body {{
                margin: 0;
                padding: 20px;
                font-family: {self.global_config['font_family']};
                font-size: {self.global_config['font_size']};
                background-color: {theme_styles['body_bg']};
                color: {theme_styles['text_color']};
                line-height: 1.6;
            }}
            
            .content-wrapper {{
                background-color: {theme_styles['content_bg']};
                padding: 30px;
                border-radius: 8px;
                box-shadow: {theme_styles['shadow']};
                max-width: 100%;
                overflow: hidden;
                margin: 0 auto;
            }}
            
            /* テーブル間のスペーシング */
            .table-section {{
                margin-bottom: 40px;
            }}
            
            .table-section:last-child {{
                margin-bottom: 0;
            }}
            
            /* グリッドレイアウト */
            .multi-table-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
                gap: 30px;
                margin-top: 20px;
            }}
            
            /* レスポンシブ対応 */
            @media (max-width: 768px) {{
                body {{
                    padding: 10px;
                }}
                
                .content-wrapper {{
                    padding: 15px;
                }}
                
                .multi-table-grid {{
                    grid-template-columns: 1fr;
                    gap: 20px;
                }}
                
                table {{
                    font-size: 12px !important;
                }}
            }}
            
            /* インタラクティブテーブル用のスタイル */
            .sortable th {{
                cursor: pointer;
                position: relative;
            }}
            
            .sortable th::after {{
                content: '↕️';
                position: absolute;
                right: 8px;
                opacity: 0.5;
            }}
            
            .filterable-container {{
                margin-bottom: 15px;
            }}
            
            .filter-input {{
                padding: 8px;
                border: 1px solid {theme_styles['border_color']};
                border-radius: 4px;
                width: 200px;
                background-color: {theme_styles['content_bg']};
                color: {theme_styles['text_color']};
            }}
        </style>
        """
        
        # レイアウトに基づいてコンテンツを配置
        if self.global_config['layout'] == 'multi':
            content_html = f'<div class="multi-table-grid">{tables_html}</div>'
        else:
            content_html = tables_html
        
        return f"""
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="utf-8">
    {responsive_meta}
    <title>{escape(self.global_config.get('title', 'テーブル'))}</title>
    {css_styles}
</head>
<body>
    <div class="content-wrapper">
        {title_html}
        {content_html}
    </div>
    
    <!-- インタラクティブ機能用JavaScript -->
    <script>
        // ソート機能
        function makeTableSortable(tableId) {{
            const table = document.getElementById(tableId);
            if (!table) return;
            
            const headers = table.querySelectorAll('th');
            headers.forEach((header, index) => {{
                header.addEventListener('click', () => {{
                    sortTable(table, index);
                }});
            }});
        }}
        
        function sortTable(table, columnIndex) {{
            const tbody = table.querySelector('tbody');
            const rows = Array.from(tbody.querySelectorAll('tr'));
            
            rows.sort((a, b) => {{
                const aValue = a.cells[columnIndex].textContent.trim();
                const bValue = b.cells[columnIndex].textContent.trim();
                
                // 数値として比較を試行
                const aNum = parseFloat(aValue);
                const bNum = parseFloat(bValue);
                
                if (!isNaN(aNum) && !isNaN(bNum)) {{
                    return aNum - bNum;
                }}
                
                // 文字列として比較
                return aValue.localeCompare(bValue);
            }});
            
            rows.forEach(row => tbody.appendChild(row));
        }}
        
        // フィルタ機能
        function makeTableFilterable(tableId, filterId) {{
            const table = document.getElementById(tableId);
            const filter = document.getElementById(filterId);
            
            if (!table || !filter) return;
            
            filter.addEventListener('keyup', function() {{
                const filterValue = this.value.toLowerCase();
                const rows = table.querySelectorAll('tbody tr');
                
                rows.forEach(row => {{
                    const text = row.textContent.toLowerCase();
                    row.style.display = text.includes(filterValue) ? '' : 'none';
                }});
            }});
        }}
        
        // DOMロード後に初期化
        document.addEventListener('DOMContentLoaded', function() {{
            // ソートテーブルを初期化
            document.querySelectorAll('.sortable').forEach(table => {{
                makeTableSortable(table.id);
            }});
            
            // フィルタテーブルを初期化
            document.querySelectorAll('.filterable').forEach(table => {{
                const filterId = table.id + '_filter';
                makeTableFilterable(table.id, filterId);
            }});
        }});
    </script>
</body>
</html>
        """
    
    def add_table_content(self, html_content: str):
        """テーブルコンテンツを追加"""
        self.table_contents.append(f'<div class="table-section">{html_content}</div>')


# ======== コンポーネント実装 ========

class BasicTableComponent(BaseComponent):
    """基本テーブルコンポーネント"""
    
    type_name = "BasicTable"
    required_props = ['headers', 'rows']
    optional_props = {
        'title': '',
        'style': {},
        'responsive': True,
        'show_borders': True
    }
    
    @classmethod
    def render(cls, props: Dict[str, Any], renderer: TableRenderer):
        props = cls.validate_props(props)
        
        headers = props['headers']
        rows = props['rows']
        title = props.get('title', '')
        style = props.get('style', {})
        
        # 既存のTableGeneratorを使用
        temp_path = renderer.table_generator.create_basic_table(
            headers=headers,
            rows=rows,
            title=title,
            output_filename="temp_table.html",
            custom_styles=style,
            output_dir=renderer.output_dir
        )
        
        # HTMLコンテンツを読み取り、テーブル部分のみを抽出
        full_html = temp_path.read_text(encoding='utf-8')
        
        # テーブル部分のみを抽出（簡略化された実装）
        start_marker = '<div class="table-container">'
        end_marker = '</div>'
        
        start_idx = full_html.find(start_marker)
        if start_idx != -1:
            end_idx = full_html.find(end_marker, start_idx) + len(end_marker)
            table_html = full_html[start_idx:end_idx]
            renderer.add_table_content(table_html)
        
        # 一時ファイルを削除
        temp_path.unlink()


class ComparisonTableComponent(BaseComponent):
    """比較テーブルコンポーネント"""
    
    type_name = "ComparisonTable"
    required_props = ['categories', 'items', 'data']
    optional_props = {
        'title': '',
        'style': {},
        'highlight_differences': True
    }
    
    @classmethod
    def render(cls, props: Dict[str, Any], renderer: TableRenderer):
        props = cls.validate_props(props)
        
        categories = props['categories']
        items = props['items']
        data = props['data']
        title = props.get('title', '')
        style = props.get('style', {})
        
        # 既存のTableGeneratorを使用
        temp_path = renderer.table_generator.create_comparison_table(
            categories=categories,
            items=items,
            data=data,
            title=title,
            output_filename="temp_comparison.html",
            custom_styles=style,
            output_dir=renderer.output_dir
        )
        
        # HTMLコンテンツを読み取り、テーブル部分のみを抽出
        full_html = temp_path.read_text(encoding='utf-8')
        
        # テーブル部分のみを抽出
        start_marker = '<div class="table-container">'
        end_marker = '</div>'
        
        start_idx = full_html.find(start_marker)
        if start_idx != -1:
            end_idx = full_html.find(end_marker, start_idx) + len(end_marker)
            table_html = full_html[start_idx:end_idx]
            renderer.add_table_content(table_html)
        
        # 一時ファイルを削除
        temp_path.unlink()


class DataTableComponent(BaseComponent):
    """データテーブルコンポーネント（Pandas DataFrame対応）"""
    
    type_name = "DataTable"
    required_props = ['data']
    optional_props = {
        'title': '',
        'columns': None,
        'style': {},
        'format': {},
        'show_index': False
    }
    
    @classmethod
    def render(cls, props: Dict[str, Any], renderer: TableRenderer):
        props = cls.validate_props(props)
        
        data = props['data']
        title = props.get('title', '')
        columns = props.get('columns')
        style = props.get('style', {})
        format_config = props.get('format', {})
        show_index = props.get('show_index', False)
        
        # DataFrameを作成または変換
        if isinstance(data, dict):
            df = pd.DataFrame(data)
        elif isinstance(data, list):
            df = pd.DataFrame(data, columns=columns)
        else:
            df = data  # 既にDataFrameの場合
        
        # フォーマット適用
        for col, fmt in format_config.items():
            if col in df.columns:
                if fmt == 'currency':
                    df[col] = df[col].apply(lambda x: f"¥{x:,}" if pd.notna(x) else '')
                elif fmt == 'percentage':
                    df[col] = df[col].apply(lambda x: f"{x:.1%}" if pd.notna(x) else '')
                elif isinstance(fmt, str) and '{' in fmt:
                    df[col] = df[col].apply(lambda x: fmt.format(x) if pd.notna(x) else '')
        
        # HTMLテーブル生成
        table_id = f"table_{slugify(title) if title else 'data'}"
        
        # スタイル適用でテーブルHTML生成
        table_html = renderer.table_generator._generate_html_table_string(
            df, table_id, title, style
        )
        
        renderer.add_table_content(table_html)


class GridComponent(BaseComponent):
    """グリッドレイアウトコンポーネント"""
    
    type_name = "Grid"
    required_props = ['tables']
    optional_props = {
        'columns': 2,
        'gap': '20px',
        'responsive': True
    }
    
    @classmethod
    def render(cls, props: Dict[str, Any], renderer: TableRenderer):
        props = cls.validate_props(props)
        
        tables = props['tables']
        columns = props.get('columns', 2)
        gap = props.get('gap', '20px')
        
        # グリッド開始
        grid_html = f'<div style="display: grid; grid-template-columns: repeat({columns}, 1fr); gap: {gap};">'
        
        # 各テーブルをレンダリング
        for table_spec in tables:
            component_type = table_spec['type']
            if component_type in renderer.component_registry:
                component_class = renderer.component_registry[component_type]
                
                # 一時レンダラーを使用してテーブルを生成
                temp_renderer = TableRenderer(renderer.output_dir, renderer.config)
                component_class.render(table_spec['props'], temp_renderer)
                
                # 生成されたコンテンツを取得
                if temp_renderer.table_contents:
                    grid_html += f'<div>{temp_renderer.table_contents[0]}</div>'
        
        grid_html += '</div>'
        renderer.add_table_content(grid_html)


class InteractiveTableComponent(BaseComponent):
    """インタラクティブテーブルコンポーネント（ソート・フィルタ対応）"""
    
    type_name = "InteractiveTable"
    required_props = ['headers', 'rows']
    optional_props = {
        'title': '',
        'sortable': True,
        'filterable': True,
        'style': {}
    }
    
    @classmethod
    def render(cls, props: Dict[str, Any], renderer: TableRenderer):
        props = cls.validate_props(props)
        
        headers = props['headers']
        rows = props['rows']
        title = props.get('title', '')
        sortable = props.get('sortable', True)
        filterable = props.get('filterable', True)
        style = props.get('style', {})
        
        # DataFrameを作成
        df = pd.DataFrame(rows, columns=headers)
        table_id = f"table_{slugify(title) if title else 'interactive'}"
        
        # テーブルクラスを設定
        table_classes = []
        if sortable:
            table_classes.append('sortable')
        if filterable:
            table_classes.append('filterable')
        
        # フィルタ入力を追加
        filter_html = ''
        if filterable:
            filter_id = f"{table_id}_filter"
            filter_html = f'''
            <div class="filterable-container">
                <input type="text" id="{filter_id}" class="filter-input" placeholder="テーブルを検索...">
            </div>
            '''
        
        # テーブルHTML生成（カスタムクラス付き）
        table_html = renderer.table_generator._generate_html_table_string(
            df, table_id, title, style
        )
        
        # クラスを追加
        if table_classes:
            class_str = ' '.join(table_classes)
            table_html = table_html.replace('<table ', f'<table class="{class_str}" ')
        
        # 完全なHTMLを組み合わせ
        complete_html = filter_html + table_html
        renderer.add_table_content(complete_html)


# 簡略版の追加コンポーネント
class SortableTableComponent(InteractiveTableComponent):
    type_name = "SortableTable"
    
    @classmethod
    def render(cls, props: Dict[str, Any], renderer: TableRenderer):
        props['sortable'] = True
        props['filterable'] = False
        super().render(props, renderer)


class FilterableTableComponent(InteractiveTableComponent):
    type_name = "FilterableTable"
    
    @classmethod
    def render(cls, props: Dict[str, Any], renderer: TableRenderer):
        props['sortable'] = False
        props['filterable'] = True
        super().render(props, renderer)


class PivotTableComponent(BaseComponent):
    """ピボットテーブルコンポーネント"""
    
    type_name = "PivotTable"
    required_props = ['data', 'index', 'columns', 'values']
    optional_props = {
        'title': '',
        'aggfunc': 'sum',
        'style': {}
    }
    
    @classmethod
    def render(cls, props: Dict[str, Any], renderer: TableRenderer):
        props = cls.validate_props(props)
        
        data = props['data']
        index = props['index']
        columns = props['columns']
        values = props['values']
        title = props.get('title', '')
        aggfunc = props.get('aggfunc', 'sum')
        style = props.get('style', {})
        
        # DataFrameを作成
        if isinstance(data, dict):
            df = pd.DataFrame(data)
        else:
            df = data
        
        # ピボットテーブル作成
        pivot_df = df.pivot_table(
            index=index,
            columns=columns,
            values=values,
            aggfunc=aggfunc,
            fill_value=0
        )
        
        # インデックスをリセットして通常の列にする
        pivot_df = pivot_df.reset_index()
        
        # テーブルHTML生成
        table_id = f"table_{slugify(title) if title else 'pivot'}"
        table_html = renderer.table_generator._generate_html_table_string(
            pivot_df, table_id, title, style
        )
        
        renderer.add_table_content(table_html)


class SummaryTableComponent(BaseComponent):
    """サマリーテーブルコンポーネント"""
    
    type_name = "SummaryTable"
    required_props = ['data']
    optional_props = {
        'title': '',
        'metrics': ['count', 'mean', 'std', 'min', 'max'],
        'style': {}
    }
    
    @classmethod
    def render(cls, props: Dict[str, Any], renderer: TableRenderer):
        props = cls.validate_props(props)
        
        data = props['data']
        title = props.get('title', '')
        metrics = props.get('metrics', ['count', 'mean', 'std', 'min', 'max'])
        style = props.get('style', {})
        
        # DataFrameを作成
        if isinstance(data, dict):
            df = pd.DataFrame(data)
        else:
            df = data
        
        # 統計サマリーを生成
        summary_df = df.describe().loc[metrics].round(2)
        summary_df = summary_df.reset_index()
        summary_df.rename(columns={'index': '統計量'}, inplace=True)
        
        # テーブルHTML生成
        table_id = f"table_{slugify(title) if title else 'summary'}"
        table_html = renderer.table_generator._generate_html_table_string(
            summary_df, table_id, title, style
        )
        
        renderer.add_table_content(table_html)


class StatisticsTableComponent(BaseComponent):
    """統計テーブルコンポーネント"""
    
    type_name = "StatisticsTable"
    required_props = ['data', 'statistics']
    optional_props = {
        'title': '',
        'style': {},
        'format': 'auto'
    }
    
    @classmethod
    def render(cls, props: Dict[str, Any], renderer: TableRenderer):
        props = cls.validate_props(props)
        
        data = props['data']
        statistics = props['statistics']
        title = props.get('title', '')
        style = props.get('style', {})
        fmt = props.get('format', 'auto')
        
        # DataFrameを作成
        if isinstance(data, dict):
            df = pd.DataFrame(data)
        else:
            df = data
        
        # 統計情報を計算
        stats_data = []
        for stat in statistics:
            if stat == 'count':
                stats_data.append(['件数', df.shape[0]])
            elif stat == 'mean':
                stats_data.append(['平均', df.select_dtypes(include=['number']).mean().round(2).to_dict()])
            elif stat == 'median':
                stats_data.append(['中央値', df.select_dtypes(include=['number']).median().round(2).to_dict()])
            elif stat == 'std':
                stats_data.append(['標準偏差', df.select_dtypes(include=['number']).std().round(2).to_dict()])
        
        # 統計テーブル作成
        if stats_data:
            stats_df = pd.DataFrame(stats_data, columns=['統計量', '値'])
            
            # テーブルHTML生成
            table_id = f"table_{slugify(title) if title else 'statistics'}"
            table_html = renderer.table_generator._generate_html_table_string(
                stats_df, table_id, title, style
            )
            
            renderer.add_table_content(table_html)
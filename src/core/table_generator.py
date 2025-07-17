"""
Table generator for MkDocs Materials Generator
様々な形式の表データを生成し、HTMLファイルとして出力するためのクラス
"""

import logging
import html
from pathlib import Path
from typing import Dict, List, Optional, Any, Union

import pandas as pd

from .config import PATHS, GLOBAL_COLORS
from .base_config import BASE_TABLE_STYLES
from .utils import ensure_directory_exists, safe_filename

logger = logging.getLogger(__name__)


class TableGenerator:
    """
    表データを生成し、HTMLファイルとして出力するためのクラス
    """
    
    def __init__(self, colors: Optional[Dict[str, str]] = None, styles: Optional[Dict[str, Any]] = None):
        """
        初期化
        
        Args:
            colors: カスタムカラー辞書
            styles: カスタムスタイル辞書
        """
        self.colors = colors or GLOBAL_COLORS
        self.styles = {**BASE_TABLE_STYLES, **(styles or {})}
        self.output_dir = ensure_directory_exists(PATHS["tables_dir"])
        self.logger = logging.getLogger(__name__ + ".TableGenerator")
    
    def _generate_html_table_string(
        self, 
        df: pd.DataFrame, 
        table_id: str, 
        title: str = "", 
        custom_styles: Optional[Dict[str, str]] = None
    ) -> str:
        """
        Pandas DataFrameからHTMLテーブル文字列を生成
        
        Args:
            df: データフレーム
            table_id: テーブルの一意ID
            title: テーブルタイトル
            custom_styles: カスタムスタイル辞書
            
        Returns:
            HTMLテーブル文字列
        """
        try:
            # スタイル設定
            table_styles = {**self.styles, **(custom_styles or {})}
            
            # CSSスタイルを構築（レスポンシブ対応）
            css_styles = f"""
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                
                body {{
                    font-family: {table_styles.get('font_family', 'Arial')};
                    background-color: #ffffff;
                    padding: 20px;
                    height: 100vh;
                    overflow: auto;
                }}
                
                .table-container {{
                    width: 100%;
                    height: 100%;
                    background-color: #ffffff;
                    border-radius: 8px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                    overflow: hidden;
                }}
                
                .table-title {{
                    font-size: 18px;
                    font-weight: bold;
                    padding: 20px;
                    color: {table_styles.get('header_bg_color', '#1976d2')};
                    background-color: #f8f9fa;
                    border-bottom: 2px solid {table_styles.get('header_bg_color', '#1976d2')};
                }}
                
                .table-responsive {{
                    width: 100%;
                    overflow-x: auto;
                    overflow-y: auto;
                    max-height: calc(100vh - 120px);
                }}
                
                #{table_id} {{
                    width: 100%;
                    min-width: 600px;
                    border-collapse: collapse;
                    font-family: {table_styles.get('font_family', 'Arial')};
                    font-size: {table_styles.get('font_size', '14px')};
                    background-color: white;
                }}
                
                #{table_id} th {{
                    background-color: {table_styles.get('header_bg_color', '#1976d2')};
                    color: {table_styles.get('header_text_color', '#ffffff')};
                    padding: {table_styles.get('cell_padding', '12px 16px')};
                    text-align: left;
                    font-weight: bold;
                    border: 1px solid {table_styles.get('border_color', '#e0e0e0')};
                    position: sticky;
                    top: 0;
                    z-index: 10;
                }}
                
                #{table_id} td {{
                    padding: {table_styles.get('cell_padding', '12px 16px')};
                    border: 1px solid {table_styles.get('border_color', '#e0e0e0')};
                    text-align: left;
                    vertical-align: top;
                }}
                
                #{table_id} tr:nth-child(even) {{
                    background-color: {table_styles.get('row_even_bg_color', '#f8f9fa')};
                }}
                
                #{table_id} tr:nth-child(odd) {{
                    background-color: {table_styles.get('row_odd_bg_color', '#ffffff')};
                }}
                
                #{table_id} tr:hover {{
                    background-color: rgba(25, 118, 210, 0.1);
                }}
                
                @media (max-width: 768px) {{
                    body {{
                        padding: 10px;
                    }}
                    
                    #{table_id} {{
                        font-size: 12px;
                        min-width: 500px;
                    }}
                    
                    #{table_id} th,
                    #{table_id} td {{
                        padding: 8px 12px;
                    }}
                    
                    .table-title {{
                        font-size: 16px;
                        padding: 15px;
                    }}
                }}
            </style>
            """
            
            # テーブルHTMLを構築
            html_parts = []
            
            # 完全なHTMLドキュメント
            html_parts.append('<!DOCTYPE html>')
            html_parts.append('<html lang="ja">')
            html_parts.append('<head>')
            html_parts.append('<meta charset="UTF-8">')
            html_parts.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
            html_parts.append(f'<title>{html.escape(title) if title else "Table"}</title>')
            html_parts.append(css_styles)
            html_parts.append('</head>')
            html_parts.append('<body>')
            
            # コンテナ開始
            html_parts.append('<div class="table-container">')
            
            # タイトル
            if title:
                escaped_title = html.escape(title)
                html_parts.append(f'<div class="table-title">{escaped_title}</div>')
            
            # レスポンシブラッパー
            html_parts.append('<div class="table-responsive">')
            
            # テーブル開始
            html_parts.append(f'<table id="{table_id}">')
            
            # ヘッダー
            html_parts.append('<thead>')
            html_parts.append('<tr>')
            for col in df.columns:
                escaped_col = html.escape(str(col))
                html_parts.append(f'<th>{escaped_col}</th>')
            html_parts.append('</tr>')
            html_parts.append('</thead>')
            
            # ボディ
            html_parts.append('<tbody>')
            for _, row in df.iterrows():
                html_parts.append('<tr>')
                for value in row:
                    escaped_value = html.escape(str(value))
                    html_parts.append(f'<td>{escaped_value}</td>')
                html_parts.append('</tr>')
            html_parts.append('</tbody>')
            
            # テーブル終了
            html_parts.append('</table>')
            html_parts.append('</div>')  # table-responsive
            html_parts.append('</div>')  # table-container
            html_parts.append('</body>')
            html_parts.append('</html>')
            
            return '\n'.join(html_parts)
            
        except Exception as e:
            self.logger.error(f"Failed to generate HTML table: {e}")
            raise    

        
    def create_basic_table(
        self, 
        headers: List[str], 
        rows: List[List[Any]], 
        title: str, 
        output_filename: str = "basic_table.html",
        custom_styles: Optional[Dict[str, str]] = None
    ) -> Path:
        """
        基本的なテーブルを生成
        
        Args:
            headers: テーブルヘッダー
            rows: テーブルの行データ
            title: テーブルタイトル
            output_filename: 出力ファイル名
            custom_styles: カスタムスタイル辞書
            
        Returns:
            保存されたファイルのパス
        """
        try:
            # データフレームを作成
            df = pd.DataFrame(rows, columns=headers)
            
            # 安全なファイル名
            safe_name = safe_filename(output_filename)
            if not safe_name.endswith('.html'):
                safe_name += '.html'
            
            output_path = self.output_dir / safe_name
            
            # テーブルIDを生成
            table_id = f"table_{safe_name.replace('.html', '').replace('-', '_')}"
            
            # HTMLを生成
            html_content = self._generate_html_table_string(df, table_id, title, custom_styles)
            
            # ファイルに保存
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            self.logger.info(f"Basic table saved: {output_path}")
            
            return output_path
            
        except Exception as e:
            self.logger.error(f"Failed to create basic table: {e}")
            raise
    
    def create_comparison_table(
        self, 
        categories: List[str], 
        items: List[str], 
        data: List[List[Any]], 
        title: str, 
        output_filename: str = "comparison_table.html",
        custom_styles: Optional[Dict[str, str]] = None
    ) -> Path:
        """
        比較表を生成
        
        Args:
            categories: カテゴリー（列ヘッダー）
            items: アイテム（行ヘッダー）
            data: 比較データ（2次元配列）
            title: テーブルタイトル
            output_filename: 出力ファイル名
            custom_styles: カスタムスタイル辞書
            
        Returns:
            保存されたファイルのパス
        """
        try:
            # データフレームを作成
            df = pd.DataFrame(data, columns=categories, index=items)
            
            # インデックスをリセットして列として扱う
            df.reset_index(inplace=True)
            df.rename(columns={'index': 'アイテム'}, inplace=True)
            
            # 安全なファイル名
            safe_name = safe_filename(output_filename)
            if not safe_name.endswith('.html'):
                safe_name += '.html'
            
            output_path = self.output_dir / safe_name
            
            # テーブルIDを生成
            table_id = f"table_{safe_name.replace('.html', '').replace('-', '_')}"
            
            # HTMLを生成
            html_content = self._generate_html_table_string(df, table_id, title, custom_styles)
            
            # ファイルに保存
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            self.logger.info(f"Comparison table saved: {output_path}")
            
            return output_path
            
        except Exception as e:
            self.logger.error(f"Failed to create comparison table: {e}")
            raise
    
    def create_styled_table(
        self, 
        df: pd.DataFrame, 
        title: str, 
        output_filename: str,
        style_config: Optional[Dict[str, Any]] = None
    ) -> Path:
        """
        スタイル付きテーブルを生成
        
        Args:
            df: データフレーム
            title: テーブルタイトル
            output_filename: 出力ファイル名
            style_config: スタイル設定辞書
            
        Returns:
            保存されたファイルのパス
        """
        try:
            # 安全なファイル名
            safe_name = safe_filename(output_filename)
            if not safe_name.endswith('.html'):
                safe_name += '.html'
            
            output_path = self.output_dir / safe_name
            
            # テーブルIDを生成
            table_id = f"table_{safe_name.replace('.html', '').replace('-', '_')}"
            
            # スタイル設定を適用
            custom_styles = {}
            if style_config:
                # セルの背景色変更
                if 'cell_colors' in style_config:
                    cell_colors = style_config['cell_colors']
                    # カスタムCSSを追加
                    custom_styles.update(cell_colors)
                
                # その他のスタイル設定
                if 'font_size' in style_config:
                    custom_styles['font_size'] = style_config['font_size']
                if 'header_bg_color' in style_config:
                    custom_styles['header_bg_color'] = style_config['header_bg_color']
            
            # HTMLを生成
            html_content = self._generate_html_table_string(df, table_id, title, custom_styles)
            
            # ファイルに保存
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            self.logger.info(f"Styled table saved: {output_path}")
            
            return output_path
            
        except Exception as e:
            self.logger.error(f"Failed to create styled table: {e}")
            raise
    
    def create_data_table(
        self, 
        data: Union[List[Dict[str, Any]], pd.DataFrame], 
        title: str, 
        output_filename: str,
        sortable: bool = True,
        searchable: bool = True
    ) -> Path:
        """
        データテーブル（ソート・検索機能付き）を生成
        
        Args:
            data: データ（List of Dict or DataFrame）
            title: テーブルタイトル
            output_filename: 出力ファイル名
            sortable: ソート機能を有効にするか
            searchable: 検索機能を有効にするか
            
        Returns:
            保存されたファイルのパス
        """
        try:
            # データフレームに変換
            if isinstance(data, list):
                df = pd.DataFrame(data)
            else:
                df = data
            
            # 安全なファイル名
            safe_name = safe_filename(output_filename)
            if not safe_name.endswith('.html'):
                safe_name += '.html'
            
            output_path = self.output_dir / safe_name
            
            # テーブルIDを生成
            table_id = f"table_{safe_name.replace('.html', '').replace('-', '_')}"
            
            # JavaScriptライブラリを含むHTMLを生成
            js_libraries = ""
            if sortable or searchable:
                js_libraries = """
                <script src="https://cdn.jsdelivr.net/npm/sortable-tablesort@1.3.0/sortable.min.js"></script>
                <style>
                    .search-container {
                        margin-bottom: 15px;
                    }
                    .search-input {
                        width: 100%;
                        max-width: 300px;
                        padding: 8px 12px;
                        border: 1px solid #ddd;
                        border-radius: 4px;
                        font-size: 14px;
                    }
                    .sortable th {
                        cursor: pointer;
                        user-select: none;
                    }
                    .sortable th:hover {
                        background-color: rgba(255, 255, 255, 0.1);
                    }
                </style>
                """
            
            # 検索機能のHTML
            search_html = ""
            if searchable:
                search_html = f"""
                <div class="search-container">
                    <input type="text" id="search_{table_id}" class="search-input" placeholder="テーブルを検索...">
                </div>
                """
            
            # 基本HTMLを生成
            base_html = self._generate_html_table_string(df, table_id, title)
            
            # JavaScriptを追加
            js_script = ""
            if sortable or searchable:
                js_script = f"""
                <script>
                    document.addEventListener('DOMContentLoaded', function() {{
                        const table = document.getElementById('{table_id}');
                        
                        // ソート機能
                        if (table && {str(sortable).lower()}) {{
                            table.classList.add('sortable');
                            Sortable.initTable(table);
                        }}
                        
                        // 検索機能
                        if ({str(searchable).lower()}) {{
                            const searchInput = document.getElementById('search_{table_id}');
                            const tbody = table.querySelector('tbody');
                            const rows = tbody.querySelectorAll('tr');
                            
                            searchInput.addEventListener('input', function(e) {{
                                const searchTerm = e.target.value.toLowerCase();
                                
                                rows.forEach(row => {{
                                    const text = row.textContent.toLowerCase();
                                    if (text.includes(searchTerm)) {{
                                        row.style.display = '';
                                    }} else {{
                                        row.style.display = 'none';
                                    }}
                                }});
                            }});
                        }}
                    }});
                </script>
                """
            
            # HTMLを組み立て
            html_parts = base_html.split('<body>')
            if len(html_parts) == 2:
                html_content = html_parts[0].replace('</head>', f"{js_libraries}</head>") + \
                                '<body>' + search_html + html_parts[1].replace('</body>', f"{js_script}</body>")
            else:
                html_content = base_html
            
            # ファイルに保存
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            self.logger.info(f"Data table saved: {output_path}")
            
            return output_path
            
        except Exception as e:
            self.logger.error(f"Failed to create data table: {e}")
            raise
    
    def create_responsive_table(
        self, 
        df: pd.DataFrame, 
        title: str, 
        output_filename: str,
        mobile_columns: Optional[List[str]] = None
    ) -> Path:
        """
        レスポンシブテーブルを生成
        
        Args:
            df: データフレーム
            title: テーブルタイトル
            output_filename: 出力ファイル名
            mobile_columns: モバイル表示時に表示する列
            
        Returns:
            保存されたファイルのパス
        """
        try:
            # 安全なファイル名
            safe_name = safe_filename(output_filename)
            if not safe_name.endswith('.html'):
                safe_name += '.html'
            
            output_path = self.output_dir / safe_name
            
            # テーブルIDを生成
            table_id = f"table_{safe_name.replace('.html', '').replace('-', '_')}"
            
            # モバイル用の列を決定
            if mobile_columns is None:
                mobile_columns = df.columns[:3].tolist()  # デフォルトで最初の3列
            
            # カスタムスタイルを追加
            responsive_styles = {
                **self.styles,
                'responsive_css': f"""
                @media (max-width: 768px) {{
                    #{table_id} th,
                    #{table_id} td {{
                        display: none;
                    }}
                    
                    #{table_id} th:nth-child(1),
                    #{table_id} td:nth-child(1),
                    #{table_id} th:nth-child(2),
                    #{table_id} td:nth-child(2),
                    #{table_id} th:nth-child(3),
                    #{table_id} td:nth-child(3) {{
                        display: table-cell;
                    }}
                }}
                """
            }
            
            # HTMLを生成
            html_content = self._generate_html_table_string(df, table_id, title, responsive_styles)
            
            # レスポンシブCSSを追加
            html_content = html_content.replace(
                '</style>',
                f"{responsive_styles['responsive_css']}</style>"
            )
            
            # ファイルに保存
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            self.logger.info(f"Responsive table saved: {output_path}")
            
            return output_path
            
        except Exception as e:
            self.logger.error(f"Failed to create responsive table: {e}")
            raise
    
    def create_pivot_table(
        self, 
        df: pd.DataFrame, 
        index: str, 
        columns: str, 
        values: str, 
        title: str, 
        output_filename: str,
        aggfunc: str = 'mean'
    ) -> Path:
        """
        ピボットテーブルを生成
        
        Args:
            df: データフレーム
            index: インデックス列
            columns: 列名
            values: 値列
            title: テーブルタイトル
            output_filename: 出力ファイル名
            aggfunc: 集約関数
            
        Returns:
            保存されたファイルのパス
        """
        try:
            # ピボットテーブルを作成
            pivot_df = pd.pivot_table(
                df, 
                index=index, 
                columns=columns, 
                values=values, 
                aggfunc=aggfunc,
                fill_value=0
            )
            
            # インデックスをリセット
            pivot_df.reset_index(inplace=True)
            
            # 安全なファイル名
            safe_name = safe_filename(output_filename)
            if not safe_name.endswith('.html'):
                safe_name += '.html'
            
            output_path = self.output_dir / safe_name
            
            # テーブルIDを生成
            table_id = f"table_{safe_name.replace('.html', '').replace('-', '_')}"
            
            # HTMLを生成
            html_content = self._generate_html_table_string(pivot_df, table_id, title)
            
            # ファイルに保存
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            self.logger.info(f"Pivot table saved: {output_path}")
            
            return output_path
            
        except Exception as e:
            self.logger.error(f"Failed to create pivot table: {e}")
            raise
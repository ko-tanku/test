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
                    padding: 16px;
                    background-color: #f5f5f5;
                    border-bottom: 1px solid #e0e0e0;
                }}

                .table-responsive {{
                    overflow-x: auto;
                    width: 100%;
                }}

                table#table_{table_id} {{
                    width: 100%;
                    border-collapse: collapse;
                    border-spacing: 0;
                    font-size: {table_styles.get('font_size', '14px')};
                }}

                table#table_{table_id} th {{
                    background-color: {table_styles.get('header_bg_color', '#1976d2')};
                    color: {table_styles.get('header_text_color', '#ffffff')};
                    padding: {table_styles.get('cell_padding', '8px 12px')};
                    text-align: left;
                    font-weight: bold;
                    border-bottom: 2px solid {table_styles.get('border_color', '#e0e0e0')};
                    position: sticky;
                    top: 0;
                    z-index: 10;
                }}

                table#table_{table_id} td {{
                    padding: {table_styles.get('cell_padding', '8px 12px')};
                    border-bottom: {table_styles.get('border_width', '1px')} solid {table_styles.get('border_color', '#e0e0e0')};
                }}

                table#table_{table_id} tr:nth-child(even) {{
                    background-color: {table_styles.get('row_even_bg_color', '#f5f5f5')};
                }}

                table#table_{table_id} tr:nth-child(odd) {{
                    background-color: {table_styles.get('row_odd_bg_color', '#ffffff')};
                }}

                table#table_{table_id} tr:hover {{
                    background-color: #e3f2fd;
                    transition: background-color 0.2s;
                }}

                /* レスポンシブデザイン */
                @media screen and (max-width: 768px) {{
                    .table-container {{
                        border-radius: 0;
                    }}

                    body {{
                        padding: 0;
                    }}

                    table#table_{table_id} {{
                        font-size: 12px;
                    }}

                    table#table_{table_id} th,
                    table#table_{table_id} td {{
                        padding: 6px 8px;
                    }}
                }}
            </style>
            """

            # HTMLテーブルを生成
            html_table = df.to_html(
                index=False,
                table_id=f"table_{table_id}",
                escape=True,
                classes=table_styles.get('class_name', 'mkdocs-table')
            )

            # 完全なHTML文書を構築
            html_content = f"""
            <!DOCTYPE html>
            <html lang="ja">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{title}</title>
                {css_styles}
            </head>
            <body>
                <div class="table-container">
                    {f'<div class="table-title">{html.escape(title)}</div>' if title else ''}
                    <div class="table-responsive">
                        {html_table}
                    </div>
                </div>
            </body>
            </html>
            """

            return html_content

        except Exception as e:
            self.logger.error(f"Failed to generate HTML table string: {e}")
            raise

    def create_basic_table(
        self,
        headers: List[str],
        rows: List[List[Any]],
        title: str = "",
        output_filename: str = "basic_table.html",
        custom_styles: Optional[Dict[str, str]] = None
    ) -> Path:
        """
        基本的なテーブルを生成

        Args:
            headers: ヘッダー行
            rows: データ行のリスト
            title: テーブルタイトル
            output_filename: 出力ファイル名
            custom_styles: カスタムスタイル

        Returns:
            生成されたファイルのパス
        """
        try:
            # DataFrameを作成
            df = pd.DataFrame(rows, columns=headers)

            # ファイル名を安全な形式に変換
            safe_name = safe_filename(output_filename)
            if not safe_name.endswith('.html'):
                safe_name += '.html'

            output_path = self.output_dir / safe_name

            # HTMLを生成
            html_content = self._generate_html_table_string(
                df,
                table_id=safe_name.replace('.html', ''),
                title=title,
                custom_styles=custom_styles
            )

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
        title: str = "",
        output_filename: str = "comparison_table.html",
        custom_styles: Optional[Dict[str, str]] = None
    ) -> Path:
        """
        比較表を生成

        Args:
            categories: カテゴリ（列）のリスト
            items: 項目（行）のリスト
            data: データ行列
            title: テーブルタイトル
            output_filename: 出力ファイル名
            custom_styles: カスタムスタイル

        Returns:
            生成されたファイルのパス
        """
        try:
            # DataFrameを作成
            df = pd.DataFrame(data, index=items, columns=categories)
            df.reset_index(inplace=True)
            df.rename(columns={'index': '項目'}, inplace=True)

            # ファイル名を安全な形式に変換
            safe_name = safe_filename(output_filename)
            if not safe_name.endswith('.html'):
                safe_name += '.html'

            output_path = self.output_dir / safe_name

            # HTMLを生成
            html_content = self._generate_html_table_string(
                df,
                table_id=safe_name.replace('.html', ''),
                title=title,
                custom_styles=custom_styles
            )

            # ファイルに保存
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)

            self.logger.info(f"Comparison table saved: {output_path}")

            return output_path

        except Exception as e:
            self.logger.error(f"Failed to create comparison table: {e}")
            raise

    def create_data_table(
        self,
        data: Union[List[Dict], pd.DataFrame],
        title: str = "",
        output_filename: str = "data_table.html",
        sortable: bool = True,
        searchable: bool = True,
        custom_styles: Optional[Dict[str, str]] = None
    ) -> Path:
        """
        検索・ソート機能付きデータテーブルを生成

        Args:
            data: データ（辞書のリストまたはDataFrame）
            title: テーブルタイトル
            output_filename: 出力ファイル名
            sortable: ソート可能にするか
            searchable: 検索可能にするか
            custom_styles: カスタムスタイル

        Returns:
            生成されたファイルのパス
        """
        try:
            # DataFrameに変換
            if isinstance(data, list):
                df = pd.DataFrame(data)
            else:
                df = data

            # ファイル名を安全な形式に変換
            safe_name = safe_filename(output_filename)
            if not safe_name.endswith('.html'):
                safe_name += '.html'

            output_path = self.output_dir / safe_name
            table_id = safe_name.replace('.html', '')

            # スタイル設定
            table_styles = {**self.styles, **(custom_styles or {})}

            # HTMLテーブルを生成
            html_table = df.to_html(
                index=False,
                table_id=f"table_{table_id}",
                escape=True,
                classes=table_styles.get('class_name', 'mkdocs-table')
            )

            # JavaScriptコード（検索・ソート機能）
            js_code = ""
            if searchable or sortable:
                js_code = f"""
                <script>
                document.addEventListener('DOMContentLoaded', function() {{
                    const table = document.getElementById('table_{table_id}');
                    const tbody = table.querySelector('tbody');
                    const rows = Array.from(tbody.querySelectorAll('tr'));

                    {"// 検索機能" if searchable else ""}
                    {f'''
                    const searchInput = document.getElementById('search_{table_id}');
                    if (searchInput) {{
                        searchInput.addEventListener('input', function(e) {{
                            const searchTerm = e.target.value.toLowerCase();
                            rows.forEach(row => {{
                                const text = row.textContent.toLowerCase();
                                row.style.display = text.includes(searchTerm) ? '' : 'none';
                            }});
                        }});
                    }}
                    ''' if searchable else ''}

                    {"// ソート機能" if sortable else ""}
                    {f'''
                    const headers = table.querySelectorAll('th');
                    headers.forEach((header, index) => {{
                        header.style.cursor = 'pointer';
                        header.style.userSelect = 'none';

                        let sortOrder = 0; // 0: なし, 1: 昇順, -1: 降順

                        header.addEventListener('click', function() {{
                            sortOrder = sortOrder === 1 ? -1 : 1;

                            // ソートインジケータを更新
                            headers.forEach(h => h.textContent = h.textContent.replace(/ ▲| ▼/g, ''));
                            header.textContent += sortOrder === 1 ? ' ▲' : ' ▼';

                            // 行をソート
                            const sortedRows = rows.sort((a, b) => {{
                                const aValue = a.cells[index].textContent.trim();
                                const bValue = b.cells[index].textContent.trim();

                                // 数値かどうか判定
                                const aNum = parseFloat(aValue);
                                const bNum = parseFloat(bValue);

                                if (!isNaN(aNum) && !isNaN(bNum)) {{
                                    return (aNum - bNum) * sortOrder;
                                }}

                                // 文字列として比較
                                return aValue.localeCompare(bValue) * sortOrder;
                            }});

                            // DOMを更新
                            tbody.innerHTML = '';
                            sortedRows.forEach(row => tbody.appendChild(row));
                        }});
                    }});
                    ''' if sortable else ''}
                }});
                </script>
                """

            # CSSスタイル
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
                    min-height: 100vh;
                }}

                .search-container {{
                    margin-bottom: 20px;
                }}

                .search-input {{
                    width: 100%;
                    max-width: 400px;
                    padding: 10px 15px;
                    font-size: 14px;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    outline: none;
                }}

                .search-input:focus {{
                    border-color: {table_styles.get('header_bg_color', '#1976d2')};
                    box-shadow: 0 0 0 2px rgba(25, 118, 210, 0.1);
                }}

                .table-container {{
                    width: 100%;
                    background-color: #ffffff;
                    border-radius: 8px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                    overflow: hidden;
                }}

                .table-title {{
                    font-size: 18px;
                    font-weight: bold;
                    padding: 16px;
                    background-color: #f5f5f5;
                    border-bottom: 1px solid #e0e0e0;
                }}

                .table-responsive {{
                    overflow-x: auto;
                    width: 100%;
                }}

                table#table_{table_id} {{
                    width: 100%;
                    border-collapse: collapse;
                    border-spacing: 0;
                    font-size: {table_styles.get('font_size', '14px')};
                }}

                table#table_{table_id} th {{
                    background-color: {table_styles.get('header_bg_color', '#1976d2')};
                    color: {table_styles.get('header_text_color', '#ffffff')};
                    padding: {table_styles.get('cell_padding', '8px 12px')};
                    text-align: left;
                    font-weight: bold;
                    border-bottom: 2px solid {table_styles.get('border_color', '#e0e0e0')};
                    position: sticky;
                    top: 0;
                    z-index: 10;
                    white-space: nowrap;
                }}

                table#table_{table_id} td {{
                    padding: {table_styles.get('cell_padding', '8px 12px')};
                    border-bottom: {table_styles.get('border_width', '1px')} solid {table_styles.get('border_color', '#e0e0e0')};
                }}

                table#table_{table_id} tr:nth-child(even) {{
                    background-color: {table_styles.get('row_even_bg_color', '#f5f5f5')};
                }}

                table#table_{table_id} tr:nth-child(odd) {{
                    background-color: {table_styles.get('row_odd_bg_color', '#ffffff')};
                }}

                table#table_{table_id} tr:hover {{
                    background-color: #e3f2fd;
                    transition: background-color 0.2s;
                }}

                /* ソート可能なヘッダーのスタイル */
                {"table#table_" + table_id + " th:hover { background-color: #1565c0; }" if sortable else ""}

                /* レスポンシブデザイン */
                @media screen and (max-width: 768px) {{
                    body {{
                        padding: 10px;
                    }}

                    .table-container {{
                        border-radius: 0;
                    }}

                    table#table_{table_id} {{
                        font-size: 12px;
                    }}

                    table#table_{table_id} th,
                    table#table_{table_id} td {{
                        padding: 6px 8px;
                    }}
                }}
            </style>
            """

            # 完全なHTML文書を構築
            html_content = f"""
            <!DOCTYPE html>
            <html lang="ja">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{title}</title>
                {css_styles}
            </head>
            <body>
                {f'''<div class="search-container">
                    <input type="text" id="search_{table_id}" class="search-input" placeholder="テーブルを検索...">
                </div>''' if searchable else ''}

                <div class="table-container">
                    {f'<div class="table-title">{html.escape(title)}</div>' if title else ''}
                    <div class="table-responsive">
                        {html_table}
                    </div>
                </div>

                {js_code}
            </body>
            </html>
            """

            # ファイルに保存
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)

            self.logger.info(f"Data table saved: {output_path}")

            return output_path

        except Exception as e:
            self.logger.error(f"Failed to create data table: {e}")
            raise

    def create_styled_table(
        self,
        df: pd.DataFrame,
        title: str = "",
        output_filename: str = "styled_table.html",
        style_config: Optional[Dict[str, Any]] = None
    ) -> Path:
        """
        カスタムスタイル付きテーブルを生成

        Args:
            df: データフレーム
            title: テーブルタイトル
            output_filename: 出力ファイル名
            style_config: スタイル設定辞書
                - highlight_rows: ハイライトする行のインデックスリスト
                - highlight_cols: ハイライトする列名リスト
                - cell_colors: セル別の背景色辞書

        Returns:
            生成されたファイルのパス
        """
        try:
            # ファイル名を安全な形式に変換
            safe_name = safe_filename(output_filename)
            if not safe_name.endswith('.html'):
                safe_name += '.html'

            output_path = self.output_dir / safe_name
            table_id = safe_name.replace('.html', '')

            # スタイル設定
            style_config = style_config or {}

            # DataFrameのスタイル設定
            styled_df = df.style

            # 行のハイライト
            if 'highlight_rows' in style_config:
                for row_idx in style_config['highlight_rows']:
                    styled_df = styled_df.set_properties(
                        subset=pd.IndexSlice[row_idx, :],
                        **{'background-color': self.colors.get('warning', '#ff9800')}
                    )

            # 列のハイライト
            if 'highlight_cols' in style_config:
                for col in style_config['highlight_cols']:
                    if col in df.columns:
                        styled_df = styled_df.set_properties(
                            subset=[col],
                            **{'background-color': self.colors.get('info', '#2196f3'),
                               'color': 'white'}
                        )

            # セル別の色設定
            if 'cell_colors' in style_config:
                for (row, col), color in style_config['cell_colors'].items():
                    if row in df.index and col in df.columns:
                        styled_df = styled_df.set_properties(
                            subset=pd.IndexSlice[row, col],
                            **{'background-color': color}
                        )

            # HTMLを生成
            styled_html = styled_df.to_html(
                table_id=f"table_{table_id}",
                escape=True
            )

            # CSSスタイル
            css_styles = f"""
            <style>
                body {{
                    font-family: {self.styles.get('font_family', 'Arial')};
                    padding: 20px;
                    background-color: #ffffff;
                }}

                .table-container {{
                    width: 100%;
                    background-color: #ffffff;
                    border-radius: 8px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                    overflow: hidden;
                }}

                .table-title {{
                    font-size: 18px;
                    font-weight: bold;
                    padding: 16px;
                    background-color: #f5f5f5;
                    border-bottom: 1px solid #e0e0e0;
                }}

                table#table_{table_id} {{
                    width: 100%;
                    border-collapse: collapse;
                    font-size: {self.styles.get('font_size', '14px')};
                }}

                table#table_{table_id} th {{
                    background-color: {self.styles.get('header_bg_color', '#1976d2')};
                    color: {self.styles.get('header_text_color', '#ffffff')};
                    padding: {self.styles.get('cell_padding', '8px 12px')};
                    text-align: left;
                    font-weight: bold;
                }}

                table#table_{table_id} td {{
                    padding: {self.styles.get('cell_padding', '8px 12px')};
                    border: 1px solid {self.styles.get('border_color', '#e0e0e0')};
                }}
            </style>
            """

            # 完全なHTML文書
            html_content = f"""
            <!DOCTYPE html>
            <html lang="ja">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{title}</title>
                {css_styles}
            </head>
            <body>
                <div class="table-container">
                    {f'<div class="table-title">{html.escape(title)}</div>' if title else ''}
                    {styled_html}
                </div>
            </body>
            </html>
            """

            # ファイルに保存
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)

            self.logger.info(f"Styled table saved: {output_path}")

            return output_path

        except Exception as e:
            self.logger.error(f"Failed to create styled table: {e}")
            raise
"""
様々な形式の表データを生成し、HTMLファイルとして出力
Pandas DataFrameを活用し、CSSスタイルを適用して整形
"""

import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from html import escape

import pandas as pd

from .utils import slugify
from .config import GLOBAL_COLORS, BASE_TABLE_STYLES

logger = logging.getLogger(__name__)


class TableGenerator:
    """表生成クラス"""
    
    def __init__(self, colors: Dict[str, str] = None, styles: Dict[str, Any] = None):
        """
        初期化
        
        Args:
            colors: カスタムカラーパレット
            styles: カスタムスタイル設定
        """
        self.colors = colors or GLOBAL_COLORS
        self.styles = styles or BASE_TABLE_STYLES
        
    def _generate_html_table_string(
        self,
        df: pd.DataFrame,
        table_id: str,
        title: str = "",
        custom_styles: Optional[Dict[str, str]] = None
    ) -> str:
        """
        Pandas DataFrameをHTMLテーブル文字列に変換
        
        Args:
            df: データフレーム
            table_id: テーブルID
            title: テーブルタイトル
            custom_styles: カスタムスタイル
            
        Returns:
            HTMLテーブル文字列
        """
        # スタイルをマージ
        styles = self.styles.copy()
        if custom_styles:
            styles.update(custom_styles)
        
        # HTMLエスケープ処理を適用
        df_escaped = df.applymap(lambda x: escape(str(x)) if pd.notna(x) else '')
        
        # テーブルHTML生成
        table_html = df_escaped.to_html(
            table_id=table_id,
            classes=styles.get("class_name", "mkdocs-table"),
            escape=False,  # 既にエスケープ済み
            index=False
        )
        
        # CSSスタイル定義
        css_styles = f"""
        <style>
            #{table_id} {{
                width: 100%;
                table-layout: fixed;
                word-wrap: break-word;
                border-collapse: collapse;
                margin: 20px 0;
            }}
            
            #{table_id} th {{
                background-color: {styles.get("header_bg_color", "#00BCD4")};
                color: {styles.get("header_text_color", "#FFFFFF")};
                padding: {styles.get("cell_padding", "8px 12px")};
                text-align: left;
                font-weight: bold;
                border: {styles.get("border_width", "1px")} solid {styles.get("border_color", "#CCCCCC")};
            }}
            
            #{table_id} td {{
                padding: {styles.get("cell_padding", "8px 12px")};
                border: {styles.get("border_width", "1px")} solid {styles.get("border_color", "#CCCCCC")};
            }}
            
            #{table_id} tr:nth-child(even) {{
                background-color: {styles.get("row_even_bg_color", "#FAFAFA")};
            }}
            
            #{table_id} tr:nth-child(odd) {{
                background-color: {styles.get("row_odd_bg_color", "#F0F0F0")};
            }}
            
            #{table_id} {{
                font-size: {styles.get("font_size", "0.9em")};
            }}
            
            .table-container {{
                overflow-x: auto;
                margin: 20px 0;
            }}
            
            .table-title {{
                font-size: 1.2em;
                font-weight: bold;
                margin-bottom: 10px;
                color: #333;
            }}
        </style>
        """
        
        # 完全なHTML生成
        if title:
            title_html = f'<div class="table-title">{escape(title)}</div>'
        else:
            title_html = ""
            
        full_html = f"""
        {css_styles}
        <div class="table-container">
            {title_html}
            {table_html}
        </div>
        """
        
        return full_html
        
    def create_basic_table(
        self,
        headers: List[str],
        rows: List[List[Any]],
        title: str,
        output_filename: str = "basic_table.html",
        custom_styles: Optional[Dict[str, str]] = None,
        output_dir: Path = None  # この引数を追加
    ) -> Path:
        """
        基本的な表を生成
        """
        # ファイル名をスラッグ化
        safe_filename = slugify(output_filename.replace('.html', '')) + '.html'
        
        if output_dir:
            output_path = output_dir / safe_filename
        else:
            output_path = Path(safe_filename)
        
        try:
            # DataFrameを作成
            df = pd.DataFrame(rows, columns=headers)
            
            # テーブルID生成
            table_id = f"table_{slugify(title)}"
            
            # HTMLテーブル生成
            table_html = self._generate_html_table_string(
                df, table_id, title, custom_styles
            )
            
            # 完全なHTMLドキュメント
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
        .content-wrapper {{
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            max-width: 100%;
            overflow: hidden;
        }}
    </style>
</head>
<body>
    <div class="content-wrapper">
        {table_html}
    </div>
</body>
</html>
"""
            
            # ファイル保存
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(html_content, encoding='utf-8')
            
            logger.info(f"表HTMLを保存しました: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"基本表の生成中にエラーが発生しました: {e}")
            raise
            
    def create_comparison_table(
        self,
        categories: List[str],
        items: List[str],
        data: List[List[Any]],
        title: str,
        output_filename: str = "comparison_table.html",
        custom_styles: Optional[Dict[str, str]] = None,
        output_dir: Path = None  # この引数を追加
    ) -> Path:
        """
        比較表を生成
        
        Args:
            categories: カテゴリのリスト（列ヘッダー）
            items: 項目のリスト（行ヘッダー）
            data: データマトリックス
            title: 表のタイトル
            output_filename: 出力ファイル名
            custom_styles: カスタムスタイル
            
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
            # DataFrameを作成
            df = pd.DataFrame(data, index=items, columns=categories)
            df.reset_index(inplace=True)
            df.rename(columns={'index': '項目'}, inplace=True)
            
            # テーブルID生成
            table_id = f"table_{slugify(title)}"
            
            # カスタムスタイルで最初の列を強調
            if custom_styles is None:
                custom_styles = {}
            
            # HTMLテーブル生成
            table_html = self._generate_html_table_string(
                df, table_id, title, custom_styles
            )
            
            # 追加のスタイル（最初の列を強調）
            additional_styles = f"""
            <style>
                #{table_id} td:first-child {{
                    font-weight: bold;
                    background-color: {self.colors.get("info", "#00BCD4")}22;
                }}
            </style>
            """
            
            # 完全なHTMLドキュメント
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
        .content-wrapper {{
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            max-width: 100%;
            overflow: hidden;
        }}
    </style>
</head>
<body>
    <div class="content-wrapper">
        {additional_styles}
        {table_html}
    </div>
</body>
</html>
"""
            
            # ファイル保存
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(html_content, encoding='utf-8')
            
            logger.info(f"比較表HTMLを保存しました: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"比較表の生成中にエラーが発生しました: {e}")
            raise
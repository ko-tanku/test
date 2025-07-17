"""
Utility functions for MkDocs Materials Generator
汎用ヘルパー関数を提供
"""

import re
import html
import logging
import unicodedata
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def slugify(text: str) -> str:
    """
    テキストをURLフレンドリーなスラッグに変換
    
    Args:
        text: 変換対象のテキスト
        
    Returns:
        スラッグ化されたテキスト
    """
    if not text:
        return ""
    
    # Unicodeの正規化
    text = unicodedata.normalize('NFKC', text)
    
    # 小文字変換
    text = text.lower()
    
    # 日本語文字を除去し、英数字とハイフンのみを許可
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    
    # 前後のハイフンを削除
    text = text.strip('-')
    
    # 空文字列の場合はデフォルト値を返す
    if not text:
        return "untitled"
    
    return text


def hex_to_rgb(hex_color: str) -> tuple:
    """
    HEXカラーコードをRGBタプルに変換
    
    Args:
        hex_color: HEXカラーコード (#RRGGBB形式)
        
    Returns:
        RGBタプル (r, g, b)
    """
    try:
        hex_color = hex_color.lstrip('#')
        if len(hex_color) != 6:
            raise ValueError("Invalid hex color format")
        
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    except Exception as e:
        logger.warning(f"Invalid hex color '{hex_color}': {e}")
        return (128, 128, 128)  # デフォルト値（グレー）


def rgb_to_hex(rgb_color: tuple) -> str:
    """
    RGBタプルをHEXカラーコードに変換
    
    Args:
        rgb_color: RGBタプル (r, g, b)
        
    Returns:
        HEXカラーコード
    """
    try:
        r, g, b = rgb_color
        return f"#{r:02x}{g:02x}{b:02x}"
    except Exception as e:
        logger.warning(f"Invalid RGB color '{rgb_color}': {e}")
        return "#808080"  # デフォルト値（グレー）


def apply_matplotlib_japanese_font(font_family: Optional[List[str]] = None) -> bool:
    """
    Matplotlibで日本語フォントを設定
    
    Args:
        font_family: フォントファミリーのリスト
        
    Returns:
        設定が成功したかどうか
    """
    if font_family is None:
        font_family = ["Meiryo", "Yu Gothic", "Hiragino Sans", "Noto Sans CJK JP", "DejaVu Sans"]
    
    success = False
    
    for font_name in font_family:
        try:
            # フォントが利用可能かチェック
            available_fonts = [f.name for f in fm.fontManager.ttflist]
            if font_name in available_fonts:
                plt.rcParams['font.family'] = font_name
                logger.info(f"Japanese font set to: {font_name}")
                success = True
                break
        except Exception as e:
            logger.warning(f"Failed to set font '{font_name}': {e}")
            continue
    
    if not success:
        logger.warning("No Japanese font found, using default font")
        plt.rcParams['font.family'] = 'sans-serif'
    
    # その他のMatplotlib設定
    plt.rcParams['axes.unicode_minus'] = False
    
    return success


def create_html_tag(tag: str, content: Any = "", attributes: Optional[Dict[str, str]] = None) -> str:
    """
    汎用HTMLタグを生成
    
    Args:
        tag: HTMLタグ名
        content: タグ内容
        attributes: タグ属性の辞書
        
    Returns:
        HTMLタグ文字列
    """
    if attributes is None:
        attributes = {}
    
    # 属性文字列を構築
    attr_str = ""
    if attributes:
        attr_parts = []
        for key, value in attributes.items():
            escaped_value = html.escape(str(value), quote=True)
            attr_parts.append(f'{key}="{escaped_value}"')
        attr_str = " " + " ".join(attr_parts)
    
    # コンテンツをエスケープ
    escaped_content = html.escape(str(content)) if content else ""
    
    # 自己閉じタグの場合
    if tag in ['br', 'hr', 'img', 'input', 'meta', 'link']:
        return f"<{tag}{attr_str} />"
    
    return f"<{tag}{attr_str}>{escaped_content}</{tag}>"


def generate_admonition_markdown(
    type: str, 
    title: str, 
    content: str, 
    collapsible: bool = False
) -> str:
    """
    MkDocs Materialの注記ブロックMarkdownを生成
    
    Args:
        type: 注記タイプ (note, warning, info, etc.)
        title: 注記タイトル
        content: 注記内容
        collapsible: 折りたたみ可能かどうか
        
    Returns:
        Markdown文字列
    """
    # 注記タイプの正規化
    valid_types = [
        'note', 'abstract', 'info', 'tip', 'success', 'question', 
        'warning', 'failure', 'danger', 'bug', 'example', 'quote'
    ]
    
    if type not in valid_types:
        logger.warning(f"Invalid admonition type '{type}', using 'note'")
        type = 'note'
    
    # 開始マーカー
    marker = "???" if collapsible else "!!!"
    
    # タイトルの処理
    title_part = f' "{title}"' if title else ""
    
    # コンテンツをインデント
    indented_content = "\n".join(f"    {line}" for line in content.split("\n"))
    
    return f'{marker} {type}{title_part}\n\n{indented_content}\n'


def generate_tabbed_markdown(tabs_data: Dict[str, str]) -> str:
    """
    MkDocs MaterialのタブブロックMarkdownを生成
    
    Args:
        tabs_data: タブ名とコンテンツの辞書
        
    Returns:
        Markdown文字列
    """
    if not tabs_data:
        return ""
    
    tab_blocks = []
    
    for tab_name, content in tabs_data.items():
        # タブヘッダー
        tab_header = f'=== "{tab_name}"'
        
        # コンテンツをインデント
        indented_content = "\n".join(f"    {line}" for line in content.split("\n"))
        
        tab_blocks.append(f"{tab_header}\n\n{indented_content}")
    
    return "\n\n".join(tab_blocks) + "\n"


def ensure_directory_exists(path: Union[str, Path]) -> Path:
    """
    ディレクトリが存在しない場合は作成
    
    Args:
        path: ディレクトリパス
        
    Returns:
        Pathオブジェクト
    """
    path = Path(path)
    try:
        path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Directory ensured: {path}")
    except Exception as e:
        logger.error(f"Failed to create directory '{path}': {e}")
        raise
    
    return path


def safe_filename(filename: str) -> str:
    """
    ファイル名を安全な形式に変換
    
    Args:
        filename: 元のファイル名
        
    Returns:
        安全なファイル名
    """
    # 危険文字を除去
    safe_chars = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # 連続するアンダースコアを1つにまとめる
    safe_chars = re.sub(r'_+', '_', safe_chars)
    
    # 前後のピリオドとスペースを削除
    safe_chars = safe_chars.strip('. ')
    
    # 空文字列の場合はデフォルト値
    if not safe_chars:
        return "untitled"
    
    return safe_chars


def format_file_size(size_bytes: int) -> str:
    """
    ファイルサイズを人間が読みやすい形式に変換
    
    Args:
        size_bytes: バイト数
        
    Returns:
        フォーマット済みサイズ文字列
    """
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024**2:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024**3:
        return f"{size_bytes / (1024**2):.1f} MB"
    else:
        return f"{size_bytes / (1024**3):.1f} GB"


def validate_url_path(path: str) -> bool:
    """
    URLパスの妥当性を検証
    
    Args:
        path: 検証対象のパス
        
    Returns:
        妥当性の真偽値
    """
    if not path:
        return False
    
    # 危険な文字パターンをチェック
    dangerous_patterns = [
        r'\.\./',  # ディレクトリトラバーサル
        r'[<>:"|?*]',  # 特殊文字
        r'^[./]',  # 先頭のドットやスラッシュ
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, path):
            return False
    
    return True
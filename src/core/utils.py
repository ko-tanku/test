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
        logger.warning("No Japanese font found. Using default font with fallback.")
        plt.rcParams['font.family'] = ['sans-serif']
        plt.rcParams['font.sans-serif'] = font_family

    # マイナス記号の文字化けを防ぐ
    plt.rcParams['axes.unicode_minus'] = False

    return success


def create_html_tag(tag: str, content: Any = "", attributes: Optional[Dict[str, str]] = None) -> str:
    """
    汎用HTMLタグを生成

    Args:
        tag: タグ名
        content: コンテンツ
        attributes: 属性辞書

    Returns:
        HTMLタグ文字列
    """
    if attributes is None:
        attributes = {}

    # 属性を文字列に変換
    attr_str = ""
    for key, value in attributes.items():
        # 属性値をエスケープ
        escaped_value = html.escape(str(value), quote=True)
        attr_str += f' {key}="{escaped_value}"'

    # コンテンツをエスケープ（HTMLタグが含まれる場合はエスケープしない）
    if isinstance(content, str) and not re.search(r'<[^>]+>', content):
        content = html.escape(content)

    return f"<{tag}{attr_str}>{content}</{tag}>"


def generate_admonition_markdown(
    type: str,
    title: str,
    content: str,
    collapsible: bool = False
) -> str:
    """
    MkDocs Materialの注記ブロックMarkdownを生成

    Args:
        type: 注記タイプ (note, info, tip, warning, danger, etc.)
        title: タイトル
        content: コンテンツ
        collapsible: 折りたたみ可能にするか

    Returns:
        Markdownテキスト
    """
    # 注記のベースシンタックス
    if collapsible:
        # 折りたたみ可能な注記
        admonition = f'??? {type} "{title}"\n'
    else:
        # 通常の注記
        admonition = f'!!! {type} "{title}"\n'

    # コンテンツを適切にインデント
    indented_content = '\n'.join(
        f'    {line}' if line.strip() else ''
        for line in content.split('\n')
    )

    return admonition + indented_content


def generate_tabbed_markdown(tabs_data: Dict[str, str]) -> str:
    """
    MkDocs MaterialのタブブロックMarkdownを生成

    Args:
        tabs_data: タブデータ辞書 {タブ名: コンテンツ}

    Returns:
        Markdownテキスト
    """
    if not tabs_data:
        return ""

    tabbed_content = []

    for i, (tab_name, content) in enumerate(tabs_data.items()):
        # タブヘッダー
        if i == 0:
            # 最初のタブは選択状態にする
            tabbed_content.append(f'=== "{tab_name}"')
        else:
            tabbed_content.append(f'\n=== "{tab_name}"')

        # コンテンツを適切にインデント（4スペース）
        indented_content = '\n'.join(
            f'    {line}' if line.strip() else ''
            for line in content.split('\n')
        )

        tabbed_content.append('')  # 空行
        tabbed_content.append(indented_content)

    return '\n'.join(tabbed_content)


def ensure_directory_exists(directory: Path) -> Path:
    """
    ディレクトリが存在することを確認し、存在しない場合は作成

    Args:
        directory: ディレクトリパス

    Returns:
        ディレクトリパス
    """
    try:
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        return directory
    except Exception as e:
        logger.error(f"Failed to create directory '{directory}': {e}")
        raise


def safe_filename(filename: str, max_length: int = 255) -> str:
    """
    ファイル名を安全な形式に変換

    Args:
        filename: 元のファイル名
        max_length: 最大長

    Returns:
        安全なファイル名
    """
    # 特殊文字を除去または置換
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)

    # 制御文字を除去
    filename = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', filename)

    # 前後の空白とピリオドを削除
    filename = filename.strip('. ')

    # 空文字列の場合はデフォルト値
    if not filename:
        filename = "untitled"

    # 長さ制限
    if len(filename) > max_length:
        # 拡張子を保持
        name_parts = filename.rsplit('.', 1)
        if len(name_parts) == 2:
            name, ext = name_parts
            max_name_length = max_length - len(ext) - 1
            filename = f"{name[:max_name_length]}.{ext}"
        else:
            filename = filename[:max_length]

    return filename


def validate_url_path(url_path: str) -> bool:
    """
    URLパスが有効かチェック

    Args:
        url_path: URLパス

    Returns:
        有効かどうか
    """
    try:
        # 基本的なURLパスパターン
        pattern = r'^[a-zA-Z0-9\-._~:/?#\[\]@!$&\'()*+,;=]+$'

        if not re.match(pattern, url_path):
            return False

        # 危険なパターンをチェック
        dangerous_patterns = [
            r'\.\.',  # ディレクトリトラバーサル
            r'^/',    # 絶対パス
            r'://',   # プロトコル
        ]

        for pattern in dangerous_patterns:
            if re.search(pattern, url_path):
                return False

        return True

    except Exception as e:
        logger.warning(f"URL path validation error: {e}")
        return False


def format_file_size(size_bytes: int) -> str:
    """
    ファイルサイズを人間が読みやすい形式に変換

    Args:
        size_bytes: バイト単位のサイズ

    Returns:
        フォーマットされたサイズ文字列
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0

    return f"{size_bytes:.2f} TB"


def sanitize_html_content(content: str) -> str:
    """
    HTMLコンテンツをサニタイズ

    Args:
        content: HTMLコンテンツ

    Returns:
        サニタイズされたコンテンツ
    """
    # 基本的なHTMLエスケープ
    return html.escape(content)


# エクスポート
__all__ = [
    'slugify',
    'hex_to_rgb',
    'rgb_to_hex',
    'apply_matplotlib_japanese_font',
    'create_html_tag',
    'generate_admonition_markdown',
    'generate_tabbed_markdown',
    'ensure_directory_exists',
    'safe_filename',
    'validate_url_path',
    'format_file_size',
    'sanitize_html_content'
]
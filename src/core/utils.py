"""
汎用的なヘルパー関数を提供
PythonからMarkdown/HTMLを生成する際の構文の堅牢性を高める
"""

import re
import logging
import unicodedata
from typing import List, Tuple, Dict, Any, Optional
from html import escape

# ロガーの設定
logger = logging.getLogger(__name__)


def slugify(text: str) -> str:
    """
    テキストをURLフレンドリーなスラッグに変換
    日本語を含むテキストに対応し、ASCII文字のみで構成されるスラッグを生成
    
    Args:
        text: 変換対象のテキスト
        
    Returns:
        URLおよびファイル名として安全なスラッグ
    """
    # NFKCで正規化
    text = unicodedata.normalize('NFKC', text)
    
    # 日本語文字を英語に変換する簡易マッピング
    japanese_to_english = {
        '日本語': 'nihongo',
        'の': 'no',
        '図解': 'zukai',
        'ロボット': 'robot',
        'アーム': 'arm',
        'ファイル名': 'filename'
    }
    
    # 既知の日本語を英語に置換
    for jp, en in japanese_to_english.items():
        text = text.replace(jp, en)
    
    # ASCII文字以外を除去または置換
    # 数字、アルファベット、一部の記号以外を削除
    text = re.sub(r'[^\w\s\-\.]', '-', text)
    
    # 連続するスペースやハイフンを単一のハイフンに置換
    text = re.sub(r'[\s\-]+', '-', text)
    
    # 前後のハイフンを削除
    text = text.strip('-')
    
    # 小文字に変換
    text = text.lower()
    
    # 空文字列の場合はデフォルト値を返す
    if not text:
        text = 'untitled'
    
    return text


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """
    HEXカラーコードをRGBトリプレットに変換
    
    Args:
        hex_color: #RRGGBB形式のカラーコード
        
    Returns:
        (R, G, B)のタプル
    """
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb_color: Tuple[int, int, int]) -> str:
    """
    RGBトリプレットをHEXカラーコードに変換
    
    Args:
        rgb_color: (R, G, B)のタプル
        
    Returns:
        #RRGGBB形式のカラーコード
    """
    return '#{:02x}{:02x}{:02x}'.format(*rgb_color)


def apply_matplotlib_japanese_font(font_family: List[str] = None):
    """
    Matplotlibで日本語フォントが正しく表示されるように設定
    
    Args:
        font_family: 使用するフォントファミリーのリスト
    """
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    
    if font_family is None:
        from .base_config import BASE_CHART_STYLES
        font_family = BASE_CHART_STYLES["font_family"]
    
    # 利用可能なフォントを確認
    available_fonts = set([f.name for f in font_manager.fontManager.ttflist])
    
    # 指定されたフォントから利用可能なものを選択
    selected_font = None
    for font in font_family:
        if font in available_fonts:
            selected_font = font
            break
    
    if selected_font:
        plt.rcParams['font.family'] = selected_font
        logger.info(f"フォント '{selected_font}' を使用します")
    else:
        # フォールバック
        plt.rcParams['font.family'] = 'sans-serif'
        logger.warning(
            f"指定されたフォント {font_family} が見つかりません。"
            f"sans-serifにフォールバックします。"
        )
    
    # 日本語の文字化けを防ぐ追加設定
    plt.rcParams['font.sans-serif'] = font_family + ['DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False


def create_html_tag(tag: str, content: Any = "", attributes: Dict[str, str] = None) -> str:
    """
    汎用HTMLタグを生成
    
    Args:
        tag: タグ名
        content: タグの内容
        attributes: HTML属性の辞書
        
    Returns:
        生成されたHTMLタグ文字列
    """
    if attributes is None:
        attributes = {}
    
    attr_str = ' '.join(f'{k}="{escape(str(v))}"' for k, v in attributes.items())
    
    if attr_str:
        return f"<{tag} {attr_str}>{content}</{tag}>"
    else:
        return f"<{tag}>{content}</{tag}>"


def generate_admonition_markdown(
    type: str, title: str, content: str, collapsible: bool = False
) -> str:
    """
    MkDocs Materialの注記ブロックのMarkdown構文を生成
    
    Args:
        type: 注記のタイプ (note, tip, warning, danger, etc.)
        title: 注記のタイトル
        content: 注記の内容
        collapsible: 折りたたみ可能にするか
        
    Returns:
        生成されたAdmonition Markdown文字列
    """
    prefix = "???" if collapsible else "!!!"
    lines = [f'{prefix} {type} "{title}"']
    
    # コンテンツの各行に4スペースのインデントを追加
    for line in content.split('\n'):
        lines.append(f"    {line}")
    
    return '\n'.join(lines) + '\n'


def generate_tabbed_markdown(tabs_data: Dict[str, str]) -> str:
    """
    MkDocs MaterialのタブブロックのMarkdown構文を生成
    
    Args:
        tabs_data: タブのタイトルをキー、内容を値とする辞書
        
    Returns:
        生成されたタブブロックのMarkdown文字列
    """
    lines = []
    
    for i, (tab_title, tab_content) in enumerate(tabs_data.items()):
        if i == 0:
            lines.append(f'=== "{tab_title}"')
        else:
            lines.append(f'\n=== "{tab_title}"')
        
        # タブ内容の各行に4スペースのインデントを追加
        for line in tab_content.split('\n'):
            if line.strip():  # 空行でない場合のみインデント
                lines.append(f"    {line}")
            else:
                lines.append("")
    
    return '\n'.join(lines) + '\n'
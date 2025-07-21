"""
Markdownコンテンツを構築するためのビルダークラス
MkDocs Materialテーマの拡張機能をサポート
"""

import re
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from html import escape

from .utils import (
    generate_admonition_markdown,
    generate_tabbed_markdown
)

logger = logging.getLogger(__name__)


class DocumentBuilder:
    """Markdownドキュメントを構築するビルダークラス"""
    
    def __init__(self, output_dir: Path):
        """
        初期化
        
        Args:
            output_dir: Markdownファイル出力先のベースディレクトリ
        """
        self.output_dir = Path(output_dir)
        self.content_buffer = []
        
    def clear_content(self):
        """現在構築中のMarkdownコンテンツの内部バッファをクリア"""
        self.content_buffer = []
        
    def get_content(self) -> str:
        """
        構築された現在のMarkdownコンテンツを文字列として返す
        
        Returns:
            Markdownコンテンツ文字列
        """
        return '\n'.join(self.content_buffer)
        
    def save_markdown(self, filename: str) -> Path:
        """
        現在のコンテンツをMarkdownファイルとして保存
        
        Args:
            filename: 保存するファイル名（相対パス）
            
        Returns:
            保存されたファイルのPathオブジェクト
        """
        file_path = self.output_dir / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        content = self.get_content()
        file_path.write_text(content, encoding='utf-8')
        
        logger.info(f"Markdownファイルを保存しました: {file_path}")
        
        # バッファをクリア
        self.clear_content()
        
        return file_path
        
    def add_heading(self, text: str, level: int):
        """
        Markdownの見出しを追加
        
        Args:
            text: 見出しテキスト
            level: 見出しレベル（1-6）
            
        Raises:
            ValueError: レベルが1-6の範囲外の場合
        """
        if not 1 <= level <= 6:
            raise ValueError(f"見出しレベルは1-6の範囲で指定してください: {level}")
        
        prefix = '#' * level
        self.content_buffer.append(f"{prefix} {text}")
        self.content_buffer.append("")  # 見出しの後に空行を追加
        
    def add_paragraph(self, text: str):
        """
        段落テキストを追加
        
        Args:
            text: 段落のテキスト
        """
        self.content_buffer.append(text)
        self.content_buffer.append("")  # 段落の後に厳密に1つの空行を追加
        
    def add_paragraph_with_tooltips(
        self, text: str, terms_info: Dict[str, Dict[str, str]]
    ):
        """
        専門用語にツールチップを付与した段落を追加
        
        Args:
            text: 段落のテキスト
            terms_info: 用語情報の辞書 {用語: {"tooltip_text": "ツールチップ内容"}}
        """
        # 既存のMarkdownリンクを保護するためのパターン
        link_pattern = r'\[([^\]]+)\]\([^)]+\)'
        protected_links = []
        
        # 既存のリンクを一時的に置換
        def protect_link(match):
            protected_links.append(match.group(0))
            return f"__PROTECTED_LINK_{len(protected_links) - 1}__"
        
        text_with_protected_links = re.sub(link_pattern, protect_link, text)
        
        # 用語をツールチップ付きリンクに置換
        # 各用語について、テキスト内で初回に登場した箇所のみを置換します。
        for term, info in terms_info.items():
            tooltip_text = info.get("tooltip_text", "")
            # HTMLエスケープ
            escaped_tooltip = escape(tooltip_text)
            # 改行を&#10;に置換
            escaped_tooltip = escaped_tooltip.replace('\n', '&#10;')

            # 修正: 前後の単語関係なく、正確な用語の文字列をマッチさせ、初回のみ置換
            pattern = re.escape(term)
            replacement = f'<span class="custom-tooltip" data-tooltip="{escaped_tooltip}">{term}</span>'
            text_with_protected_links = re.sub(
                pattern, replacement, text_with_protected_links, count=1 # ここで初回のみ置換を指定
            )

        
        # 保護していたリンクを復元
        for i, protected_link in enumerate(protected_links):
            text_with_protected_links = text_with_protected_links.replace(
                f"__PROTECTED_LINK_{i}__", protected_link
            )
        self.add_paragraph(text_with_protected_links)
        
    def add_code_block(self, code: str, lang: str = "python"):
        """
        コードブロックを追加
        
        Args:
            code: コード文字列
            lang: 言語指定
        """
        self.content_buffer.append(f"```{lang}")
        self.content_buffer.append(code)
        self.content_buffer.append("```")
        self.content_buffer.append("")
        
    def add_unordered_list(self, items: List[str]):
        """
        順不同リストを追加
        
        Args:
            items: リスト項目のリスト
        """
        for item in items:
            self.content_buffer.append(f"- {item}")
        self.content_buffer.append("")
        
    def add_ordered_list(self, items: List[str]):
        """
        順序付きリストを追加
        
        Args:
            items: リスト項目のリスト
        """
        for i, item in enumerate(items, 1):
            self.content_buffer.append(f"{i}. {item}")
        self.content_buffer.append("")
        
    def add_quote(self, text: str):
        """
        引用ブロックを追加
        
        Args:
            text: 引用テキスト
        """
        for line in text.split('\n'):
            line = escape(line)
            self.content_buffer.append(f"> {line}")
        self.content_buffer.append("")
        
    def add_image_reference(
        self, alt_text: str, image_path: Path, title: Optional[str] = None
    ):
        """
        画像参照を追加
        
        Args:
            alt_text: 代替テキスト
            image_path: 画像ファイルのパス
            title: タイトル（オプション）
        """
        # Unixスタイルパスに変換
        path_str = image_path.as_posix()
        
        if title:
            self.content_buffer.append(f'![{alt_text}]({path_str} "{title}")')
        else:
            self.content_buffer.append(f'![{alt_text}]({path_str})')
        self.content_buffer.append("")

    def add_html_component_reference(
        self, component_path: Path, width: str = "100%", height: Optional[str] = "400px" # heightをOptionalに
    ):
        """
        HTML図表や表をiframeで埋め込む
        
        Args:
            component_path: HTMLファイルのパス
            width: 幅の指定
            height: 高さの指定 (Noneの場合、height属性は出力されない)
        """
        # Unixスタイルパスに変換
        path_str = component_path.as_posix()
        
        # heightがNoneでない場合にのみheight属性を追加
        height_attr = f'height="{height}"' if height is not None else ''
        
        iframe_html = (
            f'<iframe src="{path_str}" '
            f'width="{width}" {height_attr} ' # height_attr を埋め込む
            f'style="border: 1px solid #ddd; border-radius: 4px;" '
            f'scrolling="no" class="auto-height-iframe">' # scrolling="no" と class を追加
            f'</iframe>'
        )
        self.content_buffer.append(iframe_html)
        self.content_buffer.append("")

    def add_markdown_content(self, content: str): # 必要に応じて追加
        self.content_buffer.append(content)
        
    def add_admonition(
        self, type: str, title: str, content: str, collapsible: bool = False
    ):
        """
        MkDocs MaterialのAdmonitionブロックを追加
        
        Args:
            type: 注記のタイプ
            title: タイトル
            content: 内容
            collapsible: 折りたたみ可能にするか
        """
        admonition_md = generate_admonition_markdown(type, title, content, collapsible)
        self.content_buffer.append(admonition_md)
        
    def add_tabbed_block(self, tabs_data: Dict[str, str]):
        """
        MkDocs MaterialのTabbedブロックを追加
        
        Args:
            tabs_data: タブデータの辞書
        """
        tabbed_md = generate_tabbed_markdown(tabs_data)
        self.content_buffer.append(tabbed_md)
        
    def add_horizontal_rule(self):
        """水平線を追加"""
        self.content_buffer.append("---")
        self.content_buffer.append("")
        
    def add_raw_markdown(self, markdown_string: str):
        """
        生のMarkdown文字列を追加
        
        Args:
            markdown_string: Markdown文字列
        """
        self.content_buffer.append(markdown_string)
        
    def add_icon_with_tooltip(self, icon_name: str, tooltip_text: str):
        """
        Material Design Iconsにツールチップを付与
        
        Args:
            icon_name: アイコン名
            tooltip_text: ツールチップテキスト
        """
        escaped_tooltip = escape(tooltip_text)
        icon_md = f':material-{icon_name}:{{ title="{escaped_tooltip}" }}'
        self.content_buffer.append(icon_md)
        self.content_buffer.append("")
        
    def add_abbreviation_definition(self, abbr: str, full_form: str):
        """
        略語の定義を追加
        
        Args:
            abbr: 略語
            full_form: フルスペルまたは説明
        """
        self.content_buffer.append(f"*[{abbr}]: {full_form}")
        self.content_buffer.append("")
        
    def add_quiz_question(self, question_data: Dict[str, Any]):
        """
        クイズ問題を追加（mkdocs-quiz-plugin形式）
        
        Args:
            question_data: 問題データの辞書
        """
        # クイズプラグインの形式に従って生成
        lines = ["??? question \"クイズ\""]
        lines.append(f"    {question_data['question']}")
        lines.append("")
        
        for i, option in enumerate(question_data['options']):
            prefix = "[x]" if i == question_data['correct'] else "[ ]"
            lines.append(f"    {prefix} {option}")
        
        if 'hint' in question_data:
            lines.append("")
            lines.append(f"    ??? tip \"ヒント\"")
            lines.append(f"        {question_data['hint']}")
        
        if 'explanation' in question_data:
            lines.append("")
            lines.append(f"    ??? success \"解説\"")
            lines.append(f"        {question_data['explanation']}")
        
        self.content_buffer.extend(lines)
        self.content_buffer.append("")
        
    def add_faq_item(self, question: str, answer: str, collapsible: bool = True):
        """
        FAQ項目を追加
        
        Args:
            question: 質問
            answer: 回答
            collapsible: 折りたたみ可能にするか
        """
        self.add_admonition("question", question, answer, collapsible)
        
    def add_tip_item(self, title: str, content: str, collapsible: bool = True):
        """
        TIPS項目を追加
        
        Args:
            title: タイトル
            content: 内容
            collapsible: 折りたたみ可能にするか
        """
        self.add_admonition("tip", title, content, collapsible)
        
    def add_code_block_with_static_output(
        self, code: str, output: str, lang: str = "python", output_label: str = "実行結果"
    ):
        """
        コードブロックと静的な実行結果を追加
        
        Args:
            code: コード
            output: 実行結果
            lang: 言語
            output_label: 出力ラベル
        """
        self.add_code_block(code, lang)
        self.add_admonition("success", output_label, f"```\n{output}\n```", False)
        
    def add_summary_section(self, title: str, points: List[str]):
        """
        学習の要点（サマリー）セクションを追加
        
        Args:
            title: セクションタイトル
            points: 要点のリスト
        """
        content = "\n".join(f"- {point}" for point in points)
        self.add_admonition("note", title, content, False)
        
    def add_recommendation_section(self, title: str, items: List[Dict[str, str]]):
        """
        関連資料や次のステップのレコメンデーションを追加
        
        Args:
            title: セクションタイトル
            items: レコメンデーション項目のリスト [{"text": "表示テキスト", "link": "URL"}]
        """
        lines = []
        for item in items:
            text = item.get("text", "")
            link = item.get("link", "")
            if link:
                lines.append(f"- [{text}]({link})")
            else:
                lines.append(f"- {text}")
        
        content = "\n".join(lines)
        self.add_admonition("info", title, content, False)
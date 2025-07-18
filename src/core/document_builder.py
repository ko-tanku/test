"""
Document builder for MkDocs Materials Generator
Markdownコンテンツを構築するためのクラス
"""

import logging
import re
import html
from pathlib import Path
from typing import Dict, List, Optional, Any, Union

from .utils import (
    slugify, ensure_directory_exists, safe_filename, validate_url_path,
    generate_admonition_markdown, generate_tabbed_markdown
)

logger = logging.getLogger(__name__)


class DocumentBuilder:
    """
    Markdownドキュメントを構築するためのクラス
    """

    def __init__(self, output_dir: Path):
        """
        初期化

        Args:
            output_dir: Markdownファイル出力先のベースディレクトリ
        """
        self.output_dir = ensure_directory_exists(output_dir)
        self.content_buffer: List[str] = []
        self.logger = logging.getLogger(__name__ + ".DocumentBuilder")

    def _add_content(self, content: str) -> None:
        """
        コンテンツバッファに追加

        Args:
            content: 追加するコンテンツ
        """
        self.content_buffer.append(content)

    def _ensure_empty_line(self) -> None:
        """
        最後の行が空行でない場合は空行を追加
        """
        if self.content_buffer and self.content_buffer[-1].strip():
            self.content_buffer.append("")

    def save_markdown(self, filename: str) -> Path:
        """
        構築中のMarkdownコンテンツをファイルとして保存

        Args:
            filename: 保存するファイル名

        Returns:
            保存されたファイルのパス
        """
        try:
            # ファイル名を安全な形式に変換
            safe_name = safe_filename(filename)
            if not safe_name.endswith('.md'):
                safe_name += '.md'

            output_path = self.output_dir / safe_name

            # コンテンツを結合
            content = "\n".join(self.content_buffer)

            # ファイルに保存
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)

            # バッファをクリア
            self.content_buffer.clear()

            self.logger.info(f"Markdown file saved: {output_path}")

            return output_path

        except Exception as e:
            self.logger.error(f"Failed to save markdown file '{filename}': {e}")
            raise

    def add_metadata(self, metadata: Dict[str, Any]) -> None:
        """
        YAMLフロントマターを追加

        Args:
            metadata: メタデータ辞書
        """
        self._add_content("---")
        for key, value in metadata.items():
            if isinstance(value, str):
                # 文字列の場合はエスケープ
                value = value.replace('"', '\\"')
                self._add_content(f'{key}: "{value}"')
            else:
                self._add_content(f"{key}: {value}")
        self._add_content("---")
        self._ensure_empty_line()

    def add_heading(self, text: str, level: int) -> None:
        """
        見出しを追加

        Args:
            text: 見出しテキスト
            level: 見出しレベル (1-6)
        """
        if not 1 <= level <= 6:
            self.logger.warning(f"Invalid heading level {level}. Using level 1.")
            level = 1

        self._ensure_empty_line()
        self._add_content(f"{'#' * level} {text}")
        self._ensure_empty_line()

    def add_paragraph(self, text: str) -> None:
        """
        段落を追加

        Args:
            text: 段落テキスト
        """
        self._ensure_empty_line()
        self._add_content(text)
        self._ensure_empty_line()

    def add_paragraph_with_tooltips(
        self,
        text: str,
        terms_info: Dict[str, Dict[str, str]]
    ) -> None:
        """
        ツールチップ付き段落を追加

        Args:
            text: 段落テキスト
            terms_info: 用語情報辞書 {"用語": {"tooltip_text": "説明"}}
        """
        if not terms_info:
            self.add_paragraph(text)
            return

        # 用語を長い順にソート（長い用語から置換することで部分一致を防ぐ）
        sorted_terms = sorted(terms_info.keys(), key=len, reverse=True)

        # テキストを処理
        processed_text = text

        for term in sorted_terms:
            tooltip_text = terms_info[term].get("tooltip_text", "")
            if not tooltip_text:
                continue

            # ツールチップテキストをHTMLエスケープ
            escaped_tooltip = html.escape(tooltip_text).replace('"', '&quot;')

            # 既存のMarkdownリンクを保護
            # 一時的なプレースホルダーに置換
            link_pattern = r'\[([^\]]+)\]\([^\)]+\)'
            links = re.findall(link_pattern, processed_text)
            placeholders = {}

            for i, link in enumerate(links):
                placeholder = f"{{{{LINK_PLACEHOLDER_{i})}}}}"
                placeholders[placeholder] = link
                processed_text = processed_text.replace(link, placeholder, 1)

            # 単語境界を使用して用語を置換
            # 日本語の場合は単語境界が機能しないため、別の方法を使用
            if re.search(r'[ぁ-んァ-ン一-龥]', term):
                # 日本語を含む場合
                pattern = re.escape(term)
            else:
                # 英語の場合
                pattern = r'\b' + re.escape(term) + r'\b'

            # ツールチップ構文に置換
            tooltip_syntax = f'<span data-md-tooltip="{escaped_tooltip}">{term}</span>'
            processed_text = re.sub(pattern, tooltip_syntax, processed_text)

            # プレースホルダーを元に戻す
            for placeholder, link in placeholders.items():
                processed_text = processed_text.replace(placeholder, link)

        self.add_paragraph(processed_text)

    def add_code_block(self, code: str, lang: str = "python") -> None:
        """
        コードブロックを追加

        Args:
            code: コード
            lang: 言語
        """
        self._ensure_empty_line()
        self._add_content(f"```{lang}")
        self._add_content(code)
        self._add_content("```")
        self._ensure_empty_line()

    def add_unordered_list(self, items: List[str]) -> None:
        """
        箇条書きリストを追加

        Args:
            items: リスト項目
        """
        self._ensure_empty_line()
        for item in items:
            self._add_content(f"- {item}")
        self._ensure_empty_line()

    def add_ordered_list(self, items: List[str]) -> None:
        """
        番号付きリストを追加

        Args:
            items: リスト項目
        """
        self._ensure_empty_line()
        for i, item in enumerate(items, 1):
            self._add_content(f"{i}. {item}")
        self._ensure_empty_line()

    def add_quote(self, text: str) -> None:
        """
        引用ブロックを追加

        Args:
            text: 引用テキスト
        """
        self._ensure_empty_line()
        for line in text.split('\n'):
            self._add_content(f"> {line}")
        self._ensure_empty_line()

    def add_table(self, headers: List[str], rows: List[List[Any]]) -> None:
        """
        Markdownテーブルを追加

        Args:
            headers: ヘッダー行
            rows: データ行のリスト
        """
        self._ensure_empty_line()

        # ヘッダー行
        header_row = "| " + " | ".join(str(h) for h in headers) + " |"
        self._add_content(header_row)

        # 区切り行
        separator_row = "| " + " | ".join("---" for _ in headers) + " |"
        self._add_content(separator_row)

        # データ行
        for row in rows:
            # 行の要素数を調整
            adjusted_row = list(row) + [""] * (len(headers) - len(row))
            data_row = "| " + " | ".join(str(cell) for cell in adjusted_row[:len(headers)]) + " |"
            self._add_content(data_row)

        self._ensure_empty_line()

    def add_image_reference(
        self,
        alt_text: str,
        image_path: Path,
        title: Optional[str] = None
    ) -> None:
        """
        画像参照を追加

        Args:
            alt_text: 代替テキスト
            image_path: 画像パス
            title: タイトル（オプション）
        """
        # Unixスタイルパスに変換
        unix_path = image_path.as_posix()

        if title:
            self._add_content(f'![{alt_text}]({unix_path} "{title}")')
        else:
            self._add_content(f'![{alt_text}]({unix_path})')
        self._ensure_empty_line()

    def add_html_component_reference(
        self,
        component_path: Path,
        width: str = "100%",
        height: str = "400px"
    ) -> None:
        """
        HTMLコンポーネント（図表や表）の埋め込み

        Args:
            component_path: コンポーネントのパス
            width: 幅
            height: 高さ
        """
        # 相対パスを計算
        try:
            # output_dirからの相対パスを計算
            relative_path = Path(component_path).relative_to(self.output_dir.parent)
        except ValueError:
            # 相対パス計算に失敗した場合は絶対パスを使用
            relative_path = component_path

        # Unixスタイルパスに変換
        unix_path = relative_path.as_posix()

        # iframeタグを生成
        iframe_html = f'<iframe src="{unix_path}" width="{width}" height="{height}" frameborder="0" style="border: 1px solid #e0e0e0; border-radius: 4px;"></iframe>'

        self._ensure_empty_line()
        self._add_content(iframe_html)
        self._ensure_empty_line()

    def add_admonition(
        self,
        type: str,
        title: str,
        content: str,
        collapsible: bool = False
    ) -> None:
        """
        Material for MkDocsの注記ブロックを追加

        Args:
            type: 注記タイプ
            title: タイトル
            content: コンテンツ
            collapsible: 折りたたみ可能か
        """
        admonition_md = generate_admonition_markdown(type, title, content, collapsible)
        self._ensure_empty_line()
        self._add_content(admonition_md)
        self._ensure_empty_line()

    def add_tabbed_block(self, tabs_data: Dict[str, str]) -> None:
        """
        Material for MkDocsのタブブロックを追加

        Args:
            tabs_data: タブデータ辞書
        """
        tabbed_md = generate_tabbed_markdown(tabs_data)
        self._ensure_empty_line()
        self._add_content(tabbed_md)
        self._ensure_empty_line()

    def add_horizontal_rule(self) -> None:
        """
        水平線を追加
        """
        self._ensure_empty_line()
        self._add_content("---")
        self._ensure_empty_line()

    def add_raw_markdown(self, markdown_string: str) -> None:
        """
        生のMarkdown文字列を追加

        Args:
            markdown_string: Markdown文字列
        """
        self._add_content(markdown_string)

    def add_link(self, text: str, url: str, title: Optional[str] = None) -> None:
        """
        リンクを追加

        Args:
            text: リンクテキスト
            url: URL
            title: タイトル（オプション）
        """
        if title:
            link_md = f'[{text}]({url} "{title}")'
        else:
            link_md = f'[{text}]({url})'

        self._add_content(link_md)

    def add_footnote(self, reference: str, content: str) -> None:
        """
        脚注を追加

        Args:
            reference: 参照名
            content: 脚注内容
        """
        # 本文中の参照
        self._add_content(f"[^{reference}]")

        # 脚注定義（ドキュメントの最後に追加される）
        self._ensure_empty_line()
        self._add_content(f"[^{reference}]: {content}")
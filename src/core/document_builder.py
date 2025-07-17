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
            
            self.logger.info(f"Markdown saved: {output_path}")
            
            # バッファをクリア
            self.content_buffer.clear()
            
            return output_path
            
        except Exception as e:
            self.logger.error(f"Failed to save markdown '{filename}': {e}")
            raise
    
    def add_heading(self, text: str, level: int) -> None:
        """
        Markdownの見出しを追加
        
        Args:
            text: 見出しテキスト
            level: 見出しレベル (1-6)
        """
        if not 1 <= level <= 6:
            self.logger.warning(f"Invalid heading level {level}, using level 1")
            level = 1
        
        self._ensure_empty_line()
        heading_marker = "#" * level
        self._add_content(f"{heading_marker} {text}")
        self._add_content("")
    
    def add_paragraph(self, text: str) -> None:
        """
        段落テキストを追加
        
        Args:
            text: 段落テキスト
        """
        if not text.strip():
            return
        
        self._ensure_empty_line()
        self._add_content(text)
        self._add_content("")
    
    def add_paragraph_with_tooltips(
        self, 
        text: str, 
        terms_info: Dict[str, Dict[str, str]]
    ) -> None:
        """
        専門用語にツールチップを付与した段落を追加
        
        Args:
            text: 段落テキスト
            terms_info: 用語情報の辞書 {"用語": {"tooltip_text": "..."}}
        """
        if not text.strip():
            return
        
        processed_text = text
        
        # 長い用語から先に処理（部分一致を防ぐため）
        sorted_terms = sorted(terms_info.keys(), key=len, reverse=True)
        
        for term in sorted_terms:
            if term in terms_info:
                tooltip_data = terms_info[term]
                tooltip_text = tooltip_data.get("tooltip_text", "")
                
                if tooltip_text:
                    # HTMLエスケープ
                    escaped_tooltip = html.escape(tooltip_text, quote=True)
                    
                    # 単語境界を使用して正確な一致のみを置換
                    pattern = r'\b' + re.escape(term) + r'\b'
                    
                    # Material for MkDocsの正しいツールチップ構文
                    # data-md-tooltip 属性を使用（リンクなし）
                    tooltip_markup = f'<span data-md-tooltip="{escaped_tooltip}">{term}</span>'
                    
                    # 置換
                    processed_text = re.sub(pattern, tooltip_markup, processed_text)
        
        self.add_paragraph(processed_text)

    def add_code_block(self, code: str, lang: str = "python") -> None:
        """
        コードブロックを追加
        
        Args:
            code: コード内容
            lang: 言語指定
        """
        self._ensure_empty_line()
        self._add_content(f"```{lang}")
        self._add_content(code)
        self._add_content("```")
        self._add_content("")
    
    def add_unordered_list(self, items: List[str]) -> None:
        """
        順序なしリストを追加
        
        Args:
            items: リスト項目
        """
        if not items:
            return
        
        self._ensure_empty_line()
        for item in items:
            self._add_content(f"- {item}")
        self._add_content("")
    
    def add_ordered_list(self, items: List[str]) -> None:
        """
        順序付きリストを追加
        
        Args:
            items: リスト項目
        """
        if not items:
            return
        
        self._ensure_empty_line()
        for i, item in enumerate(items, 1):
            self._add_content(f"{i}. {item}")
        self._add_content("")
    
    def add_quote(self, text: str) -> None:
        """
        引用ブロックを追加
        
        Args:
            text: 引用テキスト
        """
        self._ensure_empty_line()
        quote_lines = text.split("\n")
        for line in quote_lines:
            self._add_content(f"> {line}")
        self._add_content("")
    
    def add_image_reference(
        self, 
        alt_text: str, 
        image_path: Path, 
        title: Optional[str] = None
    ) -> None:
        """
        Markdownに画像参照を追加
        
        Args:
            alt_text: 代替テキスト
            image_path: 画像ファイルのパス
            title: 画像のタイトル（オプション）
        """
        # パスをUnixスタイルに変換
        unix_path = image_path.as_posix()
        
        # パスの妥当性を検証
        if not validate_url_path(unix_path):
            self.logger.warning(f"Invalid image path: {unix_path}")
            return
        
        # Markdownリンクを構築
        if title:
            escaped_title = html.escape(title, quote=True)
            markdown_link = f'![{alt_text}]({unix_path} "{escaped_title}")'
        else:
            markdown_link = f'![{alt_text}]({unix_path})'
       
        self._ensure_empty_line()
        self._add_content(markdown_link)
        self._add_content("")
    
    def add_html_component_reference(
        self, 
        component_path: Path, 
        width: str = "100%", 
        height: str = "600px"  # デフォルト高さを増加
    ) -> None:
        """
        生成されたHTMLコンポーネントをMarkdownに埋め込む
        
        Args:
            component_path: HTMLコンポーネントのパス
            width: iframeの幅
            height: iframeの高さ
        """
        try:
            # プロジェクトルートからの相対パスを計算
            from .config import PATHS
            
            # docs/ からの相対パスを計算
            try:
                relative_path = component_path.relative_to(PATHS["docs_dir"])
                unix_path = relative_path.as_posix()
                
                # MkDocsでは、assetsディレクトリへの参照は絶対パスで
                if unix_path.startswith('assets/'):
                    unix_path = '/' + unix_path
                
            except ValueError:
                # 相対パス変換に失敗した場合はファイル名のみ
                unix_path = component_path.name
                self.logger.warning(f"Could not create relative path for {component_path}, using filename only")
            
            # レスポンシブなiframeコンテナを生成
            iframe_html = f'''
    <div style="width: 100%; margin: 20px 0; border: 1px solid #ddd; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
        <iframe 
            src="{unix_path}" 
            width="100%" 
            height="{height}" 
            frameborder="0" 
            allowfullscreen
            style="display: block; border: none; background: white;"
            scrolling="no">
        </iframe>
    </div>'''
            
            self._ensure_empty_line()
            self._add_content(iframe_html)
            self._add_content("")
            
        except Exception as e:
            self.logger.error(f"Failed to add HTML component reference: {e}")
            # フォールバック: リンクとして追加
            self._add_content(f"[{component_path.name}を表示]({unix_path})")
            self._add_content("")

    def add_admonition(
        self, 
        type: str, 
        title: str, 
        content: str, 
        collapsible: bool = False
    ) -> None:
        """
        MkDocs MaterialテーマのAdmonitionブロックを追加
        
        Args:
            type: 注記タイプ
            title: 注記タイトル
            content: 注記内容
            collapsible: 折りたたみ可能かどうか
        """
        admonition_markdown = generate_admonition_markdown(type, title, content, collapsible)
        
        self._ensure_empty_line()
        self._add_content(admonition_markdown)
    
    def add_tabbed_block(self, tabs_data: Dict[str, str]) -> None:
        """
        MkDocs MaterialテーマのTabbedブロックを追加
        
        Args:
            tabs_data: タブ名とコンテンツの辞書
        """
        if not tabs_data:
            return
        
        tabbed_markdown = generate_tabbed_markdown(tabs_data)
        
        self._ensure_empty_line()
        self._add_content(tabbed_markdown)
    
    def add_horizontal_rule(self) -> None:
        """
        水平線を追加
        """
        self._ensure_empty_line()
        self._add_content("---")
        self._add_content("")
    
    def add_raw_markdown(self, markdown_string: str) -> None:
        """
        生のMarkdown文字列を直接追加
        
        Args:
            markdown_string: 追加するMarkdown文字列
        """
        if not markdown_string.strip():
            return
        
        self._ensure_empty_line()
        self._add_content(markdown_string)
        self._add_content("")
    
    def add_table(self, headers: List[str], rows: List[List[str]]) -> None:
        """
        Markdownテーブルを追加
        
        Args:
            headers: テーブルヘッダー
            rows: テーブルの行データ
        """
        if not headers or not rows:
            return
        
        self._ensure_empty_line()
        
        # ヘッダー行
        header_row = "| " + " | ".join(headers) + " |"
        self._add_content(header_row)
        
        # 区切り行
        separator_row = "| " + " | ".join(["---"] * len(headers)) + " |"
        self._add_content(separator_row)
        
        # データ行
        for row in rows:
            # 行の長さをヘッダーに合わせる
            padded_row = row + [""] * (len(headers) - len(row))
            padded_row = padded_row[:len(headers)]
            
            data_row = "| " + " | ".join(padded_row) + " |"
            self._add_content(data_row)
        
        self._add_content("")
    
    def add_link(self, text: str, url: str, title: Optional[str] = None) -> None:
        """
        リンクを追加
        
        Args:
            text: リンクテキスト
            url: リンクURL
            title: リンクタイトル（オプション）
        """
        if title:
            escaped_title = html.escape(title, quote=True)
            link_markdown = f'[{text}]({url} "{escaped_title}")'
        else:
            link_markdown = f'[{text}]({url})'
        
        self._ensure_empty_line()
        self._add_content(link_markdown)
        self._add_content("")
    
    def add_toc(self, title: str = "目次") -> None:
        """
        目次を追加
        
        Args:
            title: 目次のタイトル
        """
        self._ensure_empty_line()
        self._add_content(f"## {title}")
        self._add_content("")
        self._add_content("[TOC]")
        self._add_content("")
    
    def get_content(self) -> str:
        """
        現在のコンテンツバッファの内容を取得
        
        Returns:
            コンテンツ文字列
        """
        return "\n".join(self.content_buffer)
    
    def clear_content(self) -> None:
        """
        コンテンツバッファをクリア
        """
        self.content_buffer.clear()
    
    def add_metadata(self, metadata: Dict[str, Any]) -> None:
        """
        Markdownメタデータを追加
        
        Args:
            metadata: メタデータの辞書
        """
        if not metadata:
            return
        
        # YAMLフロントマターとして追加
        self._add_content("---")
        for key, value in metadata.items():
            self._add_content(f"{key}: {value}")
        self._add_content("---")
        self._add_content("")
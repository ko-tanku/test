"""
Markdown描画エンジン

既存のDocumentBuilderを統合し、宣言的コンポーネントシステムに適合させたレンダラー。
Markdownドキュメント、MkDocs Material拡張、HTML埋め込みなどをサポートします。
"""

from typing import Dict, List, Any, Optional
from pathlib import Path
import logging
import json
import re
from html import escape

from .component_renderer import ComponentRenderer, BaseComponent
from .document_builder import DocumentBuilder  # 既存のDocumentBuilderをインポート
from .knowledge_manager import KnowledgeManager

logger = logging.getLogger(__name__)


class MarkdownRenderer(ComponentRenderer):
    """Markdown描画エンジン"""
    
    engine_name = "markdown"
    file_extension = "md"
    supported_component_types = [
        "Heading", "Paragraph", "List", "CodeBlock", "Admonition", 
        "Tabs", "Quiz", "Embed", "Image", "Table", "Link", "Quote",
        "MermaidDiagram", "LearningSection", "Summary"
    ]
    
    def __init__(self, output_dir: Path, config: Optional[Dict] = None):
        """
        MarkdownRendererを初期化
        
        Args:
            output_dir: 出力ディレクトリ
            config: ドキュメント設定
        """
        super().__init__(output_dir, config)
        
        # 既存のDocumentBuilderとの互換性を保持
        self.doc_builder = DocumentBuilder(output_dir)
        
        # KnowledgeManager（用語管理）
        self.knowledge_mgr = None
        if config and config.get('knowledge_manager'):
            self.knowledge_mgr = config['knowledge_manager']
        
        # Markdown固有の設定
        self.markdown_config = {
            'enable_toc': False,
            'enable_footnotes': True,
            'enable_math': False,
            'meta_tags': {}
        }
        
        # コンテンツ状態管理
        self.current_chapter = {
            'title': '',
            'path': '',
            'terms': {}
        }
    
    def _register_default_components(self):
        """デフォルトコンポーネントを登録"""
        self.component_registry.update({
            'Heading': HeadingComponent,
            'Paragraph': ParagraphComponent,
            'List': ListComponent,
            'CodeBlock': CodeBlockComponent,
            'Admonition': AdmonitionComponent,
            'Tabs': TabsComponent,
            'Quiz': QuizComponent,
            'Embed': EmbedComponent,
            'Image': ImageComponent,
            'Table': TableComponent,
            'Link': LinkComponent,
            'Quote': QuoteComponent,
            'MermaidDiagram': MermaidDiagramComponent,
            'LearningSection': LearningSectionComponent,
            'Summary': SummaryComponent,
        })
    
    def _apply_global_config(self, config: Dict[str, Any]):
        """グローバル設定を適用"""
        # Markdown設定を更新
        self.markdown_config.update({
            'enable_toc': config.get('toc', False),
            'enable_footnotes': config.get('footnotes', True),
            'enable_math': config.get('math', False),
            'meta_tags': config.get('meta', {})
        })
        
        # DocumentBuilderをクリア
        self.doc_builder.clear_content()
        
        # メタタグがある場合は追加
        if self.markdown_config['meta_tags']:
            for key, value in self.markdown_config['meta_tags'].items():
                self.doc_builder.add_raw_markdown(f"---\n{key}: {value}\n---\n")
        
        # TOCを有効にする場合
        if self.markdown_config['enable_toc']:
            self.doc_builder.add_raw_markdown("[TOC]\n")
        
        # タイトルを設定
        if config.get('title'):
            self.doc_builder.add_heading(config['title'], 1)
            self.current_chapter['title'] = config['title']
        
        # 現在の章のパス設定
        filename = config.get('filename', 'document')
        self.current_chapter['path'] = f"{filename}.md"
        
        logger.info(f"Markdownドキュメントを初期化: {self.markdown_config}")
    
    def _save_rendered_content(self, content: Any, output_path: Path, config: Dict[str, Any]):
        """Markdownファイルとして保存"""
        try:
            # DocumentBuilderを使用して保存
            markdown_content = self.doc_builder.get_content()
            
            if not markdown_content.strip():
                logger.warning("生成されたMarkdownコンテンツが空です")
            
            # ファイル保存
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(markdown_content, encoding='utf-8')
            
            logger.info(f"Markdownファイルを保存: {output_path}")
            
        except Exception as e:
            logger.error(f"Markdownファイルの保存に失敗: {e}")
            raise


# ======== コンポーネント実装 ========

class HeadingComponent(BaseComponent):
    """見出しコンポーネント"""
    
    type_name = "Heading"
    required_props = ['content']
    optional_props = {
        'level': 2,
        'id': None
    }
    
    @classmethod
    def render(cls, props: Dict[str, Any], renderer: MarkdownRenderer):
        props = cls.validate_props(props)
        
        content = props['content']
        level = props.get('level', 2)
        heading_id = props.get('id')
        
        if heading_id:
            # カスタムIDを持つ見出し
            renderer.doc_builder.add_raw_markdown(f"{'#' * level} {content} {{#{heading_id}}}\n")
        else:
            renderer.doc_builder.add_heading(content, level)


class ParagraphComponent(BaseComponent):
    """段落コンポーネント"""
    
    type_name = "Paragraph"
    required_props = ['content']
    optional_props = {
        'terms': {},
        'enableTooltips': False,
        'className': None
    }
    
    @classmethod
    def render(cls, props: Dict[str, Any], renderer: MarkdownRenderer):
        props = cls.validate_props(props)
        
        content = props['content']
        terms = props.get('terms', {})
        enable_tooltips = props.get('enableTooltips', False)
        class_name = props.get('className')
        
        if enable_tooltips and terms and renderer.knowledge_mgr:
            # 用語ツールチップ付きの段落
            renderer.doc_builder.add_paragraph_with_tooltips(
                content, terms, renderer.knowledge_mgr,
                renderer.current_chapter['title'],
                renderer.current_chapter['path']
            )
        else:
            # 通常の段落
            if class_name:
                renderer.doc_builder.add_raw_markdown(f'<div class="{class_name}">')
            
            renderer.doc_builder.add_paragraph(content)
            
            if class_name:
                renderer.doc_builder.add_raw_markdown('</div>')


class ListComponent(BaseComponent):
    """リストコンポーネント"""
    
    type_name = "List"
    required_props = ['items']
    optional_props = {
        'variant': 'unordered',
        'nested': False
    }
    
    @classmethod
    def render(cls, props: Dict[str, Any], renderer: MarkdownRenderer):
        props = cls.validate_props(props)
        
        items = props['items']
        variant = props.get('variant', 'unordered')
        
        if variant == 'ordered':
            renderer.doc_builder.add_ordered_list(items)
        else:
            renderer.doc_builder.add_unordered_list(items)


class CodeBlockComponent(BaseComponent):
    """コードブロックコンポーネント"""
    
    type_name = "CodeBlock"
    required_props = ['content']
    optional_props = {
        'language': 'python',
        'showLineNumbers': False,
        'highlightLines': [],
        'title': None,
        'output': None,
        'outputLabel': '実行結果'
    }
    
    @classmethod
    def render(cls, props: Dict[str, Any], renderer: MarkdownRenderer):
        props = cls.validate_props(props)
        
        content = props['content']
        language = props.get('language', 'python')
        title = props.get('title')
        output = props.get('output')
        output_label = props.get('outputLabel', '実行結果')
        
        # タイトル付きコードブロック
        if title:
            renderer.doc_builder.add_raw_markdown(f'!!! info "{title}"')
            renderer.doc_builder.add_raw_markdown(f'    ```{language}')
            for line in content.split('\n'):
                renderer.doc_builder.add_raw_markdown(f'    {line}')
            renderer.doc_builder.add_raw_markdown(f'    ```')
        else:
            renderer.doc_builder.add_code_block(content, language)
        
        # 実行結果がある場合
        if output:
            renderer.doc_builder.add_code_block_with_static_output(
                content, output, language, output_label
            )


class AdmonitionComponent(BaseComponent):
    """注釈ボックスコンポーネント"""
    
    type_name = "Admonition"
    required_props = ['content']
    optional_props = {
        'variant': 'info',
        'title': '',
        'collapsible': False
    }
    
    @classmethod
    def render(cls, props: Dict[str, Any], renderer: MarkdownRenderer):
        props = cls.validate_props(props)
        
        content = props['content']
        variant = props.get('variant', 'info')
        title = props.get('title', '')
        collapsible = props.get('collapsible', False)
        
        renderer.doc_builder.add_admonition(variant, title, content, collapsible)


class TabsComponent(BaseComponent):
    """タブコンテナコンポーネント"""
    
    type_name = "Tabs"
    required_props = ['tabs']
    
    @classmethod
    def render(cls, props: Dict[str, Any], renderer: MarkdownRenderer):
        props = cls.validate_props(props)
        
        tabs = props['tabs']
        
        # タブデータを文字列形式に変換
        tab_data = {}
        for tab_name, tab_content in tabs.items():
            if isinstance(tab_content, list):
                # コンポーネントリストの場合は先に処理
                content_parts = []
                for component in tab_content:
                    if isinstance(component, dict) and 'type' in component:
                        # ネストしたコンポーネントを処理
                        component_type = component['type']
                        component_props = component.get('props', {})
                        
                        if component_type in renderer.component_registry:
                            component_class = renderer.component_registry[component_type]
                            # 一時的にバッファを保存
                            temp_buffer = renderer.doc_builder.content_buffer.copy()
                            renderer.doc_builder.clear_content()
                            
                            # コンポーネントをレンダリング
                            component_class.render(component_props, renderer)
                            nested_content = renderer.doc_builder.get_content()
                            
                            # バッファを復元
                            renderer.doc_builder.content_buffer = temp_buffer
                            content_parts.append(nested_content)
                        else:
                            content_parts.append(str(component))
                    else:
                        content_parts.append(str(component))
                
                tab_data[tab_name] = '\n'.join(content_parts)
            else:
                tab_data[tab_name] = str(tab_content)
        
        renderer.doc_builder.add_tabbed_block(tab_data)


class QuizComponent(BaseComponent):
    """クイズコンポーネント"""
    
    type_name = "Quiz"
    required_props = ['variant', 'question']
    optional_props = {
        'options': [],
        'correct': [],
        'explanation': '',
        'id': None
    }
    
    @classmethod
    def render(cls, props: Dict[str, Any], renderer: MarkdownRenderer):
        props = cls.validate_props(props)
        
        variant = props['variant']
        quiz_data = {
            'question': props['question'],
            'options': props.get('options', []),
            'correct': props.get('correct', []),
            'explanation': props.get('explanation', ''),
            'quiz_id': props.get('id', f"quiz_{hash(props['question']) % 10000}")
        }
        
        if variant == 'single_choice':
            renderer.doc_builder.add_single_choice_quiz(quiz_data)
        elif variant == 'multiple_choice':
            renderer.doc_builder.add_multiple_choice_quiz(quiz_data)
        elif variant == 'categorization':
            # カテゴリ分けクイズ
            quiz_data.update({
                'items': props.get('items', []),
                'categories': props.get('categories', []),
                'correct_mapping': props.get('correct_mapping', [])
            })
            renderer.doc_builder.add_categorization_quiz(quiz_data)


class EmbedComponent(BaseComponent):
    """外部コンテンツ埋め込みコンポーネント"""
    
    type_name = "Embed"
    required_props = ['source']
    optional_props = {
        'width': '100%',
        'height': '400px',
        'title': '',
        'responsive': True
    }
    
    @classmethod
    def render(cls, props: Dict[str, Any], renderer: MarkdownRenderer):
        props = cls.validate_props(props)
        
        source = props['source']
        width = props.get('width', '100%')
        height = props.get('height', '400px')
        title = props.get('title', '')
        
        # Pathオブジェクトに変換
        source_path = Path(source)
        
        renderer.doc_builder.add_html_component_reference(
            source_path, width, height
        )


class ImageComponent(BaseComponent):
    """画像コンポーネント"""
    
    type_name = "Image"
    required_props = ['src', 'alt']
    optional_props = {
        'title': None,
        'width': None,
        'height': None,
        'className': None
    }
    
    @classmethod
    def render(cls, props: Dict[str, Any], renderer: MarkdownRenderer):
        props = cls.validate_props(props)
        
        src = props['src']
        alt = props['alt']
        title = props.get('title')
        width = props.get('width')
        height = props.get('height')
        class_name = props.get('className')
        
        # Path形式での画像参照
        image_path = Path(src)
        
        if width or height or class_name:
            # HTMLタグを使用
            style_attrs = []
            if width:
                style_attrs.append(f"width: {width}")
            if height:
                style_attrs.append(f"height: {height}")
            
            style = f' style="{"; ".join(style_attrs)}"' if style_attrs else ''
            class_attr = f' class="{class_name}"' if class_name else ''
            title_attr = f' title="{title}"' if title else ''
            
            renderer.doc_builder.add_raw_markdown(
                f'<img src="{src}" alt="{alt}"{title_attr}{class_attr}{style}>'
            )
        else:
            # 標準のMarkdown画像参照
            renderer.doc_builder.add_image_reference(image_path, alt, title)


class TableComponent(BaseComponent):
    """テーブルコンポーネント"""
    
    type_name = "Table"
    required_props = ['data']
    optional_props = {
        'variant': 'basic',
        'caption': None,
        'responsive': True
    }
    
    @classmethod
    def render(cls, props: Dict[str, Any], renderer: MarkdownRenderer):
        props = cls.validate_props(props)
        
        data = props['data']
        caption = props.get('caption')
        
        # テーブルデータを処理
        headers = data.get('headers', [])
        rows = data.get('rows', [])
        
        if not headers or not rows:
            logger.warning("テーブルデータが不完全です")
            return
        
        # Markdownテーブルを生成
        table_md = []
        
        if caption:
            table_md.append(f"*{caption}*\n")
        
        # ヘッダー行
        table_md.append("| " + " | ".join(headers) + " |")
        table_md.append("| " + " | ".join(["---"] * len(headers)) + " |")
        
        # データ行
        for row in rows:
            table_md.append("| " + " | ".join(str(cell) for cell in row) + " |")
        
        table_md.append("")  # 空行
        
        for line in table_md:
            renderer.doc_builder.add_raw_markdown(line)


class LinkComponent(BaseComponent):
    """リンクコンポーネント"""
    
    type_name = "Link"
    required_props = ['text', 'href']
    optional_props = {
        'title': None,
        'external': False
    }
    
    @classmethod
    def render(cls, props: Dict[str, Any], renderer: MarkdownRenderer):
        props = cls.validate_props(props)
        
        text = props['text']
        href = props['href']
        title = props.get('title')
        external = props.get('external', False)
        
        if external:
            # 外部リンク（新しいタブで開く）
            title_attr = f' title="{title}"' if title else ''
            renderer.doc_builder.add_raw_markdown(
                f'<a href="{href}" target="_blank" rel="noopener noreferrer"{title_attr}>{text}</a>'
            )
        else:
            # 通常のMarkdownリンク
            if title:
                renderer.doc_builder.add_raw_markdown(f'[{text}]({href} "{title}")')
            else:
                renderer.doc_builder.add_raw_markdown(f'[{text}]({href})')


class QuoteComponent(BaseComponent):
    """引用コンポーネント"""
    
    type_name = "Quote"
    required_props = ['content']
    optional_props = {
        'author': None,
        'source': None
    }
    
    @classmethod
    def render(cls, props: Dict[str, Any], renderer: MarkdownRenderer):
        props = cls.validate_props(props)
        
        content = props['content']
        author = props.get('author')
        source = props.get('source')
        
        quote_text = content
        if author:
            quote_text += f"\n\n— {author}"
        if source:
            quote_text += f", *{source}*"
        
        renderer.doc_builder.add_quote(quote_text)


class MermaidDiagramComponent(BaseComponent):
    """Mermaid図コンポーネント"""
    
    type_name = "MermaidDiagram"
    required_props = ['diagram']
    optional_props = {
        'title': None
    }
    
    @classmethod
    def render(cls, props: Dict[str, Any], renderer: MarkdownRenderer):
        props = cls.validate_props(props)
        
        diagram = props['diagram']
        title = props.get('title')
        
        renderer.doc_builder.add_mermaid_block(diagram, title)


class LearningSectionComponent(BaseComponent):
    """学習セクションコンポーネント（合成コンポーネント）"""
    
    type_name = "LearningSection"
    required_props = ['title', 'components']
    optional_props = {
        'level': 2,
        'showProgress': False
    }
    
    @classmethod
    def render(cls, props: Dict[str, Any], renderer: MarkdownRenderer):
        props = cls.validate_props(props)
        
        title = props['title']
        components = props['components']
        level = props.get('level', 2)
        show_progress = props.get('showProgress', False)
        
        # セクション見出し
        renderer.doc_builder.add_heading(title, level)
        
        # 進捗表示
        if show_progress:
            renderer.doc_builder.add_progress_indicator(0.0, 1, [False])
        
        # 子コンポーネントをレンダリング
        for component_spec in components:
            if isinstance(component_spec, dict) and 'type' in component_spec:
                component_type = component_spec['type']
                component_props = component_spec.get('props', {})
                
                if component_type in renderer.component_registry:
                    component_class = renderer.component_registry[component_type]
                    component_class.render(component_props, renderer)


class SummaryComponent(BaseComponent):
    """要約セクションコンポーネント"""
    
    type_name = "Summary"
    required_props = ['points']
    optional_props = {
        'title': 'まとめ',
        'variant': 'list'
    }
    
    @classmethod
    def render(cls, props: Dict[str, Any], renderer: MarkdownRenderer):
        props = cls.validate_props(props)
        
        points = props['points']
        title = props.get('title', 'まとめ')
        variant = props.get('variant', 'list')
        
        if variant == 'admonition':
            # アドモニション形式
            content = '\n'.join(f"- {point}" for point in points)
            renderer.doc_builder.add_admonition('success', title, content)
        else:
            # 通常のリスト形式
            renderer.doc_builder.add_summary_section(title, points)
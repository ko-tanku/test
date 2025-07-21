"""
学習資料のコンテンツ生成を管理する基底クラス
各種ジェネレータを統合し、章ごとのコンテンツ構築のフレームワークを提供
"""

import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
from abc import ABC, abstractmethod

from jinja2 import Environment, FileSystemLoader, select_autoescape

from .document_builder import DocumentBuilder
from .chart_generator import ChartGenerator
from .table_generator import TableGenerator
from .knowledge_manager import KnowledgeManager, Term, FaqItem, TipItem
from .config import GLOBAL_COLORS, BASE_CHART_STYLES, BASE_TABLE_STYLES

logger = logging.getLogger(__name__)


class BaseContentManager(ABC):
    """コンテンツ管理の基底クラス"""
    
    def __init__(
        self,
        material_name: str,
        output_base_dir: Path,
        colors: Optional[Dict[str, str]] = None,
        chart_styles: Optional[Dict[str, Any]] = None,
        table_styles: Optional[Dict[str, Any]] = None
    ):
        """
        初期化
        
        Args:
            material_name: 教材名
            output_base_dir: 出力ベースディレクトリ
            colors: カスタムカラー設定
            chart_styles: カスタム図表スタイル
            table_styles: カスタム表スタイル
        """
        self.material_name = material_name
        self.output_base_dir = Path(output_base_dir)
        
        # カラーとスタイルの設定
        self.colors = colors or GLOBAL_COLORS
        self.chart_styles = chart_styles or BASE_CHART_STYLES
        self.table_styles = table_styles or BASE_TABLE_STYLES
        
        # 各ジェネレータのインスタンス化
        self.doc_builder = DocumentBuilder(self.output_base_dir)
        self.chart_gen = ChartGenerator(self.colors, self.chart_styles)
        self.table_gen = TableGenerator(self.colors, self.table_styles)
        self.knowledge_mgr = KnowledgeManager(self.output_base_dir)
        
        # Jinja2環境の初期化
        template_dir = Path(__file__).parent.parent / "materials" / material_name / "templates"
        if template_dir.exists():
            self.jinja_env = Environment(
                loader=FileSystemLoader(str(template_dir)),
                autoescape=select_autoescape(['html', 'xml'])
            )
        else:
            # テンプレートディレクトリが存在しない場合は警告
            logger.warning(
                f"テンプレートディレクトリが見つかりません: {template_dir}"
            )
            self.jinja_env = None
            
    def _register_material_terms(self, terms_list: List[Term]):
        """
        専門用語を一括登録
        
        Args:
            terms_list: Termオブジェクトのリスト
        """
        self.knowledge_mgr.register_terms_batch(terms_list)
        
    def _register_faq_tips(self, faq_list: List[FaqItem], tip_list: List[TipItem]):
        """
        FAQとTIPSを一括登録
        
        Args:
            faq_list: FaqItemオブジェクトのリスト
            tip_list: TipItemオブジェクトのリスト
        """
        for faq in faq_list:
            self.knowledge_mgr.register_faq_item(faq)
        
        for tip in tip_list:
            self.knowledge_mgr.register_tip_item(tip)
            
    def _get_chapter_terms(self, chapter_title: str) -> Dict[str, Dict[str, str]]:
        """
        指定された章の用語情報を取得
        
        Args:
            chapter_title: 章のタイトル
            
        Returns:
            用語情報の辞書
        """
        return self.knowledge_mgr.get_terms_for_chapter(chapter_title)
        
    def generate_glossary(self) -> Path:
        """
        用語集を生成
        
        Returns:
            生成されたファイルのパス
        """
        return self.knowledge_mgr.generate_glossary_markdown()
        
    def generate_faq_page(self) -> Path:
        """
        FAQページを生成
        
        Returns:
            生成されたファイルのパス
        """
        return self.knowledge_mgr.generate_faq_markdown()
        
    def generate_tips_page(self) -> Path:
        """
        TIPSページを生成
        
        Returns:
            生成されたファイルのパス
        """
        return self.knowledge_mgr.generate_tips_markdown()
        
    @abstractmethod
    def generate_content(self) -> List[Path]:
        """
        資料全体のコンテンツを生成（継承クラスで実装必須）
        
        Returns:
            生成されたMarkdownファイルのパスリスト
        """
        raise NotImplementedError("継承クラスでgenerate_contentメソッドを実装してください")
        
    def _create_chapter_template(
        self, chapter_info: Dict[str, Any], chapter_func: Callable
    ) -> Path:
        """
        各章のコンテンツを生成
        
        Args:
            chapter_info: 章の情報
            chapter_func: 章のコンテンツ生成関数
            
        Returns:
            生成されたファイルのパス
        """
        # バッファをクリア
        self.doc_builder.clear_content()
        
        # 章のタイトルを追加
        self.doc_builder.add_heading(chapter_info.get("title", ""), 1)
        
        # Jinja2テンプレートを使用する場合
        if self.jinja_env and "template" in chapter_info:
            template = self.jinja_env.get_template(chapter_info["template"])
            
            # コンテキストデータを生成
            context = chapter_func()
            
            # テンプレートをレンダリング
            rendered_content = template.render(**context)
            self.doc_builder.add_raw_markdown(rendered_content)
        else:
            # テンプレートを使用しない場合は直接生成
            chapter_func()
        
        # ファイル保存
        filename = chapter_info.get("filename", "chapter.md")
        return self.doc_builder.save_markdown(filename)
        
    def _create_chapter_and_document_paths(
        self, chapter_name: str, doc_name: str = None
    ) -> Path:
        """
        章やドキュメントの出力パスを構築
        
        Args:
            chapter_name: 章の名前
            doc_name: ドキュメント名（オプション）
            
        Returns:
            構築されたパス
        """
        chapter_path = self.output_base_dir / chapter_name
        
        if doc_name:
            doc_path = chapter_path / "documents"
            doc_path.mkdir(parents=True, exist_ok=True)
            
            # 関連ディレクトリも作成
            (chapter_path / "charts").mkdir(parents=True, exist_ok=True)
            (chapter_path / "tables").mkdir(parents=True, exist_ok=True)
            
            return doc_path / doc_name
        else:
            # 章のルートディレクトリを作成
            chapter_path.mkdir(parents=True, exist_ok=True)
            
            # 関連ディレクトリも作成
            (chapter_path / "charts").mkdir(parents=True, exist_ok=True)
            (chapter_path / "tables").mkdir(parents=True, exist_ok=True)
            
            return chapter_path

    def _process_content_list(self, contents: List[Dict[str, Any]], charts_dir: Path, tables_dir: Path):
        """
        コンテンツリストを処理してMarkdownに変換
        
        Args:
            contents: コンテンツ要素のリスト
            charts_dir: 図表の出力ディレクトリ
            tables_dir: 表の出力ディレクトリ
        """
        for item in contents:
            content_type = item.get('type')
            
            if content_type == 'text':
                self.doc_builder.add_paragraph(item.get('text', ''))
                
            elif content_type == 'text_with_tooltips':
                text = item.get('text', '')
                terms = item.get('terms', {})
                self.doc_builder.add_paragraph_with_tooltips(text, terms)
                
            elif content_type == 'heading':
                text = item.get('text', '')
                level = item.get('level', 2)
                self.doc_builder.add_heading(text, level)
                
            elif content_type == 'chart':
                self._process_chart(item, charts_dir)
                
            elif content_type == 'table':
                self._process_table(item, tables_dir)
                
            elif content_type == 'code':
                code = item.get('code', '')
                lang = item.get('lang', 'python')
                self.doc_builder.add_code_block(code, lang)
                
            elif content_type == 'code_with_output':
                code = item.get('code', '')
                output = item.get('output', '')
                lang = item.get('lang', 'python')
                output_label = item.get('output_label', '実行結果')
                self.doc_builder.add_code_block_with_static_output(code, output, lang, output_label)
                
            elif content_type == 'list':
                items_list = item.get('items', [])
                list_type = item.get('list_type', 'unordered')
                if list_type == 'ordered':
                    self.doc_builder.add_ordered_list(items_list)
                else:
                    self.doc_builder.add_unordered_list(items_list)
                    
            elif content_type == 'quote':
                text = item.get('text', '')
                self.doc_builder.add_quote(text)
                
            elif content_type == 'admonition':
                adm_type = item.get('admonition_type', 'note')
                title = item.get('title', '')
                text = item.get('text', '')
                collapsible = item.get('collapsible', False)
                self.doc_builder.add_admonition(adm_type, title, text, collapsible)
                
            elif content_type == 'tabs':
                tabs_data = item.get('tabs_data', {})
                self.doc_builder.add_tabbed_block(tabs_data)
                
            elif content_type == 'quiz':
                question_data = item.get('question_data', {})
                self.doc_builder.add_quiz_question(question_data)
                
            elif content_type == 'image':
                alt_text = item.get('alt_text', '')
                image_path = Path(item.get('path', ''))
                title = item.get('title', None)
                self.doc_builder.add_image_reference(alt_text, image_path, title)
                
            elif content_type == 'html_component':
                component_path = Path(item.get('path', ''))
                width = item.get('width', '100%')
                height = item.get('height', '400px')
                self.doc_builder.add_html_component_reference(component_path, width, height)
                
            elif content_type == 'horizontal_rule':
                self.doc_builder.add_horizontal_rule()
                
            elif content_type == 'summary':
                title = item.get('title', '要点')
                points = item.get('points', [])
                self.doc_builder.add_summary_section(title, points)
                
            elif content_type == 'recommendations':
                title = item.get('title', '関連資料')
                items_list = item.get('items', [])
                self.doc_builder.add_recommendation_section(title, items_list)
                
    def _process_chart(self, chart_config: Dict[str, Any], output_dir: Path):
        """
        図表設定を処理して生成・埋め込み
        
        Args:
            chart_config: 図表の設定
            output_dir: 出力ディレクトリ
        """
        chart_type = chart_config.get('chart_type', 'line')
        config = chart_config.get('config', {})
        
        if chart_type == 'custom':
            plot_function = config.get('plot_function')
            if plot_function:
                filename = config.get('filename', 'custom_chart.html')
                chart_path = self.chart_gen.create_custom_figure(
                    plot_function, filename, output_dir=output_dir
                )
            else:
                logger.warning("カスタムチャートに描画関数が指定されていません")
                return
        else:
            data = chart_config.get('data', {})
            if chart_type == 'line':
                chart_path = self.chart_gen.create_simple_line_chart(
                    data, 
                    config.get('x_col', 'x'),
                    config.get('y_col', 'y'),
                    config.get('title', ''),
                    config.get('xlabel', ''),
                    config.get('ylabel', ''),
                    config.get('filename', 'line_chart.html'),
                    config.get('use_plotly', False),
                    output_dir
                )
            elif chart_type == 'bar':
                chart_path = self.chart_gen.create_bar_chart(
                    data,
                    config.get('x_col', 'x'),
                    config.get('y_col', 'y'),
                    config.get('title', ''),
                    config.get('xlabel', ''),
                    config.get('ylabel', ''),
                    config.get('filename', 'bar_chart.html'),
                    config.get('use_plotly', False),
                    output_dir
                )
        
        if 'chart_path' in locals():
            caption = chart_config.get('caption', '')
            if caption:
                self.doc_builder.add_paragraph(f"**{caption}**")
            
            # documentsフォルダから2階層上がってchartsフォルダへ
            relative_path = Path("../..") / "charts" / chart_path.name
            self.doc_builder.add_html_component_reference(
                relative_path,
                '100%',  # 幅は100%
                 None  # 高さは固定（スクロール防止）
            )

    def _process_table(self, table_config: Dict[str, Any], output_dir: Path):
        """
        表設定を処理して生成・埋め込み
        """
        table_type = table_config.get('table_type', 'basic')
        headers = table_config.get('headers', [])
        rows = table_config.get('rows', [])
        title = table_config.get('title', '')
        filename = table_config.get('filename', 'table.html') + '.html'
        
        if table_type == 'basic':
            table_path = self.table_gen.create_basic_table(
                headers, rows, title, filename, output_dir=output_dir
            )
        elif table_type == 'comparison':
            categories = table_config.get('categories', [])
            items = table_config.get('items', [])
            data = table_config.get('data', [])
            table_path = self.table_gen.create_comparison_table(
                categories, items, data, title, filename, output_dir=output_dir
            )
            
        if 'table_path' in locals():
            relative_path = Path("../..") / "tables" / table_path.name
            self.doc_builder.add_html_component_reference(
                relative_path,
                '100%',
                 None  # 表も固定高さ
            )
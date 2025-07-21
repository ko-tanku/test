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

    def render_template(self, template_name: str, context: Dict[str, Any]) -> str:
        """
        Jinja2テンプレートをレンダリング
        
        Args:
            template_name: テンプレートファイル名
            context: テンプレートに渡すデータ
            
        Returns:
            レンダリング済みMarkdown文字列
        """
        if not self.jinja_env:
            logger.warning("Jinja2環境が初期化されていません")
            return ""
            
        try:
            template = self.jinja_env.get_template(template_name)
            return template.render(**context)
        except Exception as e:
            logger.error(f"テンプレートレンダリングエラー: {e}")
            return ""
        
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
            elif content_type == 'exercises':

                question_data = item.get('question_data', {})
                self.doc_builder.add_exercise_question(question_data)
                
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
                
            elif content_type == 'icon_tooltip':
                icon_name = item.get('icon_name', 'help')
                tooltip_text = item.get('tooltip_text', '')
                self.doc_builder.add_icon_with_tooltip(icon_name, tooltip_text)
                
            elif content_type == 'abbreviation':
                abbr = item.get('abbr', '')
                full_form = item.get('full_form', '')
                self.doc_builder.add_abbreviation_definition(abbr, full_form)



    def _process_chart(self, chart_config: Dict[str, Any], output_dir: Path):
        """
        図表設定を処理して生成・埋め込み
        全てのチャートタイプに対応
        
        Args:
            chart_config: 図表の設定
            output_dir: 出力ディレクトリ
        """
        chart_type = chart_config.get('chart_type', 'line')
        config = chart_config.get('config', {})
        data = chart_config.get('data', {})
        chart_path = None
        
        try:
            # ファイル名の正規化
            filename = config.get('filename', f'{chart_type}_chart')
            if not filename.endswith('.html'):
                filename += '.html'
            
            if chart_type == 'custom':
                # カスタム描画関数による図表
                plot_function = config.get('plot_function')
                if plot_function:
                    chart_path = self.chart_gen.create_custom_figure(
                        plot_function, filename, output_dir=output_dir
                    )
                else:
                    logger.warning("カスタムチャートに描画関数が指定されていません")
                    return
                    
            elif chart_type == 'line':
                # 折れ線グラフ
                chart_path = self.chart_gen.create_simple_line_chart(
                    data, 
                    config.get('x_col', 'x'),
                    config.get('y_col', 'y'),
                    config.get('title', ''),
                    config.get('xlabel', ''),
                    config.get('ylabel', ''),
                    filename,
                    config.get('use_plotly', False),
                    output_dir
                )
                
            elif chart_type == 'bar':
                # 棒グラフ
                chart_path = self.chart_gen.create_bar_chart(
                    data,
                    config.get('x_col', 'x'),
                    config.get('y_col', 'y'),
                    config.get('title', ''),
                    config.get('xlabel', ''),
                    config.get('ylabel', ''),
                    filename,
                    config.get('use_plotly', False),
                    output_dir
                )
                
            elif chart_type == 'pie':
                # 円グラフ
                chart_path = self.chart_gen.create_pie_chart(
                    data,
                    config.get('values_col', 'values'),
                    config.get('labels_col', 'labels'),
                    config.get('title', ''),
                    filename,
                    config.get('use_plotly', False),
                    output_dir
                )
                
            elif chart_type == 'scatter':
                # 散布図（既存メソッドがある場合）
                if hasattr(self.chart_gen, 'create_scatter_chart'):
                    chart_path = self.chart_gen.create_scatter_chart(
                        data,
                        config.get('x_col', 'x'),
                        config.get('y_col', 'y'),
                        config.get('title', ''),
                        config.get('xlabel', ''),
                        config.get('ylabel', ''),
                        filename,
                        config.get('use_plotly', False),
                        output_dir
                    )
                else:
                    logger.warning(f"散布図メソッドが実装されていません")
                    

            elif chart_type == 'animation':
                # アニメーションGIF生成
                frames_data = data.get('frames', [])
                if frames_data:
                    # GIFファイル名に変更
                    gif_filename = filename.replace('.html', '.gif')
                    chart_path = self.chart_gen.create_animation_from_data(
                        frames_data, config, gif_filename, output_dir
                    )
                    
                    # GIFファイルの場合は画像参照として埋め込み
                    if chart_path and chart_path.suffix == '.gif':
                        caption = chart_config.get('caption', '')
                        if caption:
                            self.doc_builder.add_paragraph(f"**{caption}**")
                        
                        # GIFファイルは画像として埋め込み（相対パス修正）
                        relative_path = Path("../../charts") / chart_path.name
                        self.doc_builder.add_image_reference(
                            "アニメーション図表", relative_path
                        )
                        logger.debug(f"アニメーションGIF埋め込み成功: {chart_path.name}")
                        return  # 早期リターン（通常のiframe処理をスキップ）
                else:
                    logger.warning("アニメーション用のフレームデータが見つかりません")
                    
            elif chart_type == 'interactive':
                # インタラクティブチャートの分岐処理
                interactive_type = config.get('interactive_type', 'state_transition')
                
                if interactive_type == 'state_transition':
                    chart_path = self.chart_gen.create_state_transition_chart(
                        data, config, filename, output_dir
                    )
                elif interactive_type == 'dropdown_filter':
                    chart_path = self.chart_gen.create_dropdown_filter_chart(
                        data, config, filename, output_dir
                    )
                elif interactive_type == 'slider':
                    chart_path = self.chart_gen.create_slider_chart(
                        data, config, filename, output_dir
                    )
                elif interactive_type == 'hover_details':
                    chart_path = self.chart_gen.create_hover_details_chart(
                        data, config, filename, output_dir
                    )
                else:
                    logger.warning(f"サポートされていないインタラクティブタイプ: {interactive_type}")
                    
            else:
                logger.warning(f"サポートされていないチャートタイプ: {chart_type}")
                    
            # 図表が正常に生成された場合の共通処理（アニメーション以外）
            if chart_path is not None:
                # キャプションの追加
                caption = chart_config.get('caption', '')
                if caption:
                    self.doc_builder.add_paragraph(f"**{caption}**")
                
                # iframeタグの生成と埋め込み
                relative_path = Path("../../charts") / chart_path.name
                self.doc_builder.add_html_component_reference(
                    relative_path,
                    '100%',  # 幅は100%
                    None     # 高さは自動調整
                )
                
                logger.debug(f"図表埋め込み成功: {chart_path.name}")
            else:
                logger.error(f"図表生成失敗 - タイプ: {chart_type}, 設定: {config}")
                    
        except Exception as e:
            logger.error(f"図表処理中にエラーが発生しました: {e}")

    def _process_table(self, table_config: Dict[str, Any], output_dir: Path):
        """
        表設定を処理して生成・埋め込み
        全ての表タイプに対応
        
        Args:
            table_config: 表の設定
            output_dir: 出力ディレクトリ
        """
        table_type = table_config.get('table_type', 'basic')
        title = table_config.get('title', '')
        table_path = None
        
        try:
            # ファイル名の正規化
            filename = table_config.get('filename', f'{table_type}_table')
            if not filename.endswith('.html'):
                filename += '.html'
            
            # カスタムスタイルの取得
            custom_styles = table_config.get('custom_styles', None)
            
            if table_type == 'basic':
                # 基本的な表
                headers = table_config.get('headers', [])
                rows = table_config.get('rows', [])
                
                table_path = self.table_gen.create_basic_table(
                    headers, rows, title, filename, 
                    custom_styles, output_dir=output_dir
                )
                
            elif table_type == 'comparison':
                # 比較表
                categories = table_config.get('categories', [])
                items = table_config.get('items', [])
                data = table_config.get('data', [])
                
                table_path = self.table_gen.create_comparison_table(
                    categories, items, data, title, filename,
                    custom_styles, output_dir=output_dir
                )
                
            elif table_type == 'wide':
                # 幅広表（横スクロール対応）
                headers = table_config.get('headers', [])
                rows = table_config.get('rows', [])
                
                # 幅広表用のカスタムスタイルを自動設定
                wide_styles = custom_styles or {}
                wide_styles.update({
                    'table_layout': 'auto',
                    'overflow_x': 'auto'
                })
                
                table_path = self.table_gen.create_basic_table(
                    headers, rows, title, filename,
                    wide_styles, output_dir=output_dir
                )
                
            elif table_type == 'styled':
                # スタイル付き表（カスタムスタイル重視）
                headers = table_config.get('headers', [])
                rows = table_config.get('rows', [])
                
                table_path = self.table_gen.create_basic_table(
                    headers, rows, title, filename,
                    custom_styles, output_dir=output_dir
                )
                
            else:
                logger.warning(f"サポートされていない表タイプ: {table_type}")
                
            # 表が正常に生成された場合の共通処理
            if table_path is not None:
                # キャプションの追加
                caption = table_config.get('caption', '')
                if caption:
                    self.doc_builder.add_paragraph(f"**{caption}**")
                
                # iframeタグの生成と埋め込み
                # documentsフォルダから2階層上がってtablesフォルダへの相対パス
                relative_path = Path("../..") / "tables" / table_path.name
                self.doc_builder.add_html_component_reference(
                    relative_path,
                    '100%',  # 幅は100%
                    None     # 高さは自動調整
                )
                
                logger.debug(f"表埋め込み成功: {table_path.name}")
            else:
                logger.error(f"表生成失敗 - タイプ: {table_type}, 設定: {table_config}")
                section_title = table_config.get('caption', '不明なセクション')
                logger.error(f"セクション「{section_title}」の表が生成されませんでした")
                
        except Exception as e:
            logger.error(f"表処理中にエラーが発生しました: {e}")
            logger.error(f"表タイプ: {table_type}, 設定: {table_config}")
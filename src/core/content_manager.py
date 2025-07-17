"""
Content manager for MkDocs Materials Generator
学習資料のコンテンツ生成を管理する基底クラス
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from abc import ABC, abstractmethod
from jinja2 import Environment, FileSystemLoader, DictLoader

from .document_builder import DocumentBuilder
from .chart_generator import ChartGenerator
from .table_generator import TableGenerator
from .knowledge_manager import KnowledgeManager, Term
from .config import GLOBAL_COLORS, PATHS
from .base_config import BASE_CHART_STYLES, BASE_TABLE_STYLES

logger = logging.getLogger(__name__)


class BaseContentManager(ABC):
    """
    学習資料のコンテンツ生成を管理する基底クラス
    """
    
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
            material_name: 資料名
            output_base_dir: 出力ベースディレクトリ
            colors: カスタムカラー辞書
            chart_styles: カスタム図表スタイル辞書
            table_styles: カスタム表スタイル辞書
        """
        self.material_name = material_name
        self.output_base_dir = Path(output_base_dir)
        self.colors = colors or GLOBAL_COLORS
        self.chart_styles = {**BASE_CHART_STYLES, **(chart_styles or {})}
        self.table_styles = {**BASE_TABLE_STYLES, **(table_styles or {})}
        
        # 各ジェネレータとマネージャを初期化
        self.doc_builder = DocumentBuilder(self.output_base_dir)
        self.chart_generator = ChartGenerator(self.colors, self.chart_styles)
        self.table_generator = TableGenerator(self.colors, self.table_styles)
        self.knowledge_manager = KnowledgeManager(self.output_base_dir)
        
        # Jinja2環境を初期化
        self.jinja_env = Environment(
            loader=DictLoader({}),
            autoescape=True,
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # カスタムフィルタを追加
        self.jinja_env.filters['slugify'] = self._slugify_filter
        
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    def _slugify_filter(self, text: str) -> str:
        """
        Jinja2用のslugifyフィルタ
        
        Args:
            text: 変換対象のテキスト
            
        Returns:
            スラッグ化されたテキスト
        """
        from .utils import slugify
        return slugify(text)
    
    def _register_material_terms(self, terms_list: List[Term]) -> None:
        """
        KnowledgeManagerへの用語一括登録ヘルパー
        
        Args:
            terms_list: 用語オブジェクトのリスト
        """
        try:
            self.knowledge_manager.register_terms_batch(terms_list)
            self.logger.info(f"Registered {len(terms_list)} terms for {self.material_name}")
        except Exception as e:
            self.logger.error(f"Failed to register terms: {e}")
            raise
    
    def _get_chapter_terms(self, chapter_title: str) -> Dict[str, Dict[str, str]]:
        """
        KnowledgeManagerから章ごとの用語情報を取得するヘルパー
        
        Args:
            chapter_title: 章タイトル
            
        Returns:
            章の用語辞書
        """
        return self.knowledge_manager.get_terms_for_chapter(chapter_title)
    
    def generate_glossary(self, filename: str = "glossary.md") -> Path:
        """
        用語集生成メソッド
        
        Args:
            filename: 出力ファイル名
            
        Returns:
            生成されたファイルのパス
        """
        try:
            return self.knowledge_manager.generate_glossary_markdown(filename)
        except Exception as e:
            self.logger.error(f"Failed to generate glossary: {e}")
            raise
    
    def _create_chapter_template(
        self, 
        chapter_info: Dict[str, Any], 
        chapter_func: Callable
    ) -> Path:
        """
        各章のコンテンツを生成し、Markdownファイルとして保存する共通ロジック
        
        Args:
            chapter_info: 章情報辞書
            chapter_func: 章生成関数
            
        Returns:
            生成されたファイルのパス
        """
        try:
            # 章タイトルとスラッグを取得
            chapter_title = chapter_info.get("title", "無題")
            chapter_slug = chapter_info.get("slug", "untitled")
            chapter_number = chapter_info.get("number", 1)
            
            self.logger.info(f"Generating chapter: {chapter_title}")
            
            # 新しいDocumentBuilderインスタンスを作成
            doc_builder = DocumentBuilder(self.output_base_dir)
            
            # 章の用語を取得
            chapter_terms = self._get_chapter_terms(chapter_title)
            
            # Jinja2テンプレートの活用
            template_context = {
                "chapter_title": chapter_title,
                "chapter_number": chapter_number,
                "chapter_slug": chapter_slug,
                "material_name": self.material_name,
                "terms": chapter_terms,
                "colors": self.colors,
                "chart_styles": self.chart_styles,
                "table_styles": self.table_styles
            }
            
            # 章のメタデータを追加
            doc_builder.add_metadata({
                "title": chapter_title,
                "description": f"{self.material_name} - {chapter_title}",
                "chapter_number": chapter_number,
                "material": self.material_name
            })
            
            # 章のヘッダーを追加
            doc_builder.add_heading(f"第{chapter_number}章 {chapter_title}", 1)
            
            # 章の導入部分をテンプレートで生成
            if "introduction_template" in chapter_info:
                intro_template = self.jinja_env.from_string(chapter_info["introduction_template"])
                intro_content = intro_template.render(**template_context)
                doc_builder.add_raw_markdown(intro_content)
            
            # 章固有のコンテンツを生成
            chapter_func(doc_builder, chapter_info, template_context)
            
            # 章の終了部分をテンプレートで生成
            if "conclusion_template" in chapter_info:
                conclusion_template = self.jinja_env.from_string(chapter_info["conclusion_template"])
                conclusion_content = conclusion_template.render(**template_context)
                doc_builder.add_raw_markdown(conclusion_content)
            
            # 章のナビゲーションを追加
            self._add_chapter_navigation(doc_builder, chapter_info)
            
            # ファイル名を生成
            filename = f"chapter_{chapter_number:02d}_{chapter_slug}.md"
            
            # Markdownファイルを保存
            output_path = doc_builder.save_markdown(filename)
            
            self.logger.info(f"Chapter generated: {output_path}")
            
            return output_path
            
        except Exception as e:
            self.logger.error(f"Failed to create chapter template: {e}")
            raise
    
    def _add_chapter_navigation(self, doc_builder: DocumentBuilder, chapter_info: Dict[str, Any]) -> None:
        """
        章のナビゲーションを追加
        
        Args:
            doc_builder: DocumentBuilderインスタンス
            chapter_info: 章情報辞書
        """
        try:
            # 水平線で区切り
            doc_builder.add_horizontal_rule()
            
            # ナビゲーションセクション
            navigation_links = []
            
            # 前の章へのリンク
            if "previous_chapter" in chapter_info:
                prev_chapter = chapter_info["previous_chapter"]
                prev_filename = f"chapter_{prev_chapter['number']:02d}_{prev_chapter['slug']}.md"
                navigation_links.append(f"[← 前の章: {prev_chapter['title']}]({prev_filename})")
            
            # 目次へのリンク
            navigation_links.append("[📚 目次](index.md)")
            
            # 用語集へのリンク
            navigation_links.append("[📖 用語集](glossary.md)")
            
            # 次の章へのリンク
            if "next_chapter" in chapter_info:
                next_chapter = chapter_info["next_chapter"]
                next_filename = f"chapter_{next_chapter['number']:02d}_{next_chapter['slug']}.md"
                navigation_links.append(f"[次の章: {next_chapter['title']} →]({next_filename})")
            
            # ナビゲーションを表示
            if navigation_links:
                doc_builder.add_paragraph(" | ".join(navigation_links))
            
            # 章の情報を表示
            chapter_info_content = f"""
                                    **章番号**: {chapter_info.get('number', 1)}  
                                    **所要時間**: {chapter_info.get('estimated_time', '不明')}  
                                    **難易度**: {chapter_info.get('difficulty', '不明')}
                                    """
                                            
            doc_builder.add_admonition(
                "info",
                "章の情報",
                chapter_info_content
            )
        
        except Exception as e:
            self.logger.error(f"Failed to add chapter navigation: {e}")    
            
    def _create_index_page(self, chapters_info: List[Dict[str, Any]]) -> Path:
        """
        インデックスページを生成
        
        Args:
            chapters_info: 章情報のリスト
            
        Returns:
            生成されたファイルのパス
        """
        try:
            doc_builder = DocumentBuilder(self.output_base_dir)
            
            # メタデータを追加
            doc_builder.add_metadata({
                "title": self.material_name,
                "description": f"{self.material_name}の学習資料",
                "material": self.material_name
            })
            
            # タイトルを追加
            doc_builder.add_heading(self.material_name, 1)
            
            # 資料の概要
            doc_builder.add_paragraph(f"この資料は{self.material_name}に関する学習資料です。")
            
            # 統計情報
            stats = self.knowledge_manager.get_term_statistics()
            stats_content = f"""
**総章数**: {len(chapters_info)}章  
**専門用語数**: {stats['total_terms']}語  
**カテゴリ数**: {len(stats['categories'])}カテゴリ
"""
            
            doc_builder.add_admonition("info", "資料統計", stats_content)
            
            # 目次を追加
            doc_builder.add_heading("目次", 2)
            
            chapter_links = []
            for chapter_info in chapters_info:
                chapter_title = chapter_info.get("title", "無題")
                chapter_slug = chapter_info.get("slug", "untitled")
                chapter_number = chapter_info.get("number", 1)
                estimated_time = chapter_info.get("estimated_time", "不明")
                difficulty = chapter_info.get("difficulty", "不明")
                
                chapter_links.append(
                    f"[第{chapter_number}章: {chapter_title}](chapter_{chapter_number:02d}_{chapter_slug}.md) "
                    f"(所要時間: {estimated_time}, 難易度: {difficulty})"
                )
            
            doc_builder.add_ordered_list(chapter_links)
            
            # 用語集へのリンク
            doc_builder.add_heading("参考資料", 2)
            doc_builder.add_unordered_list([
                "[📖 用語集](glossary.md) - 専門用語の定義集"
            ])
            
            # 学習の進め方
            learning_guide = """
この資料を効果的に学習するために、以下の点に注意してください：

1. **順序立てて学習** - 各章は前の章の内容を前提としています
2. **用語の確認** - 分からない用語は用語集で確認してください  
3. **実習の実施** - 各章の実習問題に取り組んでください
4. **復習の重要性** - 定期的に前の章を復習してください
"""
            
            doc_builder.add_admonition("tip", "学習の進め方", learning_guide)
            
            # ファイルを保存
            output_path = doc_builder.save_markdown("index.md")
            
            self.logger.info(f"Index page generated: {output_path}")
            
            return output_path
            
        except Exception as e:
            self.logger.error(f"Failed to create index page: {e}")
            raise
    
    def create_template_from_string(self, template_string: str) -> Any:
        """
        文字列からJinja2テンプレートを作成
        
        Args:
            template_string: テンプレート文字列
            
        Returns:
            Jinja2テンプレートオブジェクト
        """
        return self.jinja_env.from_string(template_string)
    
    def render_template(self, template_string: str, context: Dict[str, Any]) -> str:
        """
        テンプレートをレンダリング
        
        Args:
            template_string: テンプレート文字列
            context: テンプレートコンテキスト
            
        Returns:
            レンダリング結果
        """
        template = self.create_template_from_string(template_string)
        return template.render(**context)
    
    def get_material_statistics(self) -> Dict[str, Any]:
        """
        資料の統計情報を取得
        
        Returns:
            統計情報辞書
        """
        return {
            "material_name": self.material_name,
            "knowledge_stats": self.knowledge_manager.get_term_statistics(),
            "colors": self.colors,
            "chart_styles": self.chart_styles,
            "table_styles": self.table_styles
        }
    
    @abstractmethod
    def generate_content(self) -> List[Path]:
        """
        資料全体のコンテンツ生成フロー（抽象メソッド）
        
        Returns:
            生成されたファイルのパスリスト
        """
        raise NotImplementedError("Subclasses must implement generate_content method")
    
    def validate_content(self) -> List[str]:
        """
        コンテンツの妥当性を検証
        
        Returns:
            検証エラーのリスト
        """
        errors = []
        
        # 用語の妥当性を検証
        term_errors = self.knowledge_manager.validate_terms()
        errors.extend(term_errors)
        
        # 出力ディレクトリの存在確認
        if not self.output_base_dir.exists():
            errors.append(f"Output directory does not exist: {self.output_base_dir}")
        
        return errors
    
    def cleanup_generated_files(self) -> None:
        """
        生成されたファイルをクリーンアップ
        """
        try:
            # 生成されたMarkdownファイルを削除
            for md_file in self.output_base_dir.glob("*.md"):
                md_file.unlink()
                self.logger.info(f"Deleted: {md_file}")
            
            # 生成されたHTMLファイルを削除
            charts_dir = PATHS["charts_dir"]
            tables_dir = PATHS["tables_dir"]
            
            for html_file in charts_dir.glob("*.html"):
                html_file.unlink()
                self.logger.info(f"Deleted: {html_file}")
            
            for html_file in tables_dir.glob("*.html"):
                html_file.unlink()
                self.logger.info(f"Deleted: {html_file}")
            
            self.logger.info("Cleanup completed")
            
        except Exception as e:
            self.logger.error(f"Failed to cleanup files: {e}")
            raise
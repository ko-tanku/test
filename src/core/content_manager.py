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
from .config import GLOBAL_COLORS, PATHS, FILE_NAMING_PATTERNS
from .base_config import BASE_CHART_STYLES, BASE_TABLE_STYLES
from .utils import slugify

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
            chapter_func: 章のコンテンツを生成する関数

        Returns:
            生成されたファイルのパス
        """
        try:
            # DocumentBuilderを新規作成
            doc_builder = DocumentBuilder(self.output_base_dir)

            # メタデータを追加
            metadata = {
                "title": chapter_info.get("title", "無題"),
                "description": f"{self.material_name} - {chapter_info.get('title', '無題')}",
                "chapter_number": chapter_info.get("number", 1),
                "material": self.material_name
            }
            doc_builder.add_metadata(metadata)

            # 章タイトル
            doc_builder.add_heading(f"第{chapter_info.get('number', 1)}章 {chapter_info.get('title', '無題')}", 1)

            # イントロダクション（テンプレートがあれば使用）
            if 'introduction_template' in chapter_info:
                intro_text = self.render_template(
                    chapter_info['introduction_template'],
                    {"chapter": chapter_info, "material": self.material_name}
                )
                doc_builder.add_raw_markdown(intro_text)

            # 章の専門用語を取得
            chapter_terms = self._get_chapter_terms(chapter_info.get("title", ""))

            # コンテキストを準備
            context = {
                "chapter_info": chapter_info,
                "material_name": self.material_name,
                "terms": chapter_terms,
                "colors": self.colors
            }

            # 章固有のコンテンツを生成
            chapter_func(doc_builder, chapter_info, context)

            # 結論（テンプレートがあれば使用）
            if 'conclusion_template' in chapter_info:
                conclusion_text = self.render_template(
                    chapter_info['conclusion_template'],
                    {"chapter": chapter_info, "material": self.material_name}
                )
                doc_builder.add_raw_markdown(conclusion_text)

            # ナビゲーション
            doc_builder.add_horizontal_rule()
            nav_links = []
            nav_links.append("[📚 目次](index.md)")
            nav_links.append("[📖 用語集](glossary.md)")

            # 前章・次章のリンク
            chapter_num = chapter_info.get("number", 1)
            if chapter_num > 1:
                nav_links.append(f"[← 前の章](chapter_{chapter_num-1:02d}_*.md)")
            if 'next_chapter' in chapter_info:
                next_num = chapter_info['next_chapter']['number']
                next_slug = slugify(chapter_info['next_chapter']['title'])
                nav_links.append(f"[次の章: {chapter_info['next_chapter']['title']} →](chapter_{next_num:02d}_{next_slug}.md)")

            doc_builder.add_paragraph(" | ".join(nav_links))

            # 章の情報ボックス
            chapter_stats = f"""
                            **章番号**: {chapter_info.get('number', 1)}
                            **所要時間**: {chapter_info.get('estimated_time', '不明')}
                            **難易度**: {chapter_info.get('difficulty', '不明')}"""

            doc_builder.add_admonition("info", "章の情報", chapter_stats)

            # ファイル名を生成
            chapter_slug = slugify(chapter_info.get("title", "untitled"))
            filename = FILE_NAMING_PATTERNS["md_chapter"].format(
                chapter_num=chapter_info.get("number", 1),
                chapter_slug=chapter_slug
            )

            # 保存
            output_path = doc_builder.save_markdown(filename)

            self.logger.info(f"Chapter {chapter_info.get('number', 1)} generated: {output_path}")

            return output_path

        except Exception as e:
            self.logger.error(f"Failed to create chapter template: {e}")
            raise

    def create_index_page(self, chapters_info: List[Dict[str, Any]]) -> Path:
        """
        目次ページを生成

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
                chapter_slug = slugify(chapter_title)
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
            # 学習の進め方（続き）
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

        # 必須ファイルの存在確認
        required_files = ["index.md", "glossary.md"]
        for filename in required_files:
            file_path = self.output_base_dir / filename
            if not file_path.exists():
                errors.append(f"Required file missing: {filename}")

        return errors

    def cleanup_output_directory(self) -> None:
        """
        出力ディレクトリをクリーンアップ
        """
        try:
            if self.output_base_dir.exists():
                import shutil
                # 既存のMarkdownファイルを削除
                for md_file in self.output_base_dir.glob("*.md"):
                    md_file.unlink()

                self.logger.info(f"Cleaned up output directory: {self.output_base_dir}")
        except Exception as e:
            self.logger.error(f"Failed to cleanup output directory: {e}")
            raise
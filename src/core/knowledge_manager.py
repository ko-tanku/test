"""
Knowledge manager for MkDocs Materials Generator
専門用語を一元的に管理し、用語集を生成するためのクラス
"""

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Any

from .utils import slugify, ensure_directory_exists, safe_filename
from .document_builder import DocumentBuilder

logger = logging.getLogger(__name__)


@dataclass
class Term:
    """
    専門用語を表すデータクラス
    """
    term: str
    definition: str
    category: str = "一般"
    related_terms: List[str] = None
    first_chapter: Optional[str] = None
    slug: Optional[str] = None
    
    def __post_init__(self):
        if self.related_terms is None:
            self.related_terms = []
        if self.slug is None:
            self.slug = slugify(self.term)


class KnowledgeManager:
    """
    専門用語を一元的に管理するクラス
    """
    
    def __init__(self, output_dir: Path):
        """
        初期化
        
        Args:
            output_dir: 用語集Markdown出力先のベースディレクトリ
        """
        self.output_dir = ensure_directory_exists(output_dir)
        self.terms: Dict[str, Term] = {}
        self.categories: Dict[str, List[str]] = {}
        self.logger = logging.getLogger(__name__ + ".KnowledgeManager")
    
    def register_term(self, term_obj: Term) -> None:
        """
        用語を登録
        
        Args:
            term_obj: 用語オブジェクト
        """
        try:
            # 用語を辞書に追加
            self.terms[term_obj.term] = term_obj
            
            # カテゴリーごとの用語リストを更新
            if term_obj.category not in self.categories:
                self.categories[term_obj.category] = []
            
            if term_obj.term not in self.categories[term_obj.category]:
                self.categories[term_obj.category].append(term_obj.term)
            
            self.logger.info(f"Term registered: {term_obj.term} ({term_obj.category})")
            
        except Exception as e:
            self.logger.error(f"Failed to register term '{term_obj.term}': {e}")
            raise
    
    def register_terms_batch(self, term_list: List[Term]) -> None:
        """
        用語を一括登録
        
        Args:
            term_list: 用語オブジェクトのリスト
        """
        for term_obj in term_list:
            self.register_term(term_obj)
    
    def get_term_definition(self, term_name: str) -> Optional[str]:
        """
        用語の定義を取得
        
        Args:
            term_name: 用語名
            
        Returns:
            用語の定義（存在しない場合はNone）
        """
        if term_name in self.terms:
            return self.terms[term_name].definition
        return None
    
    def get_all_terms(self) -> List[Term]:
        """
        全用語を取得
        
        Returns:
            全用語のリスト
        """
        return list(self.terms.values())
    
    def get_terms_by_category(self, category: str) -> List[Term]:
        """
        カテゴリ別の用語を取得
        
        Args:
            category: カテゴリ名
            
        Returns:
            指定カテゴリの用語リスト
        """
        if category not in self.categories:
            return []
        
        return [self.terms[term_name] for term_name in self.categories[category]]
    
    def get_terms_for_chapter(self, chapter_title: str) -> Dict[str, Dict[str, str]]:
        """
        特定の章で使用される用語を取得
        
        Args:
            chapter_title: 章タイトル
            
        Returns:
            用語辞書 {"用語": {"tooltip_text": "定義"}}
        """
        chapter_terms = {}
        
        for term_name, term_obj in self.terms.items():
            # 章で初出する用語、または関連する用語を含める
            if (term_obj.first_chapter == chapter_title or 
                chapter_title in term_obj.related_terms or
                term_obj.first_chapter is None):
                
                chapter_terms[term_name] = {
                    "tooltip_text": term_obj.definition
                }
        
        return chapter_terms
    
    def search_terms(self, query: str) -> List[Term]:
        """
        用語を検索
        
        Args:
            query: 検索クエリ
            
        Returns:
            検索結果の用語リスト
        """
        query_lower = query.lower()
        results = []
        
        for term_obj in self.terms.values():
            if (query_lower in term_obj.term.lower() or 
                query_lower in term_obj.definition.lower() or
                query_lower in term_obj.category.lower()):
                results.append(term_obj)
        
        return results
    
    def get_related_terms(self, term_name: str) -> List[Term]:
        """
        関連用語を取得
        
        Args:
            term_name: 基準となる用語名
            
        Returns:
            関連用語のリスト
        """
        if term_name not in self.terms:
            return []
        
        term_obj = self.terms[term_name]
        related_terms = []
        
        for related_term_name in term_obj.related_terms:
            if related_term_name in self.terms:
                related_terms.append(self.terms[related_term_name])
        
        return related_terms
    
    def generate_glossary_markdown(self, filename: str = "glossary.md") -> Path:
        """
        用語集Markdownファイルを生成
        
        Args:
            filename: 出力ファイル名
            
        Returns:
            生成されたファイルのパス
        """
        try:
            # DocumentBuilderを初期化
            doc_builder = DocumentBuilder(self.output_dir)
            
            # メタデータを追加
            doc_builder.add_metadata({
                "title": "用語集",
                "description": "学習資料で使用される専門用語の定義集"
            })
            
            # タイトルを追加
            doc_builder.add_heading("用語集", 1)
            doc_builder.add_paragraph("この用語集は学習資料で使用される専門用語の定義をまとめたものです。")
            
            # 統計情報を追加
            total_terms = len(self.terms)
            total_categories = len(self.categories)
            
            doc_builder.add_admonition(
                "info",
                "用語集統計",
                f"**総用語数**: {total_terms}語  \n**カテゴリ数**: {total_categories}カテゴリ"
            )
            
            # カテゴリ別に用語を整理
            sorted_categories = sorted(self.categories.keys())
            
            for category in sorted_categories:
                doc_builder.add_heading(category, 2)
                
                # カテゴリ内の用語をソート
                category_terms = sorted(self.categories[category])
                
                for term_name in category_terms:
                    term_obj = self.terms[term_name]
                    
                    # 用語名（アンカー付き）
                    doc_builder.add_heading(term_name, 3)
                    doc_builder.add_raw_markdown(f'<a id="{term_obj.slug}"></a>')
                    
                    # 定義
                    doc_builder.add_paragraph(term_obj.definition)
                    
                    # 初出章を表示
                    if term_obj.first_chapter:
                        doc_builder.add_paragraph(f"**初出章**: {term_obj.first_chapter}")
                    
                    # 関連用語を表示
                    if term_obj.related_terms:
                        related_links = []
                        for related_term in term_obj.related_terms:
                            if related_term in self.terms:
                                related_term_obj = self.terms[related_term]
                                related_links.append(f"[{related_term}](#{related_term_obj.slug})")
                        
                        if related_links:
                            doc_builder.add_paragraph(f"**関連用語**: {', '.join(related_links)}")
                    
                    # 水平線で区切り
                    doc_builder.add_horizontal_rule()
            
            # 索引を追加
            doc_builder.add_heading("索引", 2)
            doc_builder.add_paragraph("用語をアルファベット順に並べた索引です。")
            
            # 用語をアルファベット順にソート
            sorted_terms = sorted(self.terms.keys(), key=lambda x: x.lower())
            
            # 50音順索引を作成
            index_dict = {}
            for term_name in sorted_terms:
                first_char = term_name[0].upper()
                if first_char not in index_dict:
                    index_dict[first_char] = []
                index_dict[first_char].append(term_name)
            
            for char in sorted(index_dict.keys()):
                doc_builder.add_heading(char, 3)
                term_links = []
                for term_name in index_dict[char]:
                    term_obj = self.terms[term_name]
                    term_links.append(f"[{term_name}](#{term_obj.slug})")
                
                doc_builder.add_paragraph(" | ".join(term_links))
            
            # ファイルを保存
            output_path = doc_builder.save_markdown(filename)
            
            self.logger.info(f"Glossary generated: {output_path}")
            
            return output_path
            
        except Exception as e:
            self.logger.error(f"Failed to generate glossary: {e}")
            raise
    
    def export_terms_to_dict(self) -> Dict[str, Any]:
        """
        用語をDict形式でエクスポート
        
        Returns:
            用語辞書
        """
        export_dict = {
            "metadata": {
                "total_terms": len(self.terms),
                "categories": list(self.categories.keys())
            },
            "terms": {}
        }
        
        for term_name, term_obj in self.terms.items():
            export_dict["terms"][term_name] = {
                "definition": term_obj.definition,
                "category": term_obj.category,
                "related_terms": term_obj.related_terms,
                "first_chapter": term_obj.first_chapter,
                "slug": term_obj.slug
            }
        
        return export_dict
    
    def import_terms_from_dict(self, import_dict: Dict[str, Any]) -> None:
        """
        Dict形式から用語をインポート
        
        Args:
            import_dict: インポートする用語辞書
        """
        try:
            terms_data = import_dict.get("terms", {})
            
            for term_name, term_data in terms_data.items():
                term_obj = Term(
                    term=term_name,
                    definition=term_data.get("definition", ""),
                    category=term_data.get("category", "一般"),
                    related_terms=term_data.get("related_terms", []),
                    first_chapter=term_data.get("first_chapter"),
                    slug=term_data.get("slug")
                )
                
                self.register_term(term_obj)
            
            self.logger.info(f"Imported {len(terms_data)} terms")
           
        except Exception as e:
            self.logger.error(f"Failed to import terms: {e}")
            raise
    
    def validate_terms(self) -> List[str]:
        """
        用語の妥当性を検証
        
        Returns:
            検証エラーのリスト
        """
        errors = []
        
        for term_name, term_obj in self.terms.items():
            # 定義が空でないかチェック
            if not term_obj.definition.strip():
                errors.append(f"Term '{term_name}' has empty definition")
            
            # 関連用語が存在するかチェック
            for related_term in term_obj.related_terms:
                if related_term not in self.terms:
                    errors.append(f"Term '{term_name}' references non-existent related term '{related_term}'")
            
            # スラッグの重複チェック
            duplicate_slugs = []
            for other_term_name, other_term_obj in self.terms.items():
                if (term_name != other_term_name and 
                    term_obj.slug == other_term_obj.slug):
                    duplicate_slugs.append(other_term_name)
            
            if duplicate_slugs:
                errors.append(f"Term '{term_name}' has duplicate slug with: {', '.join(duplicate_slugs)}")
        
        return errors
    
    def get_term_statistics(self) -> Dict[str, Any]:
        """
        用語の統計情報を取得
        
        Returns:
            統計情報辞書
        """
        stats = {
            "total_terms": len(self.terms),
            "categories": {},
            "chapters": {},
            "average_definition_length": 0,
            "terms_with_related": 0
        }
        
        # カテゴリ別統計
        for category, terms in self.categories.items():
            stats["categories"][category] = len(terms)
        
        # 章別統計
        chapter_counts = {}
        definition_lengths = []
        related_count = 0
        
        for term_obj in self.terms.values():
            # 章別カウント
            if term_obj.first_chapter:
                if term_obj.first_chapter not in chapter_counts:
                    chapter_counts[term_obj.first_chapter] = 0
                chapter_counts[term_obj.first_chapter] += 1
            
            # 定義の長さ
            definition_lengths.append(len(term_obj.definition))
            
            # 関連用語を持つ用語の数
            if term_obj.related_terms:
                related_count += 1
        
        stats["chapters"] = chapter_counts
        stats["average_definition_length"] = sum(definition_lengths) / len(definition_lengths) if definition_lengths else 0
        stats["terms_with_related"] = related_count
        
        return stats
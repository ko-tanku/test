"""
専門用語を一元的に管理し、用語集やFAQ、TIPSを生成
"""

import logging
from pathlib import Path
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field

from .utils import slugify
from .config import FILE_NAMING_PATTERNS

logger = logging.getLogger(__name__)


@dataclass
class Term:
    """専門用語クラス"""
    term: str
    definition: str
    category: str
    related_terms: Optional[List[str]] = None
    first_chapter: Optional[str] = None
    context_snippets: Optional[List[str]] = None
    
    def __post_init__(self):
        """初期化後処理"""
        self.slug = slugify(self.term)
        if self.related_terms is None:
            self.related_terms = []
        if self.context_snippets is None:
            self.context_snippets = []


@dataclass
class FaqItem:
    """FAQ項目クラス"""
    question: str
    answer: str
    category: Optional[str] = None


@dataclass
class TipItem:
    """TIPS項目クラス"""
    title: str
    content: str
    category: Optional[str] = None


class KnowledgeManager:
    """知識管理クラス"""
    
    def __init__(self, output_dir: Path):
        """
        初期化
        
        Args:
            output_dir: 出力先ディレクトリ
        """
        self.output_dir = Path(output_dir)
        self.terms: Dict[str, Term] = {}
        self.faq_items: List[FaqItem] = []
        self.tip_items: List[TipItem] = []
        self.term_usage: Dict[str, List[Dict[str, str]]] = {}
        self.doc_builder = None
        
    def _get_doc_builder(self):
        """DocumentBuilderを遅延初期化で取得"""
        if self.doc_builder is None:
            from .document_builder import DocumentBuilder
            self.doc_builder = DocumentBuilder(self.output_dir)
        return self.doc_builder
        
    def register_term(self, term_obj: Term):
        """
        単一の専門用語を登録
        
        Args:
            term_obj: Termオブジェクト
        """
        if term_obj.term in self.terms:
            logger.warning(f"用語 '{term_obj.term}' は既に登録されています")
        self.terms[term_obj.term] = term_obj
        logger.debug(f"用語を登録しました: {term_obj.term}")
        
    def register_terms_batch(self, term_list: List[Term]):
        """
        複数の専門用語を一括登録
        
        Args:
            term_list: Termオブジェクトのリスト
        """
        for term_obj in term_list:
            self.register_term(term_obj)

    def register_faq_batch(self, faq_list: List[FaqItem]):
        """
        複数のFAQ項目を一括登録
        
        Args:
            faq_list: FaqItemオブジェクトのリスト
        """
        for faq_item in faq_list:
            self.register_faq_item(faq_item)

    def register_tips_batch(self, tip_list: List[TipItem]):
        """
        複数のTIPS項目を一括登録
        
        Args:
            tip_list: TipItemオブジェクトのリスト
        """
        for tip_item in tip_list:
            self.register_tip_item(tip_item)
            
    def register_faq_item(self, faq_item: FaqItem):
        """
        FAQ項目を登録
        
        Args:
            faq_item: FaqItemオブジェクト
        """
        self.faq_items.append(faq_item)
        logger.debug(f"FAQ項目を登録しました: {faq_item.question}")
        
    def register_tip_item(self, tip_item: TipItem):
        """
        TIPS項目を登録
        
        Args:
            tip_item: TipItemオブジェクト
        """
        self.tip_items.append(tip_item)
        logger.debug(f"TIPS項目を登録しました: {tip_item.title}")

    def record_term_usage(self, term_name: str, chapter_title: str, chapter_path: str, anchor_id: str):
        """
        用語の使用箇所を記録する

        Args:
            term_name: 用語名
            chapter_title: 章のタイトル
            chapter_path: 章のMarkdownファイルへのパス（docs/からの相対）
            anchor_id: 段落のアンカーID
        """
        if term_name not in self.term_usage:
            self.term_usage[term_name] = []
        
        self.term_usage[term_name].append({
            "title": chapter_title,
            "path": chapter_path,
            "anchor": anchor_id
        })
        logger.debug(f"用語の使用箇所を記録: {term_name} in {chapter_path}#{anchor_id}")
        
    def get_term_definition(self, term_name: str) -> Optional[str]:
        """
        指定された専門用語の定義を取得
        
        Args:
            term_name: 用語名
            
        Returns:
            定義文字列、見つからない場合はNone
        """
        term = self.terms.get(term_name)
        return term.definition if term else None
        
    def get_all_terms(self) -> List[Term]:
        """
        登録されている全ての用語を取得
        
        Returns:
            Termオブジェクトのリスト
        """
        return list(self.terms.values())
        
    def get_terms_for_chapter(self, chapter_title: str) -> Dict[str, Dict[str, str]]:
        """
        特定の章に関連する用語情報を取得
        
        Args:
            chapter_title: 章のタイトル
            
        Returns:
            用語情報の辞書 {用語: {"tooltip_text": "ツールチップ内容"}}
        """
        terms_info = {}
        
        for term_name, term_obj in self.terms.items():
            # 章に関連する用語かチェック
            if (term_obj.first_chapter == chapter_title or 
                chapter_title.lower() in term_obj.term.lower()):
                # ツールチップ用の短い説明を生成
                tooltip_text = term_obj.definition
                if len(tooltip_text) > 100:
                    tooltip_text = tooltip_text[:97] + "..."
                
                terms_info[term_name] = {
                    "tooltip_text": tooltip_text
                }
                
        return terms_info
        
    def generate_glossary_markdown(self) -> Path:
        """
        用語集Markdownファイルを生成
        
        Returns:
            生成されたファイルのパス
        """
        self._get_doc_builder().clear_content()
        
        # タイトル
        self._get_doc_builder().add_heading("用語集", 1)
        self._get_doc_builder().add_paragraph(
            "本資料で使用される専門用語の定義と説明をまとめています。"
        )
        
        # カテゴリごとに用語を整理
        categories = {}
        for term in self.terms.values():
            if term.category not in categories:
                categories[term.category] = []
            categories[term.category].append(term)
        
        # カテゴリごとに表示
        for category, terms in sorted(categories.items()):
            self._get_doc_builder().add_heading(category, 2)
            
            # 用語をアルファベット順にソート
            for term in sorted(terms, key=lambda t: t.term):
                # アンカーリンク
                self._get_doc_builder().add_raw_markdown(f'<a id="{term.slug}"></a>')
                
                # 用語名
                self._get_doc_builder().add_heading(term.term, 3)
                
                # 定義
                self._get_doc_builder().add_paragraph(f"**定義:** {term.definition}")
                
                # 初出章
                if term.first_chapter:
                    self._get_doc_builder().add_paragraph(
                        f"**初出章:** {term.first_chapter}"
                    )
                
                # 関連用語
                if term.related_terms:
                    related_links = []
                    for related in term.related_terms:
                        if related in self.terms:
                            related_slug = self.terms[related].slug
                            related_links.append(f"[{related}](#{related_slug})")
                        else:
                            related_links.append(related)
                    
                    self._get_doc_builder().add_paragraph(
                        f"**関連用語:** {', '.join(related_links)}"
                    )

                # 使用箇所の表示
                if term.term in self.term_usage:
                    usage_links = []
                    for usage in self.term_usage[term.term]:
                        # usage['path'] は docs/ からの相対パスを想定
                        path = Path(usage['path']).as_posix()
                        anchor = usage['anchor']
                        title = usage['title']
                        usage_links.append(f"[{title}]({path}#{anchor})")

                    if usage_links:
                        usage_text = ", ".join(usage_links)
                        self._get_doc_builder().add_paragraph(f"**使用箇所:** {usage_text}")
                
                # 文脈表示
                if term.context_snippets:
                    self._get_doc_builder().add_paragraph("**使用例:**")
                    for snippet in term.context_snippets[:3]:  # 最大3つまで
                        self._get_doc_builder().add_quote(snippet)
                
                # 区切り線
                self._get_doc_builder().add_horizontal_rule()
        
        # ファイル保存
        filename = FILE_NAMING_PATTERNS["md_glossary"]
        return self._get_doc_builder().save_markdown(filename)
        
    def generate_faq_markdown(self) -> Path:
        """
        FAQ Markdownファイルを生成
        
        Returns:
            生成されたファイルのパス
        """
        self._get_doc_builder().clear_content()
        
        # タイトル
        self._get_doc_builder().add_heading("よくある質問（FAQ）", 1)
        self._get_doc_builder().add_paragraph(
            "学習者からよく寄せられる質問とその回答をまとめています。"
        )
        
        # カテゴリごとに整理
        categories = {}
        uncategorized = []
        
        for faq in self.faq_items:
            if faq.category:
                if faq.category not in categories:
                    categories[faq.category] = []
                categories[faq.category].append(faq)
            else:
                uncategorized.append(faq)
        
        # カテゴリごとに表示
        for category, faqs in sorted(categories.items()):
            self._get_doc_builder().add_heading(category, 2)
            
            for faq in faqs:
                self._get_doc_builder().add_faq_item(
                    faq.question, 
                    faq.answer, 
                    collapsible=True
                )
        
        # カテゴリなしの項目
        if uncategorized:
            if categories:  # 他にカテゴリがある場合
                self._get_doc_builder().add_heading("その他", 2)
            
            for faq in uncategorized:
                self._get_doc_builder().add_faq_item(
                    faq.question, 
                    faq.answer, 
                    collapsible=True
                )
        
        # ファイル保存
        return self._get_doc_builder().save_markdown("faq.md")
        
    def generate_tips_markdown(self) -> Path:
        """
        TIPS Markdownファイルを生成
        
        Returns:
            生成されたファイルのパス
        """
        self._get_doc_builder().clear_content()
        
        # タイトル
        self._get_doc_builder().add_heading("学習のヒント（TIPS）", 1)
        self._get_doc_builder().add_paragraph(
            "効率的な学習のためのヒントやコツをまとめています。"
        )
        
        # カテゴリごとに整理
        categories = {}
        uncategorized = []
        
        for tip in self.tip_items:
            if tip.category:
                if tip.category not in categories:
                    categories[tip.category] = []
                categories[tip.category].append(tip)
            else:
                uncategorized.append(tip)
        
        # カテゴリごとに表示
        for category, tips in sorted(categories.items()):
            self._get_doc_builder().add_heading(category, 2)
            
            for tip in tips:
                self._get_doc_builder().add_tip_item(
                    tip.title,
                    tip.content,
                    collapsible=True
                )
        
        # カテゴリなしの項目
        if uncategorized:
            if categories:  # 他にカテゴリがある場合
                self._get_doc_builder().add_heading("その他", 2)
            
            for tip in uncategorized:
                self._get_doc_builder().add_tip_item(
                    tip.title,
                    tip.content,
                    collapsible=True
                )
        
        # ファイル保存
        return self._get_doc_builder().save_markdown("tips.md")

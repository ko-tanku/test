"""
Test Material Terms
テスト資料で使用する専門用語の定義
"""

from typing import List
import sys
from pathlib import Path

# プロジェクトルートをsys.pathに追加
project_root = Path(__file__).resolve().parents[3]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.core.knowledge_manager import Term

# テスト資料で使用する専門用語
TEST_MATERIAL_TERMS: List[Term] = [
    # システム関連用語
    Term(
        term="MkDocs",
        definition="Pythonで書かれた静的サイトジェネレータ。Markdownファイルから美しいドキュメントサイトを生成する。",
        category="システム",
        first_chapter="システムテスト概要",
        related_terms=["Markdown", "Material for MkDocs"]
    ),
    
    Term(
        term="Material for MkDocs",
        definition="MkDocsのテーマの一つ。Googleのマテリアルデザインに基づいた美しいドキュメントサイトを作成できる。",
        category="システム",
        first_chapter="システムテスト概要",
        related_terms=["MkDocs", "マテリアルデザイン"]
    ),
    
    Term(
        term="Markdown",
        definition="軽量マークアップ言語の一つ。プレーンテキストで書かれた文書をHTMLに変換する。",
        category="システム",
        first_chapter="システムテスト概要",
        related_terms=["HTML", "プレーンテキスト"]
    ),
    
    Term(
        term="DocumentBuilder",
        definition="Markdownコンテンツを構築するためのクラス。見出し、段落、リストなどの要素を生成する。",
        category="コンポーネント",
        first_chapter="システムテスト概要",
        related_terms=["Markdown", "コンテンツ生成"]
    ),
    
    # 図表関連用語
    Term(
        term="ChartGenerator",
        definition="様々な種類の図表を生成し、HTMLファイルとして出力するクラス。MatplotlibやPlotlyを使用する。",
        category="コンポーネント",
        first_chapter="図表生成テスト",
        related_terms=["Matplotlib", "Plotly", "図表"]
    ),
    
    Term(
        term="Matplotlib",
        definition="Pythonの描画ライブラリ。静的な図表を生成するために使用される。",
        category="ライブラリ",
        first_chapter="図表生成テスト",
        related_terms=["Python", "図表", "Seaborn"]
    ),
    
    Term(
        term="Plotly",
        definition="インタラクティブな図表を生成するためのライブラリ。ズームやホバーなどの機能を提供する。",
        category="ライブラリ",
        first_chapter="図表生成テスト",
        related_terms=["インタラクティブ", "図表", "JavaScript"]
    ),
    
    Term(
        term="Seaborn",
        definition="Matplotlibベースの統計データ可視化ライブラリ。美しい統計グラフを簡単に作成できる。",
        category="ライブラリ",
        first_chapter="図表生成テスト",
        related_terms=["Matplotlib", "統計", "可視化"]
    ),
    
    Term(
        term="折れ線グラフ",
        definition="データの変化を線で表したグラフ。時系列データの表示に適している。",
        category="図表",
        first_chapter="図表生成テスト",
        related_terms=["時系列", "データ可視化"]
    ),
    
    Term(
        term="棒グラフ",
        definition="データを棒の長さで表現するグラフ。カテゴリ別の比較に適している。",
        category="図表",
        first_chapter="図表生成テスト",
        related_terms=["比較", "カテゴリ"]
    ),
    
    Term(
        term="円グラフ",
        definition="データを円の扇形で表現するグラフ。全体に対する割合を示すのに適している。",
        category="図表",
        first_chapter="図表生成テスト",
        related_terms=["割合", "比率"]
    ),
    
    # 表関連用語
    Term(
        term="TableGenerator",
        definition="様々な形式の表データを生成し、HTMLファイルとして出力するクラス。",
        category="コンポーネント",
        first_chapter="表生成テスト",
        related_terms=["HTML", "テーブル", "データ"]
    ),
    
    Term(
        term="HTML",
        definition="HyperText Markup Language。Webページを作成するためのマークアップ言語。",
        category="技術",
        first_chapter="表生成テスト",
        related_terms=["Web", "マークアップ"]
    ),
    
    Term(
        term="CSS",
        definition="Cascading Style Sheets。HTMLの見た目を装飾するためのスタイルシート言語。",
        category="技術",
        first_chapter="表生成テスト",
        related_terms=["HTML", "スタイル"]
    ),
    
    Term(
        term="レスポンシブデザイン",
        definition="異なる画面サイズに対応して、レイアウトが自動調整されるデザイン手法。",
        category="技術",
        first_chapter="表生成テスト",
        related_terms=["モバイル", "デザイン"]
    ),
    
    Term(
        term="pandas",
        definition="Pythonのデータ分析ライブラリ。DataFrame構造を使ってデータを効率的に処理できる。",
        category="ライブラリ",
        first_chapter="表生成テスト",
        related_terms=["Python", "データ分析", "DataFrame"]
    ),
    
    # 用語管理関連用語
    Term(
        term="KnowledgeManager",
        definition="専門用語を一元的に管理し、用語集を生成するためのクラス。",
        category="コンポーネント",
        first_chapter="用語管理テスト",
        related_terms=["用語集", "専門用語"]
    ),
    
    Term(
        term="用語集",
        definition="専門用語とその定義をまとめた辞書的な資料。学習支援に重要な役割を果たす。",
        category="文書",
        first_chapter="用語管理テスト",
        related_terms=["専門用語", "辞書"]
    ),
    
    Term(
        term="ツールチップ",
        definition="マウスオーバーやタップ時に表示される小さなポップアップ。追加情報を提供する。",
        category="UI",
        first_chapter="用語管理テスト",
        related_terms=["UI", "ポップアップ"]
    ),
    
    Term(
        term="スラッグ",
        definition="URLやアンカーリンクで使用される文字列。特殊文字を除去し、ハイフンで区切られる。",
        category="技術",
        first_chapter="用語管理テスト",
        related_terms=["URL", "アンカー"]
    ),
    
    # 統合テスト関連用語
    Term(
        term="統合テスト",
        definition="複数のモジュールやコンポーネントを組み合わせて行うテスト。システム全体の動作を確認する。",
        category="テスト",
        first_chapter="統合テスト",
        related_terms=["モジュール", "システムテスト"]
    ),
    
    Term(
        term="単体テスト",
        definition="個別のモジュールや関数の動作を確認するテスト。最小単位でのテストを行う。",
        category="テスト",
        first_chapter="統合テスト",
        related_terms=["モジュール", "関数"]
    ),
    
    Term(
        term="パフォーマンステスト",
        definition="システムの性能や処理速度を測定するテスト。負荷テストも含む。",
        category="テスト",
        first_chapter="統合テスト",
        related_terms=["性能", "負荷"]
    ),
    
    Term(
        term="エラーハンドリング",
        definition="プログラム実行中に発生するエラーを適切に処理する仕組み。",
        category="技術",
        first_chapter="統合テスト",
        related_terms=["エラー", "例外処理"]
    ),
    
    # 技術共通用語
    Term(
        term="Python",
        definition="汎用プログラミング言語。読みやすく書きやすい構文が特徴。",
        category="プログラミング",
        first_chapter="システムテスト概要",
        related_terms=["プログラミング言語"]
    ),
    
    Term(
        term="JSON",
        definition="JavaScript Object Notation。データ交換形式の一つ。軽量で人間にも読みやすい。",
        category="技術",
        first_chapter="システムテスト概要",
        related_terms=["データ", "JavaScript"]
    ),
    
    Term(
        term="YAML",
        definition="YAML Ain't Markup Language。設定ファイルによく使われる人間が読みやすいデータ形式。",
        category="技術",
        first_chapter="システムテスト概要",
        related_terms=["設定", "データ形式"]
    ),
    
    Term(
        term="Base64",
        definition="バイナリデータをテキストで表現するためのエンコーディング方式。",
        category="技術",
        first_chapter="図表生成テスト",
        related_terms=["エンコーディング", "バイナリ"]
    ),
    
    Term(
        term="SVG",
        definition="Scalable Vector Graphics。ベクター形式の画像フォーマット。拡大縮小しても劣化しない。",
        category="技術",
        first_chapter="図表生成テスト",
        related_terms=["ベクター", "画像"]
    ),
    
    Term(
        term="JavaScript",
        definition="Webブラウザで動作するプログラミング言語。動的なWebページを作成できる。",
        category="プログラミング",
        first_chapter="図表生成テスト",
        related_terms=["Web", "ブラウザ"]
    ),
    
    Term(
        term="CDN",
        definition="Content Delivery Network。コンテンツを効率的に配信するためのネットワーク。",
        category="技術",
        first_chapter="図表生成テスト",
        related_terms=["ネットワーク", "配信"]
    ),
    
    Term(
        term="iframe",
        definition="HTMLで他のページを埋め込むためのタグ。外部コンテンツを表示できる。",
        category="技術",
        first_chapter="図表生成テスト",
        related_terms=["HTML", "埋め込み"]
    )
]

def get_test_terms() -> List[Term]:
    """
    テスト資料の専門用語リストを取得
    
    Returns:
        専門用語のリスト
    """
    return TEST_MATERIAL_TERMS

def get_terms_by_category(category: str) -> List[Term]:
    """
    カテゴリ別の専門用語を取得
    
    Args:
        category: カテゴリ名
        
    Returns:
        指定カテゴリの専門用語リスト
    """
    return [term for term in TEST_MATERIAL_TERMS if term.category == category]

def get_terms_by_chapter(chapter_title: str) -> List[Term]:
    """
    章別の専門用語を取得
    
    Args:
        chapter_title: 章タイトル
        
    Returns:
        指定章の専門用語リスト
    """
    return [term for term in TEST_MATERIAL_TERMS if term.first_chapter == chapter_title]

def get_all_categories() -> List[str]:
    """
    全カテゴリを取得
    
    Returns:
        カテゴリ名のリスト
    """
    return list(set(term.category for term in TEST_MATERIAL_TERMS))

def validate_terms() -> List[str]:
    """
    用語の妥当性を検証
    
    Returns:
        エラーメッセージのリスト
    """
    errors = []
    
    # 重複チェック
    term_names = [term.term for term in TEST_MATERIAL_TERMS]
    duplicates = [name for name in set(term_names) if term_names.count(name) > 1]
    if duplicates:
        errors.append(f"Duplicate terms found: {duplicates}")
    
    # 定義の存在チェック
    for term in TEST_MATERIAL_TERMS:
        if not term.definition.strip():
            errors.append(f"Empty definition for term: {term.term}")
    
    # 関連用語の存在チェック
    for term in TEST_MATERIAL_TERMS:
        for related_term in term.related_terms:
            if related_term not in term_names:
                errors.append(f"Related term '{related_term}' not found for term: {term.term}")
    
    return errors
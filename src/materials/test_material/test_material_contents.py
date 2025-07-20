"""
テスト資料のコンテンツ生成クラス
coreの全機能をテストするための具体的なコンテンツを生成
"""

import sys
from pathlib import Path
from typing import List, Dict, Any

# プロジェクトルートをsys.pathに追加
project_root = Path(__file__).resolve().parents[3]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.core.content_manager import BaseContentManager
from src.materials.test_material.test_material_config import (
    MATERIAL_CONFIG, TEST_MATERIAL_COLORS
)
from src.materials.test_material.test_material_terms import (
    TEST_TERMS, TEST_FAQ_ITEMS, TEST_TIP_ITEMS
)


class TestMaterialContentManager(BaseContentManager):
    """テスト資料のコンテンツ管理クラス"""
    
    def __init__(self, material_name: str, output_base_dir: Path):
        """初期化"""
        super().__init__(
            material_name=material_name,
            output_base_dir=output_base_dir,
            colors=TEST_MATERIAL_COLORS
        )
        
        # 専門用語、FAQ、TIPSを登録
        self._register_material_terms(TEST_TERMS)
        self._register_faq_tips(TEST_FAQ_ITEMS, TEST_TIP_ITEMS)
        
    def generate_content(self) -> List[Path]:
        """
        テスト資料の全コンテンツを生成
        
        Returns:
            生成されたMarkdownファイルのパスリスト
        """
        generated_files = []
        
        # 必要なディレクトリを作成
        docs_dir = self.output_base_dir / "documents"
        charts_dir = self.output_base_dir / "charts"
        tables_dir = self.output_base_dir / "tables"
        
        docs_dir.mkdir(parents=True, exist_ok=True)
        charts_dir.mkdir(parents=True, exist_ok=True)
        tables_dir.mkdir(parents=True, exist_ok=True)
        
        # テスト資料のトップページ生成
        self.doc_builder.output_dir = self.output_base_dir
        generated_files.append(self._generate_test_material_index())
        
        # 各章のコンテンツ生成
        self.doc_builder.output_dir = docs_dir
        
        # 第1章
        chapter1_data = self._create_chapter1()
        generated_files.append(self._generate_chapter_from_data(chapter1_data, "chapter01.md", charts_dir, tables_dir))
        
        # 第2章
        chapter2_data = self._create_chapter2()
        generated_files.append(self._generate_chapter_from_data(chapter2_data, "chapter02.md", charts_dir, tables_dir))
        
        # 第3章
        chapter3_data = self._create_chapter3()
        generated_files.append(self._generate_chapter_from_data(chapter3_data, "chapter03.md", charts_dir, tables_dir))
        
        # 第4章
        chapter4_data = self._create_chapter4()
        generated_files.append(self._generate_chapter_from_data(chapter4_data, "chapter04.md", charts_dir, tables_dir))
        
        # 用語集、FAQ、TIPSページ生成（test_material内）
        self.doc_builder.output_dir = self.output_base_dir
        generated_files.append(self.generate_glossary())
        generated_files.append(self.generate_faq_page())
        generated_files.append(self.generate_tips_page())
        
        return generated_files
        
    def _generate_test_material_index(self) -> Path:
        """テスト資料のトップページを生成"""
        self.doc_builder.clear_content()
        
        self.doc_builder.add_heading(MATERIAL_CONFIG["title"], 1)
        self.doc_builder.add_paragraph(MATERIAL_CONFIG["description"])
        
        self.doc_builder.add_heading("学習目標", 2)
        self.doc_builder.add_unordered_list(MATERIAL_CONFIG["learning_objectives"])
        
        self.doc_builder.add_heading("対象読者", 2)
        self.doc_builder.add_paragraph(MATERIAL_CONFIG["target_audience"])
        
        self.doc_builder.add_heading("章構成", 2)
        chapters = [
            "[第1章: MkDocs基本要素テスト](documents/chapter01/)",
            "[第2章: ツールチップ・用語集・レコメンデーションテスト](documents/chapter02/)",
            "[第3章: インタラクティブ図表・表テスト](documents/chapter03/)",
            "[第4章: 演習問題・FAQ・TIPSテスト](documents/chapter04/)"
        ]
        self.doc_builder.add_ordered_list(chapters)
        
        return self.doc_builder.save_markdown("index.md")
        
    def _generate_chapter_from_data(self, chapter_data: Dict[str, Any], filename: str, 
                                   charts_dir: Path, tables_dir: Path) -> Path:
        """
        章データからMarkdownを生成
        
        Args:
            chapter_data: 章のデータ辞書
            filename: 出力ファイル名
            charts_dir: 図表出力ディレクトリ
            tables_dir: 表出力ディレクトリ
            
        Returns:
            生成されたファイルのパス
        """
        self.doc_builder.clear_content()
        
        # タイトル
        self.doc_builder.add_heading(chapter_data.get('title', ''), 1)
        
        # 概要
        if 'overview' in chapter_data:
            self.doc_builder.add_paragraph(chapter_data['overview'])
            
        # セクション
        for section in chapter_data.get('sections', []):
            self.doc_builder.add_heading(section.get('title', ''), 2)
            
            # コンテンツリストを処理
            self._process_content_list(
                section.get('contents', []),
                charts_dir,
                tables_dir
            )
            
        # 演習問題
        if 'exercises' in chapter_data:
            self.doc_builder.add_heading("演習問題", 2)
            for exercise in chapter_data['exercises']:
                self._process_exercise(exercise)
                
        return self.doc_builder.save_markdown(filename)
        
    def _process_exercise(self, exercise: Dict[str, Any]):
        """演習問題を処理"""
        difficulty_map = {
            'easy': 'tip',
            'medium': 'question',
            'hard': 'warning'
        }
        
        difficulty = exercise.get('difficulty', 'medium')
        adm_type = difficulty_map.get(difficulty, 'question')
        
        content = f"**問題**: {exercise.get('question', '')}\n\n"
        if 'answer' in exercise:
            content += f"**解答**: {exercise.get('answer', '')}\n\n"
        if 'explanation' in exercise:
            content += f"**解説**: {exercise.get('explanation', '')}"
            
        self.doc_builder.add_admonition(
            adm_type,
            f"演習問題（{difficulty}）",
            content,
            collapsible=True
        )
        
    def _create_chapter1(self) -> Dict[str, Any]:
        """第1章のデータを作成"""
        return {
            'title': '第1章: MkDocs基本要素テスト',
            'overview': 'MkDocsの基本的なMarkdown要素とMkDocs Materialテーマの拡張機能をテストします。',
            'sections': [
                {
                    'title': '基本的なMarkdown要素',
                    'contents': [
                        {
                            'type': 'text',
                            'text': 'これは通常の段落です。**太字**や*斜体*、`インラインコード`を含むことができます。'
                        },
                        {
                            'type': 'heading',
                            'text': 'リスト',
                            'level': 3
                        },
                        {
                            'type': 'text',
                            'text': '順不同リスト:'
                        },
                        {
                            'type': 'list',
                            'list_type': 'unordered',
                            'items': ['項目1', '項目2', '入れ子の項目も可能']
                        },
                        {
                            'type': 'text',
                            'text': '順序付きリスト:'
                        },
                        {
                            'type': 'list',
                            'list_type': 'ordered',
                            'items': ['最初の項目', '2番目の項目', '3番目の項目']
                        }
                    ]
                },
                {
                    'title': 'Admonition（注記ブロック）',
                    'contents': [
                        {
                            'type': 'admonition',
                            'admonition_type': 'note',
                            'title': 'メモ',
                            'text': 'これは標準的なメモブロックです。',
                            'collapsible': False
                        },
                        {
                            'type': 'admonition',
                            'admonition_type': 'tip',
                            'title': 'ヒント',
                            'text': 'これは折りたたみ可能なヒントブロックです。',
                            'collapsible': True
                        }
                    ]
                },
                {
                    'title': 'コードブロック',
                    'contents': [
                        {
                            'type': 'code_with_output',
                            'code': 'def hello():\n    print("Hello, World!")\n\nhello()',
                            'output': 'Hello, World!',
                            'lang': 'python',
                            'output_label': '実行結果'
                        }
                    ]
                }
            ],
            'exercises': [
                {
                    'question': 'Markdownで見出しレベル2を書く方法は？',
                    'answer': '## 見出しテキスト',
                    'explanation': 'Markdownでは#の数で見出しレベルを表現します。',
                    'difficulty': 'easy'
                }
            ]
        }
        
    def _create_chapter2(self) -> Dict[str, Any]:
        """第2章のデータを作成"""
        terms = self._get_chapter_terms("第2章")
        
        return {
            'title': '第2章: ツールチップ・用語集・レコメンデーションテスト',
            'overview': 'ツールチップ機能と用語管理機能をテストします。',
            'sections': [
                {
                    'title': 'ツールチップ機能のテスト',
                    'contents': [
                        {
                            'type': 'text_with_tooltips',
                            'text': 'MkDocsでは、Markdownファイルから美しいドキュメントを生成できます。ツールチップ機能を使用すると、専門用語に説明を付与できます。',
                            'terms': terms
                        },
                        {
                            'type': 'recommendations',
                            'title': '関連資料',
                            'items': [
                                {'text': '第1章に戻る', 'link': 'chapter01/'},
                                {'text': '用語集を見る', 'link': '../glossary/'}
                            ]
                        }
                    ]
                }
            ]
        }
        
    def _create_chapter3(self) -> Dict[str, Any]:
        """第3章のデータを作成"""
        # サンプルデータ
        line_data = {
            'x': list(range(10)),
            'y': [x**2 for x in range(10)]
        }
        
        table_headers = ['項目', '説明', '重要度']
        table_rows = [
            ['MkDocs', '静的サイトジェネレータ', '高'],
            ['Markdown', '軽量マークアップ言語', '高']
        ]
        
        return {
            'title': '第3章: インタラクティブ図表・表テスト',
            'overview': '様々な種類の図表と表を表示します。',
            'sections': [
                {
                    'title': '図表のテスト',
                    'contents': [
                        {
                            'type': 'chart',
                            'chart_type': 'line',
                            'data': line_data,
                            'config': {
                                'x_col': 'x',
                                'y_col': 'y',
                                'title': '二次関数のグラフ',
                                'xlabel': 'X値',
                                'ylabel': 'Y値',
                                'filename': 'quadratic_function',
                                'use_plotly': False
                            },
                            'caption': '図3-1: y = x²のグラフ',
                            'width': 100,
                            'height': 500
                        }
                    ]
                },
                {
                    'title': '表のテスト',
                    'contents': [
                        {
                            'type': 'table',
                            'table_type': 'basic',
                            'headers': table_headers,
                            'rows': table_rows,
                            'title': '基本ツール一覧',
                            'filename': 'basic_tools',
                            'height': 300
                        }
                    ]
                }
            ]
        }
        
    def _create_chapter4(self) -> Dict[str, Any]:
        """第4章のデータを作成"""
        return {
            'title': '第4章: 演習問題・FAQ・TIPSテスト',
            'overview': 'インタラクティブな学習要素をテストします。',
            'sections': [
                {
                    'title': 'クイズ形式の演習',
                    'contents': [
                        {
                            'type': 'quiz',
                            'question_data': {
                                'question': 'MkDocsの設定ファイルの名前は？',
                                'options': ['config.yaml', 'mkdocs.yml', 'settings.json'],
                                'correct': 1,
                                'hint': 'YAMLファイルです',
                                'explanation': 'MkDocsはmkdocs.ymlを使用します'
                            }
                        }
                    ]
                },
                {
                    'title': '学習のまとめ',
                    'contents': [
                        {
                            'type': 'summary',
                            'title': '第4章の要点',
                            'points': [
                                'クイズ形式で理解度を確認できる',
                                'FAQで疑問を解決できる',
                                'TIPSで効率的な学習が可能'
                            ]
                        }
                    ]
                }
            ],
            'exercises': [
                {
                    'question': 'MkDocs Materialテーマの主な利点を3つ挙げてください',
                    'answer': '1. モダンなデザイン、2. 豊富な拡張機能、3. レスポンシブ対応',
                    'difficulty': 'medium'
                }
            ]
        }
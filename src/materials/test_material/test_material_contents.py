"""
テスト資料のコンテンツ生成クラス
IT・組み込み技術入門テーマで全機能をテスト
"""

import sys
from pathlib import Path
from typing import List, Dict, Any
import numpy as np
# プロジェクトルートをsys.pathに追加
project_root = Path(__file__).resolve().parents[3]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.core.content_manager import BaseContentManager
from src.materials.test_material.test_material_config import (
    MATERIAL_CONFIG, TEST_MATERIAL_COLORS
)
from src.materials.test_material.test_material_terms import (
    EMBEDDED_TERMS, EMBEDDED_FAQ_ITEMS, EMBEDDED_TIP_ITEMS
)
from src.materials.test_material.test_material_charts import create_all_test_charts
from src.materials.test_material.test_material_tables import create_all_test_tables


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
        self._register_material_terms(EMBEDDED_TERMS)
        self._register_faq_tips(EMBEDDED_FAQ_ITEMS, EMBEDDED_TIP_ITEMS)
        
    def generate_content(self) -> List[Path]:
        """
        テスト資料の全コンテンツを生成
        """
        generated_files = []
        
        # 必要なディレクトリを作成
        docs_dir = self.output_base_dir / "documents"
        charts_dir = self.output_base_dir / "charts"
        tables_dir = self.output_base_dir / "tables"
        docs_dir.mkdir(parents=True, exist_ok=True)
        charts_dir.mkdir(parents=True, exist_ok=True)
        tables_dir.mkdir(parents=True, exist_ok=True)
        
        # 図表と表を事前生成
        self.generated_charts = create_all_test_charts(self.chart_gen, charts_dir)
        self.generated_tables = create_all_test_tables(self.table_gen, tables_dir)
        
        # テスト資料のトップページ生成
        self.doc_builder.output_dir = self.output_base_dir
        generated_files.append(self._generate_test_material_index())
        
        # 各章のコンテンツ生成
        self.doc_builder.output_dir = docs_dir
        
        # 第1章
        chapter1_data = self._create_chapter1()
        generated_files.append(self._generate_chapter_from_data(
            chapter1_data, "chapter01.md", charts_dir, tables_dir
        ))
        
        # 第2章
        chapter2_data = self._create_chapter2()
        generated_files.append(self._generate_chapter_from_data(
            chapter2_data, "chapter02.md", charts_dir, tables_dir
        ))
        
        # 第3章
        chapter3_data = self._create_chapter3()
        generated_files.append(self._generate_chapter_from_data(
            chapter3_data, "chapter03.md", charts_dir, tables_dir
        ))
        
        # 第4章
        chapter4_data = self._create_chapter4()
        generated_files.append(self._generate_chapter_from_data(
            chapter4_data, "chapter04.md", charts_dir, tables_dir
        ))
        
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
            "[第1章: プログラミングの基礎](documents/chapter01.md)",
            "[第2章: 組み込みシステム入門](documents/chapter02.md)",
            "[第3章: ハードウェアとソフトウェア](documents/chapter03.md)",
            "[第4章: リアルタイムシステム](documents/chapter04.md)"
        ]
        self.doc_builder.add_ordered_list(chapters)
        
        self.doc_builder.add_heading("参考資料", 2)
        other_pages = [
            "[用語集](glossary.md)",
            "[よくある質問（FAQ）](faq.md)",
            "[学習のヒント（TIPS）](tips.md)"
        ]
        self.doc_builder.add_unordered_list(other_pages)
        
        return self.doc_builder.save_markdown("index.md")
        
    def _generate_chapter_from_data(self, chapter_data: Dict[str, Any], filename: str, 
                                   charts_dir: Path, tables_dir: Path) -> Path:
        """章データからMarkdownを生成"""
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
        """第1章: プログラミングの基礎"""
        return {
            'title': '第1章: プログラミングの基礎',
            'overview': 'プログラミングの基本概念を学び、様々なMarkdown要素をテストします。',
            'sections': [
                {
                    'title': 'プログラミングとは',
                    'contents': [
                        {
                            'type': 'text',
                            'text': 'プログラミングとは、コンピュータに対する**命令**を記述することです。'
                        },
                        {
                            'type': 'quote',
                            'text': 'プログラムとは、料理のレシピのようなもの。\n材料（データ）と手順（アルゴリズム）を組み合わせて、\n目的の結果を得るための指示書です。'
                        },
                        {
                            'type': 'horizontal_rule'
                        }
                    ]
                },
                {
                    'title': 'プログラミング言語の種類',
                    'contents': [
                        {
                            'type': 'tabs',
                            'tabs_data': {
                                'Python': '```python\n# Pythonの例\ndef hello():\n    print("Hello, World!")\n\nhello()\n```',
                                'C言語': '```c\n// C言語の例\n#include <stdio.h>\n\nint main() {\n    printf("Hello, World!\\n");\n    return 0;\n}\n```',
                                'JavaScript': '```javascript\n// JavaScriptの例\nfunction hello() {\n    console.log("Hello, World!");\n}\n\nhello();\n```'
                            }
                        },
                        {
                            'type': 'table',
                            'table_type': 'comparison',
                            'categories': ['Python', 'C言語', 'JavaScript'],
                            'items': ['用途', '実行速度', '学習難易度', '組み込み適性'],
                            'data': [
                                ['汎用・AI', '組み込み・OS', 'Web開発'],
                                ['遅い', '非常に速い', '中程度'],
                                ['簡単', '難しい', '中程度'],
                                ['△', '◎', '×']
                            ],
                            'title': 'プログラミング言語の比較',
                            'filename': 'language_comparison'
                        }
                    ]
                },
                {
                    'title': '基本的なプログラム構造',
                    'contents': [
                        {
                            'type': 'admonition',
                            'admonition_type': 'note',
                            'title': '重要な概念',
                            'text': 'すべてのプログラムは「順次」「分岐」「反復」の3つの基本構造で構成されます。',
                            'collapsible': False
                        },
                        {
                            'type': 'code_with_output',
                            'code': '# 順次処理の例\na = 10\nb = 20\nc = a + b\nprint(f"{a} + {b} = {c}")',
                            'output': '10 + 20 = 30',
                            'lang': 'python',
                            'output_label': '実行結果'
                        }
                    ]
                }
            ],
            'exercises': [
                {
                    'question': 'プログラミングの3つの基本構造を挙げてください。',
                    'answer': '順次・分岐・反復',
                    'explanation': 'これらの構造を組み合わせることで、どんな複雑なプログラムも作成できます。',
                    'difficulty': 'easy'
                }
            ]
        }
        
    def _create_chapter2(self) -> Dict[str, Any]:
        """第2章: 組み込みシステム入門"""
        terms = self._get_chapter_terms("第2章")
        
        return {
            'title': '第2章: 組み込みシステム入門',
            'overview': '組み込みシステムの基礎概念とツールチップ機能をテストします。',
            'sections': [
                {
                    'title': '組み込みシステムとは',
                    'contents': [
                        {
                            'type': 'text_with_tooltips',
                            'text': '組み込みシステムは、特定の機能を実現するために機器に組み込まれたコンピュータシステムです。マイコンやセンサー、アクチュエータなどで構成されます。',
                            'terms': terms
                        },
                        {
                            'type': 'list',
                            'list_type': 'unordered',
                            'items': [
                                '家電製品（洗濯機、電子レンジ、エアコン）',
                                '自動車（エンジン制御、ブレーキシステム）',
                                '医療機器（心電図モニター、人工呼吸器）',
                                '産業機器（ロボット、製造装置）'
                            ]
                        }
                    ]
                },
                {
                    'title': '組み込みシステムの特徴',
                    'contents': [
                        {
                            'type': 'table',
                            'table_type': 'basic',
                            'headers': ['特徴', '説明', '例'],
                            'rows': [
                                ['リアルタイム性', '決められた時間内に処理を完了', 'エアバッグの展開'],
                                ['省資源', '限られたメモリ・CPUで動作', 'マイコンは数KB〜数MB'],
                                ['高信頼性', '長時間の連続動作が必要', '24時間365日稼働'],
                                ['専用設計', '特定用途に最適化', '単機能で高効率']
                            ],
                            'title': '組み込みシステムの主要な特徴',
                            'filename': 'embedded_features'
                        },
                        {
                            'type': 'recommendations',
                            'title': '関連情報',
                            'items': [
                                {'text': '第4章でリアルタイムシステムを詳しく学ぶ', 'link': 'chapter04.md'},
                                {'text': '用語集で専門用語を確認', 'link': '../glossary.md'}
                            ]
                        }
                    ]
                }
            ]
        }
        
    def _create_chapter3(self) -> Dict[str, Any]:
        """第3章: ハードウェアとソフトウェア（全図表機能テスト）"""
        return {
            'title': '第3章: ハードウェアとソフトウェア',
            'overview': 'ハードウェアとソフトウェアの関係を、様々な図表を使って理解します。',
            'sections': [
                {
                    'title': 'CPUの性能推移',
                    'contents': [
                        {
                            'type': 'chart',
                            'chart_type': 'line',
                            'data': {
                                'year': [2010, 2012, 2014, 2016, 2018, 2020, 2022, 2024],
                                'performance': [100, 150, 200, 280, 350, 450, 550, 700]
                            },
                            'config': {
                                'x_col': 'year',
                                'y_col': 'performance',
                                'title': 'CPU性能の推移（相対値）',
                                'xlabel': '年',
                                'ylabel': '性能指数',
                                'filename': 'cpu_performance_trend',
                                'use_plotly': True
                            },
                            'caption': '図3-1: ムーアの法則に従うCPU性能の向上',
                            'width': 100,
                            'height': 450
                        }
                    ]
                },
                {
                    'title': 'メモリ階層',
                    'contents': [
                        {
                            'type': 'chart',
                            'chart_type': 'bar',
                            'data': {
                                'memory_type': ['レジスタ', 'L1キャッシュ', 'L2キャッシュ', 'メインメモリ', 'SSD', 'HDD'],
                                'access_time': [0.1, 1, 10, 100, 10000, 10000000]
                            },
                            'config': {
                                'x_col': 'memory_type',
                                'y_col': 'access_time',
                                'title': 'メモリ階層とアクセス時間（ナノ秒）',
                                'xlabel': 'メモリ種別',
                                'ylabel': 'アクセス時間（対数スケール）',
                                'filename': 'memory_hierarchy',
                                'use_plotly': True
                            },
                            'caption': '図3-2: メモリ階層による速度とコストのトレードオフ',
                            'width': 100,
                            'height': 450
                        }
                    ]
                },
                # {
                #     'title': '組み込みシステムの構成',
                #     'contents': [
                #         {
                #             'type': 'chart',
                #             'chart_type': 'custom',
                #             'data': None,
                #             'config': {
                #                 'plot_function': self._draw_embedded_system,
                #                 'title': '組み込みシステムの基本構成',
                #                 'filename': 'embedded_system_diagram'
                #             },
                #             'caption': '図3-3: 典型的な組み込みシステムの構成要素',
                #             'width': 100,
                #             'height': 450
                #         }
                #     ]
                # },
                {
                    'title': 'プロセッサの市場シェア',
                    'contents': [
                        {
                            'type': 'chart',
                            'chart_type': 'pie',
                            'data': {
                                'vendor': ['ARM', 'Intel', 'AMD', 'その他'],
                                'share': [45, 30, 15, 10]
                            },
                            'config': {
                                'values_col': 'share',
                                'labels_col': 'vendor',
                                'title': '組み込みプロセッサの市場シェア（2024年）',
                                'filename': 'processor_market_share',
                                'use_plotly': True
                            },
                            'caption': '図3-4: ARM社が組み込み市場をリード',
                            'width': 100,
                            'height': 450
                        }
                    ]
                },
                {
                    'title': 'インタラクティブなデータ分析',
                    'contents': [
                        {
                            'type': 'chart',
                            'chart_type': 'interactive',
                            'data': {
                                'states': [
                                    {'name': '通常時', 'x': ['CPU', 'メモリ', 'I/O'], 'y': [30, 20, 10]},
                                    {'name': 'ピーク時', 'x': ['CPU', 'メモリ', 'I/O'], 'y': [90, 60, 40]},
                                    {'name': 'アイドル時', 'x': ['CPU', 'メモリ', 'I/O'], 'y': [5, 10, 2]}
                                ]
                            },
                            'config': {
                                'interactive_type': 'state_transition',
                                'title': 'システムリソース使用率',
                                'xlabel': 'リソース',
                                'ylabel': '使用率（%）',
                                'filename': 'resource_usage_states'
                            },
                            'caption': '図3-5: ボタンクリックで状態を切り替え',
                            'width': 100,
                            'height': 450
                        }
                    ]
                },
                {
                    'title': '時系列データの分析',
                    'contents': [
                        {
                            'type': 'chart',
                            'chart_type': 'interactive',
                            'data': {
                                'datasets': {
                                    '2022年': {'x': ['Q1', 'Q2', 'Q3', 'Q4'], 'y': [100, 120, 115, 140]},
                                    '2023年': {'x': ['Q1', 'Q2', 'Q3', 'Q4'], 'y': [110, 135, 125, 155]},
                                    '2024年': {'x': ['Q1', 'Q2', 'Q3', 'Q4'], 'y': [120, 145, 140, 170]}
                                }
                            },
                            'config': {
                                'interactive_type': 'dropdown_filter',
                                'xlabel': '四半期',
                                'ylabel': '出荷台数（千台）',
                                'filename': 'quarterly_shipments'
                            },
                            'caption': '図3-6: ドロップダウンで年度を選択',
                            'width': 100,
                            'height': 450
                        }
                    ]
                },
                {
                    'title': 'パラメータ調整シミュレーション',
                    'contents': [
                        {
                            'type': 'chart',
                            'chart_type': 'interactive',
                            'data': {
                                'x': list(np.linspace(0, 2*np.pi, 100)),
                                'parameters': [
                                    {'name': '振幅0.5', 'function': lambda x: 0.5 * np.sin(x), 'label': '0.5'},
                                    {'name': '振幅1.0', 'function': lambda x: 1.0 * np.sin(x), 'label': '1.0'},
                                    {'name': '振幅1.5', 'function': lambda x: 1.5 * np.sin(x), 'label': '1.5'},
                                    {'name': '振幅2.0', 'function': lambda x: 2.0 * np.sin(x), 'label': '2.0'}
                                ]
                            },
                            'config': {
                                'interactive_type': 'slider',
                                'title': 'PWM信号の振幅調整',
                                'xlabel': '時間',
                                'ylabel': '電圧',
                                'slider_prefix': '振幅: ',
                                'filename': 'pwm_amplitude_slider'
                            },
                            'caption': '図3-7: スライダーで振幅を調整',
                            'width': 100,
                            'height': 450
                        }
                    ]
                },
                {
                    'title': 'センサーデータの詳細表示',
                    'contents': [
                        {
                            'type': 'chart',
                            'chart_type': 'interactive',
                            'data': {
                                'x': list(np.random.randn(50)),
                                'y': list(np.random.randn(50)),
                                'size': list(np.random.randint(10, 50, 50)),
                                'labels': [f'センサー{i+1}' for i in range(50)]
                            },
                            'config': {
                                'interactive_type': 'hover_details',
                                'title': 'センサー配置と測定値',
                                'xlabel': 'X座標',
                                'ylabel': 'Y座標',
                                'colorbar_title': '測定値',
                                'filename': 'sensor_placement_hover'
                            },
                            'caption': '図3-8: マウスホバーで詳細情報を表示',
                            'width': 100,
                            'height': 450
                        }
                    ]
                },
            ]
        }
        
    def _create_chapter4(self) -> Dict[str, Any]:
        """第4章: リアルタイムシステム"""
        return {
            'title': '第4章: リアルタイムシステム',
            'overview': 'リアルタイムシステムの概念を学び、演習問題で理解を深めます。',
            'sections': [
                {
                    'title': 'リアルタイムシステムの分類',
                    'contents': [
                        {
                            'type': 'admonition',
                            'admonition_type': 'warning',
                            'title': 'ハードリアルタイムシステム',
                            'text': 'デッドラインを1回でも守れないとシステム全体が破綻します。\n例：航空機の制御システム、原子力発電所の制御',
                            'collapsible': False
                        },
                        {
                            'type': 'admonition',
                            'admonition_type': 'info',
                            'title': 'ソフトリアルタイムシステム',
                            'text': 'デッドラインを時々守れなくても、品質が低下するだけです。\n例：動画ストリーミング、オンラインゲーム',
                            'collapsible': False
                        }
                    ]
                },
                {
                    'title': 'スケジューリングアルゴリズム',
                    'contents': [
                        {
                            'type': 'quiz',
                            'question_data': {
                                'question': '優先度ベースのスケジューリングで最も重要な概念は？',
                                'options': ['FIFO', 'プリエンプション', 'ラウンドロビン'],
                                'correct': 1,
                                'hint': '高優先度タスクが低優先度タスクを中断できる仕組み',
                                'explanation': 'プリエンプションにより、緊急タスクが即座に実行されます。'
                            }
                        }
                    ]
                },
                {
                    'title': 'まとめ',
                    'contents': [
                        {
                            'type': 'summary',
                            'title': '第4章の要点',
                            'points': [
                                'リアルタイムシステムには「ハード」と「ソフト」の2種類がある',
                                'デッドラインの厳格さが異なる',
                                'プリエンプションにより優先度の高いタスクが実行される',
                                'スケジューリングアルゴリズムがシステムの性能を左右する'
                            ]
                        }
                    ]
                },
                {
                    'title': 'よくある質問',
                    'contents': [
                        {
                            'type': 'text',
                            'text': '以下はこの章に関するFAQの抜粋です：'
                        },
                        {
                            'type': 'admonition',
                            'admonition_type': 'question',
                            'title': 'RTOSは必ず必要ですか？',
                            'text': '小規模なシステムではベアメタルプログラミングでも十分な場合があります。',
                            'collapsible': True
                        }
                    ]
                }
            ],
            'exercises': [
                        {
                            'question': 'エレベーターの制御システムはハードリアルタイムですか、ソフトリアルタイムですか？理由も説明してください。',
                            'answer': 'ハードリアルタイムシステム。扉の開閉制御や非常停止などは、決められた時間内に確実に動作しなければ人命に関わるため。',
                            'explanation': 'エレベーターは安全性が最優先されるシステムで、タイミングの遅れは許されません。',
                            'difficulty': 'medium'
                        },
                        {
                            'question': '車載ECUでプリエンプションが無効だとどのような問題が起きる可能性がありますか？',
                            'answer': 'エアバッグの展開やABSの作動など、緊急性の高い処理が通常処理の終了を待つ必要があり、致命的な遅延が発生する可能性がある。',
                            'explanation': '車載システムでは、安全に関わる処理が最優先で実行される必要があります。',
                            'difficulty': 'hard'
                        },
                        {
                            'question': 'ソフトリアルタイムシステムの例を3つ挙げてください。',
                            'answer': '1. 動画ストリーミング 2. オンラインゲーム 3. 音声通話アプリ',
                            'explanation': 'これらは多少の遅延があっても機能は継続しますが、品質が低下します。',
                            'difficulty': 'easy'
                        }
                    ]
                }
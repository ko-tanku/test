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
        
        # 第1章 - YAMLから読み込み
        chapter1_data = self.load_chapter_from_yaml("chapter1.yml")
        if chapter1_data:
            generated_files.append(self._generate_chapter_from_data(
                chapter1_data, "chapter01.md", charts_dir, tables_dir
            ))
        
        # 第2章 - YAMLから読み込み
        chapter2_data = self.load_chapter_from_yaml("chapter2.yml")
        if chapter2_data:
            generated_files.append(self._generate_chapter_from_data(
                chapter2_data, "chapter02.md", charts_dir, tables_dir
            ))
        
        # 第3章 - YAMLから読み込み
        chapter3_data = self.load_chapter_from_yaml("chapter3.yml")
        if chapter3_data:
            generated_files.append(self._generate_chapter_from_data(
                chapter3_data, "chapter03.md", charts_dir, tables_dir
            ))
        else:
            # フォールバック: 既存のメソッドを使用
            chapter3_data = self._create_chapter3()
            generated_files.append(self._generate_chapter_from_data(
                chapter3_data, "chapter03.md", charts_dir, tables_dir
            ))
        
        # 第4章 - YAMLから読み込み
        chapter4_data = self.load_chapter_from_yaml("chapter4.yml")
        if chapter4_data:
            generated_files.append(self._generate_chapter_from_data(
                chapter4_data, "chapter04.md", charts_dir, tables_dir
            ))
        else:
            # フォールバック: 既存のメソッドを使用
            chapter4_data = self._create_chapter4()
            generated_files.append(self._generate_chapter_from_data(
                chapter4_data, "chapter04.md", charts_dir, tables_dir
            ))

        # 第5章 - YAMLから読み込み（インタラクティブクイズ機能）
        chapter5_data = self.load_chapter_from_yaml("chapter5.yml")
        if chapter5_data:
            generated_files.append(self._generate_chapter_from_data(
                chapter5_data, "chapter05.md", charts_dir, tables_dir
            ))
        else:
            # フォールバック: 既存のメソッドを使用
            chapter5_data = self._create_chapter5()
            generated_files.append(self._generate_chapter_from_data(
                chapter5_data, "chapter05.md", charts_dir, tables_dir
            ))
        # 第5章（新機能統合テスト）
        chapter6_data = self._create_chapter6()
        generated_files.append(self._generate_chapter_from_data(
            chapter6_data, "chapter06.md", charts_dir, tables_dir
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
                
        return self.doc_builder.save_markdown(filename)
    
        
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
                            'width': "100%",
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
                            'width': "100%",
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
                #             'width': "100%",
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
                            'width': "100%",
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
                            'width': "100%",
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
                            'width': "100%",
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
                            'width': "100%",
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
                            'width': "100%",
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
                },
                {
                    'title': '演習問題',
                    'contents': [
                        {
                            'type': 'exercises',
                            'question_data': {
                            'question': 'エレベーターの制御システムはハードリアルタイムですか、ソフトリアルタイムですか？理由も説明してください。',
                            'answer': 'ハードリアルタイムシステム。扉の開閉制御や非常停止などは、決められた時間内に確実に動作しなければ人命に関わるため。',
                            'explanation': 'エレベーターは安全性が最優先されるシステムで、タイミングの遅れは許されません。',
                            'difficulty': 'medium'
                            }
                        },
                        {
                            'type': 'exercises',
                            'question_data': {
                            'question': '車載ECUでプリエンプションが無効だとどのような問題が起きる可能性がありますか？',
                            'answer': 'エアバッグの展開やABSの作動など、緊急性の高い処理が通常処理の終了を待つ必要があり、致命的な遅延が発生する可能性がある。',
                            'explanation': '車載システムでは、安全に関わる処理が最優先で実行される必要があります。',
                            'difficulty': 'hard'
                            }
                        },
                        {
                            'type': 'exercises',
                            'question_data': {
                            'question': 'ソフトリアルタイムシステムの例を3つ挙げてください。',
                            'answer': '1. 動画ストリーミング 2. オンラインゲーム 3. 音声通話アプリ',
                            'explanation': 'これらは多少の遅延があっても機能は継続しますが、品質が低下します。',
                            'difficulty': 'easy'
                            }
                        }
                    ]
                },
            ]
        }
    
    def _create_chapter5(self) -> Dict[str, Any]:
        """第5章: 全機能統合テスト（新機能含む）"""
        terms = self._get_chapter_terms("第5章")
        
        return {
            'title': '第5章: 全機能統合テスト',
            'overview': '全ての実装済み機能を網羅的にテストします。',
            'sections': [
                {
                    'title': 'ツールチップ機能の詳細テスト',
                    'contents': [
                        {
                            'type': 'text_with_tooltips',
                            'text': 'マイコンはセンサーからの入力を処理し、アクチュエータを制御します。RTOSを使用することで複雑なタスク管理が可能になります。',
                            'terms': terms
                        },
                        {
                            'type': 'text_with_tooltips',
                            'text': 'PWM制御によりモーターの回転速度を調整し、I2C通信でセンサーデータを取得します。',
                            'terms': terms
                        }
                    ]
                },
                {
                    'title': 'アイコン・略語ツールチップテスト',
                    'contents': [
                        {
                            'type': 'icon_tooltip',
                            'icon_name': 'memory',
                            'tooltip_text': 'メモリ使用量を表示'
                        },
                        {
                            'type': 'icon_tooltip', 
                            'icon_name': 'speed',
                            'tooltip_text': 'CPU使用率を監視'
                        },
                        {
                            'type': 'abbreviation',
                            'abbr': 'MCU',
                            'full_form': 'Microcontroller Unit - マイクロコントローラユニット'
                        },
                        {
                            'type': 'abbreviation',
                            'abbr': 'GPIO',
                            'full_form': 'General Purpose Input/Output - 汎用入出力ポート'
                        }
                    ]
                },
                {
                    'title': 'アニメーション図表テスト',
                    'contents': [
                        {
                            'type': 'chart',
                            'chart_type': 'animation',
                            'data': {
                                'frames': [
                                    {'x': [1, 2, 3, 4, 5], 'y': [1, 4, 2, 3, 5], 'title': 'フレーム 1', 'type': 'line'},
                                    {'x': [1, 2, 3, 4, 5], 'y': [2, 3, 5, 1, 4], 'title': 'フレーム 2', 'type': 'line'},
                                    {'x': [1, 2, 3, 4, 5], 'y': [5, 1, 3, 4, 2], 'title': 'フレーム 3', 'type': 'line'},
                                    {'x': [1, 2, 3, 4, 5], 'y': [3, 5, 1, 2, 4], 'title': 'フレーム 4', 'type': 'line'},
                                    {'x': [1, 2, 3, 4, 5], 'y': [4, 2, 4, 5, 1], 'title': 'フレーム 5', 'type': 'line'}
                                ]
                            },
                            'config': {
                                'title': 'データ変化のアニメーション',
                                'xlabel': 'サンプル',
                                'ylabel': '値',
                                'filename': 'data_animation',
                                'fps': 1,
                                'xlim': [0, 6],
                                'ylim': [0, 6]
                            },
                            'caption': '図5-1: 時系列データの変化をアニメーションで表示'
                        }
                    ]
                },
                {
                    'title': 'クイズ・FAQ・TIPS統合テスト',
                    'contents': [
                        {
                            'type': 'quiz',
                            'question_data': {
                                'question': 'RTOSの主な特徴は何ですか？',
                                'options': [
                                    'リアルタイム性の保証',
                                    'グラフィック処理の高速化',
                                    'ネットワーク通信の最適化',
                                    'データベース管理'
                                ],
                                'correct': 0,
                                'hint': 'RTOSはReal-Time Operating Systemの略です',
                                'explanation': 'RTOSは決められた時間内に処理を完了することを保証するオペレーティングシステムです。'
                            }
                        },
                        {
                            'type': 'quiz',
                            'question_data': {
                                'question': 'I2C通信の特徴として正しいものは？',
                                'options': [
                                    '2本の信号線で通信',
                                    '1本の信号線で通信', 
                                    '4本の信号線で通信',
                                    '8本の信号線で通信'
                                ],
                                'correct': 0,
                                'hint': 'I2CはSDAとSCLの2本の線を使用します',
                                'explanation': 'I2C通信はSDA（データ線）とSCL（クロック線）の2本で通信を行います。'
                            }
                        },
                        {
                            'type': 'quiz',
                            'question_data': {
                                'question': 'マイコンの主要な構成要素でないものは？',
                                'options': [
                                    'CPU',
                                    'RAM',
                                    'プリンター',
                                    'I/Oポート'
                                ],
                                'correct': 2,
                                'hint': 'マイコンは組み込みシステム用の小型コンピュータです',
                                'explanation': 'マイコンはCPU、メモリ、I/Oポートを1つのチップに集積した小型コンピュータです。プリンターは外部機器です。'
                            }
                        }
                    ]
                },
                {
                    'title': '学習サマリーと関連資料',
                    'contents': [
                        {
                            'type': 'summary',
                            'title': '第5章で学んだ重要事項',
                            'points': [
                                'ツールチップ機能により用語理解が向上',
                                'アニメーション図表で動的な現象を可視化',
                                'クイズ機能で理解度の確認が可能',
                                'FAQ・TIPSで自主学習を支援'
                            ]
                        },
                        {
                            'type': 'recommendations',
                            'title': '関連資料と次のステップ',
                            'items': [
                                {'text': '第1章: プログラミング基礎の復習', 'link': 'chapter01.md'},
                                {'text': '第2章: 組み込みシステム概要', 'link': 'chapter02.md'},
                                {'text': '第3章: ハードウェア理解', 'link': 'chapter03.md'},
                                {'text': '第4章: 演習問題に挑戦', 'link': 'chapter04.md'},
                                {'text': '用語集で知識を体系化', 'link': '../glossary.md'},
                                {'text': 'FAQで疑問を解決', 'link': '../faq.md'}
                            ]
                        }
                    ]
                },
                {
                    'title': '高度なインタラクティブ図表',
                    'contents': [
                        {
                            'type': 'chart',
                            'chart_type': 'interactive',
                            'data': {
                                'datasets': {
                                    'CPU使用率': {
                                        'x': [0, 1, 2, 3, 4, 5],
                                        'y': [20, 45, 78, 56, 32, 67]
                                    },
                                    'メモリ使用率': {
                                        'x': [0, 1, 2, 3, 4, 5], 
                                        'y': [15, 28, 45, 52, 38, 44]
                                    },
                                    'ディスク使用率': {
                                        'x': [0, 1, 2, 3, 4, 5],
                                        'y': [5, 8, 12, 15, 18, 22]
                                    }
                                }
                            },
                            'config': {
                                'interactive_type': 'dropdown_filter',
                                'title': 'システムリソース監視',
                                'xlabel': '時間（分）',
                                'ylabel': '使用率（%）',
                                'filename': 'system_resource_monitor'
                            },
                            'caption': '図5-2: ドロップダウンでリソース種別を切り替え'
                        }
                    ]
                }
            ]
        }
    
    def _create_chapter6(self) -> Dict[str, Any]:
            """第6章: アセット機能統合テスト（新機能）"""
            return {
                'title': '第6章: アセット機能統合テスト',
                'overview': 'AssetGeneratorとMkDocsManagerの全機能をテストします。',
                'sections': [
                    {
                        'title': 'CSS動的生成テスト',
                        'contents': [
                            {
                                'type': 'text',
                                'text': '以下は動的に生成されたCSSの効果をテストする要素です。'
                            },
                            {
                                'type': 'html_block',
                                'html': '''
                                <div class="quiz-container" data-quiz-id="css-test-1">
                                    <div class="quiz-question">CSS生成機能のテスト</div>
                                    <div class="quiz-options">
                                        <div class="quiz-option" data-index="0">オプション1（デフォルトスタイル）</div>
                                        <div class="quiz-option" data-index="1">オプション2（ホバー効果あり）</div>
                                        <div class="quiz-option" data-index="2">オプション3（アニメーション付き）</div>
                                    </div>
                                </div>
                                '''
                            },
                            {
                                'type': 'admonition',
                                'admonition_type': 'info',
                                'title': 'テーマ切り替えテスト',
                                'text': '以下のボタンでテーマを切り替えできます。',
                                'collapsible': False
                            },
                            {
                                'type': 'html_block',
                                'html': '''
                                <div style="margin: 20px 0; text-align: center;">
                                    <button onclick="switchTheme('default')" style="margin: 5px;">デフォルト</button>
                                    <button onclick="switchTheme('dark')" style="margin: 5px;">ダーク</button>
                                    <button onclick="switchTheme('high_contrast')" style="margin: 5px;">高コントラスト</button>
                                </div>
                                
                                <script>
                                function switchTheme(theme) {
                                    const link = document.querySelector('link[href*="custom"]');
                                    if (link) {
                                        const newHref = theme === 'default' ? 'custom.css' : `custom_${theme}.css`;
                                        link.href = newHref;
                                    }
                                }
                                </script>
                                '''
                            }
                        ]
                    },
                    {
                        'title': 'JavaScript機能テスト',
                        'contents': [
                            {
                                'type': 'text',
                                'text': '動的に生成されたJavaScript機能をテストします。'
                            },
                            {
                                'type': 'html_block',
                                'html': '''
                                <div class="learning-animation" id="js-test-animation">
                                    <h4>インタラクティブ要素テスト</h4>
                                    <p>この要素は画面に表示された時にアニメーションします。</p>
                                    <div class="animate-child">子要素1（遅延アニメーション）</div>
                                    <div class="animate-child">子要素2（遅延アニメーション）</div>
                                    <div class="animate-child">子要素3（遅延アニメーション）</div>
                                </div>
                                
                                <button class="animation-trigger" data-target="js-test-animation" data-animation="bounce-in">
                                    アニメーション再実行
                                </button>
                                '''
                            },
                            {
                                'type': 'text',
                                'text': '学習進度追跡機能のテスト:'
                            },
                            {
                                'type': 'html_block',
                                'html': '''
                                <div style="margin: 20px 0;">
                                    <button onclick="testProgressTracking()">進度テスト実行</button>
                                    <button onclick="showProgress()">現在の進度表示</button>
                                    <button onclick="resetProgress()">進度リセット</button>
                                    <div id="progress-display" style="margin-top: 10px; padding: 10px; background: #f0f0f0; border-radius: 4px;"></div>
                                </div>
                                
                                <script>
                                function testProgressTracking() {
                                    if (window.LearningMaterial && window.LearningMaterial.api) {
                                        window.LearningMaterial.api.markChapterComplete();
                                        alert('第6章完了をマークしました！');
                                    } else {
                                        alert('学習進度システムが見つかりません');
                                    }
                                }
                                
                                function showProgress() {
                                    const display = document.getElementById('progress-display');
                                    const progress = JSON.parse(localStorage.getItem('learning_progress') || '{}');
                                    display.innerHTML = '<strong>学習進度:</strong><br>' + JSON.stringify(progress, null, 2);
                                }
                                
                                function resetProgress() {
                                    if (window.LearningMaterial && window.LearningMaterial.api) {
                                        window.LearningMaterial.api.resetProgress();
                                        alert('学習進度をリセットしました');
                                        showProgress();
                                    }
                                }
                                </script>
                                '''
                            }
                        ]
                    },
                    {
                        'title': 'MkDocs設定管理テスト',
                        'contents': [
                            {
                                'type': 'text',
                                'text': 'MkDocsManagerによる設定管理機能の動作確認です。'
                            },
                            {
                                'type': 'code_block',
                                'language': 'yaml',
                                'code': '''# 自動生成されたmkdocs.yml設定例
    site_name: MkDocs Learning Material Generator
    theme:
    name: material
    palette:
        - media: "(prefers-color-scheme: light)"
        scheme: default
        primary: blue
        accent: cyan
        toggle:
            icon: material/brightness-7
            name: ダークモードに切り替え
        - media: "(prefers-color-scheme: dark)"
        scheme: slate
        primary: blue
        accent: cyan
        toggle:
            icon: material/brightness-4
            name: ライトモードに切り替え
    features:
        - navigation.tabs
        - navigation.sections
        - content.tooltips
        - content.code.copy

    extra_css:
    - custom.css
    - custom_dark.css
    - custom_high_contrast.css
    - animations.css

    extra_javascript:
    - custom.js
    - interactive.js
    - quiz.js
    - animations.js
    '''
                            },
                            {
                                'type': 'admonition',
                                'admonition_type': 'success',
                                'title': '設定検証結果',
                                'text': '''設定ファイルの検証が正常に完了しました：
                                
    - ナビゲーション構造: ✅ 正常
    - アセットファイル: ✅ 存在確認済み
    - プラグイン設定: ✅ 正常
    - マークダウン拡張: ✅ 正常''',
                                'collapsible': True
                            }
                        ]
                    },
                    {
                        'title': 'アセット更新機能テスト',
                        'contents': [
                            {
                                'type': 'text',
                                'text': 'アセットファイルの動的更新機能をテストします。'
                            },
                            {
                                'type': 'html_block',
                                'html': '''
                                <div style="border: 2px solid #2196F3; padding: 20px; margin: 20px 0; border-radius: 8px;">
                                    <h4>動的スタイル更新テスト</h4>
                                    <p>以下のボタンで追加CSSを適用/解除できます。</p>
                                    <button onclick="applyAdditionalCSS()">追加CSS適用</button>
                                    <button onclick="removeAdditionalCSS()">追加CSS削除</button>
                                    
                                    <div id="dynamic-style-test" style="margin-top: 15px; padding: 15px; background: #f5f5f5;">
                                        このエリアにスタイルが適用されます
                                    </div>
                                </div>
                                
                                <script>
                                function applyAdditionalCSS() {
                                    const style = document.createElement('style');
                                    style.id = 'dynamic-test-style';
                                    style.textContent = `
                                        #dynamic-style-test {
                                            background: linear-gradient(45deg, #FF6B6B, #4ECDC4) !important;
                                            color: white !important;
                                            transform: scale(1.05);
                                            transition: all 0.3s ease;
                                        }
                                    `;
                                    document.head.appendChild(style);
                                }
                                
                                function removeAdditionalCSS() {
                                    const style = document.getElementById('dynamic-test-style');
                                    if (style) {
                                        style.remove();
                                    }
                                }
                                </script>
                                '''
                            }
                        ]
                    },
                    {
                        'title': '統合機能総合テスト',
                        'contents': [
                            {
                                'type': 'quiz',
                                'question_data': {
                                    'question': 'AssetGeneratorとMkDocsManagerの主な利点は何ですか？',
                                    'options': [
                                        '手動でのファイル管理が必要',
                                        '動的なアセット生成と設定管理の自動化',
                                        '静的なファイルのみ対応'
                                    ],
                                    'correct': 1,
                                    'hint': '自動化がキーワードです',
                                    'explanation': '動的生成により、効率的で一貫性のあるアセット管理が可能になります。'
                                }
                            },
                            {
                                'type': 'summary',
                                'title': '第6章で確認した機能',
                                'points': [
                                    'CSS テンプレートの動的生成とテーマ切り替え',
                                    'JavaScript 機能の自動統合とインタラクティブ要素',
                                    'MkDocs設定の自動管理と検証',
                                    'アセットファイルの更新と履歴管理',
                                    '学習進度追跡とローカルストレージ活用',
                                    '設定の妥当性検証とエラーハンドリング'
                                ]
                            }
                        ]
                    }
                ]
            }
"""
包括的統一コンポーネントシステムのデモンストレーション

Phase 2完了版 - 4つのレンダラー（matplotlib, markdown, plotly, table）を統合したデモ
実際の業務シナリオを想定した包括的な例を提供します。
"""

from pathlib import Path
import sys
import os
import numpy as np
import pandas as pd

# プロジェクトルートをPythonパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core import UniversalContentGenerator


def create_plotly_dashboard_demo():
    """Plotlyインタラクティブダッシュボードのデモ"""
    spec = {
        "type": "content_block",
        "engine": "plotly",
        "filename": "interactive_dashboard",
        "config": {
            "title": "売上パフォーマンス ダッシュボード",
            "theme": "default",
            "width": 1200,
            "height": 800,
            "subplots": {
                "rows": 2,
                "cols": 2,
                "titles": ["月次売上推移", "商品カテゴリ分析", "地域別売上", "トレンド予測"],
                "vertical_spacing": 0.1,
                "horizontal_spacing": 0.1
            }
        },
        "components": [
            # 1. 月次売上推移（左上）
            {
                "type": "DataVisualization",
                "props": {
                    "variant": "line",
                    "data": {
                        "x": ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"],
                        "y": [1200, 1350, 1100, 1500, 1800, 2100, 2300, 2000, 1750, 1900, 2200, 2500]
                    },
                    "style": {
                        "color": "#1f77b4",
                        "lineWidth": 3,
                        "label": "売上（万円）"
                    },
                    "subplot": {"row": 1, "col": 1},
                    "name": "月次売上"
                }
            },
            # 2. 商品カテゴリ分析（右上）
            {
                "type": "DataVisualization",
                "props": {
                    "variant": "pie",
                    "data": {
                        "labels": ["電子機器", "衣料品", "書籍", "食品", "その他"],
                        "values": [35, 25, 15, 20, 5]
                    },
                    "style": {
                        "colors": ["#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"],
                        "textInfo": "label+percent",
                        "hole": 0.3
                    },
                    "subplot": {"row": 1, "col": 2},
                    "name": "商品分布"
                }
            },
            # 3. 地域別売上（左下）
            {
                "type": "DataVisualization",
                "props": {
                    "variant": "bar",
                    "data": {
                        "x": ["東京", "大阪", "名古屋", "福岡", "札幌"],
                        "y": [4500, 3200, 2800, 2100, 1900]
                    },
                    "style": {
                        "colors": ["#17becf", "#bcbd22", "#ff7f0e", "#2ca02c", "#d62728"],
                        "opacity": 0.8
                    },
                    "subplot": {"row": 2, "col": 1},
                    "name": "地域別売上"
                }
            },
            # 4. 3Dトレンド分析（右下）
            {
                "type": "DataVisualization",
                "props": {
                    "variant": "3d_scatter",
                    "data": {
                        "x": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                        "y": [1200, 1350, 1100, 1500, 1800, 2100, 2300, 2000, 1750, 1900, 2200, 2500],
                        "z": [85, 78, 92, 88, 95, 82, 89, 91, 87, 93, 96, 90]
                    },
                    "style": {
                        "color": "#e74c3c",
                        "markerSize": [8, 9, 7, 10, 12, 14, 15, 13, 11, 13, 14, 16],
                        "opacity": 0.8
                    },
                    "subplot": {"row": 2, "col": 2},
                    "name": "トレンド分析"
                }
            },
            # インタラクティブコントロール
            {
                "type": "Interactive",
                "props": {
                    "variant": "dropdown",
                    "position": {"x": 0.85, "y": 1.15},
                    "actions": [
                        {
                            "label": "全期間表示",
                            "method": "relayout",
                            "args": [{"xaxis.range": [0, 12]}]
                        },
                        {
                            "label": "第1四半期",
                            "method": "relayout", 
                            "args": [{"xaxis.range": [0, 3]}]
                        },
                        {
                            "label": "第2四半期",
                            "method": "relayout",
                            "args": [{"xaxis.range": [3, 6]}]
                        }
                    ]
                }
            }
        ]
    }
    return spec


def create_comprehensive_table_demo():
    """包括的テーブルデモ"""
    # サンプルデータ生成
    np.random.seed(42)
    sales_data = {
        '商品名': ['ノートPC', 'スマートフォン', 'タブレット', 'イヤホン', 'キーボード'],
        '1月売上': np.random.randint(100, 500, 5),
        '2月売上': np.random.randint(100, 500, 5),
        '3月売上': np.random.randint(100, 500, 5),
        '単価': [89800, 78500, 45900, 12800, 8900],
        'カテゴリ': ['PC', '通信機器', 'PC', 'アクセサリ', 'アクセサリ']
    }
    
    spec = {
        "type": "content_block",
        "engine": "table",
        "filename": "comprehensive_tables",
        "config": {
            "title": "売上データ分析レポート",
            "theme": "default",
            "layout": "single",
            "responsive": True
        },
        "components": [
            # 1. 基本的な売上データテーブル
            {
                "type": "DataTable",
                "props": {
                    "title": "月次売上データ",
                    "data": sales_data,
                    "format": {
                        "単価": "¥{:,}",
                        "1月売上": "{:,}個",
                        "2月売上": "{:,}個", 
                        "3月売上": "{:,}個"
                    },
                    "style": {
                        "header_bg_color": "#2196F3",
                        "header_text_color": "#FFFFFF"
                    }
                }
            },
            # 2. インタラクティブテーブル（ソート・フィルタ対応）
            {
                "type": "InteractiveTable",
                "props": {
                    "title": "インタラクティブ売上分析",
                    "headers": ["商品名", "総売上数", "平均売上", "売上トレンド", "評価"],
                    "rows": [
                        ["ノートPC", 1247, 415.7, "↗", "優秀"],
                        ["スマートフォン", 1156, 385.3, "→", "良好"],
                        ["タブレット", 891, 297.0, "↘", "要改善"],
                        ["イヤホン", 1432, 477.3, "↗", "優秀"],
                        ["キーボード", 768, 256.0, "→", "普通"]
                    ],
                    "sortable": True,
                    "filterable": True,
                    "style": {
                        "header_bg_color": "#4CAF50",
                        "row_even_bg_color": "#F1F8E9"
                    }
                }
            },
            # 3. 比較テーブル
            {
                "type": "ComparisonTable",
                "props": {
                    "title": "四半期比較分析",
                    "categories": ["Q1目標", "Q1実績", "達成率", "Q2予測"],
                    "items": ["ノートPC", "スマートフォン", "タブレット", "イヤホン", "キーボード"],
                    "data": [
                        [1200, 1247, "103.9%", 1300],
                        [1100, 1156, "105.1%", 1200],
                        [950, 891, "93.8%", 950],
                        [1300, 1432, "110.2%", 1500],
                        [800, 768, "96.0%", 850]
                    ]
                }
            },
            # 4. 統計サマリーテーブル
            {
                "type": "SummaryTable",
                "props": {
                    "title": "統計サマリー",
                    "data": {
                        "売上数": [1247, 1156, 891, 1432, 768],
                        "単価": [89800, 78500, 45900, 12800, 8900],
                        "売上金額": [11196646, 90752600, 40901900, 18329600, 6835200]
                    },
                    "metrics": ["count", "mean", "std", "min", "max"],
                    "style": {
                        "header_bg_color": "#FF9800"
                    }
                }
            }
        ]
    }
    return spec


def create_advanced_matplotlib_demo():
    """高度なMatplotlib科学的描画デモ"""
    spec = {
        "type": "content_block",
        "engine": "matplotlib",
        "filename": "scientific_analysis",
        "config": {
            "title": "科学データ分析ビジュアライゼーション",
            "size": [14, 10],
            "xlim": [0, 10],
            "ylim": [-3, 3],
            "grid": True,
            "grid_alpha": 0.3
        },
        "components": [
            # 複数の数学関数を重ねて表示
            {
                "type": "MathFunction",
                "props": {
                    "function": "sin",
                    "domain": [0, 10],
                    "parameters": {
                        "amplitude": 1,
                        "frequency": 1,
                        "phase": 0
                    },
                    "style": {
                        "color": "#e74c3c",
                        "lineWidth": 2,
                        "label": "sin(x)"
                    }
                }
            },
            {
                "type": "MathFunction", 
                "props": {
                    "function": "cos",
                    "domain": [0, 10],
                    "parameters": {
                        "amplitude": 0.8,
                        "frequency": 1.5,
                        "phase": 0
                    },
                    "style": {
                        "color": "#3498db",
                        "lineWidth": 2,
                        "label": "0.8*cos(1.5x)"
                    }
                }
            },
            # データポイント散布図
            {
                "type": "DataVisualization",
                "props": {
                    "variant": "scatter",
                    "data": {
                        "x": [1, 2, 3, 4, 5, 6, 7, 8, 9],
                        "y": [0.8, 1.2, -0.5, -1.8, 0.3, 2.1, -0.7, 1.5, -2.2]
                    },
                    "style": {
                        "colors": ["red", "blue", "green", "orange", "purple", "brown", "pink", "gray", "cyan"],
                        "markerSize": 100,
                        "opacity": 0.7
                    }
                }
            },
            # 重要エリアのハイライト
            {
                "type": "Shape",
                "props": {
                    "variant": "rectangle",
                    "position": [2, -2],
                    "size": [3, 4],
                    "style": {
                        "color": "#ffeb3b",
                        "stroke": "#ffc107",
                        "strokeWidth": 2,
                        "opacity": 0.3
                    }
                }
            },
            # 注釈とラベル
            {
                "type": "Text",
                "props": {
                    "content": "重要な分析領域",
                    "position": [3.5, 1.5],
                    "style": {
                        "fontSize": 12,
                        "color": "#f57c00",
                        "fontWeight": "bold",
                        "align": "center"
                    }
                }
            },
            # グラフの軸とタイトル
            {
                "type": "Axis",
                "props": {
                    "xlabel": "時間 (秒)",
                    "ylabel": "振幅",
                    "title": "多重波形解析"
                }
            },
            # 凡例
            {
                "type": "Legend",
                "props": {
                    "location": "upper right",
                    "frameon": True,
                    "shadow": True
                }
            }
        ]
    }
    return spec


def create_enhanced_markdown_tutorial():
    """拡張Markdownチュートリアル"""
    spec = {
        "type": "content_block",
        "engine": "markdown",
        "filename": "advanced_python_tutorial",
        "config": {
            "title": "Python高度プログラミングガイド",
            "toc": True,
            "meta": {
                "author": "システム開発チーム",
                "description": "Pythonの高度な概念とベストプラクティスを学ぶ",
                "tags": ["Python", "プログラミング", "高級者向け"]
            }
        },
        "components": [
            # クラスとオブジェクト指向
            {
                "type": "LearningSection",
                "props": {
                    "title": "クラスとオブジェクト指向プログラミング",
                    "level": 2,
                    "components": [
                        {
                            "type": "Paragraph",
                            "props": {
                                "content": "**オブジェクト指向プログラミング**（OOP）は、データとそれを操作する関数を一つの**クラス**にまとめる設計手法です。Pythonでは`class`キーワードを使用してクラスを定義します。",
                                "terms": {
                                    "オブジェクト指向プログラミング": "データとメソッドをオブジェクトとしてまとめる プログラミングパラダイム",
                                    "クラス": "オブジェクトの設計図となるテンプレート"
                                },
                                "enableTooltips": False
                            }
                        },
                        {
                            "type": "Tabs",
                            "props": {
                                "tabs": {
                                    "基本クラス": [
                                        {
                                            "type": "CodeBlock",
                                            "props": {
                                                "content": "class Student:\n    def __init__(self, name, age):\n        self.name = name\n        self.age = age\n        self.grades = []\n    \n    def add_grade(self, grade):\n        self.grades.append(grade)\n    \n    def get_average(self):\n        if not self.grades:\n            return 0\n        return sum(self.grades) / len(self.grades)\n    \n    def __str__(self):\n        return f\"Student: {self.name}, Age: {self.age}\"\n\n# クラスの使用\nstudent = Student(\"太郎\", 20)\nstudent.add_grade(85)\nstudent.add_grade(92)\nprint(f\"平均点: {student.get_average():.1f}\")",
                                                "language": "python",
                                                "title": "基本的なクラス定義"
                                            }
                                        }
                                    ],
                                    "継承": [
                                        {
                                            "type": "CodeBlock",
                                            "props": {
                                                "content": "class Person:\n    def __init__(self, name, age):\n        self.name = name\n        self.age = age\n    \n    def introduce(self):\n        return f\"こんにちは、{self.name}です。{self.age}歳です。\"\n\nclass Student(Person):  # Personクラスを継承\n    def __init__(self, name, age, student_id):\n        super().__init__(name, age)  # 親クラスの初期化\n        self.student_id = student_id\n        self.courses = []\n    \n    def enroll(self, course):\n        self.courses.append(course)\n        return f\"{course}に登録しました\"\n    \n    def introduce(self):  # メソッドのオーバーライド\n        parent_intro = super().introduce()\n        return f\"{parent_intro} 学生ID: {self.student_id}\"\n\n# 使用例\nstudent = Student(\"花子\", 19, \"S12345\")\nprint(student.introduce())\nprint(student.enroll(\"データサイエンス\"))",
                                                "language": "python",
                                                "title": "継承とポリモーフィズム"
                                            }
                                        }
                                    ],
                                    "プロパティ": [
                                        {
                                            "type": "CodeBlock",
                                            "props": {
                                                "content": "class BankAccount:\n    def __init__(self, initial_balance=0):\n        self._balance = initial_balance  # プライベート属性\n    \n    @property\n    def balance(self):\n        \"\"\"残高を取得\"\"\"\n        return self._balance\n    \n    @balance.setter\n    def balance(self, value):\n        \"\"\"残高を設定（バリデーション付き）\"\"\"\n        if value < 0:\n            raise ValueError(\"残高は0以上である必要があります\")\n        self._balance = value\n    \n    def deposit(self, amount):\n        \"\"\"入金\"\"\"\n        if amount <= 0:\n            raise ValueError(\"入金額は0より大きい必要があります\")\n        self._balance += amount\n        return f\"¥{amount:,}を入金しました。残高: ¥{self._balance:,}\"\n    \n    def withdraw(self, amount):\n        \"\"\"出金\"\"\"\n        if amount > self._balance:\n            raise ValueError(\"残高不足です\")\n        self._balance -= amount\n        return f\"¥{amount:,}を出金しました。残高: ¥{self._balance:,}\"\n\n# 使用例\naccount = BankAccount(10000)\nprint(account.deposit(5000))\nprint(f\"現在の残高: ¥{account.balance:,}\")",
                                                "language": "python",
                                                "title": "プロパティとカプセル化"
                                            }
                                        }
                                    ]
                                }
                            }
                        },
                        {
                            "type": "Admonition",
                            "props": {
                                "variant": "tip",
                                "title": "オブジェクト指向設計のベストプラクティス",
                                "content": "- **単一責任の原則**: 各クラスは一つの責任のみを持つ\\n- **開放閉鎖の原則**: 拡張に対して開いており、修正に対して閉じている\\n- **リスコフの置換原則**: 派生クラスは基底クラスと置換可能\\n- **インターフェイス分離の原則**: クライアントは不要なインターフェイスに依存しない\\n- **依存関係逆転の原則**: 抽象に依存し、具象に依存しない"
                            }
                        }
                    ]
                }
            },
            # 非同期プログラミング
            {
                "type": "Heading",
                "props": {
                    "content": "非同期プログラミング（async/await）",
                    "level": 2
                }
            },
            {
                "type": "CodeBlock",
                "props": {
                    "content": "import asyncio\nimport aiohttp\nimport time\n\nasync def fetch_data(session, url):\n    \"\"\"非同期でデータを取得\"\"\"\n    async with session.get(url) as response:\n        return await response.text()\n\nasync def fetch_multiple_urls(urls):\n    \"\"\"複数のURLを同時に処理\"\"\"\n    async with aiohttp.ClientSession() as session:\n        tasks = [fetch_data(session, url) for url in urls]\n        results = await asyncio.gather(*tasks)\n        return results\n\n# 実行例\nasync def main():\n    urls = [\n        \"https://httpbin.org/delay/1\",\n        \"https://httpbin.org/delay/2\", \n        \"https://httpbin.org/delay/1\"\n    ]\n    \n    start_time = time.time()\n    results = await fetch_multiple_urls(urls)\n    end_time = time.time()\n    \n    print(f\"3つのリクエストを {end_time - start_time:.2f}秒で処理\")\n    print(f\"取得したデータ数: {len(results)}\")\n\n# asyncio.run(main())",
                    "language": "python",
                    "title": "非同期処理の実装例"
                }
            },
            # 理解度テスト
            {
                "type": "Heading",
                "props": {
                    "content": "理解度チェック",
                    "level": 2
                }
            },
            {
                "type": "Quiz",
                "props": {
                    "variant": "multiple_choice",
                    "question": "オブジェクト指向プログラミングの主要な特徴を選んでください（複数選択）",
                    "options": [
                        "カプセル化（Encapsulation）",
                        "継承（Inheritance）",
                        "ポリモーフィズム（Polymorphism）",
                        "グローバル変数の使用",
                        "関数型プログラミング"
                    ],
                    "correct": [0, 1, 2],
                    "explanation": "OOPの3つの主要な特徴は、カプセル化、継承、ポリモーフィズムです。グローバル変数の使用や関数型プログラミングはOOPの特徴ではありません。",
                    "id": "oop_features_quiz"
                }
            },
            {
                "type": "Quiz",
                "props": {
                    "variant": "single_choice", 
                    "question": "async/awaitキーワードの主な目的は何ですか？",
                    "options": [
                        "コードの実行速度を向上させる",
                        "非同期処理を同期的に書けるようにする",
                        "メモリ使用量を削減する",
                        "エラーハンドリングを自動化する"
                    ],
                    "correct": [1],
                    "explanation": "async/awaitは非同期処理を同期的なコードのように書けるようにするためのキーワードです。",
                    "id": "async_purpose_quiz"
                }
            },
            # まとめ
            {
                "type": "Summary",
                "props": {
                    "title": "この章のまとめ",
                    "variant": "admonition",
                    "points": [
                        "クラスはオブジェクトの設計図であり、データとメソッドをカプセル化する",
                        "継承により既存クラスの機能を拡張し、コードの再利用性を向上させる", 
                        "プロパティを使用してアクセス制御とデータ検証を実装する",
                        "async/awaitにより非同期処理を効率的かつ読みやすく実装できる",
                        "適切な設計原則に従うことで保守性の高いコードを作成できる"
                    ]
                }
            }
        ]
    }
    return spec


def main():
    """包括的デモンストレーションの実行"""
    print("🚀 Phase 2完了 - 包括的統一コンポーネントシステムデモ")
    print("=" * 70)
    
    # 出力ディレクトリを作成
    output_dir = Path("comprehensive_demo_output")
    output_dir.mkdir(exist_ok=True)
    
    generator = UniversalContentGenerator(output_dir)
    
    demos = [
        ("Plotlyインタラクティブダッシュボード", create_plotly_dashboard_demo),
        ("包括的テーブル分析", create_comprehensive_table_demo),
        ("高度な科学的可視化", create_advanced_matplotlib_demo),
        ("拡張Markdownチュートリアル", create_enhanced_markdown_tutorial)
    ]
    
    generated_files = []
    
    try:
        for demo_name, demo_func in demos:
            print(f"\\n📊 {demo_name}を生成中...")
            spec = demo_func()
            result_path = generator.generate_from_spec(spec)
            generated_files.append(result_path)
            print(f"✅ 生成完了: {result_path}")
        
        print("\\n🎉 全てのデモが正常に完了しました！")
        print(f"📁 生成されたファイルは {output_dir} フォルダで確認できます")
        
        # システム情報を表示
        system_info = generator.get_system_info()
        print(f"\\n🔍 システム情報:")
        print(f"  - 利用可能エンジン: {', '.join(system_info['available_engines'])}")
        print(f"  - 出力ディレクトリ: {system_info['output_dir']}")
        
        # 生成されたファイル一覧
        print("\\n📋 生成されたファイル:")
        for file_path in generated_files:
            if file_path.exists():
                size = file_path.stat().st_size
                print(f"  - {file_path.name} ({size:,} bytes)")
        
        print("\\n💡 使用されたエンジン:")
        print("  - 📊 Plotly: インタラクティブダッシュボード")
        print("  - 📋 Table: データ分析テーブル") 
        print("  - 📈 Matplotlib: 科学的可視化")
        print("  - 📝 Markdown: 学習コンテンツ")
        
        return True
        
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
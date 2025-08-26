"""
統一コンポーネントシステムのデモンストレーション

新しいReact風コンポーネントシステムの使用例を示します。
既存システムとの互換性を保ちつつ、宣言的な書き方でコンテンツを生成できます。
"""

from pathlib import Path
import sys
import os

# プロジェクトルートをPythonパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core import UniversalContentGenerator


def create_matplotlib_dashboard_demo():
    """Matplotlibを使用したダッシュボード風のデモ"""
    spec = {
        "type": "content_block",
        "engine": "matplotlib",
        "filename": "dashboard_demo",
        "config": {
            "title": "システム監視ダッシュボード",
            "size": [12, 8],
            "xlim": [0, 10],
            "ylim": [0, 10],
            "grid": True,
            "grid_alpha": 0.3
        },
        "components": [
            # CPU使用率のライングラフ
            {
                "type": "DataVisualization",
                "props": {
                    "variant": "line",
                    "data": {
                        "x": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                        "y": [20, 35, 45, 40, 55, 60, 45, 50, 65, 70]
                    },
                    "style": {
                        "color": "#1f77b4",
                        "lineWidth": 3,
                        "label": "CPU使用率(%)"
                    }
                }
            },
            # メモリ使用量のバーグラフ（散布図として近似）
            {
                "type": "DataVisualization",
                "props": {
                    "variant": "scatter",
                    "data": {
                        "x": [2, 4, 6, 8],
                        "y": [3, 4, 3.5, 4.5]
                    },
                    "style": {
                        "colors": ["#ff7f0e", "#2ca02c", "#d62728", "#9467bd"],
                        "markerSize": 200,
                        "opacity": 0.7
                    }
                }
            },
            # 警告エリア（赤い矩形）
            {
                "type": "Shape",
                "props": {
                    "variant": "rectangle",
                    "position": [8, 8],
                    "size": [3, 1.5],
                    "style": {
                        "color": "#ffcccc",
                        "stroke": "#ff0000",
                        "strokeWidth": 2,
                        "opacity": 0.6
                    }
                }
            },
            # 警告テキスト
            {
                "type": "Text",
                "props": {
                    "content": "警告エリア",
                    "position": [8, 8],
                    "style": {
                        "fontSize": 12,
                        "color": "#cc0000",
                        "fontWeight": "bold",
                        "align": "center"
                    }
                }
            },
            # 正弦波（数学関数）
            {
                "type": "MathFunction",
                "props": {
                    "function": "sin",
                    "domain": [0, 10],
                    "parameters": {
                        "amplitude": 0.5,
                        "frequency": 2,
                        "offset": 2
                    },
                    "style": {
                        "color": "#17becf",
                        "lineWidth": 2,
                        "label": "周期パターン"
                    }
                }
            },
            # 注釈
            {
                "type": "Annotation",
                "props": {
                    "text": "ピーク時間",
                    "position": [9, 6.5],
                    "arrow_position": [9, 7],
                    "style": {
                        "fontSize": 10,
                        "color": "red"
                    },
                    "bbox_style": "round,pad=0.3"
                }
            },
            # 軸設定
            {
                "type": "Axis",
                "props": {
                    "xlabel": "時間 (時)",
                    "ylabel": "使用率 / 値"
                }
            },
            # 凡例
            {
                "type": "Legend",
                "props": {
                    "location": "upper left",
                    "frameon": True,
                    "shadow": True
                }
            }
        ]
    }
    return spec


def create_markdown_tutorial_demo():
    """Markdownを使用した学習教材のデモ"""
    spec = {
        "type": "content_block",
        "engine": "markdown",
        "filename": "python_tutorial",
        "config": {
            "title": "Python入門チュートリアル",
            "toc": True,
            "meta": {
                "author": "学習プラットフォーム",
                "description": "Python初心者向けのチュートリアル"
            }
        },
        "components": [
            # 学習セクション1
            {
                "type": "LearningSection",
                "props": {
                    "title": "変数とデータ型",
                    "level": 2,
                    "components": [
                        {
                            "type": "Paragraph",
                            "props": {
                                "content": "プログラミングにおいて**変数**は、データを格納するための重要な概念です。Pythonでは動的型付けを採用しているため、変数の型を明示的に宣言する必要がありません。",
                                "terms": {
                                    "変数": "データを格納するためのメモリ領域の名前",
                                    "動的型付け": "実行時に変数の型が決定される仕組み"
                                },
                                "enableTooltips": False
                            }
                        },
                        {
                            "type": "Tabs",
                            "props": {
                                "tabs": {
                                    "基本例": [
                                        {
                                            "type": "CodeBlock",
                                            "props": {
                                                "content": "# 文字列\nname = \"太郎\"\n\n# 数値\nage = 25\nscore = 85.5\n\n# ブール値\nis_student = True\n\nprint(f\"名前: {name}, 年齢: {age}, 学生: {is_student}\")",
                                                "language": "python",
                                                "title": "Python変数の基本"
                                            }
                                        }
                                    ],
                                    "型確認": [
                                        {
                                            "type": "CodeBlock",
                                            "props": {
                                                "content": "# 変数の型を確認\nprint(type(name))    # <class 'str'>\nprint(type(age))     # <class 'int'>\nprint(type(score))   # <class 'float'>\nprint(type(is_student)) # <class 'bool'>",
                                                "language": "python"
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
                                "title": "命名規則のベストプラクティス",
                                "content": "- 変数名は小文字とアンダースコアを使用（snake_case）\n- 意味のある名前を付ける\n- 予約語は使用しない\n\n例: `user_name`, `total_score`, `is_valid`"
                            }
                        }
                    ]
                }
            },
            # クイズセクション
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
                    "variant": "single_choice",
                    "question": "Pythonで正しい変数の定義はどれですか？",
                    "options": [
                        "int age = 25",
                        "age = 25",
                        "var age = 25",
                        "age := 25"
                    ],
                    "correct": [1],
                    "explanation": "Pythonでは型を明示せずに変数名 = 値 の形式で定義します。",
                    "id": "python_variable_quiz"
                }
            },
            {
                "type": "Quiz",
                "props": {
                    "variant": "multiple_choice",
                    "question": "Pythonの基本データ型に含まれるものを選んでください（複数選択）",
                    "options": [
                        "str（文字列）",
                        "int（整数）",
                        "float（浮動小数点数）",
                        "char（文字）",
                        "bool（ブール値）"
                    ],
                    "correct": [0, 1, 2, 4],
                    "explanation": "Pythonの基本型にはstr, int, float, boolがあります。charは独立した型ではありません。",
                    "id": "python_types_quiz"
                }
            },
            # 要約セクション
            {
                "type": "Summary",
                "props": {
                    "title": "この章のまとめ",
                    "variant": "admonition",
                    "points": [
                        "Pythonは動的型付け言語で、変数の型を明示的に宣言する必要がない",
                        "基本データ型：str, int, float, bool",
                        "変数名はsnake_caseで意味のある名前を付ける",
                        "type()関数で変数の型を確認できる"
                    ]
                }
            },
            # 関連リンク
            {
                "type": "Heading",
                "props": {
                    "content": "さらに学習するために",
                    "level": 3
                }
            },
            {
                "type": "List",
                "props": {
                    "variant": "unordered",
                    "items": [
                        "📚 [Python公式チュートリアル](https://docs.python.org/ja/3/tutorial/)",
                        "💡 [次の章: 制御構文](./control_structures.md)",
                        "🎯 [演習問題](./exercises.md)"
                    ]
                }
            }
        ]
    }
    return spec


def create_yaml_demo():
    """YAMLファイルベースのデモ"""
    yaml_content = """
type: content_block
engine: matplotlib
filename: yaml_demo
config:
  title: "YAMLで定義されたグラフ"
  size: [10, 6]
  xlim: [0, 6]
  ylim: [-2, 2]

components:
  - type: MathFunction
    props:
      function: sin
      domain: [0, 6]
      parameters:
        amplitude: 1
        frequency: 1
        phase: 0
      style:
        color: "#e74c3c"
        lineWidth: 3
        label: "sin(x)"

  - type: MathFunction
    props:
      function: cos
      domain: [0, 6]
      parameters:
        amplitude: 0.8
        frequency: 1.5
        phase: 0
      style:
        color: "#3498db"
        lineWidth: 2
        label: "0.8*cos(1.5x)"

  - type: Shape
    props:
      variant: circle
      position: [3, 0]
      size: 0.2
      style:
        color: "gold"
        stroke: "orange"
        strokeWidth: 2

  - type: Text
    props:
      content: "交点付近"
      position: [3.2, 0.3]
      style:
        fontSize: 10
        color: "orange"

  - type: Legend
    props:
      location: "upper right"
"""
    
    return yaml_content


def main():
    """デモンストレーションの実行"""
    print("🚀 統一コンポーネントシステムのデモンストレーション")
    print("=" * 60)
    
    # 出力ディレクトリを作成
    output_dir = Path("demo_output")
    output_dir.mkdir(exist_ok=True)
    
    generator = UniversalContentGenerator(output_dir)
    
    try:
        # 1. Matplotlibダッシュボードデモ
        print("📊 Matplotlibダッシュボードを生成中...")
        dashboard_spec = create_matplotlib_dashboard_demo()
        dashboard_path = generator.generate_from_spec(dashboard_spec)
        print(f"✅ 生成完了: {dashboard_path}")
        
        # 2. Markdownチュートリアルデモ
        print("\n📝 Markdownチュートリアルを生成中...")
        tutorial_spec = create_markdown_tutorial_demo()
        tutorial_path = generator.generate_from_spec(tutorial_spec)
        print(f"✅ 生成完了: {tutorial_path}")
        
        # 3. YAMLファイルデモ
        print("\n🔧 YAMLファイルから生成中...")
        yaml_content = create_yaml_demo()
        yaml_file = output_dir / "yaml_demo.yml"
        yaml_file.write_text(yaml_content, encoding='utf-8')
        yaml_result = generator.generate_from_yaml(yaml_file)
        print(f"✅ 生成完了: {yaml_result}")
        
        print("\n🎉 すべてのデモが正常に完了しました！")
        print(f"📁 生成されたファイルは {output_dir} フォルダで確認できます")
        
        # 生成されたファイル一覧を表示
        print("\n📋 生成されたファイル:")
        for file_path in sorted(output_dir.iterdir()):
            if file_path.is_file():
                size = file_path.stat().st_size
                print(f"  - {file_path.name} ({size:,} bytes)")
        
        # システム情報を表示
        system_info = generator.get_system_info()
        print(f"\n🔍 システム情報:")
        print(f"  - 利用可能エンジン: {', '.join(system_info['available_engines'])}")
        print(f"  - 出力ディレクトリ: {system_info['output_dir']}")
        
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
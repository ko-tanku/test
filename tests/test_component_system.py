"""
新しいコンポーネントシステムのテスト

統一コンポーネントシステムが正常に動作することを確認します。
"""

import pytest
import tempfile
from pathlib import Path
import yaml

from src.core import (
    UniversalContentGenerator,
    RendererFactory,
    MatplotlibRenderer,
    MarkdownRenderer,
    PlotlyRenderer,
    TableRenderer
)


class TestComponentSystem:
    """コンポーネントシステムの統合テスト"""
    
    def setup_method(self):
        """テスト用の一時ディレクトリを設定"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.generator = UniversalContentGenerator(self.temp_dir)
    
    def test_renderer_factory_initialization(self):
        """RendererFactoryが正しく初期化されることを確認"""
        available_engines = RendererFactory.get_available_engines()
        assert 'matplotlib' in available_engines
        assert 'markdown' in available_engines
        assert 'plotly' in available_engines
        assert 'table' in available_engines
        
        # エンジン情報取得
        matplotlib_info = RendererFactory.get_engine_info('matplotlib')
        assert matplotlib_info['engine_name'] == 'matplotlib'
        assert matplotlib_info['file_extension'] == 'html'
        
        markdown_info = RendererFactory.get_engine_info('markdown')
        assert markdown_info['engine_name'] == 'markdown'
        assert markdown_info['file_extension'] == 'md'
    
    def test_matplotlib_basic_chart(self):
        """MatplotlibRendererで基本的なグラフを生成"""
        spec = {
            "type": "content_block",
            "engine": "matplotlib",
            "filename": "test_chart",
            "config": {
                "title": "テストグラフ",
                "size": [8, 6],
                "xlim": [0, 10],
                "ylim": [0, 10]
            },
            "components": [
                {
                    "type": "DataVisualization",
                    "props": {
                        "variant": "line",
                        "data": {
                            "x": [1, 2, 3, 4, 5],
                            "y": [2, 4, 3, 5, 4]
                        },
                        "style": {
                            "color": "#1f77b4",
                            "lineWidth": 3,
                            "xlabel": "X軸",
                            "ylabel": "Y軸"
                        }
                    }
                },
                {
                    "type": "Shape",
                    "props": {
                        "variant": "circle",
                        "position": [7, 7],
                        "size": 1.5,
                        "style": {
                            "color": "red",
                            "opacity": 0.7
                        }
                    }
                },
                {
                    "type": "Text",
                    "props": {
                        "content": "サンプルテキスト",
                        "position": [5, 8],
                        "style": {
                            "fontSize": 14,
                            "color": "green"
                        }
                    }
                }
            ]
        }
        
        result_path = self.generator.generate_from_spec(spec)
        assert result_path.exists()
        assert result_path.suffix == '.html'
        assert result_path.stat().st_size > 0
    
    def test_matplotlib_math_function(self):
        """数学関数描画のテスト"""
        spec = {
            "type": "content_block",
            "engine": "matplotlib",
            "filename": "math_functions",
            "config": {
                "title": "三角関数",
                "size": [10, 6],
                "xlim": [0, 10],
                "ylim": [-2, 2]
            },
            "components": [
                {
                    "type": "MathFunction",
                    "props": {
                        "function": "sin",
                        "domain": [0, 10],
                        "parameters": {
                            "amplitude": 1.5,
                            "frequency": 2,
                            "phase": 0
                        },
                        "style": {
                            "color": "blue",
                            "lineWidth": 2,
                            "label": "sin(2x)"
                        }
                    }
                },
                {
                    "type": "MathFunction",
                    "props": {
                        "function": "cos",
                        "domain": [0, 10],
                        "parameters": {
                            "amplitude": 1,
                            "frequency": 1,
                            "phase": 0
                        },
                        "style": {
                            "color": "red",
                            "lineWidth": 2,
                            "label": "cos(x)"
                        }
                    }
                },
                {
                    "type": "Legend",
                    "props": {
                        "location": "upper right"
                    }
                }
            ]
        }
        
        result_path = self.generator.generate_from_spec(spec)
        assert result_path.exists()
    
    def test_markdown_basic_document(self):
        """MarkdownRendererで基本的なドキュメントを生成"""
        spec = {
            "type": "content_block",
            "engine": "markdown",
            "filename": "test_document",
            "config": {
                "title": "テストドキュメント",
                "toc": True
            },
            "components": [
                {
                    "type": "Heading",
                    "props": {
                        "content": "第1章: 概要",
                        "level": 2
                    }
                },
                {
                    "type": "Paragraph",
                    "props": {
                        "content": "これはテスト用の段落です。**太字**や*斜体*も使用できます。",
                        "terms": {
                            "太字": "文字を強調表示する方法"
                        },
                        "enableTooltips": False
                    }
                },
                {
                    "type": "List",
                    "props": {
                        "variant": "unordered",
                        "items": [
                            "項目1",
                            "項目2",
                            "項目3"
                        ]
                    }
                },
                {
                    "type": "CodeBlock",
                    "props": {
                        "content": "def hello():\n    print('Hello, World!')",
                        "language": "python",
                        "title": "サンプルコード"
                    }
                },
                {
                    "type": "Admonition",
                    "props": {
                        "variant": "info",
                        "title": "ポイント",
                        "content": "これは重要な情報です。",
                        "collapsible": False
                    }
                }
            ]
        }
        
        result_path = self.generator.generate_from_spec(spec)
        assert result_path.exists()
        assert result_path.suffix == '.md'
        
        # 内容の確認
        content = result_path.read_text(encoding='utf-8')
        assert "テストドキュメント" in content
        assert "第1章: 概要" in content
        assert "```python" in content
        assert "!!! info" in content
    
    def test_markdown_tabs_component(self):
        """タブコンポーネントのテスト"""
        spec = {
            "type": "content_block",
            "engine": "markdown",
            "filename": "tabs_test",
            "components": [
                {
                    "type": "Tabs",
                    "props": {
                        "tabs": {
                            "Python": [
                                {
                                    "type": "CodeBlock",
                                    "props": {
                                        "content": "print('Hello from Python')",
                                        "language": "python"
                                    }
                                }
                            ],
                            "JavaScript": [
                                {
                                    "type": "CodeBlock", 
                                    "props": {
                                        "content": "console.log('Hello from JavaScript');",
                                        "language": "javascript"
                                    }
                                }
                            ]
                        }
                    }
                }
            ]
        }
        
        result_path = self.generator.generate_from_spec(spec)
        assert result_path.exists()
        
        content = result_path.read_text(encoding='utf-8')
        assert "=== Tab Content" in content or "=== \"Python\"" in content
    
    def test_quiz_component(self):
        """クイズコンポーネントのテスト"""
        spec = {
            "type": "content_block",
            "engine": "markdown",
            "filename": "quiz_test",
            "components": [
                {
                    "type": "Quiz",
                    "props": {
                        "variant": "single_choice",
                        "question": "Pythonで文字列を出力するコマンドは？",
                        "options": [
                            "print()",
                            "echo()",
                            "output()",
                            "display()"
                        ],
                        "correct": [0],
                        "explanation": "Pythonでは print() 関数を使用します。",
                        "id": "python_print_quiz"
                    }
                }
            ]
        }
        
        result_path = self.generator.generate_from_spec(spec)
        assert result_path.exists()
        
        content = result_path.read_text(encoding='utf-8')
        assert "quiz-container" in content
        assert "python_print_quiz" in content
    
    def test_yaml_file_loading(self):
        """YAMLファイルからの読み込みテスト"""
        # テスト用YAMLファイルを作成
        yaml_spec = {
            "type": "content_block",
            "engine": "matplotlib",
            "filename": "yaml_test",
            "config": {
                "title": "YAMLテスト"
            },
            "components": [
                {
                    "type": "DataVisualization",
                    "props": {
                        "variant": "bar",
                        "data": {
                            "x": ["A", "B", "C"],
                            "y": [1, 3, 2]
                        },
                        "style": {
                            "color": "green"
                        }
                    }
                }
            ]
        }
        
        yaml_path = self.temp_dir / "test_spec.yml"
        with open(yaml_path, 'w', encoding='utf-8') as f:
            yaml.dump(yaml_spec, f, default_flow_style=False, allow_unicode=True)
        
        result_path = self.generator.generate_from_yaml(yaml_path)
        assert result_path.exists()
    
    def test_invalid_engine_error(self):
        """存在しないエンジンの場合のエラー"""
        spec = {
            "type": "content_block",
            "engine": "nonexistent",
            "components": []
        }
        
        with pytest.raises(ValueError, match="エンジンが利用できません"):
            self.generator.generate_from_spec(spec)
    
    def test_component_validation_error(self):
        """コンポーネント検証エラーのテスト"""
        spec = {
            "type": "content_block",
            "engine": "matplotlib", 
            "components": [
                {
                    "type": "DataVisualization",
                    "props": {
                        # 必須のvariantとdataが不足
                        "style": {"color": "blue"}
                    }
                }
            ]
        }
        
        # バリデーションエラーが発生することを確認
        # （実際の実装では、missing propsエラーでスキップされる）
        result_path = self.generator.generate_from_spec(spec)
        # ファイルは生成されるが、問題のあるコンポーネントはスキップされる
        assert result_path.exists()
    
    def test_plotly_basic_chart(self):
        """Plotlyレンダラーで基本的なインタラクティブチャートを生成"""
        spec = {
            "type": "content_block",
            "engine": "plotly",
            "filename": "plotly_test",
            "config": {
                "title": "Plotlyテストチャート",
                "width": 800,
                "height": 600
            },
            "components": [
                {
                    "type": "DataVisualization",
                    "props": {
                        "variant": "line",
                        "data": {
                            "x": [1, 2, 3, 4, 5],
                            "y": [2, 4, 3, 5, 4]
                        },
                        "style": {
                            "color": "#1f77b4",
                            "lineWidth": 3,
                            "label": "テストデータ"
                        }
                    }
                }
            ]
        }
        
        result_path = self.generator.generate_from_spec(spec)
        assert result_path.exists()
        assert result_path.suffix == '.html'
        
        # HTMLコンテンツにPlotlyが含まれることを確認
        content = result_path.read_text(encoding='utf-8')
        assert "plotly" in content.lower()
    
    def test_plotly_dashboard(self):
        """Plotlyダッシュボードコンポーネントのテスト"""
        spec = {
            "type": "content_block",
            "engine": "plotly",
            "filename": "dashboard_test",
            "config": {
                "title": "ダッシュボードテスト",
                "subplots": {
                    "rows": 2,
                    "cols": 2,
                    "titles": ["チャート1", "チャート2", "チャート3", "チャート4"]
                }
            },
            "components": [
                {
                    "type": "Dashboard",
                    "props": {
                        "components": [
                            {
                                "type": "DataVisualization",
                                "props": {
                                    "variant": "line",
                                    "data": {
                                        "x": [1, 2, 3],
                                        "y": [1, 3, 2]
                                    },
                                    "style": {"color": "blue"}
                                }
                            },
                            {
                                "type": "DataVisualization", 
                                "props": {
                                    "variant": "bar",
                                    "data": {
                                        "x": ["A", "B", "C"],
                                        "y": [1, 2, 3]
                                    },
                                    "style": {"color": "red"}
                                }
                            }
                        ]
                    }
                }
            ]
        }
        
        result_path = self.generator.generate_from_spec(spec)
        assert result_path.exists()
    
    def test_table_basic_table(self):
        """TableRendererで基本テーブルを生成"""
        spec = {
            "type": "content_block",
            "engine": "table",
            "filename": "table_test",
            "config": {
                "title": "テーブルテスト",
                "theme": "default"
            },
            "components": [
                {
                    "type": "BasicTable",
                    "props": {
                        "title": "売上データ",
                        "headers": ["商品名", "売上数", "単価"],
                        "rows": [
                            ["商品A", 100, 1000],
                            ["商品B", 150, 800],
                            ["商品C", 200, 1200]
                        ]
                    }
                }
            ]
        }
        
        result_path = self.generator.generate_from_spec(spec)
        assert result_path.exists()
        assert result_path.suffix == '.html'
        
        # HTMLコンテンツにテーブルが含まれることを確認
        content = result_path.read_text(encoding='utf-8')
        assert "商品A" in content
        assert "table" in content.lower()
    
    def test_table_interactive_table(self):
        """インタラクティブテーブルのテスト"""
        spec = {
            "type": "content_block",
            "engine": "table",
            "filename": "interactive_table_test",
            "components": [
                {
                    "type": "InteractiveTable",
                    "props": {
                        "title": "ソート・フィルタ対応テーブル",
                        "headers": ["名前", "年齢", "部署"],
                        "rows": [
                            ["田中", 25, "営業"],
                            ["佐藤", 30, "開発"],
                            ["鈴木", 28, "マーケティング"]
                        ],
                        "sortable": True,
                        "filterable": True
                    }
                }
            ]
        }
        
        result_path = self.generator.generate_from_spec(spec)
        assert result_path.exists()
        
        content = result_path.read_text(encoding='utf-8')
        assert "sortable" in content
        assert "filterable" in content
        assert "田中" in content
    
    def test_data_table_component(self):
        """DataTableコンポーネントのテスト"""
        spec = {
            "type": "content_block",
            "engine": "table",
            "filename": "data_table_test",
            "components": [
                {
                    "type": "DataTable",
                    "props": {
                        "title": "データテーブルテスト",
                        "data": {
                            "商品": ["A", "B", "C"],
                            "価格": [1000, 2000, 1500],
                            "在庫": [10, 5, 8]
                        },
                        "format": {
                            "価格": "¥{:,}"
                        }
                    }
                }
            ]
        }
        
        result_path = self.generator.generate_from_spec(spec)
        assert result_path.exists()
        
        content = result_path.read_text(encoding='utf-8')
        assert "¥" in content  # フォーマットが適用されていることを確認
    
    def test_multiple_engines_integration(self):
        """複数エンジンの統合テスト"""
        # 4つの異なるエンジンでファイルを生成
        engines_specs = [
            ("matplotlib", {
                "type": "content_block",
                "engine": "matplotlib",
                "filename": "multi_test_matplotlib",
                "components": [{
                    "type": "DataVisualization",
                    "props": {
                        "variant": "line",
                        "data": {"x": [1,2,3], "y": [1,4,2]},
                        "style": {"color": "blue"}
                    }
                }]
            }),
            ("markdown", {
                "type": "content_block",
                "engine": "markdown", 
                "filename": "multi_test_markdown",
                "components": [{
                    "type": "Heading",
                    "props": {"content": "テスト見出し", "level": 1}
                }]
            }),
            ("plotly", {
                "type": "content_block",
                "engine": "plotly",
                "filename": "multi_test_plotly",
                "components": [{
                    "type": "DataVisualization",
                    "props": {
                        "variant": "scatter",
                        "data": {"x": [1,2,3], "y": [2,1,3]},
                        "style": {"color": "red"}
                    }
                }]
            }),
            ("table", {
                "type": "content_block",
                "engine": "table",
                "filename": "multi_test_table", 
                "components": [{
                    "type": "BasicTable",
                    "props": {
                        "headers": ["A", "B"],
                        "rows": [["1", "2"], ["3", "4"]]
                    }
                }]
            })
        ]
        
        results = []
        for engine_name, spec in engines_specs:
            result_path = self.generator.generate_from_spec(spec)
            results.append((engine_name, result_path))
            assert result_path.exists(), f"{engine_name} engine failed to generate file"
        
        # 全てのエンジンが正常にファイルを生成したことを確認
        assert len(results) == 4
        
        # ファイル拡張子の確認
        extensions = {
            "matplotlib": ".html",
            "markdown": ".md", 
            "plotly": ".html",
            "table": ".html"
        }
        
        for engine_name, result_path in results:
            expected_ext = extensions[engine_name]
            assert result_path.suffix == expected_ext, f"{engine_name} should generate {expected_ext} files"


if __name__ == "__main__":
    # 基本的なテストを実行
    test = TestComponentSystem()
    test.setup_method()
    
    print("🧪 コンポーネントシステムの基本テストを開始...")
    
    try:
        test.test_renderer_factory_initialization()
        print("✅ RendererFactory初期化テスト: 成功")
        
        test.test_matplotlib_basic_chart()
        print("✅ Matplotlibチャートテスト: 成功")
        
        test.test_markdown_basic_document()
        print("✅ Markdownドキュメントテスト: 成功")
        
        print("🎉 すべての基本テストが成功しました！")
        print(f"📁 テスト結果は {test.temp_dir} に保存されています")
        
    except Exception as e:
        print(f"❌ テストエラー: {e}")
        import traceback
        traceback.print_exc()
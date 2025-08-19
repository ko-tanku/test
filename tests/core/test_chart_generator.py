"""
ChartGeneratorのテスト
"""

import pytest
import tempfile
from pathlib import Path
import sys
import os

# プロジェクトルートをpathに追加
project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.core.chart_generator import ChartGenerator
from src.core.config import GLOBAL_COLORS, BASE_CHART_STYLES


@pytest.fixture
def chart_generator():
    """ChartGeneratorのインスタンスを作成"""
    return ChartGenerator(GLOBAL_COLORS, BASE_CHART_STYLES)


@pytest.fixture
def temp_output_dir():
    """テスト用の一時ディレクトリを作成"""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


def test_chart_generator_initialization(chart_generator):
    """ChartGeneratorの初期化テスト"""
    assert chart_generator.colors == GLOBAL_COLORS
    assert chart_generator.styles == BASE_CHART_STYLES


def test_create_simple_line_chart(chart_generator, temp_output_dir):
    """線グラフ作成のテスト"""
    test_data = {
        'x': [1, 2, 3, 4, 5],
        'y': [2, 4, 6, 8, 10]
    }
    
    chart_path = chart_generator.create_simple_line_chart(
        data=test_data,
        x_col='x',
        y_col='y',
        title='テスト線グラフ',
        xlabel='X軸',
        ylabel='Y軸',
        output_filename='test_line_chart.html',
        use_plotly=False,
        output_dir=temp_output_dir
    )
    
    # ファイルが生成されたかを確認
    assert chart_path is not None
    assert chart_path.exists()
    assert chart_path.suffix == '.html'
    assert 'test_line_chart' in chart_path.name


def test_create_bar_chart(chart_generator, temp_output_dir):
    """棒グラフ作成のテスト"""
    test_data = {
        'category': ['A', 'B', 'C', 'D'],
        'value': [10, 25, 15, 30]
    }
    
    chart_path = chart_generator.create_bar_chart(
        data=test_data,
        x_col='category',
        y_col='value',
        title='テスト棒グラフ',
        xlabel='カテゴリ',
        ylabel='値',
        output_filename='test_bar_chart.html',
        use_plotly=False,
        output_dir=temp_output_dir
    )
    
    # ファイルが生成されたかを確認
    assert chart_path is not None
    assert chart_path.exists()
    assert chart_path.suffix == '.html'


def test_create_pie_chart(chart_generator, temp_output_dir):
    """円グラフ作成のテスト"""
    test_data = {
        'labels': ['項目A', '項目B', '項目C'],
        'values': [30, 45, 25]
    }
    
    chart_path = chart_generator.create_pie_chart(
        data=test_data,
        values_col='values',
        labels_col='labels',
        title='テスト円グラフ',
        output_filename='test_pie_chart.html',
        use_plotly=False,
        output_dir=temp_output_dir
    )
    
    # ファイルが生成されたかを確認
    assert chart_path is not None
    assert chart_path.exists()
    assert chart_path.suffix == '.html'


def test_invalid_data_handling(chart_generator, temp_output_dir):
    """無効なデータの処理テスト"""
    # 空のデータでテスト
    empty_data = {}
    
    chart_path = chart_generator.create_simple_line_chart(
        data=empty_data,
        x_col='x',
        y_col='y',
        title='空データテスト',
        xlabel='X軸',
        ylabel='Y軸',
        output_filename='empty_test.html',
        use_plotly=False,
        output_dir=temp_output_dir
    )
    
    # エラーハンドリングが適切に行われているかを確認
    # (実装によっては None が返されるか、例外が発生する可能性がある)
    # ここではファイルが生成されないことを確認
    expected_path = temp_output_dir / 'empty_test.html'
    assert not expected_path.exists() or chart_path is None


def test_plotly_chart_generation(chart_generator, temp_output_dir):
    """Plotlyを使用した図表生成のテスト"""
    test_data = {
        'x': [1, 2, 3, 4, 5],
        'y': [1, 4, 9, 16, 25]
    }
    
    chart_path = chart_generator.create_simple_line_chart(
        data=test_data,
        x_col='x',
        y_col='y',
        title='Plotlyテスト',
        xlabel='X軸',
        ylabel='Y軸',
        output_filename='plotly_test.html',
        use_plotly=True,
        output_dir=temp_output_dir
    )
    
    # ファイルが生成されたかを確認
    assert chart_path is not None
    assert chart_path.exists()
    
    # HTMLファイルの内容にplotlyが含まれているかを確認
    with open(chart_path, 'r', encoding='utf-8') as f:
        content = f.read()
        assert 'plotly' in content.lower() or 'Plotly' in content


if __name__ == "__main__":
    pytest.main([__file__])
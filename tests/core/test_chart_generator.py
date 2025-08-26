
import pytest
from pathlib import Path
from src.core.chart_generator import ChartGenerator

def test_create_bar_chart_creates_html_file(tmp_path):
    """
    create_bar_chartが指定されたパスにHTMLファイルを正しく生成することをテストする。
    """
    # 1. Arrange
    generator = ChartGenerator()
    test_data = {
        "x": ["A", "B", "C"],
        "y": [10, 20, 15]
    }
    output_dir = tmp_path
    filename = "test_chart.html"

    # 2. Act
    generated_file_path = generator.create_bar_chart(
        data=test_data,
        x_col="x",
        y_col="y",
        title="Test Chart",
        xlabel="Category",
        ylabel="Value",
        output_filename=filename,
        output_dir=output_dir
    )

    # 3. Assert
    assert generated_file_path.exists()
    assert generated_file_path.is_file()
    assert generated_file_path.name == filename

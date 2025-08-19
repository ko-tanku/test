"""
YAMLコンテンツとCSVデータ読み込みの統合テスト
"""

import pytest
import tempfile
from pathlib import Path
import sys
import os
import yaml
import pandas as pd

# プロジェクトルートをpathに追加
project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.core.content_manager import BaseContentManager
from src.materials.test_material.test_material_config import TEST_MATERIAL_COLORS


class TestContentManager(BaseContentManager):
    """テスト用のContentManager実装"""
    
    def generate_content(self):
        """テスト用の簡単な実装"""
        return []


@pytest.fixture
def temp_project_structure():
    """テスト用のプロジェクト構造を作成"""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # 必要なディレクトリ構造を作成
        data_dir = temp_path / "data"
        content_dir = temp_path / "src" / "materials" / "test_material" / "content"
        output_dir = temp_path / "docs" / "test_material"
        
        data_dir.mkdir(parents=True)
        content_dir.mkdir(parents=True)
        output_dir.mkdir(parents=True)
        
        # テスト用CSVファイルを作成
        test_csv = data_dir / "test_data.csv"
        test_data = pd.DataFrame({
            'year': [2020, 2021, 2022, 2023, 2024],
            'value': [100, 120, 140, 160, 180]
        })
        test_data.to_csv(test_csv, index=False)
        
        # テスト用YAMLファイルを作成
        test_yaml = content_dir / "test_chapter.yml"
        chapter_data = {
            'title': 'テスト章',
            'overview': 'テスト用の章です',
            'sections': [
                {
                    'title': 'セクション1',
                    'contents': [
                        {
                            'type': 'text',
                            'text': 'これはテスト用のテキストです。'
                        },
                        {
                            'type': 'chart',
                            'chart_type': 'line',
                            'data_source': 'test_data.csv',
                            'config': {
                                'x_col': 'year',
                                'y_col': 'value',
                                'title': 'テストグラフ',
                                'filename': 'test_chart'
                            }
                        }
                    ]
                }
            ]
        }
        
        with open(test_yaml, 'w', encoding='utf-8') as f:
            yaml.dump(chapter_data, f, allow_unicode=True, default_flow_style=False)
        
        yield {
            'project_root': temp_path,
            'data_dir': data_dir,
            'content_dir': content_dir,
            'output_dir': output_dir,
            'csv_file': test_csv,
            'yaml_file': test_yaml
        }


@pytest.fixture
def content_manager(temp_project_structure):
    """TestContentManagerのインスタンスを作成"""
    
    # BaseContentManagerを継承したクラスで、パスを直接設定
    class TestContentManagerWithPaths(TestContentManager):
        def __init__(self):
            material_name = "test_material"
            output_base_dir = temp_project_structure['output_dir']
            super().__init__(material_name, output_base_dir, TEST_MATERIAL_COLORS)
            
            # テスト用にパスを上書き
            self.project_root = temp_project_structure['project_root']
            self.data_dir = temp_project_structure['data_dir']
            self.content_dir = temp_project_structure['content_dir']
    
    return TestContentManagerWithPaths()


def test_load_csv_data(content_manager):
    """CSVデータ読み込みのテスト"""
    data = content_manager.load_data_from_csv("test_data.csv")
    
    # データが正しく読み込まれているかを確認
    assert 'year' in data
    assert 'value' in data
    assert len(data['year']) == 5
    assert data['year'][0] == 2020
    assert data['value'][-1] == 180


def test_load_yaml_content(content_manager):
    """YAMLコンテンツ読み込みのテスト"""
    chapter_data = content_manager.load_chapter_from_yaml("test_chapter.yml")
    
    # YAMLデータが正しく読み込まれているかを確認
    assert chapter_data['title'] == 'テスト章'
    assert chapter_data['overview'] == 'テスト用の章です'
    assert len(chapter_data['sections']) == 1
    assert chapter_data['sections'][0]['title'] == 'セクション1'


def test_nonexistent_csv_file(content_manager):
    """存在しないCSVファイルの処理テスト"""
    data = content_manager.load_data_from_csv("nonexistent.csv")
    
    # 空の辞書が返されることを確認
    assert data == {}


def test_nonexistent_yaml_file(content_manager):
    """存在しないYAMLファイルの処理テスト"""
    chapter_data = content_manager.load_chapter_from_yaml("nonexistent.yml")
    
    # 空の辞書が返されることを確認
    assert chapter_data == {}


def test_yaml_content_with_csv_reference(content_manager, temp_project_structure):
    """YAMLコンテンツ内でCSVファイルを参照するテスト"""
    chapter_data = content_manager.load_chapter_from_yaml("test_chapter.yml")
    
    # YAMLファイル内のCSV参照を確認
    chart_content = chapter_data['sections'][0]['contents'][1]
    assert chart_content['chart_type'] == 'line'
    assert chart_content['data_source'] == 'test_data.csv'
    
    # 実際にCSVデータを読み込んで確認
    csv_data = content_manager.load_data_from_csv(chart_content['data_source'])
    assert len(csv_data['year']) == 5
    assert csv_data['year'][0] == 2020


def test_process_content_list_with_external_data(content_manager, temp_project_structure):
    """外部データを使用したコンテンツリスト処理のテスト"""
    chapter_data = content_manager.load_chapter_from_yaml("test_chapter.yml")
    
    # 章データが正しく構造化されていることを確認
    section = chapter_data['sections'][0]
    contents = section['contents']
    
    # テキストコンテンツとチャートコンテンツが含まれていることを確認
    text_content = contents[0]
    chart_content = contents[1]
    
    assert text_content['type'] == 'text'
    assert text_content['text'] == 'これはテスト用のテキストです。'
    
    assert chart_content['type'] == 'chart'
    assert chart_content['chart_type'] == 'line'
    assert 'data_source' in chart_content


if __name__ == "__main__":
    pytest.main([__file__])
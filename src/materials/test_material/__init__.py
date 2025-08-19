"""
Test Material module
テスト資料を生成するためのモジュール
"""

from . import test_material_config
from . import test_material_terms
from . import test_material_charts  
from . import test_material_tables
from . import test_material_contents
from . import test_material_main

__all__ = [
    "test_material_config",
    "test_material_terms",
    "test_material_charts",
    "test_material_tables", 
    "test_material_contents",
    "test_material_main"
]
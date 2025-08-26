"""
統一コンポーネントシステム - Core モジュール

React風宣言的コンポーネントシステムのメインエントリーポイントです。
既存モジュールとの互換性を保ちつつ、新しいコンポーネントシステムを提供します。
"""

# 既存モジュール（後方互換性のため）
from . import base_config
from . import config
from . import utils
from . import document_builder
from . import chart_generator
from . import table_generator
from . import knowledge_manager
from . import content_manager

# 新しいコンポーネントシステム
from .component_renderer import (
    ComponentRenderer,
    BaseComponent,
    ComponentSpec,
    validate_content_spec,
    load_spec_from_yaml
)

from .renderer_factory import (
    RendererFactory,
    UniversalContentGenerator
)

from .matplotlib_renderer import MatplotlibRenderer
from .markdown_renderer import MarkdownRenderer
from .plotly_renderer import PlotlyRenderer
from .table_renderer import TableRenderer

# システム初期化
def initialize_component_system():
    """コンポーネントシステムを初期化"""
    # 標準レンダラーを登録
    RendererFactory.register_engine('matplotlib', MatplotlibRenderer)
    RendererFactory.register_engine('markdown', MarkdownRenderer)
    RendererFactory.register_engine('plotly', PlotlyRenderer)
    RendererFactory.register_engine('table', TableRenderer)

# 自動初期化
initialize_component_system()

# 公開API
__all__ = [
    # 既存モジュール（後方互換性）
    'base_config',
    'config',
    'utils',
    'document_builder',
    'chart_generator',
    'table_generator',
    'knowledge_manager',
    'content_manager',
    
    # 新しいコンポーネントシステム
    'ComponentRenderer',
    'BaseComponent',
    'ComponentSpec',
    'RendererFactory', 
    'UniversalContentGenerator',
    'MatplotlibRenderer',
    'MarkdownRenderer',
    'PlotlyRenderer',
    'TableRenderer',
    'validate_content_spec',
    'load_spec_from_yaml',
    'initialize_component_system'
]
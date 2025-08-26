"""
統一コンポーネントレンダリングシステムの基底クラス群

このモジュールは、PROJECT_BLUEPRINT.mdとUNIVERSAL_COMPONENT_DESIGN.mdに基づく
React風宣言的コンポーネントシステムの実装です。
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Type
from pathlib import Path
import yaml
import json
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class ComponentSpec:
    """コンポーネント仕様を格納するデータクラス"""
    type: str
    props: Dict[str, Any]
    children: Optional[List['ComponentSpec']] = None
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ComponentSpec':
        """辞書からComponentSpecを生成"""
        return cls(
            type=data.get('type', ''),
            props=data.get('props', {}),
            children=[cls.from_dict(child) for child in data.get('children', [])]
        )


class BaseComponent(ABC):
    """
    個別コンポーネントの基底クラス
    
    すべてのコンポーネントはこのクラスを継承し、render()メソッドを実装する必要があります。
    Reactコンポーネントの思想に基づき、propsから出力を生成する純粋関数として設計されています。
    """
    
    type_name: str = None
    required_props: List[str] = []
    optional_props: Dict[str, Any] = {}
    
    @classmethod
    @abstractmethod
    def render(cls, props: Dict[str, Any], renderer: 'ComponentRenderer') -> Any:
        """
        プロパティを受け取ってコンポーネントをレンダリング
        
        Args:
            props: コンポーネントのプロパティ
            renderer: 描画エンジン
            
        Returns:
            レンダリング結果（エンジン固有の形式）
        """
        pass
    
    @classmethod
    def validate_props(cls, props: Dict[str, Any]) -> Dict[str, Any]:
        """
        プロパティの検証と正規化
        
        Args:
            props: 検証するプロパティ
            
        Returns:
            正規化されたプロパティ
            
        Raises:
            ValueError: 必須プロパティが不足している場合
        """
        validated = props.copy()
        
        # 必須プロパティのチェック
        missing_props = [prop for prop in cls.required_props if prop not in props]
        if missing_props:
            raise ValueError(f"{cls.type_name}コンポーネントに必須プロパティが不足: {missing_props}")
        
        # オプショナルプロパティのデフォルト値設定
        for prop, default_value in cls.optional_props.items():
            if prop not in validated:
                validated[prop] = default_value
        
        return validated
    
    @classmethod
    def get_schema(cls) -> Dict[str, Any]:
        """コンポーネントのスキーマ情報を取得"""
        return {
            'type_name': cls.type_name,
            'required_props': cls.required_props,
            'optional_props': cls.optional_props,
            'description': cls.__doc__ or f"{cls.type_name}コンポーネント"
        }


class ComponentRenderer(ABC):
    """
    すべての描画エンジンの基底クラス
    
    各描画エンジン（matplotlib、plotly、markdown等）はこのクラスを継承し、
    統一されたインターフェースを提供します。
    """
    
    engine_name: str = None
    file_extension: str = None
    supported_component_types: List[str] = []
    
    def __init__(self, output_dir: Path, config: Optional[Dict] = None):
        """
        レンダラーを初期化
        
        Args:
            output_dir: 出力ディレクトリ
            config: エンジン固有の設定
        """
        self.output_dir = Path(output_dir)
        self.config = config or {}
        self.component_registry: Dict[str, Type[BaseComponent]] = {}
        self.global_context: Dict[str, Any] = {}
        
        # 出力ディレクトリを作成
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # デフォルトコンポーネントを登録
        self._register_default_components()
        
        logger.info(f"{self.engine_name}レンダラーを初期化しました。出力先: {self.output_dir}")
    
    @abstractmethod
    def _register_default_components(self):
        """デフォルトコンポーネントを登録"""
        pass
    
    def render_spec(self, spec: Dict[str, Any]) -> Path:
        """
        YAML仕様を受け取ってレンダリング
        
        Args:
            spec: レンダリング仕様
            
        Returns:
            生成されたファイルのパス
            
        Raises:
            ValueError: エンジンが一致しない、または仕様が不正な場合
        """
        # エンジン検証
        engine = spec.get('engine')
        if engine != self.engine_name:
            raise ValueError(f"エンジンが一致しません: {engine}, 期待値: {self.engine_name}")
        
        # グローバル設定を適用
        global_config = spec.get('config', {})
        self._apply_global_config(global_config)
        
        # コンポーネントリストを処理
        components = spec.get('components', [])
        component_specs = [ComponentSpec.from_dict(comp) for comp in components]
        
        rendered_content = self._render_components(component_specs)
        
        # ファイル保存
        filename = spec.get('filename', 'output')
        output_path = self._get_output_path(filename)
        
        self._save_rendered_content(rendered_content, output_path, global_config)
        
        logger.info(f"レンダリング完了: {output_path}")
        return output_path
    
    def _render_components(self, components: List[ComponentSpec]) -> Any:
        """
        コンポーネントリストをレンダリング
        
        Args:
            components: コンポーネント仕様のリスト
            
        Returns:
            レンダリング結果
        """
        rendered_items = []
        
        for component_spec in components:
            try:
                rendered_item = self._render_single_component(component_spec)
                if rendered_item is not None:
                    rendered_items.append(rendered_item)
            except Exception as e:
                logger.error(f"コンポーネント {component_spec.type} のレンダリングに失敗: {e}")
                # エラー時はスキップして続行
                continue
        
        return rendered_items
    
    def _render_single_component(self, component_spec: ComponentSpec) -> Any:
        """
        単一のコンポーネントをレンダリング
        
        Args:
            component_spec: コンポーネント仕様
            
        Returns:
            レンダリング結果
            
        Raises:
            ValueError: サポートされていないコンポーネントタイプの場合
        """
        component_type = component_spec.type
        props = component_spec.props
        
        if component_type not in self.component_registry:
            raise ValueError(f"サポートされていないコンポーネントタイプ: {component_type}")
        
        component_class = self.component_registry[component_type]
        
        # プロパティを検証・正規化
        validated_props = component_class.validate_props(props)
        
        # 子コンポーネントがある場合は先に処理
        if component_spec.children:
            child_results = self._render_components(component_spec.children)
            validated_props['children'] = child_results
        
        # コンポーネントをレンダリング
        return component_class.render(validated_props, self)
    
    def register_component(self, component_class: Type[BaseComponent]):
        """
        カスタムコンポーネントを登録
        
        Args:
            component_class: コンポーネントクラス
        """
        if not issubclass(component_class, BaseComponent):
            raise ValueError("BaseComponentを継承したクラスを指定してください")
        
        if not component_class.type_name:
            raise ValueError("type_nameが設定されていません")
        
        self.component_registry[component_class.type_name] = component_class
        logger.info(f"コンポーネント '{component_class.type_name}' を登録しました")
    
    def get_registered_components(self) -> Dict[str, Dict[str, Any]]:
        """登録されているコンポーネントの一覧とスキーマを取得"""
        return {
            name: component_class.get_schema()
            for name, component_class in self.component_registry.items()
        }
    
    def _get_output_path(self, filename: str) -> Path:
        """出力ファイルのパスを生成"""
        if not filename.endswith(f'.{self.file_extension}'):
            filename += f'.{self.file_extension}'
        return self.output_dir / filename
    
    @abstractmethod
    def _apply_global_config(self, config: Dict[str, Any]):
        """
        グローバル設定を適用
        
        Args:
            config: グローバル設定
        """
        pass
    
    @abstractmethod  
    def _save_rendered_content(self, content: Any, output_path: Path, config: Dict[str, Any]):
        """
        レンダリング結果をファイルに保存
        
        Args:
            content: レンダリング結果
            output_path: 出力ファイルパス
            config: グローバル設定
        """
        pass
    
    def set_global_context(self, context: Dict[str, Any]):
        """グローバルコンテキストを設定（コンポーネント間で共有される情報）"""
        self.global_context.update(context)
    
    def get_global_context(self, key: str, default: Any = None) -> Any:
        """グローバルコンテキストから値を取得"""
        return self.global_context.get(key, default)


class RendererError(Exception):
    """レンダリング関連のエラー"""
    pass


class ComponentValidationError(Exception):
    """コンポーネント検証エラー"""
    pass


def validate_content_spec(spec: Dict[str, Any]) -> Dict[str, Any]:
    """
    コンテンツ仕様の基本検証
    
    Args:
        spec: 検証する仕様
        
    Returns:
        検証済みの仕様
        
    Raises:
        ValueError: 仕様が不正な場合
    """
    if not isinstance(spec, dict):
        raise ValueError("仕様は辞書形式である必要があります")
    
    if 'engine' not in spec:
        raise ValueError("'engine'フィールドが必要です")
    
    if 'components' not in spec:
        raise ValueError("'components'フィールドが必要です")
    
    if not isinstance(spec['components'], list):
        raise ValueError("'components'はリスト形式である必要があります")
    
    return spec


def load_spec_from_yaml(yaml_path: Path) -> Dict[str, Any]:
    """
    YAMLファイルから仕様を読み込み
    
    Args:
        yaml_path: YAMLファイルのパス
        
    Returns:
        読み込まれた仕様
        
    Raises:
        FileNotFoundError: ファイルが見つからない場合
        yaml.YAMLError: YAML解析エラー
    """
    if not yaml_path.exists():
        raise FileNotFoundError(f"YAMLファイルが見つかりません: {yaml_path}")
    
    try:
        with open(yaml_path, 'r', encoding='utf-8') as f:
            spec = yaml.safe_load(f)
        
        return validate_content_spec(spec)
    
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"YAML解析エラー: {e}")
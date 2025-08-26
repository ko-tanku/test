"""
レンダラーファクトリとコンテンツジェネレータ

統一的なインターフェースで異なる描画エンジンを管理し、
YAMLベースのコンテンツ生成を提供します。
"""

from typing import Dict, List, Optional, Type, Union
from pathlib import Path
import logging

from .component_renderer import (
    ComponentRenderer, 
    load_spec_from_yaml, 
    validate_content_spec
)

logger = logging.getLogger(__name__)


class RendererFactory:
    """
    描画エンジンファクトリ
    
    異なる描画エンジンの統一的な作成・管理を行います。
    新しいエンジンも動的に登録可能です。
    """
    
    # 登録された描画エンジン
    _engines: Dict[str, Type[ComponentRenderer]] = {}
    
    @classmethod
    def register_engine(cls, name: str, renderer_class: Type[ComponentRenderer]):
        """
        新しい描画エンジンを登録
        
        Args:
            name: エンジン名
            renderer_class: レンダラークラス
            
        Raises:
            ValueError: 不正なレンダラークラスの場合
        """
        if not issubclass(renderer_class, ComponentRenderer):
            raise ValueError("ComponentRendererを継承したクラスを指定してください")
        
        if not renderer_class.engine_name:
            raise ValueError("engine_nameが設定されていません")
        
        if name != renderer_class.engine_name:
            logger.warning(f"エンジン名が一致しません: {name} != {renderer_class.engine_name}")
        
        cls._engines[name] = renderer_class
        logger.info(f"描画エンジン '{name}' を登録しました")
    
    @classmethod
    def create_renderer(
        cls, 
        engine: str, 
        output_dir: Union[str, Path], 
        config: Optional[Dict] = None
    ) -> ComponentRenderer:
        """
        指定されたエンジンのレンダラーを作成
        
        Args:
            engine: エンジン名
            output_dir: 出力ディレクトリ
            config: エンジン固有の設定
            
        Returns:
            作成されたレンダラー
            
        Raises:
            ValueError: サポートされていないエンジンの場合
        """
        if engine not in cls._engines:
            available_engines = list(cls._engines.keys())
            raise ValueError(
                f"サポートされていないエンジン: {engine}. "
                f"利用可能: {available_engines}"
            )
        
        renderer_class = cls._engines[engine]
        return renderer_class(Path(output_dir), config)
    
    @classmethod
    def get_available_engines(cls) -> List[str]:
        """利用可能なエンジン一覧を取得"""
        return list(cls._engines.keys())
    
    @classmethod
    def get_engine_info(cls, engine: str) -> Dict[str, any]:
        """エンジンの詳細情報を取得"""
        if engine not in cls._engines:
            raise ValueError(f"エンジンが見つかりません: {engine}")
        
        renderer_class = cls._engines[engine]
        return {
            'engine_name': renderer_class.engine_name,
            'file_extension': renderer_class.file_extension,
            'supported_components': renderer_class.supported_component_types,
            'description': renderer_class.__doc__ or f"{engine}レンダラー"
        }
    
    @classmethod
    def is_engine_available(cls, engine: str) -> bool:
        """エンジンが利用可能かチェック"""
        return engine in cls._engines


class UniversalContentGenerator:
    """
    すべてのコンテンツ生成の統一エントリーポイント
    
    YAMLファイルまたは辞書仕様から、適切なレンダラーを選択して
    コンテンツを生成します。複数のコンテンツを一括処理することも可能です。
    """
    
    def __init__(self, output_dir: Union[str, Path], default_config: Optional[Dict] = None):
        """
        コンテンツジェネレータを初期化
        
        Args:
            output_dir: 出力ベースディレクトリ
            default_config: デフォルト設定
        """
        self.output_dir = Path(output_dir)
        self.default_config = default_config or {}
        
        # 出力ディレクトリを作成
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"UniversalContentGeneratorを初期化しました。出力先: {self.output_dir}")
    
    def generate_from_yaml(self, yaml_path: Union[str, Path]) -> Path:
        """
        YAMLファイルからコンテンツを生成
        
        Args:
            yaml_path: YAMLファイルのパス
            
        Returns:
            生成されたファイルのパス
            
        Raises:
            FileNotFoundError: YAMLファイルが見つからない場合
            ValueError: YAML仕様が不正な場合
        """
        yaml_path = Path(yaml_path)
        logger.info(f"YAMLファイルからコンテンツを生成: {yaml_path}")
        
        try:
            spec = load_spec_from_yaml(yaml_path)
            return self.generate_from_spec(spec)
        except Exception as e:
            logger.error(f"YAMLファイルからの生成に失敗: {yaml_path}, エラー: {e}")
            raise
    
    def generate_from_spec(self, spec: Dict[str, any]) -> Path:
        """
        仕様辞書からコンテンツを生成
        
        Args:
            spec: レンダリング仕様
            
        Returns:
            生成されたファイルのパス
            
        Raises:
            ValueError: 仕様が不正な場合
        """
        spec = validate_content_spec(spec)
        
        engine = spec.get('engine')
        if not RendererFactory.is_engine_available(engine):
            raise ValueError(f"エンジンが利用できません: {engine}")
        
        # デフォルト設定を適用
        merged_config = self.default_config.copy()
        if 'config' in spec:
            merged_config.update(spec['config'])
        spec['config'] = merged_config
        
        logger.info(f"コンテンツを生成中: エンジン={engine}")
        
        try:
            renderer = RendererFactory.create_renderer(
                engine, 
                self.output_dir, 
                merged_config
            )
            return renderer.render_spec(spec)
        except Exception as e:
            logger.error(f"コンテンツ生成に失敗: エンジン={engine}, エラー: {e}")
            raise
    
    def generate_multiple(
        self, 
        specs: List[Dict[str, any]], 
        continue_on_error: bool = True
    ) -> List[Optional[Path]]:
        """
        複数の仕様を一括生成
        
        Args:
            specs: レンダリング仕様のリスト
            continue_on_error: エラー時に処理を続行するか
            
        Returns:
            生成されたファイルのパスのリスト（エラー時はNone）
        """
        results = []
        
        for i, spec in enumerate(specs):
            try:
                result = self.generate_from_spec(spec)
                results.append(result)
                logger.info(f"生成完了 ({i+1}/{len(specs)}): {result}")
            except Exception as e:
                logger.error(f"生成失敗 ({i+1}/{len(specs)}): {e}")
                results.append(None)
                
                if not continue_on_error:
                    raise
        
        return results
    
    def generate_from_yaml_directory(
        self, 
        yaml_dir: Union[str, Path], 
        pattern: str = "*.yml",
        recursive: bool = True
    ) -> List[Optional[Path]]:
        """
        ディレクトリ内のYAMLファイルを一括処理
        
        Args:
            yaml_dir: YAMLファイルが格納されたディレクトリ
            pattern: ファイル名パターン
            recursive: 再帰的にサブディレクトリも検索するか
            
        Returns:
            生成されたファイルのパスのリスト
        """
        yaml_dir = Path(yaml_dir)
        
        if not yaml_dir.exists():
            raise FileNotFoundError(f"ディレクトリが見つかりません: {yaml_dir}")
        
        # YAMLファイルを検索
        if recursive:
            yaml_files = list(yaml_dir.rglob(pattern))
        else:
            yaml_files = list(yaml_dir.glob(pattern))
        
        if not yaml_files:
            logger.warning(f"YAMLファイルが見つかりません: {yaml_dir}/{pattern}")
            return []
        
        logger.info(f"{len(yaml_files)}個のYAMLファイルを発見: {yaml_dir}")
        
        results = []
        for yaml_file in yaml_files:
            try:
                result = self.generate_from_yaml(yaml_file)
                results.append(result)
            except Exception as e:
                logger.error(f"ファイル処理失敗: {yaml_file}, エラー: {e}")
                results.append(None)
        
        return results
    
    def validate_yaml_directory(
        self, 
        yaml_dir: Union[str, Path], 
        pattern: str = "*.yml"
    ) -> Dict[str, any]:
        """
        ディレクトリ内のYAMLファイルを検証
        
        Args:
            yaml_dir: YAMLファイルが格納されたディレクトリ
            pattern: ファイル名パターン
            
        Returns:
            検証結果の辞書
        """
        yaml_dir = Path(yaml_dir)
        yaml_files = list(yaml_dir.glob(pattern))
        
        validation_results = {
            'total_files': len(yaml_files),
            'valid_files': 0,
            'invalid_files': 0,
            'errors': []
        }
        
        for yaml_file in yaml_files:
            try:
                load_spec_from_yaml(yaml_file)
                validation_results['valid_files'] += 1
            except Exception as e:
                validation_results['invalid_files'] += 1
                validation_results['errors'].append({
                    'file': str(yaml_file),
                    'error': str(e)
                })
        
        return validation_results
    
    def get_system_info(self) -> Dict[str, any]:
        """システム情報を取得"""
        return {
            'output_dir': str(self.output_dir),
            'available_engines': RendererFactory.get_available_engines(),
            'default_config': self.default_config
        }
"""
mkdocs.ymlファイルの動的生成・更新を管理
"""

import yaml
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
from .config import MKDOCS_SITE_CONFIG, PATHS

logger = logging.getLogger(__name__)


@dataclass
class NavItem:
    """ナビゲーションアイテムの定義"""
    title: str
    path: Optional[str] = None
    children: Optional[List['NavItem']] = None
    
    def to_dict(self) -> Dict[str, Union[str, List]]:
        """辞書形式に変換"""
        if self.children:
            return {self.title: [child.to_dict() for child in self.children]}
        else:
            return {self.title: self.path}


class MkDocsManager:
    """mkdocs.yml設定ファイルの管理"""
    
    def __init__(self, project_root: Path):
        """
        初期化
        
        Args:
            project_root: プロジェクトルートディレクトリ
        """
        self.project_root = project_root
        self.mkdocs_yml_path = project_root / "mkdocs.yml"
        self.config_history = []
        
    def generate_mkdocs_yml(
        self, 
        nav_structure: Union[List[Dict[str, Any]], List[NavItem]],
        custom_config: Optional[Dict[str, Any]] = None,
        backup: bool = True
    ) -> Path:
        """
        mkdocs.ymlファイルを生成
        
        Args:
            nav_structure: ナビゲーション構造
            custom_config: カスタム設定（オプション）
            backup: 既存ファイルのバックアップを作成するか
            
        Returns:
            生成されたmkdocs.ymlファイルのパス
        """
        # 既存ファイルのバックアップ
        if backup and self.mkdocs_yml_path.exists():
            self._create_backup()
        
        # ベース設定のコピー
        config = MKDOCS_SITE_CONFIG.copy()
        
        # ナビゲーション構造の変換・設定
        if isinstance(nav_structure[0], NavItem):
            nav_dict = [item.to_dict() for item in nav_structure]
        else:
            nav_dict = nav_structure
        config['nav'] = nav_dict
        
        # カスタム設定のマージ
        if custom_config:
            config = self._deep_merge_dict(config, custom_config)
        
        # アセットファイルの自動検出・追加
        self._auto_detect_assets(config)
        
        # プラグインの自動設定
        self._configure_plugins(config)
        
        # YAML形式で保存
        self._save_config(config)
        
        # 履歴に追加
        self.config_history.append({
            'timestamp': self._get_timestamp(),
            'config': config.copy(),
            'nav_items_count': len(nav_dict)
        })
        
        logger.info(f"mkdocs.yml生成完了: {self.mkdocs_yml_path}")
        return self.mkdocs_yml_path
    
    def update_config_section(
        self, 
        section: str, 
        content: Any,
        merge_mode: bool = True
    ) -> Path:
        """
        設定ファイルの特定セクションのみを更新
        
        Args:
            section: 更新対象セクション名
            content: 新しい内容
            merge_mode: マージモード（True）か置換モード（False）
            
        Returns:
            更新されたファイルのパス
        """
        if not self.mkdocs_yml_path.exists():
            logger.warning("mkdocs.ymlファイルが存在しません。新規作成します。")
            return self.generate_mkdocs_yml([])
        
        try:
            with open(self.mkdocs_yml_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f) or {}
            
            if merge_mode and isinstance(content, dict) and section in config:
                if isinstance(config[section], dict):
                    config[section].update(content)
                else:
                    config[section] = content
            else:
                config[section] = content
            
            self._save_config(config)
            logger.info(f"mkdocs.ymlの{section}セクションを更新しました")
            
        except Exception as e:
            logger.error(f"設定更新中にエラーが発生: {e}")
            raise
            
        return self.mkdocs_yml_path
    
    def add_nav_item(
        self, 
        nav_item: Union[Dict[str, str], NavItem],
        parent_path: Optional[str] = None,
        position: Optional[int] = None
    ) -> Path:
        """
        ナビゲーションアイテムを追加
        
        Args:
            nav_item: 追加するナビゲーションアイテム
            parent_path: 親項目のパス（ネストした追加の場合）
            position: 挿入位置（省略時は末尾）
            
        Returns:
            更新されたファイルのパス
        """
        config = self._load_current_config()
        nav = config.get('nav', [])
        
        # NavItemの場合は辞書に変換
        if isinstance(nav_item, NavItem):
            nav_item_dict = nav_item.to_dict()
        else:
            nav_item_dict = nav_item
        
        if parent_path:
            # ネストした追加（実装は省略 - 再帰的に親を検索して追加）
            nav = self._add_nested_nav_item(nav, nav_item_dict, parent_path)
        else:
            # ルートレベルに追加
            if position is not None:
                nav.insert(position, nav_item_dict)
            else:
                nav.append(nav_item_dict)
        
        return self.update_config_section('nav', nav, merge_mode=False)
    
    def remove_nav_item(self, item_title: str) -> Path:
        """
        ナビゲーションアイテムを削除
        
        Args:
            item_title: 削除するアイテムのタイトル
            
        Returns:
            更新されたファイルのパス
        """
        config = self._load_current_config()
        nav = config.get('nav', [])
        
        # 指定タイトルのアイテムを削除
        nav = [item for item in nav if not self._nav_item_matches_title(item, item_title)]
        
        return self.update_config_section('nav', nav, merge_mode=False)
    
    def add_asset_files(self, css_files: List[str] = None, js_files: List[str] = None) -> Path:
        """
        CSSやJSファイルを設定に追加
        
        Args:
            css_files: 追加するCSSファイルのリスト
            js_files: 追加するJavaScriptファイルのリスト
            
        Returns:
            更新されたファイルのパス
        """
        config = self._load_current_config()
        
        if css_files:
            existing_css = config.get('extra_css', [])
            new_css = list(set(existing_css + css_files))  # 重複除去
            config['extra_css'] = new_css
        
        if js_files:
            existing_js = config.get('extra_javascript', [])
            new_js = list(set(existing_js + js_files))  # 重複除去
            config['extra_javascript'] = new_js
        
        self._save_config(config)
        logger.info("アセットファイルを設定に追加しました")
        return self.mkdocs_yml_path
    
    def validate_config(self) -> Dict[str, List[str]]:
        """
        現在の設定を検証
        
        Returns:
            検証結果（エラー・警告のリスト）
        """
        issues = {'errors': [], 'warnings': []}
        
        if not self.mkdocs_yml_path.exists():
            issues['errors'].append("mkdocs.ymlファイルが存在しません")
            return issues
        
        try:
            config = self._load_current_config()
            
            # 必須項目のチェック
            required_fields = ['site_name', 'theme']
            for field in required_fields:
                if field not in config:
                    issues['errors'].append(f"必須項目 '{field}' が設定されていません")
            
            # ナビゲーション項目のファイル存在チェック
            docs_dir = self.project_root / "docs"
            nav_issues = self._validate_nav_files(config.get('nav', []), docs_dir)
            issues['warnings'].extend(nav_issues)
            
            # アセットファイルの存在チェック
            asset_issues = self._validate_asset_files(config, docs_dir)
            issues['warnings'].extend(asset_issues)
            
        except Exception as e:
            issues['errors'].append(f"設定ファイルの読み込みエラー: {e}")
        
        return issues
    
    def export_config_info(self) -> Dict[str, Any]:
        """
        現在の設定情報をエクスポート
        
        Returns:
            設定情報の辞書
        """
        config = self._load_current_config()
        
        return {
            'file_path': str(self.mkdocs_yml_path),
            'site_name': config.get('site_name', 'Unknown'),
            'theme_name': config.get('theme', {}).get('name', 'Unknown'),
            'nav_items_count': len(config.get('nav', [])),
            'css_files_count': len(config.get('extra_css', [])),
            'js_files_count': len(config.get('extra_javascript', [])),
            'plugins_count': len(config.get('plugins', [])),
            'markdown_extensions_count': len(config.get('markdown_extensions', [])),
            'last_modified': self._get_file_modified_time(),
            'validation_results': self.validate_config()
        }
    
    def _load_current_config(self) -> Dict[str, Any]:
        """現在の設定を読み込み"""
        try:
            with open(self.mkdocs_yml_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except FileNotFoundError:
            return {}
    
    def _save_config(self, config: Dict[str, Any]):
        """設定をファイルに保存"""
        with open(self.mkdocs_yml_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True, indent=2)
    
    def _auto_detect_assets(self, config: Dict[str, Any]):
        """アセットファイルを自動検出して設定に追加"""
        docs_dir = self.project_root / "docs"
        
        # CSSファイルの検出
        css_files = []
        for css_pattern in ["custom*.css", "style*.css", "theme*.css"]:
            css_files.extend([f.name for f in docs_dir.glob(css_pattern)])
        
        if css_files:
            config["extra_css"] = list(set(config.get("extra_css", []) + css_files))
            
        # JSファイルの検出
        js_files = []
        for js_pattern in ["custom*.js", "script*.js"]:
            js_files.extend([f.name for f in docs_dir.glob(js_pattern)])
            
        if js_files:
            config["extra_javascript"] = list(set(config.get("extra_javascript", []) + js_files))
    
    def _configure_plugins(self, config: Dict[str, Any]):
        """プラグインの自動設定"""
        # 基本的なプラグインを自動で有効化
        plugins = config.get('plugins', [])
        
        # 検索プラグインの追加
        if 'search' not in [p.get('search') if isinstance(p, dict) else p for p in plugins]:
            plugins.append('search')
        
        # Mermaid図表プラグインの追加
        if 'mermaid2' not in [p.get('mermaid2') if isinstance(p, dict) else p for p in plugins]:
            plugins.append('mermaid2')
        
        config['plugins'] = plugins
    
    def _create_backup(self):
        """既存ファイルのバックアップを作成"""
        timestamp = self._get_timestamp().replace(':', '-').replace(' ', '_')
        backup_path = self.mkdocs_yml_path.with_suffix(f'.yml.backup_{timestamp}')
        backup_path.write_text(self.mkdocs_yml_path.read_text(encoding='utf-8'), encoding='utf-8')
        logger.info(f"バックアップ作成: {backup_path}")
    
    def _deep_merge_dict(self, base: Dict, overlay: Dict) -> Dict:
        """辞書の深いマージを実行"""
        result = base.copy()
        for key, value in overlay.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge_dict(result[key], value)
            else:
                result[key] = value
        return result
    
    def _get_timestamp(self) -> str:
        """現在のタイムスタンプを取得"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def _get_file_modified_time(self) -> str:
        """ファイルの最終更新時刻を取得"""
        if self.mkdocs_yml_path.exists():
            import os
            from datetime import datetime
            timestamp = os.path.getmtime(self.mkdocs_yml_path)
            return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
        return "ファイルなし"
        
    def _validate_nav_files(self, nav_items: List[Dict], docs_dir: Path) -> List[str]:
        """ナビゲーション項目のファイル存在を検証"""
        warnings = []
        
        def check_nav_item(item):
            if isinstance(item, dict):
                for key, value in item.items():
                    if isinstance(value, str):
                        # ファイルパスの場合
                        file_path = docs_dir / value
                        if not file_path.exists():
                            warnings.append(f"ナビゲーション項目のファイルが見つかりません: {value}")
                    elif isinstance(value, list):
                        # ネストした項目の場合
                        for sub_item in value:
                            check_nav_item(sub_item)
        
        for item in nav_items:
            check_nav_item(item)
        
        return warnings
    
    def _validate_asset_files(self, config: Dict, docs_dir: Path) -> List[str]:
        """アセットファイルの存在を検証"""
        warnings = []
        
        # CSSファイルの検証
        for css_file in config.get('extra_css', []):
            if not (docs_dir / css_file).exists():
                warnings.append(f"CSSファイルが見つかりません: {css_file}")
        
        # JSファイルの検証
        for js_file in config.get('extra_javascript', []):
            if not (docs_dir / js_file).exists():
                warnings.append(f"JavaScriptファイルが見つかりません: {js_file}")
        
        return warnings
    
    def _add_nested_nav_item(self, nav: List, new_item: Dict, parent_path: str) -> List:
        """ネストしたナビゲーションアイテムを追加（再帰的）"""
        # 実装は複雑になるため、基本的な処理のみ示す
        for i, item in enumerate(nav):
            if isinstance(item, dict):
                for key, value in item.items():
                    if key == parent_path and isinstance(value, list):
                        value.append(new_item)
                        return nav
                    elif isinstance(value, list):
                        nav[i][key] = self._add_nested_nav_item(value, new_item, parent_path)
        return nav
    
    def _nav_item_matches_title(self, item: Dict, title: str) -> bool:
        """ナビゲーションアイテムのタイトルが一致するかチェック"""
        if isinstance(item, dict):
            return title in item
        return False
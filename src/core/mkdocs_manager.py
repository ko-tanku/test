"""
mkdocs.ymlファイルの動的生成・更新を管理
"""

import yaml
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from .config import MKDOCS_SITE_CONFIG

logger = logging.getLogger(__name__)


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
        
    def generate_mkdocs_yml(
        self, 
        nav_structure: List[Dict[str, Any]],
        custom_config: Optional[Dict[str, Any]] = None
    ) -> Path:
        """
        mkdocs.ymlファイルを生成
        
        Args:
            nav_structure: ナビゲーション構造
            custom_config: カスタム設定（オプション）
            
        Returns:
            生成されたmkdocs.ymlファイルのパス
        """
        config = MKDOCS_SITE_CONFIG.copy()
        
        # ナビゲーション構造を設定
        config['nav'] = nav_structure
        
        # カスタム設定のマージ
        if custom_config:
            config = self._deep_merge_dict(config, custom_config)
        
        # アセットファイルの存在確認と自動追加
        docs_dir = self.project_root / "docs"
        
        # CSSファイルの確認
        css_files = []
        for css_file in ["custom.css", "custom_dark.css", "custom_high_contrast.css"]:
            if (docs_dir / css_file).exists():
                css_files.append(css_file)
        
        if css_files:
            config["extra_css"] = css_files
            
        # JSファイルの確認
        js_files = []
        for js_file in ["custom.js"]:
            if (docs_dir / js_file).exists():
                js_files.append(js_file)
                
        if js_files:
            config["extra_javascript"] = js_files
        
        # YAML形式で保存
        with open(self.mkdocs_yml_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True, indent=2)
        
        logger.info(f"mkdocs.yml生成完了: {self.mkdocs_yml_path}")
        return self.mkdocs_yml_path
    
    def _deep_merge_dict(self, base: Dict, overlay: Dict) -> Dict:
        """辞書の深いマージを実行"""
        result = base.copy()
        for key, value in overlay.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge_dict(result[key], value)
            else:
                result[key] = value
        return result
    
    def update_nav_section(self, nav_structure: List[Dict[str, Any]]):
        """既存のmkdocs.ymlのnavセクションのみを更新"""
        if not self.mkdocs_yml_path.exists():
            logger.warning("mkdocs.ymlファイルが存在しません。新規作成します。")
            return self.generate_mkdocs_yml(nav_structure)
        
        try:
            with open(self.mkdocs_yml_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            config['nav'] = nav_structure
            
            with open(self.mkdocs_yml_path, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, default_flow_style=False, allow_unicode=True, indent=2)
            
            logger.info("mkdocs.ymlのnavセクションを更新しました")
            
        except Exception as e:
            logger.error(f"mkdocs.yml更新中にエラーが発生: {e}")
            raise
"""
テスト資料生成のメインエントリポイント
このファイルを実行すると、テスト資料が自動生成される
"""

import sys
import logging
from pathlib import Path
import yaml
from typing import Dict, Any

# プロジェクトルートをsys.pathに追加
project_root = Path(__file__).resolve().parents[3]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.core.config import PATHS, MKDOCS_SITE_CONFIG
from src.materials.test_material.test_material_config import (
    MATERIAL_CONFIG, MKDOCS_MATERIAL_OVERRIDE
)
from src.materials.test_material.test_material_contents import TestMaterialContentManager

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def update_mkdocs_config(material_config: Dict[str, Any]) -> None:
    """
    mkdocs.ymlにテスト資料のナビゲーションを追加
    
    Args:
        material_config: 資料の設定情報
    """
    mkdocs_yml_path = project_root / "mkdocs.yml"
    
    try:
        # 既存の設定を読み込み
        if mkdocs_yml_path.exists():
            with open(mkdocs_yml_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f) or {}
        else:
            config = MKDOCS_SITE_CONFIG.copy()
        
        # Material設定のオーバーライド適用
        if MKDOCS_MATERIAL_OVERRIDE:
            for key, value in MKDOCS_MATERIAL_OVERRIDE.items():
                if key in config:
                    if isinstance(value, dict) and isinstance(config[key], dict):
                        config[key].update(value)
                    else:
                        config[key] = value
        
        # ナビゲーションの更新
        if 'nav' not in config:
            config['nav'] = []
        
        # テスト資料のナビゲーション項目
        test_material_nav = {
            material_config["title"]: [
                {"ホーム": "test_material/index.md"},
                {"第1章: 基本要素": "test_material/documents/chapter01.md"},
                {"第2章: ツールチップ": "test_material/documents/chapter02.md"},
                {"第3章: 図表": "test_material/documents/chapter03.md"},
                {"第4章: 演習": "test_material/documents/chapter04.md"},
                {"用語集": "test_material/glossary.md"},
                {"FAQ": "test_material/faq.md"},
                {"TIPS": "test_material/tips.md"}
            ]
        }

        # 既存のテスト資料項目を削除（重複防止）
        config['nav'] = [
            item for item in config['nav'] 
            if not isinstance(item, dict) or material_config["title"] not in item
        ]

        # テスト資料を追加
        config['nav'].append(test_material_nav)

        # YAMLファイルに保存
        with open(mkdocs_yml_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        
        logger.info("mkdocs.ymlを更新しました")
        
    except Exception as e:
        logger.error(f"mkdocs.yml更新中にエラーが発生しました: {e}")
        raise


def create_test_material() -> None:
    """
    テスト資料を生成するメイン関数
    """
    logger.info("テスト資料の生成を開始します...")
    
    try:
        # 出力ディレクトリの設定
        output_dir = PATHS["TEST_MATERIAL_DIR"]
        logger.info(f"出力ディレクトリ: {output_dir}")
        
        # コンテンツマネージャーの初期化
        content_manager = TestMaterialContentManager(
            material_name="test_material",
            output_base_dir=output_dir
        )
        
        # コンテンツの生成
        logger.info("コンテンツを生成中...")
        generated_files = content_manager.generate_content()
        
        logger.info(f"生成されたファイル数: {len(generated_files)}")
        for file_path in generated_files:
            logger.info(f"  - {file_path}")
        
        # mkdocs.ymlの更新
        logger.info("mkdocs.ymlを更新中...")
        update_mkdocs_config(MATERIAL_CONFIG)
        
        logger.info("テスト資料の生成が完了しました！")
        logger.info("\n実行方法:")
        logger.info("  1. プロジェクトルートで: mkdocs serve")
        logger.info("  2. ブラウザで: http://127.0.0.1:8000")
        
    except Exception as e:
        logger.error(f"テスト資料生成中にエラーが発生しました: {e}")
        logger.exception("詳細なエラー情報:")
        raise


if __name__ == "__main__":
    """
    直接実行時のエントリポイント
    """
    try:
        create_test_material()
    except KeyboardInterrupt:
        logger.info("\n処理が中断されました")
        sys.exit(1)
    except Exception as e:
        logger.error(f"予期しないエラーが発生しました: {e}")
        sys.exit(1)
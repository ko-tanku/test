import sys
import logging
from pathlib import Path

# プロジェクトルートをsys.pathに追加
project_root = Path(__file__).resolve().parents[3]
sys.path.append(str(project_root))

from src.core.mkdocs_manager import MkDocsManager
from src.core.asset_generator import AssetGenerator
from src.materials.test_material.contents import TestMaterialContentManager

# ロギング設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    """
    test_materialのビルドプロセス全体を実行するメイン関数。
    """
    logging.info("test_materialのビルドプロセスを開始します...")

    # --- 1. パスの設定 ---
    # このスクリプトの場所を基準に、プロジェクトルートと出力ディレクトリを決定
    material_root = Path(__file__).parent
    output_dir = project_root / "docs"
    content_config_path = material_root / "content" / "config.yml"

    # --- 2. MkDocs設定の生成 ---
    logging.info("mkdocs.ymlを生成しています...")
    mkdocs_mgr = MkDocsManager(project_root)
    # TODO: 本来はconfig.ymlからナビゲーション構造を読み込む
    # 今回はテストのため、静的なナビゲーション構造を定義
    nav_structure = [
        {"ホーム": "index.md"}, # サイトのトップレベルのindex.md
        {
            "テスト教材": [
                {"概要": f"{material_root.name}/documents/index.md"}, # 既存のindex.mdを概要として
                {"第1章": f"{material_root.name}/documents/chapter01.md"},
                {"第2章": f"{material_root.name}/documents/chapter02.md"},
                {"第3章": f"{material_root.name}/documents/chapter03.md"},
                {"第4章": f"{material_root.name}/documents/chapter04.md"},
                {"第5章": f"{material_root.name}/documents/chapter05.md"},
                {"第6章": f"{material_root.name}/documents/chapter06.md"},
                {"用語集": f"{material_root.name}/glossary.md"},
                {"FAQ": f"{material_root.name}/faq.md"},
                {"TIPS": f"{material_root.name}/tips.md"},
            ]
        }
    ]
    mkdocs_mgr.generate_mkdocs_yml(nav_structure)
    logging.info("mkdocs.ymlの生成が完了しました。")

    # --- 3. 共通アセットの生成 ---
    logging.info("共通アセットを生成しています...")
    asset_gen = AssetGenerator(output_dir)
    # TODO: config.ymlから読み込むようにする
    # asset_gen.generate_from_templates(material_root / "templates")
    logging.info("共通アセットの生成が完了しました。")

    # --- 4. コンテンツの生成 ---
    logging.info("Markdownコンテンツを生成しています...")
    content_mgr = TestMaterialContentManager(output_dir)
    generated_files = content_mgr.generate_content()
    logging.info(f"{len(generated_files)}個のファイルを生成しました。")

    # --- 5. ホームページの生成 (仮) ---
    # サイトのルートにindex.mdを生成
    index_content = "# MkDocs学習資料ジェネレーター\n\nこのサイトは、MkDocsとPythonのCoreフレームワークで自動生成された学習資料のサンプルです。\n\n左側のナビゲーションから各教材のコンテンツを選択してください。"
    (output_dir / "index.md").write_text(index_content, encoding="utf-8")
    # 既存のtest_material/documents/index.mdも残しておく
    (output_dir / material_root.name / "documents" / "index.md").write_text("# テスト教材概要\n\nこの教材はCore機能のテストとデモンストレーションを目的としています。", encoding="utf-8")

    logging.info("test_materialのビルドプロセスが正常に完了しました。")
    logging.info(f"出力先: {output_dir}")
    logging.info("ローカルサーバーで確認するには、プロジェクトルートで `mkdocs serve` を実行してください。")

if __name__ == "__main__":
    main()

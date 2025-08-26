from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def generate(output_dir: Path, **kwargs) -> Path:
    """
    引数で受け取ったテキストからアスキーアート画像を生成する（という想定の）関数。
    実際の描画処理は複雑なため、このテストではダミーの画像を生成する。

    Args:
        output_dir: 画像の出力先ディレクトリ。
        **kwargs: YAMLのparamsで指定された引数（text, filenameなど）。

    Returns:
        生成された画像のパス。
    """
    text = kwargs.get("text", "DEFAULT")
    filename = kwargs.get("filename", "default_art.png")
    output_path = output_dir / filename

    logger.info(f"独自ジェネレータ実行: アスキーアート画像を {output_path} に生成します。")
    logger.info(f"受け取ったテキスト: {text}")

    # TODO: 本来はここでpyfigletやPillowなどを使って画像を生成する
    # このテストでは、ファイルが生成されたことだけを確認するため、空ファイルを作成する
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.touch()

    return output_path

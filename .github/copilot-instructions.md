# Copilot Instructions for This Codebase

## 概要・全体構造
- 本プロジェクトは「src/core」（共通基盤）と「src/materials」（教材ごとの個別実装）の明確な分離が特徴。
- `core`配下は再利用可能な機能部品群（例: `DocumentBuilder`, `ChartGenerator`, `MkDocsManager`, `asset_generator.py`）。教材追加や拡張時は既存機能を壊さずに済む設計。
- `materials`配下は教材ごとのmainスクリプト・定義・設定を持つ。新教材は`src/materials/`にディレクトリ追加でOK。
- 静的/動的なグラフ・表現やインタラクティブ要素（クイズ等）をPython+JS/CSSで生成し、`docs/`配下に出力。
- サイト全体は`mkdocs.yml`で管理、出力はMkDocs Materialで静的サイト化。

## 主要ワークフロー
- 教材生成: `python src/materials/<教材名>/<教材>_main.py`
- サイト確認: `mkdocs serve` → http://127.0.0.1:8000 で確認
- テスト教材例: `src/materials/test_material/test_material_main.py`
- coreの構文チェック: `python -m py_compile src/core/*.py`
- 生成物（docs/配下）は直接編集禁止。必ず生成元スクリプトを修正。

## プロジェクト固有のルール・注意点
- 直接編集禁止: `docs/`配下や自動生成ファイルは絶対に直接編集しない
- 変更は必ず生成元（`src/materials`や`src/core`）で行う
- 1箇所ずつ修正・テスト・動作確認を徹底
- 影響範囲を常に意識し、最小限の修正で解決する
- バックアップや元状態の記録を忘れずに
- 推測や一括変更は禁止。必ず根拠を持って修正

## 重要ファイル・ディレクトリ
- `src/core/asset_generator.py`: CSS/JS生成の中核
- `docs/asset_manifest.json`: 生成アセットの管理情報
- `mkdocs.yml`: サイト設定（プラグイン・テーマ等）
- `src/materials/test_material/`: テスト教材例

## 参考: よく使うコマンド
```bash
python src/materials/test_material/test_material_main.py  # 教材生成
mkdocs serve                                             # サイト起動
python -m py_compile src/core/*.py                      # core構文チェック
```

---

このドキュメントは`README.md`・`CLAUDE.md`の内容を反映し、AIエージェントが本プロジェクトで即戦力となるための要点をまとめています。疑問点や不明点があれば、必ず既存ドキュメントや生成元スクリプトを確認してください。

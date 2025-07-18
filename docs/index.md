# MkDocs Materials Generator

このサイトは、MkDocs Materials Generator によって自動生成された学習資料のデモサイトです。

## システム情報

- **バージョン**: 1.0.0
- **最終更新**: 2025-07-18 22:09:49
- **作者**: MkDocs Materials Generator

## 利用可能な資料

### 📚 テスト資料

MkDocs Materials Generator の全機能をテストするための資料です。

- [テスト資料を見る](assets/test_material/index.md)

## 機能一覧

このシステムは以下の機能を提供します：

1. **Markdownコンテンツ生成**
   - 見出し、段落、リスト、コードブロック
   - Material for MkDocsの拡張機能（Admonition、Tabs）
   - 専門用語のツールチップ

2. **図表生成**
   - Matplotlib/Seabornによる静的図表
   - Plotlyによるインタラクティブ図表
   - カスタム描画関数のサポート

3. **表生成**
   - 基本的なHTMLテーブル
   - スタイル付きテーブル
   - 検索・ソート機能付きテーブル

4. **用語管理**
   - 専門用語の一元管理
   - 自動用語集生成
   - ツールチップ機能

## 使い方

### 1. プレビューサーバーの起動

```bash
mkdocs serve
'''
### 2. 静的サイトのビルド
```bash
mkdocs build
'''

### 3. 新しい資料の追加
src/materials/ディレクトリに新しいモジュールを作成し、BaseContentManagerを継承してください。

!!! info "お問い合わせ"
このシステムに関するお問い合わせは、GitHubのIssueでお願いします。

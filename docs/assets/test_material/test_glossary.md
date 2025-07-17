---
title: 用語集
description: 学習資料で使用される専門用語の定義集
---

# 用語集

この用語集は学習資料で使用される専門用語の定義をまとめたものです。

!!! info "用語集統計"

    **総用語数**: 32語  
    **カテゴリ数**: 9カテゴリ


## UI

### ツールチップ

<a id="ツールチップ"></a>

マウスオーバーやタップ時に表示される小さなポップアップ。追加情報を提供する。

**初出章**: 用語管理テスト

---

## コンポーネント

### ChartGenerator

<a id="chartgenerator"></a>

様々な種類の図表を生成し、HTMLファイルとして出力するクラス。MatplotlibやPlotlyを使用する。

**初出章**: 図表生成テスト

**関連用語**: [Matplotlib](#matplotlib), [Plotly](#plotly)

---

### DocumentBuilder

<a id="documentbuilder"></a>

Markdownコンテンツを構築するためのクラス。見出し、段落、リストなどの要素を生成する。

**初出章**: システムテスト概要

**関連用語**: [Markdown](#markdown)

---

### KnowledgeManager

<a id="knowledgemanager"></a>

専門用語を一元的に管理し、用語集を生成するためのクラス。

**初出章**: 用語管理テスト

**関連用語**: [用語集](#用語集)

---

### TableGenerator

<a id="tablegenerator"></a>

様々な形式の表データを生成し、HTMLファイルとして出力するクラス。

**初出章**: 表生成テスト

**関連用語**: [HTML](#html)

---

## システム

### Markdown

<a id="markdown"></a>

軽量マークアップ言語の一つ。プレーンテキストで書かれた文書をHTMLに変換する。

**初出章**: システムテスト概要

**関連用語**: [HTML](#html)

---

### Material for MkDocs

<a id="material-for-mkdocs"></a>

MkDocsのテーマの一つ。Googleのマテリアルデザインに基づいた美しいドキュメントサイトを作成できる。

**初出章**: システムテスト概要

**関連用語**: [MkDocs](#mkdocs)

---

### MkDocs

<a id="mkdocs"></a>

Pythonで書かれた静的サイトジェネレータ。Markdownファイルから美しいドキュメントサイトを生成する。

**初出章**: システムテスト概要

**関連用語**: [Markdown](#markdown), [Material for MkDocs](#material-for-mkdocs)

---

## テスト

### パフォーマンステスト

<a id="パフォーマンステスト"></a>

システムの性能や処理速度を測定するテスト。負荷テストも含む。

**初出章**: 統合テスト

---

### 単体テスト

<a id="単体テスト"></a>

個別のモジュールや関数の動作を確認するテスト。最小単位でのテストを行う。

**初出章**: 統合テスト

---

### 統合テスト

<a id="統合テスト"></a>

複数のモジュールやコンポーネントを組み合わせて行うテスト。システム全体の動作を確認する。

**初出章**: 統合テスト

---

## プログラミング

### JavaScript

<a id="javascript"></a>

Webブラウザで動作するプログラミング言語。動的なWebページを作成できる。

**初出章**: 図表生成テスト

---

### Python

<a id="python"></a>

汎用プログラミング言語。読みやすく書きやすい構文が特徴。

**初出章**: システムテスト概要

---

## ライブラリ

### Matplotlib

<a id="matplotlib"></a>

Pythonの描画ライブラリ。静的な図表を生成するために使用される。

**初出章**: 図表生成テスト

**関連用語**: [Python](#python), [Seaborn](#seaborn)

---

### Plotly

<a id="plotly"></a>

インタラクティブな図表を生成するためのライブラリ。ズームやホバーなどの機能を提供する。

**初出章**: 図表生成テスト

**関連用語**: [JavaScript](#javascript)

---

### Seaborn

<a id="seaborn"></a>

Matplotlibベースの統計データ可視化ライブラリ。美しい統計グラフを簡単に作成できる。

**初出章**: 図表生成テスト

**関連用語**: [Matplotlib](#matplotlib)

---

### pandas

<a id="pandas"></a>

Pythonのデータ分析ライブラリ。DataFrame構造を使ってデータを効率的に処理できる。

**初出章**: 表生成テスト

**関連用語**: [Python](#python)

---

## 図表

### 円グラフ

<a id="円グラフ"></a>

データを円の扇形で表現するグラフ。全体に対する割合を示すのに適している。

**初出章**: 図表生成テスト

---

### 折れ線グラフ

<a id="折れ線グラフ"></a>

データの変化を線で表したグラフ。時系列データの表示に適している。

**初出章**: 図表生成テスト

---

### 棒グラフ

<a id="棒グラフ"></a>

データを棒の長さで表現するグラフ。カテゴリ別の比較に適している。

**初出章**: 図表生成テスト

---

## 技術

### Base64

<a id="base64"></a>

バイナリデータをテキストで表現するためのエンコーディング方式。

**初出章**: 図表生成テスト

---

### CDN

<a id="cdn"></a>

Content Delivery Network。コンテンツを効率的に配信するためのネットワーク。

**初出章**: 図表生成テスト

---

### CSS

<a id="css"></a>

Cascading Style Sheets。HTMLの見た目を装飾するためのスタイルシート言語。

**初出章**: 表生成テスト

**関連用語**: [HTML](#html)

---

### HTML

<a id="html"></a>

HyperText Markup Language。Webページを作成するためのマークアップ言語。

**初出章**: 表生成テスト

---

### JSON

<a id="json"></a>

JavaScript Object Notation。データ交換形式の一つ。軽量で人間にも読みやすい。

**初出章**: システムテスト概要

**関連用語**: [JavaScript](#javascript)

---

### SVG

<a id="svg"></a>

Scalable Vector Graphics。ベクター形式の画像フォーマット。拡大縮小しても劣化しない。

**初出章**: 図表生成テスト

---

### YAML

<a id="yaml"></a>

YAML Ain't Markup Language。設定ファイルによく使われる人間が読みやすいデータ形式。

**初出章**: システムテスト概要

---

### iframe

<a id="iframe"></a>

HTMLで他のページを埋め込むためのタグ。外部コンテンツを表示できる。

**初出章**: 図表生成テスト

**関連用語**: [HTML](#html)

---

### エラーハンドリング

<a id="エラーハンドリング"></a>

プログラム実行中に発生するエラーを適切に処理する仕組み。

**初出章**: 統合テスト

---

### スラッグ

<a id="スラッグ"></a>

URLやアンカーリンクで使用される文字列。特殊文字を除去し、ハイフンで区切られる。

**初出章**: 用語管理テスト

---

### レスポンシブデザイン

<a id="レスポンシブデザイン"></a>

異なる画面サイズに対応して、レイアウトが自動調整されるデザイン手法。

**初出章**: 表生成テスト

---

## 文書

### 用語集

<a id="用語集"></a>

専門用語とその定義をまとめた辞書的な資料。学習支援に重要な役割を果たす。

**初出章**: 用語管理テスト

---

## 索引

用語をアルファベット順に並べた索引です。

### B

[Base64](#base64)

### C

[CDN](#cdn) | [ChartGenerator](#chartgenerator) | [CSS](#css)

### D

[DocumentBuilder](#documentbuilder)

### H

[HTML](#html)

### I

[iframe](#iframe)

### J

[JavaScript](#javascript) | [JSON](#json)

### K

[KnowledgeManager](#knowledgemanager)

### M

[Markdown](#markdown) | [Material for MkDocs](#material-for-mkdocs) | [Matplotlib](#matplotlib) | [MkDocs](#mkdocs)

### P

[pandas](#pandas) | [Plotly](#plotly) | [Python](#python)

### S

[Seaborn](#seaborn) | [SVG](#svg)

### T

[TableGenerator](#tablegenerator)

### Y

[YAML](#yaml)

### エ

[エラーハンドリング](#エラーハンドリング)

### ス

[スラッグ](#スラッグ)

### ツ

[ツールチップ](#ツールチップ)

### パ

[パフォーマンステスト](#パフォーマンステスト)

### レ

[レスポンシブデザイン](#レスポンシブデザイン)

### 円

[円グラフ](#円グラフ)

### 単

[単体テスト](#単体テスト)

### 折

[折れ線グラフ](#折れ線グラフ)

### 棒

[棒グラフ](#棒グラフ)

### 用

[用語集](#用語集)

### 統

[統合テスト](#統合テスト)

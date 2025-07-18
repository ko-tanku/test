---
title: "図表生成テスト"
description: "テスト資料 - 図表生成テスト"
chapter_number: 2
material: "テスト資料"
---

# 第2章 図表生成テスト


この章では、ChartGeneratorクラスの機能をテストし、
様々な種類の図表を生成して動作確認を行います。

!!! tip "図表生成のポイント"
    - Matplotlib/Seaborn と Plotly の両方をサポート
    - 日本語フォント対応
    - レスポンシブデザイン対応

## 図表生成機能


<span data-md-tooltip="様々な種類の図表を生成し、HTMLファイルとして出力するクラス。MatplotlibやPlotlyを使用する。">ChartGenerator</span> クラスは以下の機能を提供します：

- **<span data-md-tooltip="データの変化を線で表したグラフ。時系列データの表示に適している。">折れ線グラフ</span>**: 時系列データの可視化に適用
- **<span data-md-tooltip="データを棒の長さで表現するグラフ。カテゴリ別の比較に適している。">棒グラフ</span>**: カテゴリ別データの比較に適用
- **<span data-md-tooltip="データを円の扇形で表現するグラフ。全体に対する割合を示すのに適している。">円グラフ</span>**: 全体に対する割合の表示に適用
- **カスタム図表**: 独自の描画ロジックによる図表生成
- **インタラクティブ図表**: Plotlyによる動的な図表生成


## 図表生成テスト実行

以下の図表を生成してテストを実行します：

### 折れ線グラフテスト

<iframe src="test_material/assets/charts/test_line_chart.html" width="100%" height="400px" frameborder="0" style="border: 1px solid #e0e0e0; border-radius: 4px;"></iframe>

### 棒グラフテスト

<iframe src="test_material/assets/charts/test_bar_chart.html" width="100%" height="400px" frameborder="0" style="border: 1px solid #e0e0e0; border-radius: 4px;"></iframe>

### 円グラフテスト

<iframe src="test_material/assets/charts/test_pie_chart.html" width="100%" height="400px" frameborder="0" style="border: 1px solid #e0e0e0; border-radius: 4px;"></iframe>

### インタラクティブ図表テスト

<iframe src="test_material/assets/charts/test_interactive_chart.html" width="100%" height="500px" frameborder="0" style="border: 1px solid #e0e0e0; border-radius: 4px;"></iframe>

### カスタム図表テスト

<iframe src="test_material/assets/charts/test_custom_figure.html" width="100%" height="400px" frameborder="0" style="border: 1px solid #e0e0e0; border-radius: 4px;"></iframe>


!!! success "第2章完了"
    図表生成機能のテストが完了しました。
    次章では表生成機能のテストを行います。

---

[📚 目次](index.md) | [📖 用語集](glossary.md) | [← 前の章](chapter_01_*.md) | [次の章: 表生成テスト →](chapter_03_表生成テスト.md)

!!! info "章の情報"

                                **章番号**: 2
                                **所要時間**: 20分
                                **難易度**: 基本

---
title: 図表生成テスト
description: テスト資料 - 図表生成テスト
chapter_number: 2
material: テスト資料
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


    <div style="width: 100%; margin: 20px 0; border: 1px solid #ddd; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
        <iframe 
            src="/assets/charts/test_line_chart_matplotlib.html" 
            width="100%" 
            height="600px" 
            frameborder="0" 
            allowfullscreen
            style="display: block; border: none; background: white;"
            scrolling="no">
        </iframe>
    </div>

### 棒グラフテスト


    <div style="width: 100%; margin: 20px 0; border: 1px solid #ddd; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
        <iframe 
            src="/assets/charts/test_bar_chart_matplotlib.html" 
            width="100%" 
            height="600px" 
            frameborder="0" 
            allowfullscreen
            style="display: block; border: none; background: white;"
            scrolling="no">
        </iframe>
    </div>

### 円グラフテスト


    <div style="width: 100%; margin: 20px 0; border: 1px solid #ddd; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
        <iframe 
            src="/assets/charts/test_pie_chart_matplotlib.html" 
            width="100%" 
            height="600px" 
            frameborder="0" 
            allowfullscreen
            style="display: block; border: none; background: white;"
            scrolling="no">
        </iframe>
    </div>

### カスタム図表テスト


    <div style="width: 100%; margin: 20px 0; border: 1px solid #ddd; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
        <iframe 
            src="/assets/charts/test_custom_chart.html" 
            width="100%" 
            height="600px" 
            frameborder="0" 
            allowfullscreen
            style="display: block; border: none; background: white;"
            scrolling="no">
        </iframe>
    </div>

### インタラクティブ図表テスト


    <div style="width: 100%; margin: 20px 0; border: 1px solid #ddd; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
        <iframe 
            src="/assets/charts/test_interactive_chart.html" 
            width="100%" 
            height="600px" 
            frameborder="0" 
            allowfullscreen
            style="display: block; border: none; background: white;"
            scrolling="no">
        </iframe>
    </div>

!!! success "図表生成テスト完了"

    全ての図表が正常に生成されました。


## 図表生成のポイント

- 日本語フォントの適切な設定
- レスポンシブデザインへの対応
- カラーパレットの統一
- インタラクティブ機能の活用
- ファイルサイズの最適化


!!! success "第2章完了"
    図表生成機能のテストが完了しました。
    次章では表生成機能のテストを行います。

---

[← 前の章: システムテスト概要](chapter_01_system_test_overview.md) | [📚 目次](index.md) | [📖 用語集](glossary.md) | [次の章: 表生成テスト →](chapter_03_table_generation_test.md)

!!! info "章の情報"

    
                                        **章番号**: 2  
                                        **所要時間**: 20分  
                                        **難易度**: 基本
                                        

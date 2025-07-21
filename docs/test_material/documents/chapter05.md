# 第5章: 全機能統合テスト

全ての実装済み機能を網羅的にテストします。

## ツールチップ機能の詳細テスト

マイコンはセンサーからの入力を処理し、アクチュエータを制御します。RTOSを使用することで複雑なタスク管理が可能になります。

PWM制御によりモーターの回転速度を調整し、I2C通信でセンサーデータを取得します。

## アイコン・略語ツールチップテスト

:material-memory:{ title="メモリ使用量を表示" }

:material-speed:{ title="CPU使用率を監視" }

<span class="custom-tooltip" data-tooltip="Microcontroller Unit - マイクロコントローラユニット">MCU</span>

<span class="custom-tooltip" data-tooltip="General Purpose Input/Output - 汎用入出力ポート">GPIO</span>

## アニメーション図表テスト

**図5-1: 時系列データの変化をアニメーションで表示**

![アニメーション図表](../../charts/data_animation.gif)

## クイズ・FAQ・TIPS統合テスト

!!! question "クイズ"
    **問題**: RTOSの主な特徴は何ですか？

    **選択肢**:
    1. リアルタイム性の保証
    2. グラフィック処理の高速化
    3. ネットワーク通信の最適化
    4. データベース管理

    ??? tip "ヒント"
        RTOSはReal-Time Operating Systemの略です

    ??? success "解説"
        **正解**: 1

        **解説**: RTOSは決められた時間内に処理を完了することを保証するオペレーティングシステムです。

!!! question "クイズ"
    **問題**: I2C通信の特徴として正しいものは？

    **選択肢**:
    1. 2本の信号線で通信
    2. 1本の信号線で通信
    3. 4本の信号線で通信
    4. 8本の信号線で通信

    ??? tip "ヒント"
        I2CはSDAとSCLの2本の線を使用します

    ??? success "解説"
        **正解**: 1

        **解説**: I2C通信はSDA（データ線）とSCL（クロック線）の2本で通信を行います。

!!! question "クイズ"
    **問題**: マイコンの主要な構成要素でないものは？

    **選択肢**:
    1. CPU
    2. RAM
    3. プリンター
    4. I/Oポート

    ??? tip "ヒント"
        マイコンは組み込みシステム用の小型コンピュータです

    ??? success "解説"
        **正解**: 3

        **解説**: マイコンはCPU、メモリ、I/Oポートを1つのチップに集積した小型コンピュータです。プリンターは外部機器です。

## 学習サマリーと関連資料

!!! note "第5章で学んだ重要事項"
    - ツールチップ機能により用語理解が向上
    - アニメーション図表で動的な現象を可視化
    - クイズ機能で理解度の確認が可能
    - FAQ・TIPSで自主学習を支援

!!! info "関連資料と次のステップ"
    - [第1章: プログラミング基礎の復習](chapter01.md)
    - [第2章: 組み込みシステム概要](chapter02.md)
    - [第3章: ハードウェア理解](chapter03.md)
    - [第4章: 演習問題に挑戦](chapter04.md)
    - [用語集で知識を体系化](../glossary.md)
    - [FAQで疑問を解決](../faq.md)

## 高度なインタラクティブ図表

**図5-2: ドロップダウンでリソース種別を切り替え**

<iframe src="../../charts/system_resource_monitor.html" width="100%"  style="border: 1px solid #ddd; border-radius: 4px;" scrolling="no" class="auto-height-iframe"></iframe>

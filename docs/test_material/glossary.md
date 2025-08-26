# 用語集

本資料で使用される専門用語の定義と説明をまとめています。

## Core機能

<a id="assetgenerator"></a>
### AssetGenerator

**定義:** Core機能の一つ。CSS、JavaScriptファイルを動的生成・管理するクラス。

**初出章:** 第6章

**関連用語:** [MkDocsManager](#mkdocsmanager), [Jinjaテンプレート](#jinjaテンプレート)

---

<a id="basecontentmanager"></a>
### BaseContentManager

**定義:** Core機能の基底クラス。各種ジェネレータを統合し、章ごとのコンテンツ構築フレームワークを提供。

**初出章:** 第6章

**関連用語:** [DocumentBuilder](#documentbuilder), [ChartGenerator](#chartgenerator), [TableGenerator](#tablegenerator)

---

<a id="chartgenerator"></a>
### ChartGenerator

**定義:** Core機能の一つ。matplotlib、plotlyを使用して図表を生成するクラス。

**初出章:** 第6章

**関連用語:** [DocumentBuilder](#documentbuilder), [TableGenerator](#tablegenerator)

---

<a id="documentbuilder"></a>
### DocumentBuilder

**定義:** Core機能の一つ。Markdownコンテンツを構築するためのビルダークラス。

**初出章:** 第6章

**関連用語:** [ChartGenerator](#chartgenerator), [TableGenerator](#tablegenerator), [KnowledgeManager](#knowledgemanager)

**使用例:**

> DocumentBuilderを使用してMarkdownコンテンツを動的生成します。

---

<a id="knowledgemanager"></a>
### KnowledgeManager

**定義:** Core機能の一つ。専門用語、FAQ、TIPSを管理し、用語集ページを生成するクラス。

**初出章:** 第6章

**関連用語:** [DocumentBuilder](#documentbuilder), [AssetGenerator](#assetgenerator)

---

<a id="mkdocsmanager"></a>
### MkDocsManager

**定義:** Core機能の一つ。mkdocs.ymlファイルの動的生成・更新を管理するクラス。

**初出章:** 第6章

**関連用語:** [AssetGenerator](#assetgenerator), NavItem

---

<a id="tablegenerator"></a>
### TableGenerator

**定義:** Core機能の一つ。HTMLテーブルを生成し、カスタムスタイルを適用するクラス。

**初出章:** 第6章

**関連用語:** [DocumentBuilder](#documentbuilder), [ChartGenerator](#chartgenerator)

---

## アーキテクチャ

<a id="テンプレート外部化"></a>
### テンプレート外部化

**定義:** CSS/JSテンプレートをPythonコードから分離し、独立ファイルとして管理する手法。

**初出章:** 第7章

**関連用語:** [Jinjaテンプレート](#jinjaテンプレート), 保守性向上

---

## システム

<a id="割り込み"></a>
### 割り込み

**定義:** CPUの通常処理を一時中断して、緊急の処理を実行する仕組み。

**初出章:** 第3章

**関連用語:** ISR, プリエンプション

---

## ソフトウェア

<a id="rtos"></a>
### RTOS

**定義:** Real-Time Operating System。リアルタイム性を保証するOS。

**初出章:** 第4章

**関連用語:** リアルタイムシステム, スケジューリング

**使用例:**

> RTOSを使用することで、複雑なタスク管理が可能になります。

---

## テンプレート技術

<a id="jinjaテンプレート"></a>
### Jinjaテンプレート

**定義:** Python用のテンプレートエンジン。変数置換や条件分岐、ループ処理が可能。

**初出章:** 第7章

**関連用語:** [AssetGenerator](#assetgenerator), [テンプレート外部化](#テンプレート外部化)

---

## ハードウェア

<a id="アクチュエータ"></a>
### アクチュエータ

**定義:** 電気信号を物理的な動作（モーター回転、バルブ開閉など）に変換する装置。

**初出章:** 第2章

**関連用語:** [センサー](#センサー), サーボモーター

---

<a id="センサー"></a>
### センサー

**定義:** 物理量（温度、圧力、光など）を電気信号に変換する素子。

**初出章:** 第2章

**関連用語:** [アクチュエータ](#アクチュエータ), A/D変換

**使用例:**

> センサーからの入力を処理して、適切な制御を行います。

---

<a id="フラッシュメモリ"></a>
### フラッシュメモリ

**定義:** 電源を切ってもデータが保持される不揮発性メモリ。プログラムの格納に使用。

**初出章:** 第3章

**関連用語:** ROM, EEPROM

---

<a id="マイコン"></a>
### マイコン

**定義:** マイクロコントローラの略。CPU、メモリ、I/Oなどを1チップに集積した小型コンピュータ。

**初出章:** 第2章

**関連用語:** CPU, 組み込みシステム, SoC

**使用例:**

> マイコンは組み込みシステムの心臓部です。

> 8ビットから32ビットまで様々な種類があります。

---

## リアルタイムシステム

<a id="デッドライン"></a>
### デッドライン

**定義:** 処理が完了すべき制限時間。リアルタイムシステムで重要な概念。

**初出章:** 第4章

**関連用語:** リアルタイム性, レイテンシ

---

## 制御技術

<a id="pwm"></a>
### PWM

**定義:** Pulse Width Modulation。パルス幅変調。デジタル信号で擬似的にアナログ値を表現。

**初出章:** 第3章

**関連用語:** D/A変換, モーター制御

**使用例:**

> PWM制御によりモーターの回転速度を調整し、I2C通信でセンサーデータを取得します。

---

## 通信

<a id="i2c"></a>
### I2C

**定義:** Inter-Integrated Circuit。シリアル通信プロトコルの一種。

**初出章:** 第3章

**関連用語:** SPI, UART

**使用例:**

> PWM制御によりモーターの回転速度を調整し、I2C通信でセンサーデータを取得します。

---

## 開発ツール

<a id="デバッガ"></a>
### デバッガ

**定義:** プログラムのバグを発見・修正するためのツール。

**初出章:** 第1章

**関連用語:** IDE, エミュレータ

---

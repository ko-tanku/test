# よくある質問（FAQ）

学習者からよく寄せられる質問とその回答をまとめています。

## システム設計

??? question "RTOSは必ず必要ですか？"
    小規模なシステムではベアメタルプログラミング（OS無し）でも十分です。複数のタスクを管理する必要がある場合にRTOSが有効です。

## セキュリティ

??? question "組み込みシステムのセキュリティ対策は？"
    1. ファームウェアの暗号化 2. セキュアブート実装 3. 通信の暗号化 4. デバッグポートの無効化

## トラブルシューティング

??? question "デバッグが難しいです。良い方法はありますか？"
    1. LEDやシリアル出力でのprintf デバッグ 2. JTAGデバッガの使用 3. オシロスコープでの信号確認 4. 段階的なテスト実施

## プログラミング

??? question "組み込みプログラミングに最適な言語は？"
    C言語が最も一般的です。ハードウェア制御が可能で、実行効率が高いためです。最近はC++も使われます。

## 基本概念

??? question "マイコンとマイクロプロセッサの違いは何ですか？"
    マイコンはCPU、メモリ、I/Oを1チップに集積していますが、マイクロプロセッサはCPU機能のみです。マイコンは組み込み用途、マイクロプロセッサはPC用途が主です。

## 技術的問題

??? question "ツールチップ機能が表示されない場合の対処法は？"
    ブラウザでJavaScriptが有効になっているか確認してください。また、Material for MkDocsテーマでcontent.tooltipsが有効化されている必要があります。

??? question "アニメーションGIFが再生されない場合は？"
    ブラウザがGIFアニメーションに対応しているか確認してください。ファイルサイズが大きい場合、読み込みに時間がかかる場合があります。

??? question "図表が正しく表示されない場合は？"
    iframeの読み込みが完了するまで待ってください。ネットワーク環境により時間がかかる場合があります。

## 省電力設計

??? question "消費電力を削減する方法は？"
    1. クロック周波数の低減 2. スリープモードの活用 3. 不要な周辺機能の停止 4. 効率的なアルゴリズムの使用

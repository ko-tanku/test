# 第5章: インタラクティブクイズ機能

新しく追加された高度なクイズ機能をテストします。カテゴリ分けクイズと複数選択クイズの動作を確認できます。

## 基本的なクイズ機能の復習

まず、従来の単一選択クイズを復習しましょう。

!!! question "クイズ"
    **問題**: リアルタイムシステムの2つの分類は何ですか？

    **選択肢**:
    1. ハードリアルタイムとソフトリアルタイム
    2. バッチ処理とインタラクティブ処理
    3. 並列処理と直列処理
    4. 同期処理と非同期処理

    ??? tip "ヒント"
        第4章で学習したシステムの分類です

    ??? success "解説"
        **正解**: 1

        **解説**: リアルタイムシステムは、デッドラインの厳格さによりハードリアルタイムとソフトリアルタイムに分類されます。

## カテゴリ分けクイズ

項目を適切なカテゴリにドラッグ&ドロップで分類してください。


<div class="quiz-container categorization-quiz" data-quiz-id="system-classification">
    <h3 class="quiz-title">カテゴリ分けクイズ</h3>
    <p class="quiz-question"><strong>問題:</strong> 以下の要素を「ハードウェア」と「ソフトウェア」に分類してください。</p>

    <div class="quiz-categories">
        <strong>カテゴリ:</strong>
        <ul>
            <li>ハードウェア</li>
            <li>ソフトウェア</li>
        </ul>
    </div>

    <div class="quiz-items">
        <h4>項目をドラッグして適切なカテゴリに分類してください：</h4>
        <div class="draggable-items">
            <div class="draggable-item" data-item="0" draggable="true">CPU</div>
            <div class="draggable-item" data-item="1" draggable="true">OS</div>
            <div class="draggable-item" data-item="2" draggable="true">RAM</div>
            <div class="draggable-item" data-item="3" draggable="true">コンパイラ</div>
            <div class="draggable-item" data-item="4" draggable="true">GPIO</div>
            <div class="draggable-item" data-item="5" draggable="true">デバイスドライバ</div>
            <div class="draggable-item" data-item="6" draggable="true">センサー</div>
            <div class="draggable-item" data-item="7" draggable="true">RTOS</div>
        </div>
    </div>

    <div class="drop-zones">
        <div class="drop-zone" data-category="0">
            <h4>ハードウェア</h4>
            <div class="drop-area">ここにドロップしてください</div>
        </div>
        <div class="drop-zone" data-category="1">
            <h4>ソフトウェア</h4>
            <div class="drop-area">ここにドロップしてください</div>
        </div>
    </div>

    <button class="check-categorization" onclick="checkCategorization('system-classification')">答えを確認</button>
    <div class="categorization-result"></div>
</div>

<script>
window.categorizationData = window.categorizationData || {};
window.categorizationData["system-classification"] = [0, 1, 0, 1, 0, 1, 0, 1];
</script>


## 複数選択クイズ

複数の正解がある問題です。該当する項目を全て選択してください。


<div class="quiz-container multiple-choice-quiz" data-quiz-id="realtime-applications">
    <h3 class="quiz-title">複数選択クイズ</h3>
    <p class="quiz-question"><strong>問題:</strong> 以下の中でハードリアルタイムシステムに該当するものを全て選択してください。</p>
    <p class="quiz-instruction"><strong>複数の選択肢から正解を全て選んでください</strong></p>

    <div class="quiz-options">
        <label class="option-label">
            <input type="checkbox" name="realtime-applications" value="0">
            <span class="option-text">航空機の制御システム</span>
        </label><br>
        <label class="option-label">
            <input type="checkbox" name="realtime-applications" value="1">
            <span class="option-text">動画ストリーミングサービス</span>
        </label><br>
        <label class="option-label">
            <input type="checkbox" name="realtime-applications" value="2">
            <span class="option-text">原子力発電所の制御システム</span>
        </label><br>
        <label class="option-label">
            <input type="checkbox" name="realtime-applications" value="3">
            <span class="option-text">オンラインゲーム</span>
        </label><br>
        <label class="option-label">
            <input type="checkbox" name="realtime-applications" value="4">
            <span class="option-text">人工呼吸器の制御</span>
        </label><br>
        <label class="option-label">
            <input type="checkbox" name="realtime-applications" value="5">
            <span class="option-text">Webブラウザ</span>
        </label><br>
        <label class="option-label">
            <input type="checkbox" name="realtime-applications" value="6">
            <span class="option-text">自動車のエアバッグシステム</span>
        </label><br>
    </div>

    <button class="check-multiple-choice" onclick="checkMultipleChoice('realtime-applications')">答えを確認</button>
    <div class="multiple-choice-result"></div>
</div>

<script>
window.multipleChoiceData = window.multipleChoiceData || {};
window.multipleChoiceData["realtime-applications"] = {
    "correct": [0, 2, 4, 6],
    "explanation": "ハードリアルタイムシステムは、デッドラインを守れない場合に人命や安全に関わる致命的な問題が発生するシステムです。航空機制御、原子力発電所制御、人工呼吸器、エアバッグシステムなどがこれに該当します。"
};
</script>


## 応用問題 - 組み込みシステムの理解


<div class="quiz-container categorization-quiz" data-quiz-id="communication-protocols">
    <h3 class="quiz-title">カテゴリ分けクイズ</h3>
    <p class="quiz-question"><strong>問題:</strong> 以下の通信プロトコルを「有線」と「無線」に分類してください。</p>

    <div class="quiz-categories">
        <strong>カテゴリ:</strong>
        <ul>
            <li>有線通信</li>
            <li>無線通信</li>
        </ul>
    </div>

    <div class="quiz-items">
        <h4>項目をドラッグして適切なカテゴリに分類してください：</h4>
        <div class="draggable-items">
            <div class="draggable-item" data-item="0" draggable="true">UART</div>
            <div class="draggable-item" data-item="1" draggable="true">Wi-Fi</div>
            <div class="draggable-item" data-item="2" draggable="true">I2C</div>
            <div class="draggable-item" data-item="3" draggable="true">Bluetooth</div>
            <div class="draggable-item" data-item="4" draggable="true">SPI</div>
            <div class="draggable-item" data-item="5" draggable="true">ZigBee</div>
            <div class="draggable-item" data-item="6" draggable="true">CAN</div>
            <div class="draggable-item" data-item="7" draggable="true">LoRa</div>
        </div>
    </div>

    <div class="drop-zones">
        <div class="drop-zone" data-category="0">
            <h4>有線通信</h4>
            <div class="drop-area">ここにドロップしてください</div>
        </div>
        <div class="drop-zone" data-category="1">
            <h4>無線通信</h4>
            <div class="drop-area">ここにドロップしてください</div>
        </div>
    </div>

    <button class="check-categorization" onclick="checkCategorization('communication-protocols')">答えを確認</button>
    <div class="categorization-result"></div>
</div>

<script>
window.categorizationData = window.categorizationData || {};
window.categorizationData["communication-protocols"] = [0, 1, 0, 1, 0, 1, 0, 1];
</script>



<div class="quiz-container multiple-choice-quiz" data-quiz-id="microcontroller-features">
    <h3 class="quiz-title">複数選択クイズ</h3>
    <p class="quiz-question"><strong>問題:</strong> 組み込みシステムの特徴として正しいものを全て選択してください。</p>
    <p class="quiz-instruction"><strong>複数の選択肢から正解を全て選んでください</strong></p>

    <div class="quiz-options">
        <label class="option-label">
            <input type="checkbox" name="microcontroller-features" value="0">
            <span class="option-text">リアルタイム性が重要</span>
        </label><br>
        <label class="option-label">
            <input type="checkbox" name="microcontroller-features" value="1">
            <span class="option-text">高性能なGPUが必須</span>
        </label><br>
        <label class="option-label">
            <input type="checkbox" name="microcontroller-features" value="2">
            <span class="option-text">省電力設計が重要</span>
        </label><br>
        <label class="option-label">
            <input type="checkbox" name="microcontroller-features" value="3">
            <span class="option-text">大容量メモリが必要</span>
        </label><br>
        <label class="option-label">
            <input type="checkbox" name="microcontroller-features" value="4">
            <span class="option-text">長時間の安定動作が必要</span>
        </label><br>
        <label class="option-label">
            <input type="checkbox" name="microcontroller-features" value="5">
            <span class="option-text">インターネット接続が必須</span>
        </label><br>
        <label class="option-label">
            <input type="checkbox" name="microcontroller-features" value="6">
            <span class="option-text">決定論的な動作が求められる</span>
        </label><br>
        <label class="option-label">
            <input type="checkbox" name="microcontroller-features" value="7">
            <span class="option-text">高速な3D描画が必要</span>
        </label><br>
    </div>

    <button class="check-multiple-choice" onclick="checkMultipleChoice('microcontroller-features')">答えを確認</button>
    <div class="multiple-choice-result"></div>
</div>

<script>
window.multipleChoiceData = window.multipleChoiceData || {};
window.multipleChoiceData["microcontroller-features"] = {
    "correct": [0, 2, 4, 6],
    "explanation": "組み込みシステムは、リアルタイム性、省電力性、安定性、決定論的な動作が重要な特徴です。高性能GPU、大容量メモリ、インターネット接続、3D描画は一般的に必須ではありません。"
};
</script>


## まとめ

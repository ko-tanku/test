"""
テスト資料用の専門用語、FAQ、TIPSデータ
IT・組み込み技術テーマ
"""

from src.core.knowledge_manager import Term, FaqItem, TipItem

# 組み込み技術用専門用語リスト
EMBEDDED_TERMS = [
    Term(
        term="マイコン",
        definition="マイクロコントローラの略。CPU、メモリ、I/Oなどを1チップに集積した小型コンピュータ。",
        category="ハードウェア",
        related_terms=["CPU", "組み込みシステム", "SoC"],
        first_chapter="第2章",
        context_snippets=[
            "マイコンは組み込みシステムの心臓部です。",
            "8ビットから32ビットまで様々な種類があります。"
        ]
    ),
    Term(
        term="センサー",
        definition="物理量（温度、圧力、光など）を電気信号に変換する素子。",
        category="ハードウェア",
        related_terms=["アクチュエータ", "A/D変換"],
        first_chapter="第2章",
        context_snippets=[
            "センサーからの入力を処理して、適切な制御を行います。"
        ]
    ),
    Term(
        term="アクチュエータ",
        definition="電気信号を物理的な動作（モーター回転、バルブ開閉など）に変換する装置。",
        category="ハードウェア",
        related_terms=["センサー", "サーボモーター"],
        first_chapter="第2章"
    ),
    Term(
        term="RTOS",
        definition="Real-Time Operating System。リアルタイム性を保証するOS。",
        category="ソフトウェア",
        related_terms=["リアルタイムシステム", "スケジューリング"],
        first_chapter="第4章",
        context_snippets=[
            "RTOSを使用することで、複雑なタスク管理が可能になります。"
        ]
    ),
    Term(
        term="割り込み",
        definition="CPUの通常処理を一時中断して、緊急の処理を実行する仕組み。",
        category="システム",
        related_terms=["ISR", "プリエンプション"],
        first_chapter="第3章"
    ),
    Term(
        term="デバッガ",
        definition="プログラムのバグを発見・修正するためのツール。",
        category="開発ツール",
        related_terms=["IDE", "エミュレータ"],
        first_chapter="第1章"
    ),
    Term(
        term="フラッシュメモリ",
        definition="電源を切ってもデータが保持される不揮発性メモリ。プログラムの格納に使用。",
        category="ハードウェア",
        related_terms=["ROM", "EEPROM"],
        first_chapter="第3章"
    ),
    Term(
        term="PWM",
        definition="Pulse Width Modulation。パルス幅変調。デジタル信号で擬似的にアナログ値を表現。",
        category="制御技術",
        related_terms=["D/A変換", "モーター制御"],
        first_chapter="第3章"
    ),
    Term(
        term="I2C",
        definition="Inter-Integrated Circuit。シリアル通信プロトコルの一種。",
        category="通信",
        related_terms=["SPI", "UART"],
        first_chapter="第3章"
    ),
    Term(
        term="デッドライン",
        definition="処理が完了すべき制限時間。リアルタイムシステムで重要な概念。",
        category="リアルタイムシステム",
        related_terms=["リアルタイム性", "レイテンシ"],
        first_chapter="第4章"
    )
]

# 組み込み技術FAQリスト
EMBEDDED_FAQ_ITEMS = [
    FaqItem(
        question="マイコンとマイクロプロセッサの違いは何ですか？",
        answer="マイコンはCPU、メモリ、I/Oを1チップに集積していますが、マイクロプロセッサはCPU機能のみです。マイコンは組み込み用途、マイクロプロセッサはPC用途が主です。",
        category="基本概念"
    ),
    FaqItem(
        question="RTOSは必ず必要ですか？",
        answer="小規模なシステムではベアメタルプログラミング（OS無し）でも十分です。複数のタスクを管理する必要がある場合にRTOSが有効です。",
        category="システム設計"
    ),
    FaqItem(
        question="組み込みプログラミングに最適な言語は？",
        answer="C言語が最も一般的です。ハードウェア制御が可能で、実行効率が高いためです。最近はC++も使われます。",
        category="プログラミング"
    ),
    FaqItem(
        question="デバッグが難しいです。良い方法はありますか？",
        answer="1. LEDやシリアル出力でのprintf デバッグ 2. JTAGデバッガの使用 3. オシロスコープでの信号確認 4. 段階的なテスト実施",
        category="トラブルシューティング"
    ),
    FaqItem(
        question="消費電力を削減する方法は？",
        answer="1. クロック周波数の低減 2. スリープモードの活用 3. 不要な周辺機能の停止 4. 効率的なアルゴリズムの使用",
        category="省電力設計"
    ),
    FaqItem(
        question="組み込みシステムのセキュリティ対策は？",
        answer="1. ファームウェアの暗号化 2. セキュアブート実装 3. 通信の暗号化 4. デバッグポートの無効化",
        category="セキュリティ"
    )
]

# 組み込み技術TIPSリスト
EMBEDDED_TIP_ITEMS = [
    TipItem(
        title="割り込み処理は短く",
        content="割り込みサービスルーチン（ISR）内では最小限の処理のみ行い、時間のかかる処理はメインループに委譲しましょう。",
        category="プログラミング"
    ),
    TipItem(
        title="volatile修飾子の重要性",
        content="割り込みやハードウェアレジスタにアクセスする変数には必ずvolatile修飾子を付けて、コンパイラの最適化を防ぎましょう。",
        category="プログラミング"
    ),
    TipItem(
        title="ウォッチドッグタイマーの活用",
        content="システムの暴走を防ぐため、ウォッチドッグタイマーを設定し、定期的にリセットすることで信頼性を向上させます。",
        category="信頼性"
    ),
    TipItem(
        title="メモリマップを理解する",
        content="使用するマイコンのメモリマップ（ROM、RAM、レジスタの配置）を理解することで、効率的なプログラミングが可能になります。",
        category="システム理解"
    ),
    TipItem(
        title="オシロスコープは必須ツール",
        content="デジタル信号の波形を確認できるオシロスコープは、組み込み開発には欠かせません。タイミング問題の解析に威力を発揮します。",
        category="開発ツール"
    ),
    TipItem(
        title="状態遷移図を描く",
        content="複雑な制御ロジックは、まず状態遷移図を描いてから実装すると、バグが減り保守性も向上します。",
        category="設計手法"
    )
]
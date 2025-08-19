"""
組込制御入門の専門用語、FAQ、TIPSデータ
"""

from src.core.knowledge_manager import Term, FaqItem, TipItem

# 専門用語リスト
EMBEDDED_INTRO_TERMS = [
    Term(
        term="組込制御",
        definition="特定の機器や装置に組み込まれ、その動作を制御するコンピュータシステム。センサーで情報を取得し、プログラムで判断し、アクチュエーターで動作を実行する。",
        category="基本概念",
        related_terms=["組み込みシステム", "制御システム"],
        first_chapter="第1章",
        context_snippets=[
            "組込制御は「特定の目的のために機械に組み込まれた、賢いお世話係」",
            "私たちの身の回りにある組込制御を探してみよう！"
        ]
    ),
    Term(
        term="組み込みシステム",
        definition="特定の機能を実現するために機器に組み込まれたコンピュータシステム。汎用的なPCとは異なり、特定の用途に特化している。",
        category="基本概念",
        related_terms=["組込制御", "専用システム"],
        first_chapter="第1章"
    ),
    Term(
        term="センシング",
        definition="センサーを使って周囲の環境や状態を検知・測定すること。温度、圧力、光、動きなど様々な物理量を電気信号に変換する。",
        category="機能要素",
        related_terms=["センサー", "入力"],
        first_chapter="第1章",
        context_snippets=[
            "センシング、判断、アクチュエーションを人間の五感、脳、手足に例えて説明"
        ]
    ),
    Term(
        term="アクチュエーション",
        definition="制御システムが判断した結果に基づいて、実際に機器を動作させること。モーターを回転させたり、バルブを開閉したりする動作。",
        category="機能要素",
        related_terms=["アクチュエーター", "出力", "実行"],
        first_chapter="第1章"
    ),
    Term(
        term="フィードバック",
        definition="実行した結果を再度センシングして、目標値との差を確認し、制御を調整する仕組み。より正確な制御を実現する。",
        category="制御概念",
        related_terms=["制御ループ", "閉ループ制御"],
        first_chapter="第1章",
        context_snippets=[
            "フィードバックを「結果を見て調整する」という日常の行動に例える"
        ]
    ),
    Term(
        term="リアルタイム性",
        definition="決められた時間内に確実に処理を完了する性質。組み込みシステムでは、遅延が許されない場面が多い。",
        category="システム特性",
        related_terms=["リアルタイムOS", "応答時間"],
        first_chapter="第1章"
    ),
    Term(
        term="ITシステム",
        definition="情報技術を活用した汎用的なコンピュータシステム。PC、スマートフォン、Webサービスなど、様々な用途に対応できる。",
        category="システム分類",
        related_terms=["汎用システム", "情報システム"],
        first_chapter="第2章",
        context_snippets=[
            "ITを「オールマイティな情報処理のプロ」と比喩"
        ]
    ),
    Term(
        term="汎用OS",
        definition="Windows、macOS、Linuxなど、様々なアプリケーションを実行できる汎用的なオペレーティングシステム。",
        category="ソフトウェア",
        related_terms=["OS", "オペレーティングシステム"],
        first_chapter="第2章"
    ),
    Term(
        term="特定用途",
        definition="ある特定の目的や機能のために設計・最適化されていること。組み込みシステムの特徴の一つ。",
        category="システム特性",
        related_terms=["専用システム", "組み込みシステム"],
        first_chapter="第2章"
    ),
    Term(
        term="リアルタイムOS",
        definition="リアルタイム性を保証するために設計されたOS。RTOSとも呼ばれ、時間制約の厳しい処理を確実に実行する。",
        category="ソフトウェア",
        related_terms=["RTOS", "リアルタイム性"],
        first_chapter="第2章"
    ),
    Term(
        term="IoT",
        definition="Internet of Thingsの略。様々な機器がインターネットに接続され、相互に通信・連携する仕組み。",
        category="技術トレンド",
        related_terms=["クラウド", "ネットワーク"],
        first_chapter="第2章",
        context_snippets=[
            "近年の進化：IoTでつながる世界"
        ]
    ),
    Term(
        term="クラウド",
        definition="インターネット経由でコンピューティングリソースやサービスを提供する仕組み。組み込み機器もクラウドと連携することが増えている。",
        category="技術トレンド",
        related_terms=["IoT", "ネットワーク"],
        first_chapter="第2章"
    ),
    Term(
        term="要件定義",
        definition="システムに必要な機能や性能を明確に定義すること。開発の最初の重要なステップ。",
        category="開発プロセス",
        related_terms=["仕様書", "設計"],
        first_chapter="第3章"
    ),
    Term(
        term="テスト",
        definition="開発したシステムが正しく動作するか確認する作業。品質保証の重要な工程。",
        category="開発プロセス",
        related_terms=["検証", "デバッグ"],
        first_chapter="第3章"
    )
]

# FAQリスト
EMBEDDED_INTRO_FAQ_ITEMS = [
    FaqItem(
        question="家電とスマホ、何が違うの？",
        answer="家電は特定の機能（洗濯、調理など）に特化した組み込みシステムで、スマホは多様なアプリを実行できる汎用的なITシステムです。家電は単機能で高信頼性、スマホは多機能で柔軟性が特徴です。",
        category="基本概念"
    ),
    FaqItem(
        question="なぜITエンジニアと組み込みエンジニアは違うの？",
        answer="扱うシステムの性質が異なるためです。ITエンジニアは汎用的なソフトウェアやWebサービスを開発し、組み込みエンジニアはハードウェアと密接に連携する特定用途のシステムを開発します。必要な知識やスキルセットが異なります。",
        category="キャリア"
    ),
    FaqItem(
        question="数学が苦手でも大丈夫？",
        answer="基本的な論理的思考力があれば大丈夫です。高度な数学は必須ではありません。むしろ、ユーザー視点で考える力、コミュニケーション能力、問題解決能力などが重要です。必要な数学知識は働きながら身につけることができます。",
        category="学習"
    ),
    FaqItem(
        question="プログラミング経験がなくても組み込み技術者になれる？",
        answer="はい、なれます。多くの企業では未経験者向けの研修制度があります。大切なのは、技術に対する興味と学習意欲です。基礎から段階的に学んでいけば、必ず習得できます。",
        category="キャリア"
    ),
    FaqItem(
        question="組み込みシステムの具体的な例をもっと知りたい",
        answer="身近な例：電子レンジ（温度制御）、デジタルカメラ（画像処理）、自動車のエンジン制御、エアコンの温度調整、炊飯器の炊飯プログラム、体温計、血圧計、スマートウォッチなど、日常生活のあらゆる場面で活躍しています。",
        category="応用例"
    ),
    FaqItem(
        question="文系出身者の強みは何？",
        answer="コミュニケーション能力、文書作成能力、論理的思考力、ユーザー視点での発想力などです。技術者同士や顧客との橋渡し役として、また要件定義や仕様書作成において、これらの能力は非常に重要です。",
        category="キャリア"
    )
]

# TIPSリスト
EMBEDDED_INTRO_TIP_ITEMS = [
    TipItem(
        title="声に出して説明してみよう",
        content="学んだ概念を誰かに説明するつもりで声に出してみると、理解が深まります。「組込制御とは...」と始めて、自分の言葉で説明してみましょう。",
        category="学習方法"
    ),
    TipItem(
        title="身の回りの製品を観察しよう",
        content="家電製品を使うとき、「この製品にはどんなセンサーがあるか」「どんな制御をしているか」を考えてみましょう。学習内容が身近に感じられます。",
        category="学習方法"
    ),
    TipItem(
        title="図にまとめる習慣をつけよう",
        content="センシング→判断→アクチュエーションの流れなど、概念を図にまとめると理解しやすくなります。手書きでもデジタルでも、自分なりの図を作ってみましょう。",
        category="学習方法"
    ),
    TipItem(
        title="次のステップ：Python入門",
        content="プログラミングを始めるなら、Pythonがおすすめです。文法がシンプルで、組み込み開発でも使われることが増えています。無料のオンライン教材から始めましょう。",
        category="次のステップ"
    ),
    TipItem(
        title="簡単な電子工作から始めよう",
        content="Arduino（アルドゥイーノ）やRaspberry Pi（ラズベリーパイ）などの学習用ボードで、LEDを光らせたり、センサーを使ったりする簡単な工作から始めると、組み込みの世界が体感できます。",
        category="次のステップ"
    ),
    TipItem(
        title="技術ニュースをチェックしよう",
        content="組み込み技術の最新動向を知るために、技術系ニュースサイトを定期的にチェックしましょう。IoT、自動運転、スマート家電などのキーワードに注目です。",
        category="情報収集"
    ),
    TipItem(
        title="コミュニティに参加しよう",
        content="組み込み技術者のコミュニティやSNSグループに参加すると、現場の声が聞けます。初心者歓迎のコミュニティも多いので、積極的に質問してみましょう。",
        category="ネットワーキング"
    ),
    TipItem(
        title="失敗を恐れずに挑戦しよう",
        content="技術習得には試行錯誤がつきものです。エラーやうまくいかないことも学習の一部。失敗から学ぶ姿勢が、優秀な技術者への第一歩です。",
        category="マインドセット"
    )
]
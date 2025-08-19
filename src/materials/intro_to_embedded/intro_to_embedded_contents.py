"""
組込制御入門のコンテンツ生成管理クラス
"""

import sys
from pathlib import Path
from typing import List, Dict

# プロジェクトルートをsys.pathに追加
# 想定: .../src/materials/intro_to_embedded/intro_to_embedded_contents.py
project_root = Path(__file__).resolve().parents[3]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.core.content_manager import BaseContentManager
from src.materials.intro_to_embedded.intro_to_embedded_config import (
    MATERIAL_CONFIG, INTRO_TO_EMBEDDED_COLORS
)
from src.materials.intro_to_embedded.intro_to_embedded_terms import (
    EMBEDDED_INTRO_TERMS, EMBEDDED_INTRO_FAQ_ITEMS, EMBEDDED_INTRO_TIP_ITEMS
)
from src.materials.intro_to_embedded.intro_to_embedded_charts import create_all_intro_charts
from src.materials.intro_to_embedded.intro_to_embedded_tables import create_all_intro_tables


class IntroToEmbeddedContentManager(BaseContentManager):
    """組込制御入門のコンテンツ管理クラス"""

    def __init__(self, material_name: str, output_base_dir: Path):
        """初期化"""
        super().__init__(
            material_name=material_name,
            output_base_dir=output_base_dir,
            colors=INTRO_TO_EMBEDDED_COLORS
        )
        self.generated_charts: Dict[str, Path] = {}
        self.generated_tables: Dict[str, Path] = {}

        # 専門用語、FAQ、TIPSを登録
        self._register_material_terms(EMBEDDED_INTRO_TERMS)
        self._register_faq_tips(EMBEDDED_INTRO_FAQ_ITEMS, EMBEDDED_INTRO_TIP_ITEMS)

    def generate_content(self) -> List[Path]:
        """
        組込制御入門の全コンテンツを生成
        """
        generated_files = []

        # 必要なディレクトリを作成
        docs_dir = self.output_base_dir / "documents"
        charts_dir = self.output_base_dir / "charts"
        tables_dir = self.output_base_dir / "tables"
        docs_dir.mkdir(parents=True, exist_ok=True)
        charts_dir.mkdir(parents=True, exist_ok=True)
        tables_dir.mkdir(parents=True, exist_ok=True)

        # 図表と表を事前生成
        self.generated_charts = create_all_intro_charts(self.chart_gen, charts_dir)
        self.generated_tables = create_all_intro_tables(self.table_gen, tables_dir)

        # --- コンテンツ生成 ---

        # トップページ (index.md)
        self.doc_builder.output_dir = self.output_base_dir
        generated_files.append(self._generate_index_page())

        # 各章のコンテンツ (documents/chapterXX.md)
        self.doc_builder.output_dir = docs_dir
        generated_files.append(self._generate_chapter1_page())
        generated_files.append(self._generate_chapter2_page())
        generated_files.append(self._generate_chapter3_page())

        # 演習問題 (exercises.md)
        self.doc_builder.output_dir = self.output_base_dir
        generated_files.append(self._generate_exercises_page())

        # 付録ページ (glossary.md, faq.md, tips.md)
        generated_files.append(self.generate_glossary())
        generated_files.append(self.generate_faq_page())
        generated_files.append(self.generate_tips_page())

        return generated_files

    def _generate_index_page(self) -> Path:
        """トップページ(index.md)を生成"""
        self.doc_builder.clear_content()

        self.doc_builder.add_heading(MATERIAL_CONFIG["title"], 1) #

        self.doc_builder.add_paragraph(
            "あなたの周りを見回してみてください。スマートフォン、エアコン、電子レンジ、自動車..."
            "これらすべてに共通するものは何でしょうか？"
        )

        self.doc_builder.add_paragraph(
            "答えは「**組込制御**」です。私たちの生活を便利で快適にしている、目に見えない「賢い仕組み」"
            "が、あらゆる機器の中で働いています。"
        )

        # イントロ図を挿入
        intro_concept_path = self.generated_charts.get('intro_concept')
        if intro_concept_path:
            self.doc_builder.add_html_component_reference(
                Path("charts") / intro_concept_path.name,
                '100%',
                '450px'
            )

        self.doc_builder.add_heading("なぜ文系から組込制御技術者を目指すのか", 2)

        self.doc_builder.add_paragraph(
            "「技術者」と聞くと、理系の世界だと思われがちです。しかし、実は文系出身者こそが"
            "組込制御の世界で活躍できる素質を持っています。"
        )

        self.doc_builder.add_unordered_list([
            "**論理的思考力**: 文章を構成する力は、プログラムを設計する力につながります",
            "**コミュニケーション能力**: チーム開発や顧客との対話で大きな強みになります",
            "**ユーザー視点**: 使う人の立場で考える力が、より良い製品開発につながります"
        ])

        self.doc_builder.add_heading("この資料で何が学べるか", 2)

        self.doc_builder.add_admonition(
            "info",
            "学習ゴール",
            "\n".join([f"✅ {goal}" for goal in MATERIAL_CONFIG["learning_objectives"]]), #
            False
        )

        self.doc_builder.add_heading("資料の構成と読み進め方", 2)

        chapters = [
            "[第1章: 組込制御ってなんだろう？](documents/chapter01.md) - 基本概念と身近な例",
            "[第2章: ITと組み込み技術、何が違う？](documents/chapter02.md) - それぞれの特徴と役割",
            "[第3章: 文系から組み込み技術者を目指す意義](documents/chapter03.md) - キャリアパスの可能性",
            "[演習問題](exercises.md) - 理解度チェック"
        ]
        self.doc_builder.add_ordered_list(chapters)

        self.doc_builder.add_heading("付録", 2)
        other_pages = [
            "[用語集](glossary.md) - 専門用語の詳細解説",
            "[よくある質問（FAQ）](faq.md) - 疑問や不安を解消",
            "[学習TIPS](tips.md) - 効率的な学習のヒント"
        ]
        self.doc_builder.add_unordered_list(other_pages)

        self.doc_builder.add_admonition(
            "tip",
            "学習のヒント",
            "各章は約15-20分で読めるように構成されています。まずは全体を通して読み、"
            "その後、興味のある部分を深く学習することをおすすめします。",
            False
        )

        return self.doc_builder.save_markdown("index.md")

    def _generate_chapter1_page(self) -> Path:
        """第1章のページ(documents/chapter01.md)を生成"""
        self.doc_builder.clear_content()
        terms = self.knowledge_mgr.get_terms_for_chapter("第1章") #

        # --- 1. タイトルと概要 ---
        self.doc_builder.add_heading("第1章: 組込制御ってなんだろう？ ～私たちの身近な「賢い」仕組み～", 1)
        self.doc_builder.add_paragraph("この章では、組込制御の基本的な概念を、身近な例を通じて理解していきます。")

        # --- 1.1 組込制御って、一体何のこと？ ---
        self.doc_builder.add_heading("1.1 組込制御って、一体何のこと？", 2)
        self.doc_builder.add_paragraph_with_tooltips(
            "組込制御とは、特定の機器や装置に組み込まれたコンピュータが、その機器の動作を自動的に制御する仕組みのことです。",
            terms
        )
        self.doc_builder.add_quote(
            "組込制御は「特定の目的のために機械に組み込まれた、賢いお世話係」のようなものです。\n私たちが意識しなくても、裏で一生懸命働いてくれています。"
        )
        self.doc_builder.add_paragraph(
            "例えば、エアコンが部屋の温度を自動で調整したり、炊飯器がお米を美味しく炊いてくれたり。これらはすべて組込制御のおかげです。"
        )

        # --- 1.2 身の回りにある組込制御を探してみよう！ ---
        self.doc_builder.add_heading("1.2 身の回りにある組込制御を探してみよう！", 2)
        self.doc_builder.add_paragraph("実は、私たちの生活は組込制御に囲まれています。朝起きてから夜寝るまで、どれだけの組込制御にお世話になっているか見てみましょう。")
        self.doc_builder.add_paragraph("**図1-1: 身の回りの製品に組み込まれた制御システム**")

        embedded_examples_path = self.generated_charts.get('embedded_examples')
        if embedded_examples_path:
            self.doc_builder.add_html_component_reference(
                Path("../../charts") / embedded_examples_path.name, '100%', None
            )

        self.doc_builder.add_admonition(
            "note", "身近な組込制御の例",
            "**家電製品**: 洗濯機（水量・時間の自動調整）、電子レンジ（加熱時間の制御）\n**自動車**: エンジン制御、ブレーキアシスト、エアバッグ\n**医療機器**: 体温計、血圧計、心電図モニター",
            False
        )

        # --- 1.3 組込制御システムって何ができるの？ ---
        self.doc_builder.add_heading("1.3 組込制御システムって何ができるの？", 2)
        self.doc_builder.add_paragraph_with_tooltips(
            "組込制御システムは、基本的に「センシング」「判断」「アクチュエーション」の3つのステップで動作します。そして、結果を確認する「フィードバック」により、より正確な制御を実現します。",
            terms
        )
        self.doc_builder.add_paragraph("**図1-2: 制御ループの基本的な流れ（アニメーション）**")

        sensor_loop_path = self.generated_charts.get('sensor_actuator_loop')
        if sensor_loop_path:
            self.doc_builder.add_image_reference(
                "制御ループアニメーション",
                Path("../../charts") / sensor_loop_path.name
            )

        self.doc_builder.add_ordered_list([
            "**センシング（感知）**: センサーで周囲の状況を把握（人間の五感に相当）",
            "**判断（制御）**: 取得した情報を基に、どう動作すべきか決定（人間の脳に相当）",
            "**アクチュエーション（実行）**: 判断に基づいて実際に動作（人間の手足に相当）",
            "**フィードバック**: 実行結果を確認し、必要に応じて調整"
        ])

        # --- 1.4 まとめ ---
        self.doc_builder.add_heading("1.4 まとめ：組込制御は「縁の下の力持ち」", 2)
        self.doc_builder.add_paragraph("組込制御は、私たちが普段意識することなく、生活を支えてくれている技術です。目立たないけれど、なくてはならない存在。まさに「縁の下の力持ち」と言えるでしょう。")
        self.doc_builder.add_summary_section(
            "この章で学んだこと",
            [
                "組込制御は特定の機器に組み込まれた制御システム",
                "身の回りの多くの製品に組込制御が使われている",
                "センシング→判断→アクチュエーション→フィードバックのサイクルで動作",
                "私たちの生活を便利で快適にする「縁の下の力持ち」"
            ]
        )
        self.doc_builder.add_recommendation_section(
            "次のステップ",
            [
                {'text': '第2章でITと組み込み技術の違いを学ぶ', 'link': 'chapter02.md'},
                {'text': '用語集で専門用語を確認', 'link': '../glossary.md'}
            ]
        )

        return self.doc_builder.save_markdown("chapter01.md")

    def _generate_chapter2_page(self) -> Path:
        """第2章のページ(documents/chapter02.md)を生成"""
        self.doc_builder.clear_content()
        terms = self.knowledge_mgr.get_terms_for_chapter("第2章") #

        self.doc_builder.add_heading("第2章: ITと組み込み技術、何が違う？～それぞれの役割と未来～", 1)
        self.doc_builder.add_paragraph("この章では、ITシステムと組み込みシステムの違いと共通点を理解し、それぞれの役割を学びます。")

        self.doc_builder.add_heading("2.1 あなたのPCやスマホは「ITシステム」？", 2)
        self.doc_builder.add_paragraph_with_tooltips(
            "ITシステムとは、情報技術を活用した汎用的なコンピュータシステムのことです。PCやスマートフォンは、様々なアプリケーションを実行できる汎用OSを搭載しています。",
            terms
        )
        self.doc_builder.add_quote("ITシステムは「オールマイティな情報処理のプロ」。\n文書作成、動画視聴、ゲーム、プログラミング...何でもこなせる万能選手です。")
        self.doc_builder.add_admonition(
            "info", "ITシステムの特徴",
            "• **汎用性**: 様々な用途に対応可能\n• **柔軟性**: ソフトウェアの追加・変更が容易\n• **拡張性**: 機能を後から追加できる\n• **ネットワーク連携**: インターネットを通じた情報共有",
            False
        )

        self.doc_builder.add_heading("2.2 自動車や洗濯機は「組み込みシステム」？", 2)
        self.doc_builder.add_paragraph_with_tooltips(
            "組み込みシステムは、特定の機能を実現するために機器に組み込まれたコンピュータシステムです。特定用途に特化し、リアルタイム性が求められることが多いのが特徴です。",
            terms
        )
        self.doc_builder.add_quote("組み込みシステムは「特定の仕事を極める職人」。\n一つのことを確実に、効率的に、長時間こなすスペシャリストです。")
        self.doc_builder.add_admonition(
            "warning", "組み込みシステムの特徴",
            "• **特定用途**: 決められた機能に特化\n• **高信頼性**: 24時間365日の安定動作\n• **省資源**: 限られたメモリ・CPUで動作\n• **リアルタイム性**: 決められた時間内での処理完了",
            False
        )

        self.doc_builder.add_heading("2.3 ITと組み込み、ここが違う！ここが似てる！", 2)
        self.doc_builder.add_paragraph("それでは、ITシステムと組み込みシステムを詳しく比較してみましょう。")
        self.doc_builder.add_paragraph("**ITシステムと組み込みシステムの比較**")

        comparison_table_path = self.generated_tables.get('it_embedded_comparison')
        if comparison_table_path:
            self.doc_builder.add_html_component_reference(
                Path("../../tables") / comparison_table_path.name, '100%', None
            )

        self.doc_builder.add_paragraph("**図2-1: ITシステムと組み込みシステムの構成比較**")

        diagram_path = self.generated_charts.get('it_embedded_system_diagram')
        if diagram_path:
            self.doc_builder.add_html_component_reference(
                Path("../../charts") / diagram_path.name, '100%', None
            )

        self.doc_builder.add_heading("2.4 近年の進化：IoTでつながる世界", 2)
        self.doc_builder.add_paragraph_with_tooltips(
            "最近では、IoT（Internet of Things）により、組み込み機器もネットワークに接続され、クラウドと連携するようになってきました。ITと組み込みの境界が曖昧になりつつあります。",
            terms
        )
        self.doc_builder.add_admonition(
            "note", "IoTがもたらす変化",
            "• スマート家電: エアコンをスマホで操作\n• 見守りシステム: センサーデータをクラウドで分析\n• 予防保全: 機器の異常を事前に検知\n• ビッグデータ活用: 大量のセンサーデータから新たな価値を創出",
            False
        )

        self.doc_builder.add_heading("2.5 まとめ：それぞれの進化と融合", 2)
        self.doc_builder.add_paragraph("ITシステムと組み込みシステムは、それぞれ異なる強みを持ちながら、IoTによって融合し、新たな価値を生み出しています。")
        self.doc_builder.add_summary_section(
            "この章で学んだこと",
            [
                "ITシステムは汎用的で柔軟、組み込みシステムは特定用途で高信頼",
                "それぞれに得意分野があり、適材適所で使い分けられている",
                "IoTにより、両者が連携する新しい時代が到来",
                "技術の進化により、より便利で安全な社会が実現されつつある"
            ]
        )
        self.doc_builder.add_recommendation_section(
            "関連情報",
            [
                {'text': '第3章で組み込み技術者を目指す意義を学ぶ', 'link': 'chapter03.md'},
                {'text': 'IoTの最新動向を調べてみる', 'link': ''}
            ]
        )

        return self.doc_builder.save_markdown("chapter02.md")

    def _generate_chapter3_page(self) -> Path:
        """第3章のページ(documents/chapter03.md)を生成"""
        self.doc_builder.clear_content()
        terms = self.knowledge_mgr.get_terms_for_chapter("第3章") #

        self.doc_builder.add_heading("第3章: 文系から組み込み技術者を目指す意義", 1)
        self.doc_builder.add_paragraph("この章では、組み込み技術者の仕事内容を知り、文系出身者がこの分野で活躍できる理由を理解します。")

        self.doc_builder.add_heading("3.1 組み込み技術者ってどんな仕事？", 2)
        self.doc_builder.add_paragraph("組み込み技術者は、私たちの生活を支える様々な機器に「魂」を吹き込む仕事です。単にプログラムを書くだけでなく、製品全体を見渡し、ユーザーにとって最適な動作を実現します。")
        self.doc_builder.add_quote("組み込み技術者は「製品の『魂』を吹き込む人」。\n機械に命を与え、人々の生活を豊かにする、創造的な仕事です。")
        self.doc_builder.add_paragraph_with_tooltips(
            "主な仕事内容には、要件定義（お客様の要望を技術仕様に落とし込む）、設計・実装（実際にプログラムを作成）、テスト（正しく動作するか確認）などがあります。",
            terms
        )
        self.doc_builder.add_admonition(
            "info", "組み込み技術者の一日",
            "**午前**: チームミーティング、仕様書の確認\n**午後**: プログラミング、実機でのテスト\n**夕方**: テスト結果の分析、改善案の検討\n\n技術的な作業だけでなく、コミュニケーションも重要な仕事です。",
            False
        )

        self.doc_builder.add_heading("3.2 文系だからこそ輝ける！あなたの強みとは？", 2)
        self.doc_builder.add_paragraph("「文系だから技術者は無理」そう思っていませんか？実は、文系出身者だからこそ持っている強みが、組み込み開発の現場で大いに活かされるのです。")
        self.doc_builder.add_unordered_list([
            '**論理的思考力**: 論文やレポートで培った論理構成力は、プログラムの設計に直結します',
            '**コミュニケーション能力**: チーム開発では、技術者同士の意思疎通が成功の鍵です',
            '**文書作成能力**: 仕様書や設計書など、技術文書の作成は重要な業務です',
            '**ユーザー視点**: 技術に偏らない視点が、使いやすい製品開発につながります',
            '**問題解決能力**: 複雑な課題を整理し、解決策を見出す力は共通です'
        ])
        self.doc_builder.add_admonition(
            "tip", "成功事例",
            "多くの文系出身エンジニアが活躍しています：\n• 営業経験を活かし、顧客ニーズを的確に製品に反映\n• 語学力を活かし、海外チームとの架け橋に\n• 心理学の知識を活かし、使いやすいUIを設計",
            True
        )

        self.doc_builder.add_heading("3.3 社会を動かす、未来を創る：組み込み技術者の意義", 2)
        self.doc_builder.add_paragraph("組み込み技術者の仕事は、単なる「ものづくり」ではありません。人々の生活を支え、社会を前進させる、意義深い仕事です。")
        self.doc_builder.add_admonition(
            "success", "組み込み技術者が創る未来",
            "**医療分野**: 生命を救う医療機器の開発\n**環境分野**: 省エネ家電で地球環境に貢献\n**安全分野**: 自動運転技術で交通事故を減らす\n**福祉分野**: 高齢者や障がい者の生活を支援\n\nあなたの技術が、誰かの笑顔につながります。",
            False
        )
        self.doc_builder.add_quote("技術は人のためにある。\n組み込み技術者は、技術と人をつなぐ架け橋です。")

        self.doc_builder.add_heading("3.4 さあ、次の一歩を踏み出そう！", 2)
        self.doc_builder.add_paragraph("ここまで読んでいただいたあなたは、もう組み込み技術者への第一歩を踏み出しています。大切なのは、興味を持ち続け、少しずつ学んでいくことです。")
        self.doc_builder.add_admonition(
            "note", "今後の学習ステップ",
            "1. **基礎知識の習得**: この資料で基本概念を理解\n2. **プログラミング入門**: PythonやC言語の基礎を学ぶ\n3. **実践的な学習**: 簡単な電子工作やプロジェクトに挑戦\n4. **コミュニティ参加**: 勉強会やオンラインコミュニティで仲間を見つける\n5. **キャリア形成**: インターンシップや就職活動へ",
            False
        )
        self.doc_builder.add_summary_section(
            "この章で学んだこと",
            [
                "組み込み技術者は製品に「魂」を吹き込む創造的な仕事",
                "文系出身者の強み（論理的思考、コミュニケーション力など）が活きる",
                "社会に貢献し、人々の生活を豊かにする意義深い仕事",
                "興味と学習意欲があれば、誰でも技術者を目指せる"
            ]
        )
        self.doc_builder.add_recommendation_section(
            "次のアクション",
            [
                {'text': '演習問題で理解度をチェック', 'link': '../exercises.md'},
                {'text': '学習TIPSで効率的な学習方法を確認', 'link': '../tips.md'},
                {'text': 'FAQで疑問を解消', 'link': '../faq.md'}
            ]
        )

        return self.doc_builder.save_markdown("chapter03.md")

    def _generate_exercises_page(self) -> Path:
        """演習問題ページ(exercises.md)を生成"""
        self.doc_builder.clear_content()

        self.doc_builder.add_heading("演習問題", 1)
        self.doc_builder.add_paragraph(
            "これまでの章で学んだ内容の理解度を確認しましょう。"
            "自分の言葉で説明できるようになることが大切です。"
        )

        self.doc_builder.add_heading("第1章の確認問題", 2)
        self.doc_builder.add_exercise_question({
            'question': '組込制御とは何か、身近な例を2つ挙げて説明してください。',
            'answer': '組込制御とは、特定の機器に組み込まれたコンピュータがその機器の動作を自動制御する仕組みです。例：(1)エアコン - 室温センサーで温度を検知し、設定温度に合わせて冷暖房を自動調整。(2)炊飯器 - 温度と時間を制御して、お米を最適な状態に炊き上げる。',
            'explanation': '組込制御の定義と、センサー・制御・アクチュエーターの働きを具体例で説明できることが重要です。',
            'difficulty': 'easy'
        })
        self.doc_builder.add_exercise_question({
            'question': 'センシング、判断、アクチュエーション、フィードバックの4つの要素について、エアコンを例に説明してください。',
            'answer': 'センシング：温度センサーが室温を測定。判断：マイコンが設定温度と比較して冷房/暖房/停止を決定。アクチュエーション：コンプレッサーやファンを動作させて温度調整。フィードバック：調整後の室温を再度センシングして、継続的に最適な温度を維持。',
            'explanation': '制御ループの各要素がどのように連携して動作するかを理解することが重要です。',
            'difficulty': 'medium'
        })

        self.doc_builder.add_heading("第2章の確認問題", 2)
        self.doc_builder.add_exercise_question({
            'question': 'ITシステムと組み込みシステムの最も大きな違いを3つ挙げて説明してください。',
            'answer': '(1)用途：ITシステムは汎用的で様々な用途に対応、組み込みは特定機能に特化。(2)リアルタイム性：組み込みは決められた時間内での処理が必須、ITシステムは必須ではない。(3)動作環境：組み込みは限られたリソースで24時間365日安定動作が必要、ITシステムは豊富なリソースを使用可能。',
            'explanation': 'それぞれのシステムの特徴と、なぜそのような違いがあるのかを理解することが重要です。',
            'difficulty': 'medium'
        })
        self.doc_builder.add_exercise_question({
            'question': 'IoTによってITと組み込み技術がどのように融合しているか、具体例を挙げて説明してください。',
            'answer': 'IoTにより、組み込み機器がインターネットに接続され、クラウドと連携するようになりました。例：スマート家電では、エアコンの組み込みシステムがWi-Fi経由でクラウドに接続し、スマホアプリ（ITシステム）から遠隔操作が可能。使用データをクラウドで分析し、省エネ提案なども行えます。',
            'explanation': 'IoTが単なる遠隔操作だけでなく、データ活用による新しい価値創造につながることを理解しましょう。',
            'difficulty': 'hard'
        })

        self.doc_builder.add_heading("第3章の確認問題", 2)
        self.doc_builder.add_exercise_question({
            'question': '文系出身者が組み込み技術者として活躍できる理由を、具体的な強みを3つ挙げて説明してください。',
            'answer': '(1)論理的思考力：レポートや論文作成で培った論理構成力は、プログラムの設計に直接活かせる。(2)コミュニケーション能力：チーム開発や顧客対応で、技術者間の橋渡し役として活躍できる。(3)ユーザー視点：技術に偏らない視点で、実際に使う人の立場に立った製品開発ができる。',
            'explanation': '技術力だけでなく、総合的な能力が組み込み開発では重要であることを理解しましょう。',
            'difficulty': 'easy'
        })
        self.doc_builder.add_exercise_question({
            'question': '組み込み技術者が社会に貢献できる分野を2つ選び、具体的にどのような貢献ができるか説明してください。',
            'answer': '(1)医療分野：ペースメーカーや人工呼吸器などの生命維持装置の開発により、多くの命を救うことができる。正確で安定した動作により、患者の生活の質を向上させる。(2)環境分野：省エネ家電の制御システム開発により、電力消費を削減。スマートグリッドなどの技術で、社会全体のエネルギー効率を改善し、地球環境保護に貢献。',
            'explanation': '技術が単なる便利さだけでなく、社会課題の解決につながることを意識することが大切です。',
            'difficulty': 'medium'
        })

        self.doc_builder.add_admonition(
            "tip",
            "解答のポイント",
            "正解を暗記するのではなく、自分の言葉で説明できるようになることが大切です。"
            "実際の製品や体験と結びつけて考えると、理解が深まります。",
            False
        )

        return self.doc_builder.save_markdown("exercises.md")
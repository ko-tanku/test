import logging
from pathlib import Path
from typing import List, Dict, Any

<<<<<<< HEAD
# import matplotlib.pyplot as plt # 不要になったため削除

from src.core.content_manager import BaseContentManager
from src.core.knowledge_manager import Term, FaqItem, TipItem
=======
from src.core.content_manager import BaseContentManager
from src.core.knowledge_manager import Term, FaqItem, TipItem
from src.materials.test_material.generators import ascii_art_generator
>>>>>>> dbde2096846e5b4398413351225cc5f784d336f1

logger = logging.getLogger(__name__)

class TestMaterialContentManager(BaseContentManager):
    """
    test_materialのコンテンツ生成を統括するクラス。
    coreの全機能のテストを目的とする。
    """

    def __init__(self, output_base_dir: Path):
        super().__init__("test_material", output_base_dir)
<<<<<<< HEAD
        # custom_generatorsは不要になったため削除
        # self.custom_generators = {
        #     "draw_voltage_stabilization_graph": self._draw_voltage_stabilization_graph
        # }
=======
        # この教材固有のジェネレータを登録
        self.custom_generators = {
            "ascii_art_generator.generate": ascii_art_generator.generate
        }
>>>>>>> dbde2096846e5b4398413351225cc5f784d336f1

    def generate_content(self) -> List[Path]:
        """
        教材全体のコンテンツを生成するメインメソッド。
        """
        logger.info(f"'{self.material_name}'のコンテンツ生成を開始します。")
        generated_files = []

<<<<<<< HEAD
        # ナレッジと演習問題を読み込む
        self._register_knowledge_from_yaml()
        self._load_exercises_from_yaml()

        # ナレッジページの生成
=======
        # ナレッジページの生成
        self._register_knowledge_from_yaml()
>>>>>>> dbde2096846e5b4398413351225cc5f784d336f1
        generated_files.append(self.generate_glossary())
        generated_files.append(self.generate_faq_page())
        generated_files.append(self.generate_tips_page())

        # 各章のコンテンツを生成
        for i in range(1, 7):
            chapter_filename = f"chapter{i}.yml"
            chapter_data = self.load_chapter_from_yaml(chapter_filename)
            if not chapter_data:
                continue

            # 出力先ディレクトリを決定
            docs_dir = self.output_base_dir / self.material_name / "documents"
            charts_dir = self.output_base_dir / self.material_name / "charts"
            tables_dir = self.output_base_dir / self.material_name / "tables"
            
            # 章データからMarkdownを生成
            output_md_path = self._generate_chapter_from_data(
                chapter_data,
<<<<<<< HEAD
                str(docs_dir / f"chapter{i:02d}.md"),
=======
                docs_dir / f"chapter{i:02d}.md",
>>>>>>> dbde2096846e5b4398413351225cc5f784d336f1
                charts_dir,
                tables_dir
            )
            generated_files.append(output_md_path)

        logger.info(f"'{self.material_name}'のコンテンツ生成が完了しました。")
        return generated_files

    def _register_knowledge_from_yaml(self):
        """
<<<<<<< HEAD
        glossary.yml, faq.yml, tips.ymlからデータを読み込んでKnowledgeManagerに登録する。
        """
        # 用語の読み込み
        glossary_data = self.load_chapter_from_yaml("glossary.yml")
        if glossary_data:
            terms_list = [Term(**data) for data in glossary_data.get("terms", [])]
            self.knowledge_mgr.register_terms_batch(terms_list)

        # FAQの読み込み
        faq_data = self.load_chapter_from_yaml("faq.yml")
        if faq_data:
            faq_list = [FaqItem(**data) for data in faq_data.get("faq", [])]
            self.knowledge_mgr.register_faq_batch(faq_list)

        # TIPSの読み込み
        tips_data = self.load_chapter_from_yaml("tips.yml")
        if tips_data:
            tips_list = [TipItem(**data) for data in tips_data.get("tips", [])]
            self.knowledge_mgr.register_tips_batch(tips_list)

    def _load_exercises_from_yaml(self):
        """
        exercises.ymlから演習問題を読み込んで登録する。
        """
        exercise_data = self.load_chapter_from_yaml("exercises.yml")
        if exercise_data:
            self.exercises = exercise_data.get("exercises", {})
            logger.info(f"{len(self.exercises)}個の演習問題を読み込みました。")

    # _process_content_list のオーバーライドは不要になったため削除
    # def _process_content_list(self, contents: List[Dict[str, Any]], charts_dir: Path, tables_dir: Path, chapter_title: str, chapter_path: str):
    #     """
    #     コンテンツリストの処理をオーバーライドし、カスタムジェネレータに対応する。
    #     """
    #     for item in contents:
    #         if item.get('type') == 'custom_generator':
    #             self._process_custom_generator(item, charts_dir)
    #         else:
    #             super()._process_content_list([item], charts_dir, tables_dir, chapter_title, chapter_path)

    # _process_custom_generator も不要になったため削除
    # def _process_custom_generator(self, item: Dict[str, Any], assets_dir: Path):
    #     """
    #     YAMLで定義されたカスタムジェネレータを実行する。
    #     """
    #     generator_key = item.get("generator")
    #     params = item.get("params", {})

    #     if not generator_key or generator_key not in self.custom_generators:
    #         logger.warning(f"未定義のカスタムジェネレータ: {generator_key}")
    #         return

    #     generator_func = self.custom_generators[generator_key]
        
    #     try:
    #         if generator_key == "draw_voltage_stabilization_graph":
    #             chart_path = self.chart_gen.create_custom_figure(
    #                 generator_func, 
    #                 params.get("filename", "custom_chart.html"), 
    #                 output_dir=assets_dir, 
    #                 **params
    #             )
    #             relative_path = Path("..") / assets_dir.name / chart_path.name
    #             self.doc_builder.add_html_component_reference(
    #                 relative_path,
    #                 '100%',  # 幅は100%
    #                 None     # 高さは自動調整
    #             )
    #         else:
    #             generated_asset_path = generator_func(assets_dir, **params)
    #             relative_path = Path("..") / assets_dir.name / generated_asset_path.name
    #             self.doc_builder.add_image_reference(
    #                 alt_text=f"Generated by {generator_key}",
    #                 image_path=relative_path
    #             )

    #     except Exception as e:
    #         logger.error(f"カスタムジェネレータ '{generator_key}' の実行中にエラー: {e}")

    def _resolve_custom_function(self, function_name: str):
        """
        カスタム図表関数名を実際の関数オブジェクトに解決する。
        """
        # 利用可能なカスタム関数のマッピング
        custom_functions = {
            "draw_voltage_stabilization_graph": self._draw_voltage_stabilization_graph
        }
        
        function = custom_functions.get(function_name)
        if function:
            logger.info(f"カスタム関数 '{function_name}' を解決しました")
            return function
        else:
            logger.warning(f"カスタム関数 '{function_name}' が見つかりません")
            return None
    
    def _draw_voltage_stabilization_graph(self, ax, colors, styles, **kwargs):
        """
        電圧安定化グラフを描画するカスタム関数。
        組み込み制御技術の学習用サンプル図表。
        """
        # データの生成 (実用的なサンプルデータ)
        time = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        voltage = [12, 11.5, 11.8, 12.1, 12.0, 12.0, 12.0, 12.0, 12.0, 12.0, 12.0]

        # グラフの描画
        ax.plot(time, voltage, color=colors["info"], linewidth=styles["line_width"], marker='o', markersize=6)

        # 安定化ラインの描画
        ax.axhline(y=12.0, color='red', linestyle='--', label='目標電圧', alpha=0.8)

        # 許容範囲の描画
        ax.fill_between(time, 11.9, 12.1, color='green', alpha=0.2, label='許容範囲')

        # テキストの追加
        ax.text(5, 12.15, '安定化領域', fontsize=styles["font_size_label"], color='green', ha='center', weight='bold')
        ax.text(1, 11.6, '過渡応答', fontsize=styles["font_size_label"], color='orange', ha='center', weight='bold')

        # グラフの装飾
        ax.set_title('電圧安定化システムの応答例', fontsize=styles["font_size_title"], pad=20)
        ax.set_xlabel('時間 (秒)', fontsize=styles["font_size_label"])
        ax.set_ylabel('出力電圧 (V)', fontsize=styles["font_size_label"])
        ax.grid(True, alpha=styles["grid_alpha"], linestyle='-', linewidth=0.5)
        ax.legend(loc='upper right', framealpha=0.9)

        # Y軸の範囲を固定 (視覚的な分かりやすさのため)
        ax.set_ylim(11.0, 12.5)
        ax.set_xlim(-0.5, 10.5)
        
        # 軸の見た目を改善
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
=======
        terms.ymlから用語、FAQ、TIPSを読み込んでKnowledgeManagerに登録する。
        """
        knowledge_data = self.load_chapter_from_yaml("terms.yml")
        if not knowledge_data:
            return
        
        # YAMLから読み込んだ辞書のリストを、データクラスオブジェクトのリストに変換
        terms_list = [Term(**data) for data in knowledge_data.get("terms", [])]
        faq_list = [FaqItem(**data) for data in knowledge_data.get("faq", [])]
        tips_list = [TipItem(**data) for data in knowledge_data.get("tips", [])]

        self.knowledge_mgr.register_terms_batch(terms_list)
        self.knowledge_mgr.register_faq_batch(faq_list)
        self.knowledge_mgr.register_tips_batch(tips_list)

    def _process_content_list(self, contents: List[Dict[str, Any]], charts_dir: Path, tables_dir: Path):
        """
        コンテンツリストの処理をオーバーライドし、カスタムジェネレータに対応する。
        """
        # 親クラスのメソッドはリストを期待するため、ループで個別に処理
        for item in contents:
            if item.get('type') == 'custom_generator':
                # charts_dirをアセット用の共通ディレクトリとして流用
                self._process_custom_generator(item, charts_dir)
            else:
                # 親クラスの標準的な処理に任せる
                super()._process_content_list([item], charts_dir, tables_dir)

    def _process_custom_generator(self, item: Dict[str, Any], assets_dir: Path):
        """
        YAMLで定義されたカスタムジェネレータを実行する。
        """
        generator_key = item.get("generator")
        params = item.get("params", {})

        if not generator_key or generator_key not in self.custom_generators:
            logger.warning(f"未定義のカスタムジェネレータ: {generator_key}")
            return

        generator_func = self.custom_generators[generator_key]
        
        try:
            # 独自ジェネレータ関数を実行
            generated_asset_path = generator_func(assets_dir, **params)

            # 生成されたアセットを画像としてページに埋め込む
            relative_path = Path("..") / assets_dir.name / generated_asset_path.name
            self.doc_builder.add_image_reference(
                alt_text=f"Generated by {generator_key}",
                image_path=relative_path
            )
        except Exception as e:
            logger.error(f"カスタムジェネレータ '{generator_key}' の実行中にエラー: {e}")
>>>>>>> dbde2096846e5b4398413351225cc5f784d336f1

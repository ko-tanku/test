"""
組込制御入門の図表・アニメーション生成ロジック
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path
from typing import Dict, List, Any
import plotly.graph_objects as go

from src.core.chart_generator import ChartGenerator


def create_all_intro_charts(chart_gen: ChartGenerator, output_base_path: Path) -> Dict[str, Path]:
    """
    組込制御入門用の全図表を生成

    Args:
        chart_gen: ChartGeneratorインスタンス
        output_base_path: 出力先ベースパス

    Returns:
        生成されたファイルパスの辞書
    """
    generated_files = {}

    # 出力ディレクトリの作成
    charts_dir = output_base_path
    charts_dir.mkdir(parents=True, exist_ok=True)

    # 1. イントロコンセプト図
    def draw_intro_concept(ax, colors, styles, **kwargs):
        """現代の生活風景に組込制御が隠れているイラスト"""
        # 背景
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.set_aspect('equal')

        # スマートフォン
        phone = patches.Rectangle((1, 7), 1.5, 2,
                                facecolor=colors["info"],
                                edgecolor='black', linewidth=2)
        ax.add_patch(phone)
        # 画面を表現
        screen = patches.Rectangle((1.2, 7.3), 1.1, 1.4,
                                 facecolor='lightgray',
                                 edgecolor='black', linewidth=1)
        ax.add_patch(screen)
        ax.text(1.75, 6.5, 'スマホ', ha='center', fontsize=10, fontweight='bold')

        # 家電（洗濯機）
        washer = patches.Circle((4, 3), 1,
                              facecolor=colors["success"],
                              edgecolor='black', linewidth=2)
        ax.add_patch(washer)
        # 洗濯機の窓
        window = patches.Circle((4, 3), 0.6,
                              facecolor='white',
                              edgecolor='black', linewidth=1)
        ax.add_patch(window)
        ax.text(4, 1.5, '洗濯機', ha='center', fontsize=10, fontweight='bold')

        # 自動車
        car = patches.FancyBboxPatch((6.5, 7), 2.5, 1.5,
                                   boxstyle="round,pad=0.1",
                                   facecolor=colors["warning"],
                                   edgecolor='black', linewidth=2)
        ax.add_patch(car)
        # タイヤ
        tire1 = patches.Circle((7.2, 6.8), 0.2, facecolor='black')
        tire2 = patches.Circle((8.3, 6.8), 0.2, facecolor='black')
        ax.add_patch(tire1)
        ax.add_patch(tire2)
        ax.text(7.75, 6.5, '自動車', ha='center', fontsize=10, fontweight='bold')

        # ロボット
        robot_body = patches.Rectangle((7, 2.5), 1.5, 2,
                                     facecolor=colors["danger"],
                                     edgecolor='black', linewidth=2)
        robot_head = patches.Circle((7.75, 4.8), 0.4,
                                  facecolor=colors["danger"],
                                  edgecolor='black', linewidth=2)
        ax.add_patch(robot_body)
        ax.add_patch(robot_head)
        # ロボットの目
        eye1 = patches.Circle((7.6, 4.8), 0.1, facecolor='black')
        eye2 = patches.Circle((7.9, 4.8), 0.1, facecolor='black')
        ax.add_patch(eye1)
        ax.add_patch(eye2)
        ax.text(7.75, 1.5, 'ロボット', ha='center', fontsize=10, fontweight='bold')

        # 組込制御のアイコン（チップ）を散りばめる
        chip_positions = [(2.5, 8), (3.5, 2.5), (5.5, 7.5), (8.5, 3.5)]
        for x, y in chip_positions:
            chip = patches.Rectangle((x-0.3, y-0.3), 0.6, 0.6,
                                   facecolor='gold',
                                   edgecolor='darkgoldenrod', linewidth=1)
            ax.add_patch(chip)
            # チップの端子を表現
            for i in range(4):
                pin_x = x - 0.3 + (i + 0.5) * 0.15
                ax.plot([pin_x, pin_x], [y-0.35, y-0.3], 'k-', linewidth=0.5)
                ax.plot([pin_x, pin_x], [y+0.3, y+0.35], 'k-', linewidth=0.5)
            ax.text(x, y, 'IC', ha='center', va='center', fontsize=8, fontweight='bold')

        ax.set_title("私たちの身の回りの「賢い」仕組み", fontsize=styles["font_size_title"])
        ax.axis('off')

    file_path = charts_dir / chart_gen.create_custom_figure(
        draw_intro_concept, "intro_concept.html",
        output_dir=charts_dir
    )
    generated_files["intro_concept"] = file_path

    # 2. 組込制御の例（透視図）
    def draw_embedded_examples(ax, colors, styles, **kwargs):
        """家電内部の組込制御を示す透視図"""
        ax.set_xlim(0, 12)
        ax.set_ylim(0, 8)
        ax.set_aspect('equal')

        # エアコン
        aircon_body = patches.Rectangle((1, 5), 4, 2,
                                      facecolor='lightblue',
                                      edgecolor='black', linewidth=2)
        ax.add_patch(aircon_body)
        ax.text(3, 6.5, 'エアコン', ha='center', fontweight='bold')

        # エアコン内部の組込制御
        control_board = patches.Rectangle((2, 5.3), 1, 0.5,
                                        facecolor=colors["embedded"],
                                        edgecolor='black', linewidth=1)
        ax.add_patch(control_board)
        ax.text(2.5, 5.55, '制御基板', ha='center', fontsize=8)

        # 温度センサー
        sensor = patches.Circle((3.8, 5.5), 0.2,
                              facecolor=colors["sensor"],
                              edgecolor='black', linewidth=1)
        ax.add_patch(sensor)
        ax.text(4.3, 5.5, '温度センサー', ha='left', fontsize=8)

        # デジタルカメラ
        camera_body = patches.Rectangle((7, 5), 3, 2,
                                      facecolor='darkgray',
                                      edgecolor='black', linewidth=2)
        ax.add_patch(camera_body)
        # レンズ
        lens = patches.Circle((8.5, 6), 0.5,
                            facecolor='black',
                            edgecolor='silver', linewidth=2)
        ax.add_patch(lens)
        ax.text(8.5, 4.5, 'カメラ', ha='center', fontweight='bold')

        # カメラ内部の組込制御
        image_processor = patches.Rectangle((7.5, 5.3), 1.5, 0.5,
                                          facecolor=colors["embedded"],
                                          edgecolor='black', linewidth=1)
        ax.add_patch(image_processor)
        ax.text(8.25, 5.55, '画像処理チップ', ha='center', fontsize=8)

        # 冷蔵庫
        fridge_body = patches.Rectangle((1, 1), 3, 3,
                                      facecolor='lightyellow',
                                      edgecolor='black', linewidth=2)
        ax.add_patch(fridge_body)
        # 冷蔵庫のドア
        door = patches.Rectangle((1.1, 1.1), 2.8, 2.8,
                               facecolor='lightgray',
                               edgecolor='black', linewidth=1)
        ax.add_patch(door)
        ax.text(2.5, 3.5, '冷蔵庫', ha='center', fontweight='bold')

        # 冷蔵庫内部の組込制御
        fridge_control = patches.Rectangle((1.5, 1.5), 1, 0.5,
                                         facecolor=colors["embedded"],
                                         edgecolor='black', linewidth=1)
        ax.add_patch(fridge_control)
        ax.text(2, 1.75, '温度制御', ha='center', fontsize=8)

        # 矢印で組込制御を強調
        for pos in [(2.5, 5.1), (8.25, 5.1), (2, 1.3)]:
            ax.annotate('', xy=pos, xytext=(pos[0], pos[1]-0.5),
                       arrowprops=dict(arrowstyle='->', color='red', lw=2))

        ax.set_title("身の回りの製品に組み込まれた制御システム",
                    fontsize=styles["font_size_title"])
        ax.axis('off')

    file_path = charts_dir / chart_gen.create_custom_figure(
        draw_embedded_examples, "embedded_examples.html",
        output_dir=charts_dir
    )
    generated_files["embedded_examples"] = file_path

    # 3. センサー・アクチュエーターループのアニメーション
    frames = []

    for i in range(8):
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 8)
        ax.set_aspect('equal')

        # 温度センサー
        sensor = patches.Circle((2, 6), 0.8,
                              facecolor=chart_gen.colors["sensor"],
                              edgecolor='black', linewidth=2)
        ax.add_patch(sensor)
        # 温度計のシンボル
        thermometer = patches.Rectangle((1.9, 5.5), 0.2, 1,
                                      facecolor='red',
                                      edgecolor='black', linewidth=1)
        ax.add_patch(thermometer)
        ax.text(2, 4.8, '温度センサー', ha='center', fontsize=10)

        # コントローラー
        controller = patches.Rectangle((4, 5), 2, 2,
                                     facecolor=chart_gen.colors["controller"],
                                     edgecolor='black', linewidth=2)
        ax.add_patch(controller)
        # CPUを表現
        cpu = patches.Rectangle((4.5, 5.5), 1, 1,
                              facecolor='silver',
                              edgecolor='black', linewidth=1)
        ax.add_patch(cpu)
        ax.text(5, 6, 'CPU', ha='center', va='center', fontsize=8)
        ax.text(5, 4.5, 'コントローラー', ha='center', fontsize=10)

        # エアコン（アクチュエーター）
        actuator = patches.Rectangle((7, 5), 2, 2,
                                   facecolor=chart_gen.colors["actuator"],
                                   edgecolor='black', linewidth=2)
        ax.add_patch(actuator)
        # ファンを表現
        fan = patches.Circle((8, 6), 0.5,
                           facecolor='white',
                           edgecolor='black', linewidth=1)
        ax.add_patch(fan)
        # ファンの羽根
        for angle in [0, 90, 180, 270]:
            rad = np.radians(angle)
            x1, y1 = 8 + 0.2 * np.cos(rad), 6 + 0.2 * np.sin(rad)
            x2, y2 = 8 + 0.5 * np.cos(rad), 6 + 0.5 * np.sin(rad)
            ax.plot([x1, x2], [y1, y2], 'k-', linewidth=1)
        ax.text(8, 4.5, 'エアコン', ha='center', fontsize=10)

        # アニメーションの進行に応じて矢印を表示
        if i >= 1 and i <= 2:  # センシング
            ax.arrow(2.8, 6, 0.9, 0, head_width=0.2, head_length=0.2,
                    fc='red', ec='red', linewidth=3)
            ax.text(3.5, 6.5, '熱い！', ha='center', color='red', fontweight='bold')

        if i >= 3 and i <= 4:  # 判断
            ax.text(5, 7.5, '冷やせ！', ha='center', color='blue',
                   fontweight='bold', fontsize=14)

        if i >= 5 and i <= 6:  # アクチュエーション
            ax.arrow(6.2, 6, 0.6, 0, head_width=0.2, head_length=0.2,
                    fc='blue', ec='blue', linewidth=3)
            # 風を表現
            for j in range(3):
                y_pos = 5.5 + j * 0.5
                ax.plot([8.5, 9.5], [y_pos, y_pos], 'c-', linewidth=2)
                ax.plot([8.7, 9.3], [y_pos+0.1, y_pos-0.1], 'c-', linewidth=1)

        if i == 7:  # フィードバック（曲線矢印を直線矢印に変更）
            # 下向き矢印
            ax.arrow(5, 4.3, 0, -0.5, head_width=0.2, head_length=0.1,
                    fc='green', ec='green', linewidth=2)
            # 左向き矢印
            ax.arrow(4.8, 3.5, -2.3, 0, head_width=0.2, head_length=0.2,
                    fc='green', ec='green', linewidth=2)
            # 上向き矢印
            ax.arrow(2, 3.8, 0, 1.8, head_width=0.2, head_length=0.2,
                    fc='green', ec='green', linewidth=2)
            ax.text(3, 3, '温度下がった', ha='center', color='green', fontweight='bold')

        ax.set_title("制御ループ：センシング→判断→アクチュエーション→フィードバック",
                    fontsize=14)
        ax.axis('off')

        frames.append(fig)

    file_path = charts_dir / chart_gen.create_animation_gif(
        frames, "sensor_actuator_loop.gif", fps=1,
        output_dir=charts_dir
    )
    generated_files["sensor_actuator_loop"] = file_path

    # 4. ITと組み込みシステムの構成図
    def draw_it_embedded_diagram(ax, colors, styles, **kwargs):
        """ITシステムと組み込みシステムの構成要素比較図"""
        ax.set_xlim(0, 12)
        ax.set_ylim(0, 10)
        ax.set_aspect('equal')

        # ITシステム側
        ax.text(3, 9, 'ITシステム', ha='center', fontsize=16, fontweight='bold')

        # PC
        pc = patches.Rectangle((1, 6), 2, 1.5,
                             facecolor=colors["it_system"],
                             edgecolor='black', linewidth=2)
        ax.add_patch(pc)
        ax.text(2, 6.75, 'PC', ha='center', fontweight='bold', color='white')

        # サーバー
        server = patches.Rectangle((1, 4), 2, 1.5,
                                 facecolor=colors["it_system"],
                                 edgecolor='black', linewidth=2)
        ax.add_patch(server)
        ax.text(2, 4.75, 'サーバー', ha='center', fontweight='bold', color='white')

        # ネットワーク
        network = patches.Circle((4, 5.5), 0.8,
                               facecolor='lightblue',
                               edgecolor='black', linewidth=2)
        ax.add_patch(network)
        # ネットワークの線
        for angle in range(0, 360, 45):
            rad = np.radians(angle)
            x1, y1 = 4 + 0.5 * np.cos(rad), 5.5 + 0.5 * np.sin(rad)
            x2, y2 = 4 + 0.8 * np.cos(rad), 5.5 + 0.8 * np.sin(rad)
            ax.plot([x1, x2], [y1, y2], 'k-', linewidth=1)
        ax.text(4, 3.5, 'ネットワーク', ha='center')

        # 汎用性を示す矢印
        ax.annotate('', xy=(2, 7.7), xytext=(2, 8.3),
                   arrowprops=dict(arrowstyle='<->', color='blue', lw=2))
        ax.text(2, 8.5, '汎用的', ha='center', color='blue')

        # 組み込みシステム側
        ax.text(9, 9, '組み込みシステム', ha='center', fontsize=16, fontweight='bold')

        # センサー
        sensor = patches.Circle((7, 7), 0.6,
                              facecolor=colors["sensor"],
                              edgecolor='black', linewidth=2)
        ax.add_patch(sensor)
        ax.text(7, 7, 'S', ha='center', va='center', fontweight='bold')
        ax.text(7, 6.2, 'センサー', ha='center', fontsize=9)

        # マイコン
        mcu = patches.Rectangle((8.5, 6.5), 1.5, 1,
                              facecolor=colors["embedded"],
                              edgecolor='black', linewidth=2)
        ax.add_patch(mcu)
        ax.text(9.25, 7, 'MCU', ha='center', fontweight='bold', color='white')
        ax.text(9.25, 6, 'マイコン', ha='center', fontsize=9)

        # アクチュエーター
        actuator = patches.Circle((11, 7), 0.6,
                                facecolor=colors["actuator"],
                                edgecolor='black', linewidth=2)
        ax.add_patch(actuator)
        ax.text(11, 7, 'A', ha='center', va='center', fontweight='bold')
        ax.text(11, 6.2, 'アクチュエーター', ha='center', fontsize=9)

        # 接続線
        ax.plot([7.6, 8.5], [7, 7], 'k-', linewidth=2)
        ax.plot([10, 10.4], [7, 7], 'k-', linewidth=2)

        # 一体化を示す枠
        integrated = patches.Rectangle((6.2, 5.8), 5.6, 2,
                                     fill=False,
                                     edgecolor='red',
                                     linewidth=2,
                                     linestyle='--')
        ax.add_patch(integrated)
        ax.text(9, 5.5, '一体化', ha='center', color='red', fontweight='bold')

        # IoT連携（点線）
        ax.plot([4.8, 6.2], [5.5, 6.8], 'g--', linewidth=2)
        ax.text(5.5, 5.8, 'IoT', ha='center', color='green', fontweight='bold')

        ax.set_title("ITシステムと組み込みシステムの構成比較",
                    fontsize=styles["font_size_title"])
        ax.axis('off')

    file_path = charts_dir / chart_gen.create_custom_figure(
        draw_it_embedded_diagram, "it_embedded_system_diagram.html",
        output_dir=charts_dir
    )
    generated_files["it_embedded_system_diagram"] = file_path

    return generated_files
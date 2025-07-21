"""
テスト資料用の図表生成ロジック
core.chart_generatorの機能を網羅的にテスト
"""

import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from pathlib import Path
from typing import Dict, Any

from src.core.chart_generator import ChartGenerator


def create_all_test_charts(chart_gen: ChartGenerator, output_base_path: Path) -> Dict[str, Path]:
    """
    テスト用の全図表を生成
    
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
    
    # 1. シンプルなMatplotlib折れ線グラフ
    x_data = list(range(10))
    y_data = [x**2 for x in x_data]
    data = {"x": x_data, "y": y_data}
    
    file_path = charts_dir / chart_gen.create_simple_line_chart(
        data, "x", "y",
        "二次関数のグラフ",
        "X値",
        "Y値 (X²)",
        "matplotlib_line_chart.html",
        output_dir=charts_dir
        
    )
    generated_files["matplotlib_line"] = file_path
    
    # 2. シンプルなMatplotlib棒グラフ
    categories = ["A", "B", "C", "D", "E"]
    values = [23, 45, 56, 78, 32]
    bar_data = {"category": categories, "value": values}
    
    file_path = charts_dir / chart_gen.create_bar_chart(
        bar_data, "category", "value",
        "カテゴリ別データ",
        "カテゴリ",
        "値",
        "matplotlib_bar_chart.html",
        output_dir=charts_dir
    )
    print(f"⭐{file_path}")
    generated_files["matplotlib_bar"] = file_path
    
    # 3. Plotlyインタラクティブ折れ線グラフ
    x_interactive = np.linspace(0, 2*np.pi, 100)
    y_sin = np.sin(x_interactive)
    y_cos = np.cos(x_interactive)
    interactive_data = {"x": x_interactive.tolist(), "sin": y_sin.tolist(), "cos": y_cos.tolist()}
    
    # 複数系列のPlotlyグラフ
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=interactive_data["x"], y=interactive_data["sin"], 
                            mode='lines', name='sin(x)', line=dict(width=3)))
    fig.add_trace(go.Scatter(x=interactive_data["x"], y=interactive_data["cos"], 
                            mode='lines', name='cos(x)', line=dict(width=3)))
    fig.update_layout(
        title="三角関数のインタラクティブグラフ",
        xaxis_title="ラジアン",
        yaxis_title="値",
        hovermode='x unified'
    )
    
    file_path = charts_dir / chart_gen.create_interactive_plotly_chart(
        fig, "plotly_trigonometric.html",
        output_dir=charts_dir
    )
    generated_files["plotly_line"] = file_path
    
    # 4. Plotlyインタラクティブ棒グラフ
    file_path = charts_dir / chart_gen.create_bar_chart(
        bar_data, "category", "value",
        "インタラクティブ棒グラフ",
        "カテゴリ",
        "値",
        "plotly_bar_chart.html",
        use_plotly=True,
        output_dir=charts_dir
    )
    generated_files["plotly_bar"] = file_path
    
    # 5. カスタム描画関数によるMatplotlib図
    def draw_custom_diagram(ax, colors, styles, **kwargs):
        """カスタム図形を描画"""
        # 円を描画
        circle = plt.Circle((0.5, 0.5), 0.3, color=colors["info"], alpha=0.7)
        ax.add_patch(circle)
        
        # 矢印を描画
        ax.arrow(0.1, 0.1, 0.3, 0.3, head_width=0.05, head_length=0.05, 
                fc=colors["success"], ec=colors["success"])
        
        # テキストを追加
        ax.text(0.5, 0.5, 'カスタム図形', ha='center', va='center', 
                fontsize=styles["font_size_title"], fontweight='bold')
        
        # 軸の設定
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect('equal')
        ax.set_title("カスタム描画のデモ", fontsize=styles["font_size_title"])
        ax.grid(True, alpha=styles["grid_alpha"])
    
    file_path = charts_dir / chart_gen.create_custom_figure(
        draw_custom_diagram, "custom_diagram.html",
        output_dir=charts_dir
    )
    generated_files["custom_diagram"] = file_path


    def draw_embedded_system(ax, colors, styles, **kwargs):
        """組み込みシステムの構成図を描画"""
        import matplotlib.patches as patches
        
        # CPU
        cpu_rect = patches.Rectangle((0.3, 0.6), 0.4, 0.3, 
                                    facecolor=colors["info"], 
                                    edgecolor='black', linewidth=2)
        ax.add_patch(cpu_rect)
        ax.text(0.5, 0.75, 'CPU\n(マイコン)', ha='center', va='center', 
                fontsize=styles["font_size_label"], fontweight='bold')
        
        # メモリ
        mem_rect = patches.Rectangle((0.05, 0.3), 0.2, 0.2,
                                    facecolor=colors["success"],
                                    edgecolor='black', linewidth=2)
        ax.add_patch(mem_rect)
        ax.text(0.15, 0.4, 'メモリ', ha='center', va='center',
                fontsize=styles["font_size_label"])
        
        # センサー
        sensor_rect = patches.Rectangle((0.75, 0.7), 0.2, 0.15,
                                       facecolor=colors["warning"],
                                       edgecolor='black', linewidth=2)
        ax.add_patch(sensor_rect)
        ax.text(0.85, 0.775, 'センサー', ha='center', va='center',
                fontsize=styles["font_size_label"])
        
        # アクチュエータ
        act_rect = patches.Rectangle((0.75, 0.45), 0.2, 0.15,
                                    facecolor=colors["danger"],
                                    edgecolor='black', linewidth=2)
        ax.add_patch(act_rect)
        ax.text(0.85, 0.525, 'アクチュ\nエータ', ha='center', va='center',
                fontsize=styles["font_size_label"])
        
        # 矢印（接続）
        ax.arrow(0.25, 0.45, 0.05, 0.15, head_width=0.02, head_length=0.02,
                fc='black', ec='black')
        ax.arrow(0.7, 0.75, 0.05, 0.025, head_width=0.02, head_length=0.02,
                fc='black', ec='black')
        ax.arrow(0.7, 0.7, 0.05, -0.075, head_width=0.02, head_length=0.02,
                fc='black', ec='black')
        
        # 軸の設定
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect('equal')
        ax.set_title("組み込みシステムの基本構成", fontsize=styles["font_size_title"])
        ax.axis('off')  # 軸を非表示
    
    # カスタム組み込みシステム図を生成
    file_path = charts_dir / chart_gen.create_custom_figure(
        draw_embedded_system, "embedded_system_diagram.html",
        output_dir=charts_dir
    )
    generated_files["embedded_system"] = file_path

    # 6. Plotlyによる状態遷移デモ
    fig = go.Figure()
    
    # 初期状態のデータ
    initial_x = [1, 2, 3, 4, 5]
    initial_y = [10, 15, 13, 17, 20]
    
    # 複数の状態のデータ
    states = [
        {"x": initial_x, "y": initial_y, "name": "状態1"},
        {"x": initial_x, "y": [12, 18, 15, 20, 25], "name": "状態2"},
        {"x": initial_x, "y": [8, 12, 10, 14, 18], "name": "状態3"}
    ]
    
    # 各状態のトレースを追加
    for i, state in enumerate(states):
        fig.add_trace(go.Bar(
            x=state["x"],
            y=state["y"],
            name=state["name"],
            visible=(i == 0)  # 最初の状態のみ表示
        ))
    
    # ボタンの作成
    buttons = []
    for i, state in enumerate(states):
        visible = [False] * len(states)
        visible[i] = True
        buttons.append(dict(
            label=state["name"],
            method="update",
            args=[{"visible": visible}]
        ))
    
    fig.update_layout(
        title="クリックで状態遷移するグラフ",
        updatemenus=[dict(
            buttons=buttons,
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.1,
            xanchor="left",
            y=1.15,
            yanchor="top"
        )],
        xaxis_title="項目",
        yaxis_title="値"
    )
    
    file_path = charts_dir / chart_gen.create_interactive_plotly_chart(
        fig, "state_transition_demo.html",
        output_dir=charts_dir
    )
    generated_files["state_transition"] = file_path
    
    # 7. Plotlyによるドロップダウンフィルタリングデモ
    fig = go.Figure()
    
    # 複数のデータセット
    datasets = {
        "2022年": {"x": ["Q1", "Q2", "Q3", "Q4"], "y": [100, 120, 115, 140]},
        "2023年": {"x": ["Q1", "Q2", "Q3", "Q4"], "y": [110, 135, 125, 155]},
        "2024年": {"x": ["Q1", "Q2", "Q3", "Q4"], "y": [120, 145, 140, 170]}
    }
    
    # 全データセットのトレースを追加
    for i, (year, data) in enumerate(datasets.items()):
        fig.add_trace(go.Scatter(
            x=data["x"],
            y=data["y"],
            mode='lines+markers',
            name=year,
            visible=(i == 0),  # 最初のデータセットのみ表示
            line=dict(width=3),
            marker=dict(size=10)
        ))
    
    # ドロップダウンメニューの作成
    dropdown_buttons = []
    for i, year in enumerate(datasets.keys()):
        visible = [False] * len(datasets)
        visible[i] = True
        dropdown_buttons.append(dict(
            label=year,
            method="update",
            args=[{"visible": visible}, {"title": f"{year}の四半期別売上"}]
        ))
    
    fig.update_layout(
        title="2022年の四半期別売上",
        updatemenus=[dict(
            buttons=dropdown_buttons,
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=1.0,
            xanchor="right",
            y=1.15,
            yanchor="top"
        )],
        xaxis_title="四半期",
        yaxis_title="売上（百万円）"
    )
    
    file_path = charts_dir / chart_gen.create_interactive_plotly_chart(
        fig, "dropdown_filter_demo.html",
        output_dir=charts_dir
    )
    generated_files["dropdown_filter"] = file_path
    
    # 8. スライダーによるパラメータ調整デモ
    fig = go.Figure()
    
    # パラメータ範囲
    x = np.linspace(0, 2*np.pi, 100)
    
    # 異なる振幅でのサイン波
    amplitudes = [0.5, 1.0, 1.5, 2.0, 2.5]
    
    for amp in amplitudes:
        y = amp * np.sin(x)
        fig.add_trace(go.Scatter(
            x=x,
            y=y,
            mode='lines',
            name=f'振幅 {amp}',
            visible=(amp == 1.0)  # 振幅1.0のみ初期表示
        ))
    
    # スライダーの作成
    steps = []
    for i, amp in enumerate(amplitudes):
        visible = [False] * len(amplitudes)
        visible[i] = True
        step = dict(
            method="update",
            args=[{"visible": visible}],
            label=f"{amp}"
        )
        steps.append(step)
    
    sliders = [dict(
        active=1,  # 初期値は振幅1.0
        currentvalue={"prefix": "振幅: "},
        pad={"t": 50},
        steps=steps
    )]
    
    fig.update_layout(
        title="スライダーで振幅を調整",
        sliders=sliders,
        xaxis_title="ラジアン",
        yaxis_title="振幅"
    )
    
    file_path = charts_dir / chart_gen.create_interactive_plotly_chart(
        fig, "slider_parameter_demo.html",
        output_dir=charts_dir
    )
    generated_files["slider_parameter"] = file_path
    
    # 9. アニメーションGIFの生成
    frames = []
    
    for i in range(10):
        fig, ax = plt.subplots(figsize=(6, 4))
        
        # 時間変化するデータ
        t = np.linspace(0, 2*np.pi, 100)
        y = np.sin(t + i * np.pi / 5)
        
        ax.plot(t, y, 'b-', linewidth=2)
        ax.set_xlim(0, 2*np.pi)
        ax.set_ylim(-1.5, 1.5)
        ax.set_title(f"正弦波のアニメーション (フレーム {i+1}/10)")
        ax.set_xlabel("時間")
        ax.set_ylabel("振幅")
        ax.grid(True, alpha=0.3)
        
        frames.append(fig)
    
    file_path = charts_dir / chart_gen.create_animation_gif(
        frames, "sine_wave_animation.gif", fps=2,
        output_dir=charts_dir
    )
    generated_files["animation_gif"] = file_path
    
    # 10. マウスホバーで詳細情報表示（Plotly）
    # 散布図データ
    np.random.seed(42)
    n_points = 50
    scatter_data = {
        "x": np.random.randn(n_points),
        "y": np.random.randn(n_points),
        "size": np.random.randint(10, 50, n_points),
        "label": [f"Point {i+1}" for i in range(n_points)]
    }
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=scatter_data["x"],
        y=scatter_data["y"],
        mode='markers',
        marker=dict(
            size=scatter_data["size"],
            color=scatter_data["size"],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="サイズ")
        ),
        text=scatter_data["label"],
        hovertemplate='<b>%{text}</b><br>' +
                      'X: %{x:.2f}<br>' +
                      'Y: %{y:.2f}<br>' +
                      'サイズ: %{marker.size}<br>' +
                      '<extra></extra>'
    ))
    
    fig.update_layout(
        title="マウスホバーで詳細情報を表示",
        xaxis_title="X座標",
        yaxis_title="Y座標",
        hovermode='closest'
    )
    
    file_path = charts_dir / chart_gen.create_interactive_plotly_chart(
        fig, "hover_details_demo.html",
        output_dir=charts_dir
    )
    generated_files["hover_details"] = file_path
    
    return generated_files
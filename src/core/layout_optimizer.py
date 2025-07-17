"""
学習資料生成システム - レイアウト最適化
図表とテキストの配置最適化、文字サイズ調整機能
"""
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict, Optional
import numpy as np
from core.base_config import BASE_CHART_STYLES
import logging

logger = logging.getLogger(__name__)

class LayoutOptimizer:
    """レイアウト最適化クラス"""

    def __init__(self):
        self.min_spacing = 0.1  # 最小間隔（図の相対座標）
        self.text_buffer = 0.05  # テキスト周りのバッファ

    def avoid_text_overlap(self, ax, texts: List, positions: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
        """テキストの重なりを回避する位置調整"""
        adjusted_positions = positions.copy()

        for i in range(len(texts)):
            for j in range(i + 1, len(texts)):
                # テキストボックスの取得
                bbox1 = texts[i].get_window_extent()
                bbox2 = texts[j].get_window_extent()

                # 重なり判定
                if self._check_overlap(bbox1, bbox2):
                    # 位置調整
                    adjusted_positions[j] = self._adjust_position(
                        adjusted_positions[i], adjusted_positions[j]
                    )
                    texts[j].set_position(adjusted_positions[j])

        logger.info(f"テキスト重なり回避: {len(texts)}個のテキストを調整")
        return adjusted_positions

    def _check_overlap(self, bbox1, bbox2) -> bool:
        """2つのバウンディングボックスの重なりを判定"""
        return not (bbox1.x1 < bbox2.x0 or bbox2.x1 < bbox1.x0 or
                   bbox1.y1 < bbox2.y0 or bbox2.y1 < bbox1.y0)

    def _adjust_position(self, pos1: Tuple[float, float],
                        pos2: Tuple[float, float]) -> Tuple[float, float]:
        """重なりを解消する新しい位置を計算"""
        x1, y1 = pos1
        x2, y2 = pos2

        # 移動方向を決定
        dx = x2 - x1
        dy = y2 - y1
        distance = np.sqrt(dx**2 + dy**2)

        if distance < self.min_spacing:
            # 最小間隔を確保
            scale = self.min_spacing / distance if distance > 0 else 1
            new_x = x1 + dx * scale
            new_y = y1 + dy * scale
            return (new_x, new_y)

        return pos2

    def optimize_chart_layout(self, fig, ax, elements: Dict[str, List]) -> None:
        """チャート全体のレイアウト最適化"""
        # 凡例の位置最適化
        if 'legend' in elements and elements['legend']:
            self._optimize_legend_position(ax, elements)

        # ラベルの位置最適化
        if 'labels' in elements and elements['labels']:
            self._optimize_label_positions(ax, elements['labels'])

        # タイトルとサブタイトルの間隔調整
        if 'title' in elements:
            self._adjust_title_spacing(fig, ax)

        plt.tight_layout()
        logger.info("チャートレイアウト最適化完了")

    def _optimize_legend_position(self, ax, elements: Dict) -> None:
        """凡例の最適位置を決定"""
        # データ点との重なりを避ける位置を探索
        best_loc = 'best'
        ax.legend(loc=best_loc, frameon=True, fancybox=True, shadow=True)

    def _optimize_label_positions(self, ax, labels: List) -> None:
        """ラベルの位置を最適化"""
        # データポイントのラベルの重なりを調整
        positions = [label.get_position() for label in labels]
        self.avoid_text_overlap(ax, labels, positions)

    def _adjust_title_spacing(self, fig, ax) -> None:
        """タイトルとグラフの間隔を調整"""
        fig.subplots_adjust(top=0.93)

    def calculate_optimal_figure_size(self, content_type: str,
                                    data_points: int) -> Tuple[float, float]:
        """コンテンツタイプとデータ量に基づく最適な図サイズを計算"""
        base_width, base_height = BASE_CHART_STYLES["figure_size"]

        if content_type == "bar_chart":
            # バーの数に応じて幅を調整
            width = max(base_width, base_width * (data_points / 10))
            return (width, base_height)
        elif content_type == "line_chart":
            # データポイント数に応じて幅を調整
            width = max(base_width, base_width * (data_points / 50))
            return (width, base_height)
        elif content_type == "pie_chart":
            # 円グラフは正方形に近い比率
            size = min(base_width, base_height)
            return (size, size)
        elif content_type == "heatmap":
            # ヒートマップは正方形
            return (base_width, base_width)
        elif content_type == "scatter":
            # 散布図は標準サイズ
            return (base_width, base_height)
        else:
            return (base_width, base_height)
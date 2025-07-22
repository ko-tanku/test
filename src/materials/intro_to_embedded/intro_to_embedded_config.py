"""
組込制御入門の設定ファイル
基本情報、カラー設定、MkDocs設定のオーバーライド
"""

from src.core.base_config import MKDOCS_SITE_CONFIG
from src.core.config import GLOBAL_COLORS

# 教材のメタデータ
MATERIAL_CONFIG = {
    "title": "組込制御入門：私たちの身の回りの「賢い」仕組みを探る",
    "material_id": "intro_to_embedded",
    "version": "1.0.0",
    "author": "AI Learning Material Creator",
    "target_audience": "文系の大学生（組込制御技術者志望、プログラミング経験は問わない）",
    "purpose": "組込制御の基本概念を理解し、文系から組み込み技術者を目指す意義を認識する",
    "description": "身近な製品を例に組込制御の仕組みを学び、ITとの違いや技術者への道を探る入門資料",
    "prerequisites": ["基本的なITリテラシー"],
    "learning_objectives": [
        "組込制御とは何か、その定義を自分の言葉で説明できる",
        "身近な製品にどのような組込制御が使われているか、例を挙げて説明できる",
        "ITと組み込み技術の違いや関連性について、簡潔に説明できる",
        "組み込み技術者が社会でどのような役割を担い、なぜ目指す意義があるのかを理解し、自分の言葉で説明できる",
        "組込制御システムが持つ基本的な機能（センシング、判断、アクチュエーション）を理解し、説明できる"
    ],
    "estimated_time": "約1時間",
    "level": "概念理解レベル（実装詳細は扱わない）"
}

# MkDocs設定のオーバーライド
MKDOCS_MATERIAL_OVERRIDE = {
    "theme": {
        "palette": {
            "primary": "teal",
            "accent": "orange"
        }
    }
}

# 教材用のカスタムカラー
INTRO_TO_EMBEDDED_COLORS = GLOBAL_COLORS.copy()
INTRO_TO_EMBEDDED_COLORS.update({
    "embedded": "#00897B",  # Teal 600
    "it_system": "#1976D2",  # Blue 700
    "sensor": "#FF6F00",    # Amber 900
    "actuator": "#E91E63",  # Pink 500
    "controller": "#9C27B0" # Purple 500
})
"""
Materials index for MkDocs Materials Generator
学習資料のトピック分類とナビゲーション順序を定義
"""

from typing import Dict, List, Any

# 学習資料のトピック分類とナビゲーション順序
MATERIALS_INDEX: Dict[str, Dict[str, Any]] = {
    "embedded_control_intro": {
        "title": "組込制御入門",
        "description": "組込みシステムと制御工学の基礎を学ぶ入門資料",
        "difficulty": "初級",
        "estimated_duration": "40時間",
        "prerequisites": ["基本的なプログラミング知識", "数学の基礎知識"],
        "topics": [
            "組込みシステム概要",
            "マイコンの基礎",
            "センサとアクチュエータ",
            "制御理論入門",
            "PID制御",
            "実装とデバッグ"
        ],
        "target_audience": ["工学系学生", "組込み開発初心者", "制御工学入門者"],
        "learning_outcomes": [
            "組込みシステムの基本概念を理解する",
            "基本的な制御理論を習得する",
            "簡単な制御システムを実装できる"
        ],
        "order": 1,
        "status": "planning"
    },
    
    "test_material": {
        "title": "テスト資料",
        "description": "システムの動作確認とテスト用のサンプル資料",
        "difficulty": "テスト用",
        "estimated_duration": "1時間",
        "prerequisites": ["なし"],
        "topics": [
            "システムテスト概要",
            "図表生成テスト",
            "表生成テスト",
            "用語管理テスト",
            "統合テスト"
        ],
        "target_audience": ["開発者", "テスター"],
        "learning_outcomes": [
            "システムの基本動作を確認する",
            "各機能の動作を検証する",
            "出力品質を評価する"
        ],
        "order": 999,
        "status": "active"
    }
}

# 学習資料の推奨学習順序
LEARNING_PATH: List[str] = [
    "test_material",
    "embedded_control_intro"
]

# 学習資料の依存関係
DEPENDENCIES: Dict[str, List[str]] = {
    "embedded_control_intro": [],
    "test_material": []
}

# 学習資料の難易度レベル
DIFFICULTY_LEVELS: Dict[str, int] = {
    "入門": 1,
    "初級": 2,
    "中級": 3,
    "上級": 4,
    "テスト用": 0
}

# 学習資料のカテゴリ
CATEGORIES: Dict[str, List[str]] = {
    "工学基礎": ["embedded_control_intro"],
    "システム開発": ["test_material"],
    "制御工学": ["embedded_control_intro"],
    "テスト": ["test_material"]
}

def get_material_info(material_key: str) -> Dict[str, Any]:
    """
    指定された学習資料の情報を取得
    
    Args:
        material_key: 学習資料のキー
        
    Returns:
        学習資料の情報辞書
    """
    return MATERIALS_INDEX.get(material_key, {})

def get_materials_by_difficulty(difficulty: str) -> List[str]:
    """
    難易度別の学習資料リストを取得
    
    Args:
        difficulty: 難易度レベル
        
    Returns:
        該当する学習資料のキーリスト
    """
    return [
        key for key, info in MATERIALS_INDEX.items()
        if info.get("difficulty") == difficulty
    ]

def get_materials_by_category(category: str) -> List[str]:
    """
    カテゴリ別の学習資料リストを取得
    
    Args:
        category: カテゴリ名
        
    Returns:
        該当する学習資料のキーリスト
    """
    return CATEGORIES.get(category, [])

def get_recommended_next_materials(current_material: str) -> List[str]:
    """
    現在の学習資料から推奨される次の学習資料を取得
    
    Args:
        current_material: 現在の学習資料キー
        
    Returns:
        推奨される次の学習資料のキーリスト
    """
    try:
        current_index = LEARNING_PATH.index(current_material)
        if current_index + 1 < len(LEARNING_PATH):
            return [LEARNING_PATH[current_index + 1]]
        return []
    except ValueError:
        return []

def validate_material_key(material_key: str) -> bool:
    """
    学習資料キーの妥当性を検証
    
    Args:
        material_key: 検証対象の学習資料キー
        
    Returns:
        妥当性の真偽値
    """
    return material_key in MATERIALS_INDEX

def get_all_materials() -> List[str]:
    """
    全学習資料のキーリストを取得
    
    Returns:
        全学習資料のキーリスト
    """
    return list(MATERIALS_INDEX.keys())

def get_materials_statistics() -> Dict[str, Any]:
    """
    学習資料の統計情報を取得
    
    Returns:
        統計情報辞書
    """
    total_materials = len(MATERIALS_INDEX)
    difficulty_counts = {}
    category_counts = {}
    
    for material_info in MATERIALS_INDEX.values():
        difficulty = material_info.get("difficulty", "不明")
        difficulty_counts[difficulty] = difficulty_counts.get(difficulty, 0) + 1
    
    for category, materials in CATEGORIES.items():
        category_counts[category] = len(materials)
    
    return {
        "total_materials": total_materials,
        "difficulty_distribution": difficulty_counts,
        "category_distribution": category_counts,
        "total_topics": sum(len(info.get("topics", [])) for info in MATERIALS_INDEX.values())
    }
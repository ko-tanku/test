"""
プロジェクト内の全学習資料のトピック分類とナビゲーション順序を定義
人間が直接編集可能な辞書形式で管理
"""

GLOBAL_MATERIAL_INDEX = {
    "topics": {
        "基礎編": {
            "title": "基礎編",
            "description": "MkDocsと学習資料生成の基礎を学びます",
            "materials": ["test_material"]
        },
        "応用編": {
            "title": "応用編",
            "description": "より高度な学習資料の作成方法を学びます",
            "materials": ["embedded_control_intro"]
        }
    },
    
    "all_materials_order": [
        "test_material",
        "embedded_control_intro"
    ],
    
    "material_relationships": {
        "test_material": {
            "prerequisites": [],
            "next_steps": ["embedded_control_intro"],
            "related_materials": []
        },
        "embedded_control_intro": {
            "prerequisites": ["test_material"],
            "next_steps": [],
            "related_materials": []
        }
    }
}
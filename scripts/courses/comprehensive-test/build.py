# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
comprehensive-test コース生成スクリプト
ソースファイル（YAML, Markdown）から、フロントエンドで利用する単一のJSONファイルを生成します。
"""

import os
import sys
import yaml
import json
import re
from pathlib import Path

# 標準出力のエンコーディングをUTF-8に設定
sys.stdout.reconfigure(encoding='utf-8')

# プロジェクトのルートディレクトリを絶対パスで解決
# このスクリプト(build.py)の場所から4階層親のディレクトリをルートとする
PROJECT_ROOT = Path(__file__).resolve().parents[3]

def load_yaml_file(file_path):
    """
    YAMLファイルを安全に読み込み、内容を返します。
    エラーが発生した場合はNoneを返し、エラーメッセージを出力します。
    """
    if not file_path.is_file():
        print(f"Error: YAML file not found at {file_path}", file=sys.stderr)
        return None
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file {file_path}: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"An unexpected error occurred while reading {file_path}: {e}", file=sys.stderr)
        return None

def read_markdown_file(file_path):
    """
    Markdownファイルを読み込み、内容を返します。
    ファイルが存在しない場合は空の文字列を返します。
    """
    if not file_path.is_file():
        print(f"Warning: Markdown file not found at {file_path}", file=sys.stderr)
        return ""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading Markdown file {file_path}: {e}", file=sys.stderr)
        return ""

def transform_component_props(components_data):
    """
    コンポーネントのプロパティをフロントエンドが期待する形式に変換します。
    - 'ui/Tabs' の 'items' を 'tabs' に変更
    - 'quizzes/MultipleChoice' の 'props' を 'quizData' に変更
    """
    if not components_data:
        return []

    transformed_components = []
    for comp in components_data:
        component_name = comp.get('component')
        props = comp.get('props', {})

        if component_name == 'ui/Tabs' and 'items' in props:
            props['tabs'] = props.pop('items')
        elif component_name == 'quizzes/MultipleChoice':
            # MultipleChoiceはprops全体をquizDataとして渡す
            comp['props'] = {'quizData': props}

        transformed_components.append(comp)

    return transformed_components

def generate_page_data(page_id, source_dir):
    """
    単一ページのデータを生成します。
    meta.yaml, prose.md, components.yaml を読み込み、一つの辞書にまとめます。
    """
    page_dir = source_dir / "pages" / page_id

    meta_data = load_yaml_file(page_dir / "meta.yaml") or {}
    prose_content = read_markdown_file(page_dir / "prose.md")
    components_data = load_yaml_file(page_dir / "components.yaml") or []

    # フロントエンドでのマッピングロジックを排除するため、ここでプロパティ名を変換
    transformed_components = transform_component_props(components_data)

    final_prose_content = prose_content

    return {
        "id": page_id,
        "title": meta_data.get("title", page_id),
        "description": meta_data.get("description", ""),
        "slug": meta_data.get("slug", f"/{page_id}"),
        "prose_content": final_prose_content,
        "components": transformed_components
    }

def generate_sidebar_config(master_data, course_id, sidebars_dir):
    """
    サイドバー設定ファイル（.js）を生成します。
    """
    sidebar_config = master_data.get('sidebar', [])
    sidebar_content = f"""// @ts-check

const sidebars = {{
  {course_id}Sidebar: {json.dumps(sidebar_config, indent=2, ensure_ascii=False)}
}};

module.exports = sidebars;"""

    sidebar_file = sidebars_dir / f"{course_id}.js"
    sidebars_dir.mkdir(exist_ok=True)

    try:
        with open(sidebar_file, 'w', encoding='utf-8') as f:
            f.write(sidebar_content)
        print(f"Successfully generated sidebar: {sidebar_file}")
    except Exception as e:
        print(f"Error writing sidebar file {sidebar_file}: {e}", file=sys.stderr)
        sys.exit(1)

def update_docusaurus_navbar(master_data, course_id, config_path):
    """
    docusaurus.config.jsのナビゲーションバーにコースリンクを自動追加します。
    スマートな重複回避ロジック付き。
    """
    course_label = master_data.get('course_label', course_id)
    sidebar_items = master_data.get('sidebar', [])
    
    # ドロップダウンアイテムを生成
    dropdown_items = []
    
    def process_sidebar_items(items):
        """サイドバー設定からドロップダウンアイテムを生成"""
        for item in items:
            if item.get('type') == 'doc':
                page_id = item.get('id')
                label = item.get('label', page_id)
                dropdown_items.append({
                    'to': f'/{course_id}/{page_id}',
                    'label': label
                })
            elif item.get('type') == 'category':
                # カテゴリーの場合は子アイテムを処理
                category_items = item.get('items', [])
                process_sidebar_items(category_items)
    
    process_sidebar_items(sidebar_items)
    
    if not dropdown_items:
        print("No dropdown items to add")
        return
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 行ベースでの処理でより安全に操作
        new_lines = []
        in_target_dropdown = False
        dropdown_depth = 0
        items_found = False
        dropdown_added = False
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # すでに存在するコースのドロップダウンをチェック
            if not in_target_dropdown and f"label: '{course_label}'" in line and 'dropdown' in lines[max(0, i-2):i+1]:
                # 既存のコースドロップダウンを見つけた場合はスキップ開始
                in_target_dropdown = True
                dropdown_depth = 1
                i += 1
                continue
            
            # 既存コースドロップダウン内の処理
            if in_target_dropdown:
                # 中括弧のカウントで階層を追跡
                dropdown_depth += line.count('{') - line.count('}')
                if dropdown_depth <= 0:
                    in_target_dropdown = False
                i += 1
                continue
            
            # navbar items セクションの検出と新しいドロップダウンの追加
            if not dropdown_added and 'items: [' in line and not items_found:
                items_found = True
                new_lines.append(line)
                
                # 新しいドロップダウン設定を挿入
                dropdown_config = f"""          {{
            type: 'dropdown',
            label: '{course_label}',
            position: 'left',
            items: ["""
                
                for item in dropdown_items:
                    dropdown_config += f"""
              {{
                to: '{item['to']}',
                label: '{item['label']}',
              }},"""
                
                dropdown_config += """
            ],
          },
"""
                new_lines.append(dropdown_config)
                dropdown_added = True
            else:
                new_lines.append(line)
            
            i += 1
        
        if dropdown_added:
            # ファイルに書き戻し
            with open(config_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            
            print(f"Successfully updated navbar in docusaurus.config.js")
        else:
            print("Warning: Could not find navbar items section or course already exists", file=sys.stderr)
        
    except Exception as e:
        print(f"Error updating docusaurus.config.js: {e}", file=sys.stderr)

def main():
    """
    メイン実行関数。
    コースのビルドプロセスを管理します。
    """
    course_dir = Path(__file__).parent
    source_dir = course_dir / "source"

    master_file = course_dir / "master.yaml"
    master_data = load_yaml_file(master_file)

    if not master_data:
        print("Error: master.yaml is missing or invalid. Aborting build.", file=sys.stderr)
        sys.exit(1)

    course_id = master_data.get('course_id')
    course_label = master_data.get('course_label')

    if not course_id or not course_label:
        print("Error: 'course_id' and 'course_label' must be defined in master.yaml.", file=sys.stderr)
        sys.exit(1)

    print(f"Building course: {course_label} ({course_id})")

    # 各ディレクトリのパスを設定
    sidebars_dir = PROJECT_ROOT / "sidebars"
    output_data_dir = PROJECT_ROOT / "static" / "data"

    # サイドバー設定を生成
    generate_sidebar_config(master_data, course_id, sidebars_dir)
    
    # docusaurus.config.jsのナビゲーションを自動更新
    config_path = PROJECT_ROOT / "docusaurus.config.js"
    update_docusaurus_navbar(master_data, course_id, config_path)

    # 各ページのデータを処理
    sidebar_items = master_data.get('sidebar', [])
    all_pages_data = []

    # sidebar定義から'doc'タイプのitemを再帰的に探す
    def find_doc_items(items):
        doc_items = []
        for item in items:
            if item.get('type') == 'doc':
                doc_items.append(item)
            if item.get('type') == 'category':
                doc_items.extend(find_doc_items(item.get('items', [])))
        return doc_items

    doc_items = find_doc_items(sidebar_items)

    for item in doc_items:
        page_id = item.get('id')
        if page_id:
            print(f"Processing page: {page_id}")
            page_data = generate_page_data(page_id, source_dir)
            all_pages_data.append(page_data)

    # 全ページのJSONデータを単一ファイルに保存
    output_data_dir.mkdir(exist_ok=True)
    output_json_file = output_data_dir / f"{course_id}-pages.json"

    try:
        with open(output_json_file, 'w', encoding='utf-8') as f:
            json.dump(all_pages_data, f, ensure_ascii=False, indent=2)
        print(f"Successfully generated all pages data to: {output_json_file}")
    except Exception as e:
        print(f"Error writing JSON data to {output_json_file}: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"\nBuild completed successfully for course: {course_id}")

if __name__ == "__main__":
    main()

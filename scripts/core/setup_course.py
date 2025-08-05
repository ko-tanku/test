#!/usr/bin/env python3

import subprocess
import sys
import os
from pathlib import Path

def setup_course(course_id):
    """
    docusaurus.config.jsを自動設定するためのPythonラッパー
    """
    try:
        # スクリプトのディレクトリを取得
        script_dir = Path(__file__).parent
        
        # Node.jsスクリプトのパス
        node_script_path = script_dir / 'setup-course.js'
        
        if not node_script_path.exists():
            print(f"Error: setup-course.js not found at {node_script_path}")
            return False
        
        # Node.jsスクリプトを実行
        print(f"Setting up course configuration for: {course_id}")
        cmd = ['node', str(node_script_path), course_id]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=script_dir.parent.parent  # プロジェクトルートディレクトリ
        )
        
        # 標準出力を表示
        if result.stdout:
            print(result.stdout)
        
        # エラー出力を表示
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        
        # 終了コードをチェック
        if result.returncode == 0:
            print(f"Successfully configured course: {course_id}")
            return True
        else:
            print(f"Failed to configure course: {course_id}")
            return False
            
    except Exception as e:
        print(f"Error executing setup-course.js: {e}")
        return False

def main():
    if len(sys.argv) != 2:
        print("Usage: python setup_course.py <course_id>")
        print("Example: python setup_course.py comprehensive-test")
        sys.exit(1)
    
    course_id = sys.argv[1]
    
    success = setup_course(course_id)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
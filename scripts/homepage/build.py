# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Homepage Generation Script
Generates a single JSON file for the homepage from source files (YAML, Markdown).
"""

import sys
import yaml
import json
from pathlib import Path

# Configure stdout for UTF-8 encoding
sys.stdout.reconfigure(encoding='utf-8')

# Resolve the project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

def load_yaml_file(file_path):
    """Safely loads a YAML file and returns its content."""
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
    """Reads a Markdown file and returns its content."""
    if not file_path.is_file():
        print(f"Warning: Markdown file not found at {file_path}", file=sys.stderr)
        return ""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading Markdown file {file_path}: {e}", file=sys.stderr)
        return ""

def generate_homepage_data(source_dir):
    """
    Generates the data for the homepage.
    """
    page_dir = source_dir / "pages" / "index"
    
    meta_data = load_yaml_file(page_dir / "meta.yaml") or {}
    prose_content = read_markdown_file(page_dir / "prose.md")
    components_data = load_yaml_file(page_dir / "components.yaml") or []

    final_prose_content = prose_content

    return {
        "id": "homepage",
        "title": meta_data.get("title", "Home"),
        "description": meta_data.get("description", ""),
        "slug": "/",
        "prose_content": final_prose_content,
        "components": components_data
    }

def main():
    """
    Main execution function.
    """
    print("Building homepage data...")
    source_dir = Path(__file__).parent / "source"
    output_data_dir = PROJECT_ROOT / "static" / "data"
    
    homepage_data = generate_homepage_data(source_dir)
    
    output_data_dir.mkdir(exist_ok=True)
    output_json_file = output_data_dir / "homepage.json"

    try:
        with open(output_json_file, 'w', encoding='utf-8') as f:
            json.dump(homepage_data, f, ensure_ascii=False, indent=2)
        print(f"Successfully generated homepage data to: {output_json_file}")
    except Exception as e:
        print(f"Error writing JSON data to {output_json_file}: {e}", file=sys.stderr)
        sys.exit(1)
    
    print("\nHomepage build completed successfully!")

if __name__ == "__main__":
    main()

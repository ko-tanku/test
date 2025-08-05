import os
import yaml
import json

def get_first_chapter_slug(module_path):
    try:
        files = sorted([f for f in os.listdir(module_path) if f.endswith(('.yaml', '.yml')) and f != 'module_meta.yaml'])
        if not files:
            return '/'
        file_path = os.path.join(module_path, files[0])
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            return data.get('slug', '/')
    except (IOError, yaml.YAMLError):
        return '/'

def generate_modules_data(definitions_dir, output_path):
    modules = []
    for module_name in sorted(os.listdir(definitions_dir)):
        module_path = os.path.join(definitions_dir, module_name)
        if os.path.isdir(module_path):
            meta_path = os.path.join(module_path, 'module_meta.yaml')
            if os.path.exists(meta_path):
                try:
                    with open(meta_path, 'r', encoding='utf-8') as f:
                        meta = yaml.safe_load(f)
                    first_chapter_slug = get_first_chapter_slug(module_path)
                    modules.append({
                        'title': meta.get('title', 'No Title'),
                        'description': meta.get('description', ''),
                        'link': f'/docs{first_chapter_slug}'
                    })
                except (IOError, yaml.YAMLError) as e:
                    print(f"Error processing {meta_path}: {e}")

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(modules, f, ensure_ascii=False, indent=2)
        print(f"Successfully generated module data at {output_path}")
    except IOError as e:
        print(f"Error writing to {output_path}: {e}")

if __name__ == '__main__':
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    content_def_dir = os.path.join(base_dir, 'scripts', 'content_definitions')
    # The output is now a JSON file in the HomepageContent component's directory
    output_file_path = os.path.join(base_dir, 'src', 'components', 'HomepageContent', 'modules.json')
    
    generate_modules_data(content_def_dir, output_file_path)

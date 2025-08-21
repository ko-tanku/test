"""
テスト資料のコンテンツ生成クラス（改善版）
Core機能を最大活用し、YAML データ駆動型のコンテンツ生成
"""

import sys
import yaml
import logging
from pathlib import Path
from typing import List, Dict, Any

# プロジェクトルートをsys.pathに追加
project_root = Path(__file__).resolve().parents[3]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.core.content_manager import BaseContentManager
from src.core.knowledge_manager import Term, FaqItem, TipItem
# Chart and table generation now handled by Core functionality

logger = logging.getLogger(__name__)


class TestMaterialContentManager(BaseContentManager):
    """テスト資料のコンテンツ管理クラス（改善版）"""
    
    def __init__(self, material_name: str, output_base_dir: Path):
        """初期化（YAML駆動型）"""
        # 設定をYAMLから読み込み
        config_data = self._load_config_yaml()
        colors = config_data.get('custom_colors', {})
        
        super().__init__(
            material_name=material_name,
            output_base_dir=output_base_dir,
            colors=colors
        )
        
        self.material_config = config_data.get('material_config', {})
        
        # 専門用語、FAQ、TIPSをYAMLから登録
        self._register_yaml_knowledge()
        
    def _load_config_yaml(self) -> Dict[str, Any]:
        """設定YAMLファイルを読み込み"""
        config_path = Path(__file__).parent / "content" / "config.yml"
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return {}
    
    def _register_yaml_knowledge(self):
        """YAMLファイルから知識データを登録"""
        content_dir = Path(__file__).parent / "content"
        
        # 用語データ
        terms_path = content_dir / "terms.yml"
        if terms_path.exists():
            with open(terms_path, 'r', encoding='utf-8') as f:
                terms_data = yaml.safe_load(f)
                terms_list = []
                for term_data in terms_data.get('terms', []):
                    term = Term(
                        term=term_data['term'],
                        definition=term_data['definition'],
                        category=term_data.get('category', ''),
                        related_terms=term_data.get('related_terms', []),
                        first_chapter=term_data.get('first_chapter'),
                        context_snippets=term_data.get('context_snippets', [])
                    )
                    terms_list.append(term)
                self._register_material_terms(terms_list)
        
        # FAQ・TIPSデータ
        faq_path = content_dir / "faq.yml"
        tips_path = content_dir / "tips.yml"
        
        faq_items = []
        if faq_path.exists():
            with open(faq_path, 'r', encoding='utf-8') as f:
                faq_data = yaml.safe_load(f)
                for item_data in faq_data.get('faq_items', []):
                    faq_item = FaqItem(
                        question=item_data['question'],
                        answer=item_data['answer'],
                        category=item_data.get('category')
                    )
                    faq_items.append(faq_item)
        
        tip_items = []
        if tips_path.exists():
            with open(tips_path, 'r', encoding='utf-8') as f:
                tips_data = yaml.safe_load(f)
                for item_data in tips_data.get('tip_items', []):
                    tip_item = TipItem(
                        title=item_data['title'],
                        content=item_data['content'],
                        category=item_data.get('category')
                    )
                    tip_items.append(tip_item)
        
        self._register_faq_tips(faq_items, tip_items)

    def generate_content(self) -> List[Path]:
        """
        テスト資料の全コンテンツを生成（YAML駆動型）
        """
        generated_files = []
        
        # 必要なディレクトリを作成
        docs_dir = self.output_base_dir / "documents"
        charts_dir = self.output_base_dir / "charts"
        tables_dir = self.output_base_dir / "tables"
        docs_dir.mkdir(parents=True, exist_ok=True)
        charts_dir.mkdir(parents=True, exist_ok=True)
        tables_dir.mkdir(parents=True, exist_ok=True)
        
        # 図表と表は個別のYAMLデータからCore機能で生成される
        self.generated_charts = {}
        self.generated_tables = {}
        
        # 教材のトップページ生成
        self.doc_builder.output_dir = self.output_base_dir
        generated_files.append(self._generate_material_index())
        
        # 各章のコンテンツ生成（YAML駆動型）
        self.doc_builder.output_dir = docs_dir
        
        # 設定から章リストを取得
        chapters = self.material_config.get('chapters', [])
        
        for chapter in chapters:
            chapter_id = chapter['id']
            yaml_file = chapter['file']
            md_filename = f"{chapter_id}.md"
            
            chapter_data = self.load_chapter_from_yaml(yaml_file)
            if chapter_data:
                generated_files.append(self._generate_chapter_from_data(
                    chapter_data, md_filename, charts_dir, tables_dir
                ))
            else:
                logger.warning(f"章データが見つかりません: {yaml_file}")
        
        # 用語集、FAQ、TIPSページ生成（Core機能による動的生成）
        self.doc_builder.output_dir = self.output_base_dir
        generated_files.append(self.knowledge_mgr.generate_glossary_markdown())
        generated_files.append(self.knowledge_mgr.generate_faq_markdown())
        generated_files.append(self.knowledge_mgr.generate_tips_markdown())
        
        return generated_files
        
    def _generate_material_index(self) -> Path:
        """教材のトップページを生成（YAML駆動型）"""
        self.doc_builder.clear_content()
        
        # 設定から情報を取得
        config = self.material_config
        
        self.doc_builder.add_heading(config.get("title", "学習教材"), 1)
        self.doc_builder.add_paragraph(config.get("description", ""))
        
        self.doc_builder.add_heading("学習目標", 2)
        self.doc_builder.add_unordered_list(config.get("learning_objectives", []))
        
        self.doc_builder.add_heading("対象読者", 2)
        self.doc_builder.add_paragraph(config.get("target_audience", ""))
        
        self.doc_builder.add_heading("章構成", 2)
        chapters = []
        for chapter in config.get('chapters', []):
            title = chapter['title']
            chapter_id = chapter['id']
            chapters.append(f"[{title}](documents/{chapter_id}.md)")
        self.doc_builder.add_ordered_list(chapters)
        
        self.doc_builder.add_heading("参考資料", 2)
        other_pages = [
            "[用語集](glossary.md)",
            "[よくある質問（FAQ）](faq.md)",
            "[学習のヒント（TIPS）](tips.md)"
        ]
        self.doc_builder.add_unordered_list(other_pages)
        
        return self.doc_builder.save_markdown("index.md")
        
    def _generate_chapter_from_data(self, chapter_data: Dict[str, Any], filename: str, 
                                   charts_dir: Path, tables_dir: Path) -> Path:
        """章データからMarkdownを生成"""
        self.doc_builder.clear_content()
        
        # タイトル
        self.doc_builder.add_heading(chapter_data.get('title', ''), 1)
        
        # 概要
        if 'overview' in chapter_data:
            self.doc_builder.add_paragraph(chapter_data['overview'])
            
        # セクション
        for section in chapter_data.get('sections', []):
            self.doc_builder.add_heading(section.get('title', ''), 2)
            
            # コンテンツリストを処理
            self._process_content_list(
                section.get('contents', []),
                charts_dir,
                tables_dir
            )
                
        return self.doc_builder.save_markdown(filename)
    
    def _process_content_list(self, contents: List[Dict[str, Any]], charts_dir: Path, tables_dir: Path):
        """コンテンツリストを処理（拡張版）"""
        for content in contents:
            content_type = content.get('type')
            
            if content_type == 'text':
                self.doc_builder.add_paragraph(content['text'])
            
            elif content_type == 'text_with_tooltips':
                terms_info = content.get('terms', {})
                self.doc_builder.add_paragraph_with_tooltips(content['text'], terms_info)
            
            elif content_type == 'heading':
                self.doc_builder.add_heading(content['text'], content.get('level', 2))
            
            elif content_type == 'admonition':
                self.doc_builder.add_admonition(
                    content.get('admonition_type', 'note'),
                    content.get('title', ''),
                    content['text'],
                    content.get('collapsible', False)
                )
            
            elif content_type == 'code_block':
                self.doc_builder.add_code_block(
                    content['code'],
                    content.get('language', 'text')
                )
            
            elif content_type == 'tabs':
                self.doc_builder.add_tabbed_content(content['tabs_data'])
            
            elif content_type == 'table':
                self._process_table_content(content, tables_dir)
            
            elif content_type == 'chart':
                self._process_chart_content(content, charts_dir)
            
            elif content_type == 'html_block':
                self.doc_builder.add_html_block(content['html'])
            
            elif content_type == 'single_choice_quiz':
                self._add_single_choice_quiz(content)
            
            elif content_type == 'multiple_choice_quiz':
                self._add_multiple_choice_quiz(content)
            
            elif content_type == 'categorization_quiz':
                self._add_categorization_quiz(content)
            
            elif content_type == 'summary':
                self.doc_builder.add_summary(
                    content.get('title', ''),
                    content.get('points', [])
                )
            
            elif content_type == 'horizontal_rule':
                self.doc_builder.add_horizontal_rule()
            
            elif content_type == 'quote':
                self.doc_builder.add_blockquote(content['text'])
            
            elif content_type == 'list':
                if content.get('list_type') == 'ordered':
                    self.doc_builder.add_ordered_list(content['items'])
                else:
                    self.doc_builder.add_unordered_list(content['items'])
    
    def _process_table_content(self, content: Dict[str, Any], tables_dir: Path):
        """表コンテンツを処理"""
        table_config = content.get('config', {})
        if content.get('table_type') == 'basic':
            table_path = self.table_gen.create_basic_table(
                content['headers'],
                content['rows'],
                content.get('title', ''),
                content.get('filename', 'table') + '.html',
                output_dir=tables_dir
            )
            self._embed_table(table_path, content.get('caption', ''), content.get('title', ''))
    
    def _process_chart_content(self, content: Dict[str, Any], charts_dir: Path):
        """図表コンテンツを処理"""
        chart_type = content.get('chart_type')
        config = content.get('config', {})
        data = content.get('data')
        
        if chart_type == 'custom':
            # カスタム描画関数による図表
            plot_function_name = config.get('plot_function')
            if hasattr(self, plot_function_name):
                plot_function = getattr(self, plot_function_name)
                filename = config.get('filename', 'custom_chart') + '.html'
                chart_path = self.chart_gen.create_custom_figure(
                    plot_function, filename, output_dir=charts_dir
                )
                self._embed_chart(chart_path, content.get('caption', ''), config.get('title', ''))
        
        elif chart_type in ['line', 'bar', 'pie']:
            # 標準的な図表
            filename = config.get('filename', 'chart') + '.html'
            if chart_type == 'line':
                chart_path = self.chart_gen.create_simple_line_chart(
                    data, config['x_col'], config['y_col'],
                    config.get('title', ''),
                    config.get('xlabel', ''),
                    config.get('ylabel', ''),
                    filename,
                    output_dir=charts_dir
                )
            elif chart_type == 'bar':
                chart_path = self.chart_gen.create_bar_chart(
                    data, config['x_col'], config['y_col'],
                    config.get('title', ''),
                    config.get('xlabel', ''),
                    config.get('ylabel', ''),
                    filename,
                    use_plotly=config.get('use_plotly', False),
                    output_dir=charts_dir
                )
            elif chart_type == 'pie':
                chart_path = self.chart_gen.create_pie_chart(
                    data, config['values_col'], config['labels_col'],
                    config.get('title', ''),
                    filename,
                    use_plotly=config.get('use_plotly', False),
                    output_dir=charts_dir
                )
            
            self._embed_chart(chart_path, content.get('caption', ''), config.get('title', ''))
    
    def _embed_chart(self, chart_path: Path, caption: str, title: str):
        """図表をMarkdownに埋め込み"""
        relative_path = f"../charts/{chart_path.name}"
        width = "100%"
        height = "450px"
        
        iframe_html = f'<iframe src="{relative_path}" width="{width}" height="{height}" frameborder="0"></iframe>'
        self.doc_builder.add_html_block(iframe_html)
        
        if caption:
            self.doc_builder.add_paragraph(f"*{caption}*")
    
    def _embed_table(self, table_path: Path, caption: str, title: str):
        """表をMarkdownに埋め込み"""
        relative_path = f"../tables/{table_path.name}"
        
        iframe_html = f'<iframe src="{relative_path}" width="100%" height="400px" frameborder="0"></iframe>'
        self.doc_builder.add_html_block(iframe_html)
        
        if caption:
            self.doc_builder.add_paragraph(f"*{caption}*")
    
    def _add_single_choice_quiz(self, content: Dict[str, Any]):
        """単一選択クイズを追加"""
        quiz_id = f"single_{hash(content['question']) % 10000}"
        options = content['options']
        
        html = f'''
<div class="single-choice-quiz" data-quiz-id="{quiz_id}">
    <div class="quiz-question">{content['question']}</div>
    <div class="single-choice-options">
'''
        for i, option in enumerate(options):
            html += f'''        <div class="single-choice-option">
            <input type="radio" name="{quiz_id}" value="{i}" id="{quiz_id}_option_{i}">
            <label for="{quiz_id}_option_{i}">{option}</label>
        </div>
'''
        
        html += f'''    </div>
    <button onclick="checkSingleChoice('{quiz_id}')" style="margin-top: 15px; padding: 10px 20px; background: #4CAF50; color: white; border: none; border-radius: 4px; cursor: pointer;">答えを確認</button>
    <div class="single-choice-result quiz-result"></div>
</div>

<script>
if (!window.singleChoiceData) window.singleChoiceData = {{}};
window.singleChoiceData['{quiz_id}'] = {{
    correct: {content['correct']},
    explanation: "{content.get('explanation', '')}",
    hint: "{content.get('hint', '')}"
}};
</script>'''
        
        self.doc_builder.add_html_block(html)
    
    def _add_multiple_choice_quiz(self, content: Dict[str, Any]):
        """複数選択クイズを追加"""
        quiz_id = content.get('quiz_id', f"multi_{hash(content['question']) % 10000}")
        options = content['options']
        
        html = f'''
<div class="multiple-choice-quiz" data-quiz-id="{quiz_id}">
    <div class="quiz-question">{content['question']}</div>
    <div class="multiple-choice-options">
'''
        for i, option in enumerate(options):
            html += f'''        <div class="multiple-choice-option">
            <input type="checkbox" name="{quiz_id}" value="{i}" id="{quiz_id}_option_{i}">
            <label for="{quiz_id}_option_{i}">{option}</label>
        </div>
'''
        
        html += f'''    </div>
    <button onclick="checkMultipleChoice('{quiz_id}')" style="margin-top: 15px; padding: 10px 20px; background: #2196F3; color: white; border: none; border-radius: 4px; cursor: pointer;">答えを確認</button>
    <div class="multiple-choice-result quiz-result"></div>
</div>

<script>
if (!window.multipleChoiceData) window.multipleChoiceData = {{}};
window.multipleChoiceData['{quiz_id}'] = {{
    correct: {content['correct_answers']},
    explanation: "{content.get('explanation', '')}"
}};
</script>'''
        
        self.doc_builder.add_html_block(html)
    
    def _add_categorization_quiz(self, content: Dict[str, Any]):
        """カテゴリ分けクイズを追加"""
        quiz_id = content.get('quiz_id', f"cat_{hash(content['question']) % 10000}")
        categories = content['categories']
        items = content['items']
        
        html = f'''
<div class="categorization-quiz" data-quiz-id="{quiz_id}">
    <div class="quiz-question">{content['question']}</div>
    
    <div class="draggable-items">
'''
        for i, item in enumerate(items):
            html += f'        <div class="draggable-item" draggable="true" data-item="{i}" id="{quiz_id}_item_{i}">{item}</div>\n'
        
        html += '    </div>\n\n'
        
        for i, category in enumerate(categories):
            html += f'''    <div class="drop-zone" data-category="{i}">
        <h4>{category}</h4>
        <div class="drop-area"></div>
    </div>
'''
        
        html += f'''    <button onclick="checkCategorization('{quiz_id}')" style="margin-top: 15px; padding: 10px 20px; background: #FF9800; color: white; border: none; border-radius: 4px; cursor: pointer;">分類結果を確認</button>
    <div class="categorization-result quiz-result"></div>
</div>

<script>
if (!window.categorizationData) window.categorizationData = {{}};
window.categorizationData['{quiz_id}'] = {content['correct_answers']};
</script>'''
        
        self.doc_builder.add_html_block(html)
        
    # カスタム描画関数（第7章用）
    def draw_network_diagram(self, ax, colors, styles, **kwargs):
        """ネットワーク図を描画（第7章用拡張機能）"""
        import matplotlib.patches as patches
        
        # ノード位置の定義
        positions = {
            'マイコン': (0.5, 0.5),
            'センサー1': (0.2, 0.8),
            'センサー2': (0.2, 0.2),
            'アクチュエータ': (0.8, 0.5),
            '電源': (0.1, 0.5),
            '通信モジュール': (0.9, 0.8)
        }
        
        # ノードを描画
        for name, (x, y) in positions.items():
            circle = patches.Circle((x, y), 0.08, 
                                  facecolor=colors.get('info', '#2196F3'),
                                  edgecolor='black', linewidth=2)
            ax.add_patch(circle)
            ax.text(x, y-0.12, name, ha='center', va='center', 
                   fontsize=styles['font_size_label'], fontweight='bold')
        
        # 接続線を描画
        connections = [
            ('マイコン', 'センサー1'),
            ('マイコン', 'センサー2'),
            ('マイコン', 'アクチュエータ'),
            ('電源', 'マイコン'),
            ('マイコン', '通信モジュール')
        ]
        
        for node1, node2 in connections:
            x1, y1 = positions[node1]
            x2, y2 = positions[node2]
            ax.plot([x1, x2], [y1, y2], 'k-', linewidth=2, alpha=0.7)
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect('equal')
        ax.set_title('組み込みシステムネットワーク構成', fontsize=styles['font_size_title'])
        ax.axis('off')
    
    def draw_config_flow_diagram(self, ax, colors, styles, **kwargs):
        """設定ファイル処理フローを描画（第6章用）"""
        import matplotlib.patches as patches
        
        # フローチャートのボックス
        boxes = [
            {'name': 'config.yml', 'pos': (0.2, 0.8), 'color': colors.get('info', '#2196F3')},
            {'name': 'terms.yml', 'pos': (0.2, 0.6), 'color': colors.get('success', '#4CAF50')},
            {'name': 'faq.yml', 'pos': (0.2, 0.4), 'color': colors.get('success', '#4CAF50')},
            {'name': 'tips.yml', 'pos': (0.2, 0.2), 'color': colors.get('success', '#4CAF50')},
            {'name': 'ContentManager', 'pos': (0.5, 0.5), 'color': colors.get('warning', '#FF9800')},
            {'name': 'Markdown生成', 'pos': (0.8, 0.5), 'color': colors.get('info', '#2196F3')}
        ]
        
        # ボックスを描画
        for box in boxes:
            name, (x, y), color = box['name'], box['pos'], box['color']
            rect = patches.Rectangle((x-0.08, y-0.05), 0.16, 0.1,
                                   facecolor=color, edgecolor='black', linewidth=1)
            ax.add_patch(rect)
            ax.text(x, y, name, ha='center', va='center',
                   fontsize=styles['font_size_label'], color='white', fontweight='bold')
        
        # 矢印を描画
        arrows = [
            ((0.28, 0.8), (0.42, 0.55)),
            ((0.28, 0.6), (0.42, 0.52)),
            ((0.28, 0.4), (0.42, 0.48)),
            ((0.28, 0.2), (0.42, 0.45)),
            ((0.58, 0.5), (0.72, 0.5))
        ]
        
        for (x1, y1), (x2, y2) in arrows:
            ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                       arrowprops=dict(arrowstyle='->', lw=2, color='black'))
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect('equal')
        ax.set_title('設定ファイル処理フロー', fontsize=styles['font_size_title'])
        ax.axis('off')
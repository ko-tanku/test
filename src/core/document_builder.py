"""
Markdownコンテンツを構築するためのビルダークラス
MkDocs Materialテーマの拡張機能をサポート
"""

import re
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from html import escape

from .utils import (
    generate_admonition_markdown,
    generate_tabbed_markdown
)
from .config import MATERIAL_ICONS

logger = logging.getLogger(__name__)


class DocumentBuilder:
    """Markdownドキュメントを構築するビルダークラス"""
    
    def __init__(self, output_dir: Path):
        """
        初期化
        
        Args:
            output_dir: Markdownファイル出力先のベースディレクトリ
        """
        self.output_dir = Path(output_dir)
        self.content_buffer = []
        
    def clear_content(self):
        """現在構築中のMarkdownコンテンツの内部バッファをクリア"""
        self.content_buffer = []
        
    def get_content(self) -> str:
        """
        構築された現在のMarkdownコンテンツを文字列として返す
        
        Returns:
            Markdownコンテンツ文字列
        """
        return '\n'.join(self.content_buffer)
        
    def save_markdown(self, filename: str) -> Path:
        """
        現在のコンテンツをMarkdownファイルとして保存
        
        Args:
            filename: 保存するファイル名（相対パス）
            
        Returns:
            保存されたファイルのPathオブジェクト
        """
        file_path = self.output_dir / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        content = self.get_content()
        file_path.write_text(content, encoding='utf-8')
        
        logger.info(f"Markdownファイルを保存しました: {file_path}")
        
        # バッファをクリア
        self.clear_content()
        
        return file_path
        
    def add_heading(self, text: str, level: int):
        """
        Markdownの見出しを追加
        
        Args:
            text: 見出しテキスト
            level: 見出しレベル（1-6）
            
        Raises:
            ValueError: レベルが1-6の範囲外の場合
        """
        if not 1 <= level <= 6:
            raise ValueError(f"見出しレベルは1-6の範囲で指定してください: {level}")
        
        prefix = '#' * level
        self.content_buffer.append(f"{prefix} {text}")
        self.content_buffer.append("")  # 見出しの後に空行を追加
        
    def add_paragraph(self, text: str):
        """
        段落テキストを追加
        
        Args:
            text: 段落のテキスト
        """
        self.content_buffer.append(text)
        self.content_buffer.append("")  # 段落の後に厳密に1つの空行を追加
        
    def add_paragraph_with_tooltips(
        self, text: str, terms_info: Dict[str, Dict[str, str]]
    ):
        """
        専門用語にツールチップを付与した段落を追加
        
        Args:
            text: 段落のテキスト
            terms_info: 用語情報の辞書 {用語: {"tooltip_text": "ツールチップ内容"}}
        """
        # 既存のMarkdownリンクを保護するためのパターン
        link_pattern = r'\[([^\]]+)\]\([^)]+\)'
        protected_links = []
        
        # 既存のリンクを一時的に置換
        def protect_link(match):
            protected_links.append(match.group(0))
            return f"__PROTECTED_LINK_{len(protected_links) - 1}__"
        
        text_with_protected_links = re.sub(link_pattern, protect_link, text)
        
        # 用語をツールチップ付きリンクに置換
        for term, info in terms_info.items():
            tooltip_text = info.get("tooltip_text", "")
            # HTMLエスケープ
            escaped_tooltip = escape(tooltip_text)
            # 改行を&#10;に置換
            escaped_tooltip = escaped_tooltip.replace('\n', '&#10;')

            # 正確な用語の文字列をマッチさせ、初回のみ置換
            pattern = re.escape(term)
            replacement = f'<span class="custom-tooltip" data-tooltip="{escaped_tooltip}">{term}</span>'
            text_with_protected_links = re.sub(
                pattern, replacement, text_with_protected_links, count=1
            )
        
        # 保護していたリンクを復元
        for i, protected_link in enumerate(protected_links):
            text_with_protected_links = text_with_protected_links.replace(
                f"__PROTECTED_LINK_{i}__", protected_link
            )
        self.add_paragraph(text_with_protected_links)
        
    def add_code_block(self, code: str, lang: str = "python"):
        """
        コードブロックを追加
        
        Args:
            code: コード文字列
            lang: 言語指定
        """
        self.content_buffer.append(f"```{lang}")
        self.content_buffer.append(code)
        self.content_buffer.append("```")
        self.content_buffer.append("")
        
    def add_unordered_list(self, items: List[str]):
        """
        順不同リストを追加
        
        Args:
            items: リスト項目のリスト
        """
        for item in items:
            self.content_buffer.append(f"- {item}")
        self.content_buffer.append("")
        
    def add_ordered_list(self, items: List[str]):
        """
        順序付きリストを追加
        
        Args:
            items: リスト項目のリスト
        """
        for i, item in enumerate(items, 1):
            self.content_buffer.append(f"{i}. {item}")
        self.content_buffer.append("")
        
    def add_quote(self, text: str):
        """
        引用ブロックを追加
        
        Args:
            text: 引用テキスト
        """
        for line in text.split('\n'):
            self.content_buffer.append(f"> {line}")
        self.content_buffer.append("")
        
    def add_image_reference(
        self, alt_text: str, image_path: Path, title: Optional[str] = None
    ):
        """
        画像参照を追加
        
        Args:
            alt_text: 代替テキスト
            image_path: 画像ファイルのパス
            title: タイトル（オプション）
        """
        # Unixスタイルパスに変換
        path_str = image_path.as_posix()
        
        if title:
            self.content_buffer.append(f'![{alt_text}]({path_str} "{title}")')
        else:
            self.content_buffer.append(f'![{alt_text}]({path_str})')
        self.content_buffer.append("")

    def add_html_component_reference(
        self, component_path: Path, width: str = "100%", height: Optional[str] = "400px"
    ):
        """
        HTML図表や表をiframeで埋め込む
        
        Args:
            component_path: HTMLファイルのパス
            width: 幅の指定
            height: 高さの指定 (Noneの場合、height属性は出力されない)
        """
        # Unixスタイルパスに変換
        path_str = component_path.as_posix()
        
        # heightがNoneでない場合にのみheight属性を追加
        height_attr = f'height="{height}"' if height is not None else ''
        
        iframe_html = (
            f'<iframe src="{path_str}" '
            f'width="{width}" {height_attr} '
            f'style="border: 1px solid #ddd; border-radius: 4px;" '
            f'scrolling="no" class="auto-height-iframe">'
            f'</iframe>'
        )
        self.content_buffer.append(iframe_html)
        self.content_buffer.append("")
        
    def add_admonition(
        self, type: str, title: str, content: str, collapsible: bool = False
    ):
        """
        MkDocs MaterialのAdmonitionブロックを追加
        
        Args:
            type: 注記のタイプ
            title: タイトル
            content: 内容
            collapsible: 折りたたみ可能にするか
        """
        admonition_md = generate_admonition_markdown(type, title, content, collapsible)
        self.content_buffer.append(admonition_md)
        
    def add_tabbed_block(self, tabs_data: Dict[str, str]):
        """
        MkDocs MaterialのTabbedブロックを追加
        
        Args:
            tabs_data: タブデータの辞書
        """
        tabbed_md = generate_tabbed_markdown(tabs_data)
        self.content_buffer.append(tabbed_md)
        
    def add_horizontal_rule(self):
        """水平線を追加"""
        self.content_buffer.append("---")
        self.content_buffer.append("")
        
    def add_raw_markdown(self, markdown_string: str):
        """
        生のMarkdown文字列を追加
        
        Args:
            markdown_string: Markdown文字列
        """
        self.content_buffer.append(markdown_string)
        
    def add_icon_with_tooltip(self, icon_name: str, tooltip_text: str):
        """
        Material Design Iconsにツールチップを付与
        
        Args:
            icon_name: アイコン名（辞書のキー）
            tooltip_text: ツールチップテキスト
        """
        escaped_tooltip = escape(tooltip_text)
        
        # アイコン辞書から実際のアイコン名を取得
        actual_icon = MATERIAL_ICONS.get(icon_name, "help")  # デフォルトはhelp
        
        icon_md = f':material-{actual_icon}:{{ title="{escaped_tooltip}" }}'
        self.content_buffer.append(icon_md)
        self.content_buffer.append("")
        
    def add_abbreviation_definition(self, abbr: str, full_form: str):
        """
        略語の定義を追加
        
        Args:
            abbr: 略語
            full_form: フルスペルまたは説明
        """
        replacement = f'<span class="custom-tooltip" data-tooltip="{full_form}">{abbr}</span>'
        self.content_buffer.append(replacement)
        self.content_buffer.append("")
        
    def add_quiz_question(self, question_data: Dict[str, Any]):
        """
        改良されたクイズ問題を追加（問題を最初から表示）
        
        Args:
            question_data: 問題データの辞書
        """
        lines = []
        
        # 問題セクション
        lines.append("!!! question \"クイズ\"")
        lines.append(f"    **問題**: {question_data['question']}")
        lines.append("")
        
        # 選択肢に番号を付けて表示
        lines.append("    **選択肢**:")
        for i, option in enumerate(question_data['options'], 1):
            lines.append(f"    {i}. {option}")
        lines.append("")
        
        # ヒント（折りたたみ式）
        if 'hint' in question_data:
            lines.append("    ??? tip \"ヒント\"")
            lines.append(f"        {question_data['hint']}")
            lines.append("")
        
        # 解説（折りたたみ式、正解を含む）
        if 'explanation' in question_data:
            correct_num = question_data.get('correct', 0) + 1  # 0ベースから1ベースに変換
            lines.append("    ??? success \"解説\"")
            lines.append(f"        **正解**: {correct_num}")
            lines.append("")
            lines.append(f"        **解説**: {question_data['explanation']}")
        
        self.content_buffer.extend(lines)
        self.content_buffer.append("")

    def add_categorization_quiz(self, quiz_data: Dict[str, Any]):
        """
        カテゴリ分けクイズを追加（ドラッグ&ドロップ）
        
        Args:
            quiz_data: クイズデータの辞書
        """
        lines = []
        quiz_id = quiz_data.get('quiz_id', quiz_data.get('id', 'categorization-quiz'))
        
        lines.append("!!! question \"カテゴリ分けクイズ\"")
        lines.append(f"    **問題**: {quiz_data['question']}")
        lines.append("")
        
        # カテゴリ
        lines.append("    **カテゴリ**:")
        for category in quiz_data['categories']:
            lines.append(f"    - {category}")
        lines.append("")
        
        # ドラッグ&ドロップ用のHTMLを生成
        html_content = f'''
    <div class="categorization-quiz" data-quiz-id="{quiz_id}">
        <div class="quiz-items">
            <h4>項目をドラッグして適切なカテゴリに分類してください：</h4>
            <div class="draggable-items">'''
        
        # アイテムを追加
        for i, item in enumerate(quiz_data['items']):
            html_content += f'''
                <div class="draggable-item" data-item="{i}" draggable="true">{item}</div>'''
        
        html_content += '''
            </div>
        </div>
        
        <div class="drop-zones">'''
        
        # カテゴリのドロップゾーンを作成
        for i, category in enumerate(quiz_data['categories']):
            html_content += f'''
            <div class="drop-zone" data-category="{i}">
                <h4>{category}</h4>
                <div class="drop-area">ここにドロップしてください</div>
            </div>'''
        
        html_content += f'''
        </div>
        
        <button class="check-categorization" onclick="checkCategorization('{quiz_id}')">答えを確認</button>
        <div class="categorization-result"></div>
    </div>'''
        
        # admonitionブロックをクローズ
        self.content_buffer.extend(lines)
        self.content_buffer.append("")
        
        # HTMLコンテンツを独立したブロックとして追加（インデントしない）
        self.content_buffer.append(html_content)
        self.content_buffer.append("")
        
        # 正解データをdata属性として埋め込み
        correct_data = quiz_data.get('correct_answers', quiz_data.get('correct_mapping', []))
        self.content_buffer.append(f'<script>window.categorizationData = window.categorizationData || {{}};')
        self.content_buffer.append(f'window.categorizationData["{quiz_id}"] = {correct_data};</script>')
        self.content_buffer.append("")

    def add_multiple_choice_quiz(self, quiz_data: Dict[str, Any]):
        """
        複数選択クイズを追加（複数の正解を選択）
        
        Args:
            quiz_data: クイズデータの辞書
        """
        lines = []
        quiz_id = quiz_data.get('quiz_id', quiz_data.get('id', 'multiple-choice-quiz'))
        
        lines.append("!!! question \"複数選択クイズ\"")
        lines.append(f"    **問題**: {quiz_data['question']}")
        lines.append("")
        lines.append("    **複数の選択肢から正解を全て選んでください**:")
        lines.append("")
        
        # チェックボックス形式のHTMLを生成
        html_content = f'''
    <div class="multiple-choice-quiz" data-quiz-id="{quiz_id}">
        <div class="quiz-options">'''
        
        # 選択肢を追加（チェックボックス）
        for i, option in enumerate(quiz_data['options']):
            html_content += f'''
            <label class="option-label">
                <input type="checkbox" name="{quiz_id}" value="{i}">
                <span class="option-text">{option}</span>
            </label><br>'''
        
        html_content += f'''
        </div>
        
        <button class="check-multiple-choice" onclick="checkMultipleChoice('{quiz_id}')">答えを確認</button>
        <div class="multiple-choice-result"></div>
    </div>'''
        
        # admonitionブロックをクローズ
        self.content_buffer.extend(lines)
        self.content_buffer.append("")
        
        # HTMLコンテンツを独立したブロックとして追加（インデントしない）
        self.content_buffer.append(html_content)
        self.content_buffer.append("")
        
        # 正解データと解説をdata属性として埋め込み
        correct_indices = quiz_data.get('correct_answers', quiz_data.get('correct_indices', []))
        explanation = quiz_data.get('explanation', '')
        self.content_buffer.append(f'<script>window.multipleChoiceData = window.multipleChoiceData || {{}};')
        self.content_buffer.append(f'window.multipleChoiceData["{quiz_id}"] = {{')
        self.content_buffer.append(f'  "correct": {correct_indices},')
        self.content_buffer.append(f'  "explanation": "{explanation}"')
        self.content_buffer.append(f'}};</script>')
        self.content_buffer.append("")
        
    def add_exercise_question(self, exercise_data: Dict[str, Any]):
        """
        演習問題を統一フォーマットで追加
        
        Args:
            exercise_data: 演習問題データの辞書
        """
        difficulty_map = {
            'easy': ('tip', '初級'),
            'medium': ('question', '中級'),
            'hard': ('warning', '上級')
        }
        
        difficulty = exercise_data.get('difficulty', 'medium')
        adm_type, difficulty_label = difficulty_map.get(difficulty, ('question', '中級'))
        
        lines = []
        lines.append(f"!!! {adm_type} \"演習問題（{difficulty_label}）\"")
        lines.append(f"    **問題**: {exercise_data.get('question', '')}")
        lines.append("")
        
        # 解答（折りたたみ式）
        if 'answer' in exercise_data:
            lines.append("    ??? success \"解答\"")
            lines.append(f"        **解答**: {exercise_data.get('answer', '')}")
            lines.append("")
        
        # 解説（折りたたみ式）
        if 'explanation' in exercise_data:
            lines.append("    ??? info \"解説\"")
            lines.append(f"        **解説**: {exercise_data.get('explanation', '')}")
        
        self.content_buffer.extend(lines)
        self.content_buffer.append("")
        
    def add_faq_item(self, question: str, answer: str, collapsible: bool = True):
        """
        FAQ項目を追加
        
        Args:
            question: 質問
            answer: 回答
            collapsible: 折りたたみ可能にするか
        """
        self.add_admonition("question", question, answer, collapsible)
        
    def add_tip_item(self, title: str, content: str, collapsible: bool = True):
        """
        TIPS項目を追加
        
        Args:
            title: タイトル
            content: 内容
            collapsible: 折りたたみ可能にするか
        """
        self.add_admonition("tip", title, content, collapsible)
        
    def add_code_block_with_static_output(
        self, code: str, output: str, lang: str = "python", output_label: str = "実行結果"
    ):
        """
        コードブロックと静的な実行結果を追加
        
        Args:
            code: コード
            output: 実行結果
            lang: 言語
            output_label: 出力ラベル
        """
        self.add_code_block(code, lang)
        self.add_admonition("success", output_label, f"```\n{output}\n```", False)
        
    def add_summary_section(self, title: str, points: List[str]):
        """
        学習の要点（サマリー）セクションを追加
        
        Args:
            title: セクションタイトル
            points: 要点のリスト
        """
        content = "\n".join(f"- {point}" for point in points)
        self.add_admonition("note", title, content, False)
        
    def add_recommendation_section(self, title: str, items: List[Dict[str, str]]):
        """
        関連資料や次のステップのレコメンデーションを追加
        
        Args:
            title: セクションタイトル
            items: レコメンデーション項目のリスト [{"text": "表示テキスト", "link": "URL"}]
        """
        lines = []
        for item in items:
            text = item.get("text", "")
            link = item.get("link", "")
            if link:
                lines.append(f"- [{text}]({link})")
            else:
                lines.append(f"- {text}")
        
        content = "\n".join(lines)
        self.add_admonition("info", title, content, False)
        
    def add_mermaid_block(self, graph_string: str, title: Optional[str] = None):
        """
        Mermaid図表ブロックを追加
        
        Args:
            graph_string: Mermaid構文の図表定義
            title: 図表のタイトル（オプション）
        """
        if title:
            self.add_paragraph(f"**{title}**")
        
        # Mermaidブロックを追加
        self.content_buffer.append("```mermaid")
        self.content_buffer.append(graph_string)
        self.content_buffer.append("```")
        self.content_buffer.append("")  # 空行を追加
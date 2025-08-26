"""
Markdownコンテンツを構築するためのビルダークラス
MkDocs Materialテーマの拡張機能をサポート
"""

import re
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from html import escape
import json # 追加

from .utils import (
    generate_admonition_markdown,
    generate_tabbed_markdown,
    slugify
)
from .config import MATERIAL_ICONS
from .knowledge_manager import KnowledgeManager
from .learning_analyzer import LearningAnalyzer

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
        """
        現在構築中のMarkdownコンテンツの内部バッファをクリア
        """
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
        
    def _escape_js_string(self, s: str) -> str:
        """
        JavaScript文字列リテラル用に文字列をエスケープする
        """
        # json.dumps は文字列を二重引用符で囲み、特殊文字をエスケープする
        # JavaScriptの文字列リテラルとしてそのまま使用できる
        return json.dumps(s)

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
        self.content_buffer.append("")
        
    def add_paragraph(self, text: str):
        """
        段落テキストを追加
        
        Args:
            text: 段落のテキスト
        """
        self.content_buffer.append(text)
        self.content_buffer.append("")
        
    def add_paragraph_with_tooltips(
        self, 
        text: str, 
        terms_info: Dict[str, Dict[str, str]],
        knowledge_mgr: KnowledgeManager,
        chapter_title: str,
        chapter_path: str
    ):
        """
        専門用語にツールチップを付与した段落を追加し、使用箇所を記録する。

        Args:
            text: 段落のテキスト
            terms_info: この段落でハイライト対象となりうる用語の情報
            knowledge_mgr: KnowledgeManagerのインスタンス
            chapter_title: 現在の章のタイトル
            chapter_path: 現在の章のファイルパス (docs/からの相対)
        """
        # 既存のMarkdownリンクを保護
        link_pattern = r'\[([^\]]+)\]\([^)]+\)'
        protected_links = []
        def protect_link(match):
            protected_links.append(match.group(0))
            return f"__PROTECTED_LINK_{len(protected_links) - 1}__"
        
        processed_text = re.sub(link_pattern, protect_link, text)

        used_terms = set()
        # 用語をツールチップ付きリンクに置換
        for term, info in terms_info.items():
            # テキスト内に実際に用語が存在するか確認
            if term in processed_text:
                tooltip_text = info.get("tooltip_text", "")
                escaped_tooltip = escape(tooltip_text).replace('\n', '&#10;')
                
                replacement = f'<span class="custom-tooltip" data-tooltip="{escaped_tooltip}">{term}</span>'
                # 最初に見つかったものだけを置換
                processed_text, count = re.subn(re.escape(term), replacement, processed_text, count=1)
                if count > 0:
                    used_terms.add(term)

        # 用語が一つも使われていなければ、元のテキストをそのまま追加
        if not used_terms:
            self.add_raw_markdown(text)
            return

        # 段落にユニークなIDを付与
        first_term_slug = slugify(list(used_terms)[0])
        text_hash = abs(hash(text)) % (10**8)
        paragraph_id = f"usage-{first_term_slug}-{text_hash}"

        # 使用箇所を記録
        for term in used_terms:
            knowledge_mgr.record_term_usage(term, chapter_title, chapter_path, paragraph_id)

        # 保護していたリンクを復元
        for i, protected_link in enumerate(protected_links):
            processed_text = processed_text.replace(f"__PROTECTED_LINK_{i}__", protected_link)
        
        # ID付きのdivでラップして追加
        final_html = f"""
<div id="{paragraph_id}">
{processed_text}
</div>"""
        self.add_raw_markdown(final_html)
        self.add_raw_markdown("") # 末尾に改行を追加
        
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
        """
        水平線を追加
        """
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
        
    def add_single_choice_quiz(self, quiz_data: Dict[str, Any]):
        """
        単一選択クイズを追加
        
        Args:
            quiz_data: クイズデータの辞書
        """
        quiz_id = quiz_data.get('quiz_id', quiz_data.get('id', 'single-choice-quiz'))
        
        html_content = f'<div class="quiz-container single-choice-quiz" data-quiz-id="{quiz_id}">'
        html_content += f'<h3 class="quiz-title">クイズ</h3>'
        html_content += f'<p class="quiz-question"><strong>問題:</strong> {quiz_data["question"]}</p>'
        html_content += f'<div class="quiz-options">'
        
        for i, option in enumerate(quiz_data['options']):
            html_content += f'<label class="option-label"><input type="radio" name="{quiz_id}" value="{i}"><span class="option-text">{option}</span></label><br>'
        
        html_content += f'</div>'
        html_content += f'<button class="check-single-choice" onclick="checkSingleChoice(\'{quiz_id}\')">答えを確認</button>'
        html_content += f'<div class="single-choice-result"></div>'
        html_content += f'</div>'
        
        html_content += '<script>'
        html_content += 'window.quizData = window.quizData || { quizzes: {} };'
        html_content += f'window.quizData.quizzes["{quiz_id}"] = {{'
        html_content += '"type": "single-choice",'
        html_content += f'"question": {self._escape_js_string(quiz_data["question"])},'
        html_content += f'"options": {self._escape_js_string(quiz_data["options"])},'
        html_content += f'"correct": {quiz_data.get("correct", 0)},'
        html_content += f'"explanation": {self._escape_js_string(quiz_data.get("explanation", ""))}'
        html_content += '};'
        html_content += '</script>'

    def add_categorization_quiz(self, quiz_data: Dict[str, Any]):
        """
        カテゴリ分けクイズを追加
        
        Args:
            quiz_data: クイズデータの辞書
        """
        quiz_id = quiz_data.get('quiz_id', quiz_data.get('id', 'categorization-quiz'))
        
        html_content = f'<div class="quiz-container categorization-quiz" data-quiz-id="{quiz_id}">'
        html_content += f'<h3 class="quiz-title">クイズ</h3>'
        html_content += f'<p class="quiz-question"><strong>問題:</strong> {quiz_data["question"]}</p>'
        html_content += f'<div class="quiz-items">'
        html_content += f'<h5>分類対象の項目:</h5>'
        html_content += f'<div class="draggable-items">'
        
        for i, item_data in enumerate(quiz_data['items']):
            html_content += f'<div class="draggable-item" draggable="true" data-item="{i}">{item_data["name"]}</div>'
        
        html_content += f'</div>'
        html_content += f'</div>'
        html_content += f'<div class="drop-zones">'
        
        for i, category in enumerate(quiz_data['categories']):
            html_content += f'<div class="drop-zone"><h4>{category}</h4><div class="drop-area" data-category="{i}">ここにドロップしてください</div></div>'
        
        html_content += f'</div>'
        html_content += f'<button class="check-categorization" onclick="checkCategorization(\'{quiz_id}\')">解答をチェック</button>'
        html_content += f'<div class="categorization-result"></div>'
        html_content += f'</div>'
        
        html_content += '<script>'
        html_content += 'window.quizData = window.quizData || { quizzes: {} };'
        html_content += f'window.quizData.quizzes["{quiz_id}"] = {{'
        html_content += '"type": "categorization",'
        html_content += f'"question": {self._escape_js_string(quiz_data["question"])},'
        html_content += f'"items": {self._escape_js_string(quiz_data["items"])},'
        html_content += f'"categories": {self._escape_js_string(quiz_data["categories"])},'
        html_content += f'"correct_mapping": {self._escape_js_string(quiz_data["correct_mapping"])},'
        html_content += f'"explanation": {self._escape_js_string(quiz_data.get("explanation", ""))}'
        html_content += '};'
        html_content += '</script>'

    def add_multiple_choice_quiz(self, quiz_data: Dict[str, Any]):
        """
        複数選択クイズを追加
        
        Args:
            quiz_data: クイズデータの辞書
        """
        quiz_id = quiz_data.get('quiz_id', quiz_data.get('id', 'multiple-choice-quiz'))
        
        html_content = f'<div class="quiz-container multiple-choice-quiz" data-quiz-id="{quiz_id}">'
        html_content += f'<h3 class="quiz-title">クイズ</h3>'
        html_content += f'<p class="quiz-question"><strong>問題:</strong> {quiz_data["question"]}</p>'
        html_content += f'<div class="quiz-options">'
        
        for i, option in enumerate(quiz_data['options']):
            html_content += f'<label class="option-label"><input type="checkbox" name="{quiz_id}" value="{i}"><span class="option-text">{option}</span></label><br>'
        
        html_content += f'</div>'
        html_content += f'<button class="check-multiple-choice" onclick="checkMultipleChoice(\'{quiz_id}\')">回答をチェック</button>'
        html_content += f'<div class="multiple-choice-result"></div>'
        html_content += f'</div>'
        
        html_content += '<script>'
        html_content += 'window.quizData = window.quizData || { quizzes: {} };'
        html_content += f'window.quizData.quizzes["{quiz_id}"] = {{'
        html_content += '"type": "multiple-choice",'
        html_content += f'"question": {self._escape_js_string(quiz_data["question"])},'
        html_content += f'"options": {self._escape_js_string(quiz_data["options"])},'
        html_content += f'"correct": {self._escape_js_string(quiz_data["correct"])},'
        html_content += f'"explanation": {self._escape_js_string(quiz_data.get("explanation", ""))}'
        html_content += '};'
        html_content += '</script>'

    def add_exercise_question(self, question_data: Dict[str, Any]):
        """
        演習問題を追加
        
        Args:
            question_data: 演習問題のデータ
        """
        question_id = question_data.get('id', 'exercise-question')
        self.content_buffer.append(f'<div class="exercise-question" data-exercise-id="{question_id}">'
                                   f'<h3>演習問題</h3>'
                                   f'<p>{question_data["question"]}</p>'
                                   f'<div class="exercise-answer" style="display:none;">'
                                   f'<h4>解答</h4>'
                                   f'<p>{question_data["answer"]}</p>'
                                   f'</div>'
                                   f'<button onclick="this.nextElementSibling.style.display = this.nextElementSibling.style.display === \'none\' ? \'block\' : \'none\';">解答を表示/非表示</button>'
                                   f'</div>')
        self.content_buffer.append("")

    def add_code_block_with_static_output(self, code: str, output: str, lang: str = "python", output_label: str = "実行結果"):
        """
        コードブロックと静的な実行結果を追加
        
        Args:
            code: コード文字列
            output: 実行結果文字列
            lang: コードの言語
            output_label: 実行結果のラベル
        """
        self.add_code_block(code, lang)
        self.add_admonition("info", output_label, output)

    def add_summary_section(self, title: str, points: List[str]):
        """
        要点まとめセクションを追加
        
        Args:
            title: セクションのタイトル
            points: 要点のリスト
        """
        self.add_heading(title, 2)
        self.add_unordered_list(points)

    def add_recommendation_section(self, title: str, items: List[Dict[str, str]]):
        """
        関連資料セクションを追加
        
        Args:
            title: セクションのタイトル
            items: 資料のリスト (title, url)
        """
        self.add_heading(title, 2)
        for item in items:
            # 'title'/'url' または 'text'/'link' の両方の形式をサポート
            title = item.get("title", item.get("text", ""))
            url = item.get("url", item.get("link", ""))
            self.add_paragraph(f"- [{title}]({url})")

    def add_faq_item(self, question: str, answer: str, collapsible: bool = False):
        """
        FAQ項目をAdmonitionとして追加
        
        Args:
            question: 質問
            answer: 回答
            collapsible: 折りたたみ可能にするか
        """
        self.add_admonition("question", question, answer, collapsible)

    def add_tip_item(self, title: str, content: str, collapsible: bool = False):
        """
        TIPS項目をAdmonitionとして追加
        
        Args:
            title: TIPSのタイトル
            content: TIPSの内容
            collapsible: 折りたたみ可能にするか
        """
        self.add_admonition("tip", title, content, collapsible)

    def add_mermaid_block(self, graph_string: str, title: Optional[str] = None):
        """
        Mermaid図を追加
        
        Args:
            graph_string: Mermaidグラフ定義文字列
            title: 図のタイトル（オプション）
        """
        if title:
            self.content_buffer.append(f'```mermaid title="{title}"')
        else:
            self.content_buffer.append('```mermaid')
        self.content_buffer.append(graph_string)
        self.content_buffer.append('```')
        self.content_buffer.append("")

    def add_feedback_form(self, form_url: str, title: str = "フィードバック"):
        """
        フィードバックフォームを追加
        
        Args:
            form_url: フォームのURL
            title: フォームのタイトル
        """
        self.add_admonition("info", title, 
                           f"この章についてのご意見・ご質問がございましたら、[こちらのフォーム]({form_url})からお聞かせください。",
                           collapsible=True)
    
    def add_learning_tracker(self, content_id: str, content_type: str = "page", 
                           user_id: str = "anonymous") -> None:
        """
        学習行動追跡のJavaScriptコードを追加
        
        Args:
            content_id: コンテンツID (章IDなど)
            content_type: コンテンツの種類
            user_id: ユーザーID
        """
        tracking_script = f'''
<script>
// 学習行動追跡スクリプト
(function() {{
    const contentId = '{content_id}';
    const contentType = '{content_type}';
    const userId = localStorage.getItem('learning_user_id') || '{user_id}';
    
    // ユーザーIDをlocalStorageに保存
    if (!localStorage.getItem('learning_user_id')) {{
        localStorage.setItem('learning_user_id', userId);
    }}
    
    // ページ表示イベントを記録
    window.addEventListener('load', function() {{
        logLearningEvent({{
            user_id: userId,
            event_type: 'page_view',
            content_id: contentId,
            timestamp: new Date().toISOString(),
            metadata: {{
                content_type: contentType,
                user_agent: navigator.userAgent,
                viewport: {{
                    width: window.innerWidth,
                    height: window.innerHeight
                }}
            }}
        }});
    }});
    
    // 滞在時間を追跡
    let startTime = Date.now();
    let isActive = true;
    
    // ページがアクティブか非アクティブかを追跡
    document.addEventListener('visibilitychange', function() {{
        if (document.hidden) {{
            isActive = false;
        }} else {{
            isActive = true;
            startTime = Date.now(); // タイマーをリセット
        }}
    }});
    
    // ページ離脱時に滞在時間を記録
    window.addEventListener('beforeunload', function() {{
        if (isActive) {{
            const duration = (Date.now() - startTime) / 1000 / 60; // 分単位
            logLearningEvent({{
                user_id: userId,
                event_type: 'time_spent',
                content_id: contentId,
                timestamp: new Date().toISOString(),
                metadata: {{
                    duration_minutes: duration,
                    content_type: contentType
                }}
            }});
        }}
    }});
    
    // 学習イベントをログに記録する関数
    function logLearningEvent(event) {{
        // localStorageにイベントを保存 (簡略実装)
        const events = JSON.parse(localStorage.getItem('learning_events') || '[]');
        events.push(event);
        
        // 最大500件まで保存
        if (events.length > 500) {{
            events.shift(); // 古いイベントを削除
        }}
        
        localStorage.setItem('learning_events', JSON.stringify(events));
        
        // コンソールにログ出力 (開発用)
        console.log('学習イベント:', event);
    }}
    
    // グローバル関数として公開 (クイズなどから使用するため)
    window.logLearningEvent = logLearningEvent;
}})();
</script>
        '''
        self.content_buffer.append(tracking_script)
    
    def add_progress_indicator(self, current_progress: float, total_sections: int, 
                             section_progress: List[bool] = None) -> None:
        """
        学習進捗インジケーターを追加
        
        Args:
            current_progress: 現在の進捗率 (0.0-1.0)
            total_sections: 全セクション数
            section_progress: 各セクションの完了状況
        """
        progress_percent = int(current_progress * 100)
        progress_html = f'''
<div class="learning-progress-container" style="
    margin: 20px 0;
    padding: 15px;
    background: #f8f9fa;
    border-radius: 8px;
    border: 1px solid #e9ecef;
">
    <div class="progress-header" style="
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
    ">
        <h4 style="margin: 0; color: #495057;">📈 学習進捗</h4>
        <span style="font-weight: bold; color: #28a745;">{progress_percent}% 完了</span>
    </div>
    <div class="progress-bar-container" style="
        width: 100%;
        height: 20px;
        background-color: #e9ecef;
        border-radius: 10px;
        overflow: hidden;
    ">
        <div class="progress-bar" style="
            height: 100%;
            background: linear-gradient(90deg, #28a745, #20c997);
            width: {progress_percent}%;
            transition: width 0.3s ease;
        "></div>
    </div>
    <div class="section-indicators" style="
        display: flex;
        justify-content: space-between;
        margin-top: 10px;
        flex-wrap: wrap;
    ">
        '''
        
        if section_progress:
            for i, completed in enumerate(section_progress):
                status_icon = "✓" if completed else "○"
                color = "#28a745" if completed else "#6c757d"
                progress_html += f'''
        <span style="
            color: {color};
            font-size: 14px;
            margin: 2px;
        ">{status_icon} 第{i+1}章</span>'''
        else:
            completed_sections = int(current_progress * total_sections)
            for i in range(total_sections):
                status_icon = "✓" if i < completed_sections else "○"
                color = "#28a745" if i < completed_sections else "#6c757d"
                progress_html += f'''
        <span style="
            color: {color};
            font-size: 14px;
            margin: 2px;
        ">{status_icon} 第{i+1}章</span>'''
        
        progress_html += '''
    </div>
</div>
        '''
        
        self.content_buffer.append(progress_html)
    
    def add_learning_recommendations(self, recommendations: List[str]) -> None:
        """
        学習推奨コンテンツを追加
        
        Args:
            recommendations: 推奨コンテンツのリスト
        """
        if not recommendations:
            return
        
        recommendation_text = "あなたの学習状況に基づいて、以下のコンテンツを推奨します：\n\n"
        
        for i, rec in enumerate(recommendations[:5]):  # 最大5個まで
            recommendation_text += f"{i+1}. {rec}\n"
        
        self.add_admonition(
            "tip", 
            "🎯 あなたへのオススメ", 
            recommendation_text,
            collapsible=True
        )
    
    def add_difficulty_adjustment_notice(self, difficulty_level: str, 
                                        show_additional_help: bool = False) -> None:
        """
        難易度調整の通知を追加
        
        Args:
            difficulty_level: 難易度レベル (beginner/standard/advanced)
            show_additional_help: 追加ヘルプを表示するか
        """
        if difficulty_level == "beginner":
            icon = "🔰"
            title = "初心者向けモード"
            message = "このコンテンツはあなたの学習状況に合わせて、より丁寧な説明と追加の例を表示しています。"
        elif difficulty_level == "advanced":
            icon = "🚀"
            title = "上級者向けモード"
            message = "このコンテンツはあなたの理解度に合わせて、発展的なトピックも含まれています。"
        else:
            return  # standardの場合は表示しない
        
        self.add_admonition("note", f"{icon} {title}", message)
        
        if show_additional_help and difficulty_level == "beginner":
            help_html = '''
<details style="margin: 10px 0; padding: 10px; background: #fff3cd; border-radius: 5px;">
    <summary style="cursor: pointer; font-weight: bold;">📚 追加ヘルプが必要ですか？</summary>
    <div style="margin-top: 10px;">
        <p>この内容が難しいと感じたら、以下を試してみてください：</p>
        <ul>
            <li>🔄 前の章を復習する</li>
            <li>📝 用語集で重要な用語を確認する</li>
            <li>🤔 理解できない点をメモしておく</li>
            <li>💬 フィードバックフォームで質問する</li>
        </ul>
    </div>
</details>
            '''
            self.content_buffer.append(help_html)

"""
テスト資料用の専門用語、FAQ、TIPSデータ
coreの専門用語管理機能をテストするためのダミーデータ
"""

from src.core.knowledge_manager import Term, FaqItem, TipItem

# テスト用専門用語リスト
TEST_TERMS = [
    Term(
        term="MkDocs",
        definition="Pythonベースの静的サイトジェネレータ。Markdownファイルから美しいドキュメントサイトを生成する。",
        category="基本ツール",
        related_terms=["Markdown", "静的サイトジェネレータ"],
        first_chapter="第1章",
        context_snippets=[
            "MkDocsは設定が簡単で、すぐに使い始められます。",
            "MkDocs Materialテーマを使用すると、より洗練されたデザインになります。"
        ]
    ),
    Term(
        term="Markdown",
        definition="軽量マークアップ言語の一つ。プレーンテキストで記述し、HTMLに変換できる。",
        category="基本ツール",
        related_terms=["MkDocs", "HTML"],
        first_chapter="第1章",
        context_snippets=[
            "Markdownは読みやすく書きやすい記法です。",
            "# 見出し1、## 見出し2のように記述します。"
        ]
    ),
    Term(
        term="ツールチップ",
        definition="要素にマウスオーバーした際に表示される小さな説明ウィンドウ。",
        category="UI要素",
        related_terms=["ホバー", "ポップアップ"],
        first_chapter="第2章",
        context_snippets=[
            "ツールチップを使うと、追加情報を省スペースで提供できます。"
        ]
    ),
    Term(
        term="静的サイトジェネレータ",
        definition="事前にHTMLファイルを生成し、サーバーでの動的な処理を必要としないWebサイトを作成するツール。",
        category="基本ツール",
        related_terms=["MkDocs", "Hugo", "Jekyll"],
        first_chapter="第1章"
    ),
    Term(
        term="インタラクティブ図表",
        definition="ユーザーの操作に応じて動的に変化する図表。ホバー、クリック、ドラッグなどの操作が可能。",
        category="ビジュアライゼーション",
        related_terms=["Plotly", "D3.js"],
        first_chapter="第3章"
    ),
    Term(
        term="Plotly",
        definition="Pythonで美しいインタラクティブな図表を作成できるライブラリ。",
        category="ライブラリ",
        related_terms=["インタラクティブ図表", "データビジュアライゼーション"],
        first_chapter="第3章"
    ),
    Term(
        term="HTMLエスケープ",
        definition='HTMLで特殊な意味を持つ文字（<, >, ", &など）を文字実体参照に変換すること。',
        category="Web技術",
        related_terms=["セキュリティ", "XSS"],
        first_chapter="第2章",
        context_snippets=[
            'HTMLエスケープにより、"<script>"のような文字列を安全に表示できます。'
        ]
    ),
    Term(
        term="レスポンシブデザイン",
        definition="画面サイズに応じて自動的にレイアウトが調整されるデザイン手法。",
        category="UI/UX",
        related_terms=["CSS", "メディアクエリ"],
        first_chapter="第3章"
    )
]

# テスト用FAQリスト
TEST_FAQ_ITEMS = [
    FaqItem(
        question="MkDocsとSphinxの違いは何ですか？",
        answer="MkDocsはMarkdownベースでシンプルな設定が特徴です。一方、SphinxはreStructuredTextを使用し、より複雑なドキュメント構造に対応できます。",
        category="基本概念"
    ),
    FaqItem(
        question="ツールチップが表示されません。どうすればよいですか？",
        answer="MkDocs Materialテーマの`content.tooltips`機能が有効になっているか確認してください。また、`attr_list`と`abbr`拡張機能も必要です。",
        category="トラブルシューティング"
    ),
    FaqItem(
        question="図表のサイズを調整するにはどうすればよいですか？",
        answer="ChartGeneratorの`figsize`パラメータで調整できます。また、HTMLに埋め込む際の`width`と`height`属性でも制御可能です。",
        category="カスタマイズ"
    ),
    FaqItem(
        question="日本語フォントが文字化けします。",
        answer="Matplotlibの日本語フォント設定を確認してください。`japanize-matplotlib`パッケージをインストールするか、手動でフォントを設定する必要があります。",
        category="トラブルシューティング"
    ),
    FaqItem(
        question="生成されたサイトをGitHub Pagesで公開できますか？",
        answer="はい、可能です。`mkdocs gh-deploy`コマンドを使用すると、自動的にGitHub Pagesにデプロイされます。",
        category="デプロイメント"
    )
]

# テスト用TIPSリスト
TEST_TIP_ITEMS = [
    TipItem(
        title="Markdownの効率的な書き方",
        content="VSCodeなどのエディタでMarkdownプレビュー機能を使用すると、リアルタイムで結果を確認しながら執筆できます。",
        category="執筆のコツ"
    ),
    TipItem(
        title="図表の最適化",
        content="Web表示用の図表は、DPIを150程度に設定し、ファイルサイズと品質のバランスを取ることをお勧めします。",
        category="パフォーマンス"
    ),
    TipItem(
        title="用語の一貫性を保つ",
        content="KnowledgeManagerを活用して専門用語を一元管理することで、資料全体で用語の定義と表記を統一できます。",
        category="品質管理"
    ),
    TipItem(
        title="インタラクティブ要素の適切な使用",
        content="すべての図表をインタラクティブにする必要はありません。ユーザーが操作する価値がある場合にのみ使用しましょう。",
        category="UI/UX"
    ),
    TipItem(
        title="mkdocs serveの活用",
        content="`mkdocs serve`コマンドを使用すると、ローカルでサイトをプレビューでき、ファイルの変更が自動的に反映されます。",
        category="開発効率"
    )
]
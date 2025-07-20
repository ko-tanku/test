"""
フォント設定の確認とセットアップ
"""

import sys
import platform
from matplotlib import font_manager

def check_meiryo_font():
    """メイリオフォントの存在確認"""
    print("フォント確認を開始します...")
    
    # 利用可能なフォントを取得
    available_fonts = set([f.name for f in font_manager.fontManager.ttflist])
    
    # メイリオフォントの確認
    meiryo_found = False
    for font in ['Meiryo', 'メイリオ']:
        if font in available_fonts:
            meiryo_found = True
            print(f"✓ メイリオフォント '{font}' が見つかりました。")
            break
    
    if not meiryo_found:
        print("\n✗ エラー: メイリオフォントが見つかりません。")
        print("\nメイリオフォントのインストール方法:")
        
        os_type = platform.system()
        if os_type == "Windows":
            print("- Windows: 通常はプリインストールされています。")
            print("  もし見つからない場合は、コントロールパネルからフォントを確認してください。")
        elif os_type == "Darwin":  # macOS
            print("- macOS: 以下の手順でインストールしてください：")
            print("  1. Microsoft Office for Macをインストール（メイリオが含まれます）")
            print("  2. または、Windows PCからメイリオフォントファイルをコピー")
        else:  # Linux
            print("- Linux: 以下の手順でインストールしてください：")
            print("  1. Windows PCからメイリオフォントファイル（.ttf）をコピー")
            print("  2. ~/.fonts/ または /usr/share/fonts/ に配置")
            print("  3. fc-cache -fv コマンドでフォントキャッシュを更新")
        
        return False
    
    # その他の利用可能な日本語フォントを表示
    print("\nその他の利用可能な日本語フォント:")
    japanese_fonts = ['Yu Gothic', 'Hiragino', 'Takao', 'IPA']
    for font in available_fonts:
        for jp_font in japanese_fonts:
            if jp_font in font:
                print(f"  - {font}")
                break
    
    return True


if __name__ == "__main__":
    print("MkDocs学習資料生成システム - フォント設定確認")
    print("=" * 50)
    
    if check_meiryo_font():
        print("\n✓ フォント設定の確認が完了しました。")
        print("システムを使用する準備ができています。")
        sys.exit(0)
    else:
        print("\n✗ フォント設定に問題があります。")
        print("上記の手順に従ってメイリオフォントをインストールしてください。")
        sys.exit(1)
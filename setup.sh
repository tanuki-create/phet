#!/bin/bash

# TikTok カルーセル投稿自動作成ツール セットアップスクリプト
# Mac環境用

echo "🚀 TikTok カルーセル投稿自動作成ツール セットアップ開始"

# Python バージョン確認
python_version=$(python3 --version 2>&1)
if [[ $? -ne 0 ]]; then
    echo "❌ Python3 がインストールされていません。"
    echo "Homebrewを使用してインストールしてください:"
    echo "brew install python3"
    exit 1
fi

echo "✅ Python 確認: $python_version"

# 仮想環境作成
if [ ! -d "venv" ]; then
    echo "📦 仮想環境を作成しています..."
    python3 -m venv venv
fi

# 仮想環境アクティベート
source venv/bin/activate

# 依存関係インストール
echo "📚 依存関係をインストールしています..."
pip install --upgrade pip
pip install -r requirements.txt

# 実行権限付与
chmod +x make_carousel.py

echo "🎉 セットアップ完了！"
echo ""
echo "次のステップ:"
echo "1. input/ ディレクトリに画像を配置"
echo "2. input/texts.json を編集"
echo "3. fonts/ ディレクトリに日本語フォントを配置"
echo "4. 以下のコマンドで実行:"
echo ""
echo "   source venv/bin/activate"
echo "   python make_carousel.py --img_dir input --text_json input/texts.json --font_path fonts/NotoSansJP-Regular.otf"
echo ""
echo "詳しい使用方法は README.md を参照してください。" 
#!/bin/bash

# TikTok カルーセル投稿自動作成ツール 実行スクリプト

# 仮想環境をアクティベート
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "❌ 仮想環境が見つかりません。setup.sh を実行してください。"
    exit 1
fi

# デフォルトパラメータ
IMG_DIR="input"
TEXT_JSON="input/texts.json"
FONT_PATH="fonts/NotoSansJP-Regular.otf"
OUT_DIR="output"

# macOS標準フォントを使用する場合（フォントファイルがない場合）
if [ ! -f "$FONT_PATH" ]; then
    echo "⚠️  フォントファイルが見つかりません: $FONT_PATH"
    echo "macOS標準フォント（ヒラギノ角ゴシック）を使用します。"
    FONT_PATH="/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc"
fi

echo "🎬 カルーセル画像を生成しています..."
echo "📁 画像ディレクトリ: $IMG_DIR"
echo "📝 テキスト設定: $TEXT_JSON"
echo "🔤 フォント: $FONT_PATH"
echo "📤 出力ディレクトリ: $OUT_DIR"
echo ""

# カルーセル生成実行
python make_carousel.py \
    --img_dir "$IMG_DIR" \
    --text_json "$TEXT_JSON" \
    --font_path "$FONT_PATH" \
    --out_dir "$OUT_DIR"

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 カルーセル画像の生成が完了しました！"
    echo "📁 生成された画像は $OUT_DIR/ ディレクトリを確認してください。"
    echo ""
    echo "次のステップ:"
    echo "1. Finderで $OUT_DIR/ ディレクトリを開く"
    echo "2. TikTokアプリを開く"
    echo "3. 投稿画面で画像を選択"
    echo "4. カルーセル投稿を作成"
else
    echo "❌ エラーが発生しました。エラーメッセージを確認してください。"
fi 
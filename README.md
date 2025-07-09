# TikTok カルーセル投稿自動作成ツール

素材画像とテキストを組み合わせて、TikTokのカルーセル投稿用画像を自動生成するツールです。

## 特徴

- ✨ **フォントサイズ自動調整**: テキストが長すぎてはみ出す場合、自動でフォントを縮小
- 📂 **フォルダ自動整理**: 生成ごとに`output/`と`archive/`内にタイムスタンプ付きフォルダを自動作成し、ファイルを整理
- 🎯 **TikTok最適化**: 9:16 (1080x1920) サイズで自動リサイズ
- 🎨 **柔軟なカスタマイズ**: フォント、色、サイズ、位置を自由に設定
- 🗄️ **自動アーカイブ**: 処理済みの画像は `archive/` フォルダに自動で移動
- 🚀 **バッチ処理**: 複数枚の画像を一括生成
- 🔤 **日本語対応**: 日本語テキストの表示に対応
- 📱 **Mac対応**: macOS環境で動作確認済み

## インストール

### 1. 必要なソフトウェア
- Python 3.8 以上
- pip (Pythonパッケージマネージャー)

### 2. 依存関係のインストール
```bash
pip install -r requirements.txt
```

## 使用方法

### 1. 基本的な使い方

```bash
python make_carousel.py \
  --img_dir input \
  --text_json input/texts.json \
  --font_path fonts/NotoSansJP-Regular.otf \
  --out_dir output
```

### 2. 画像の準備

`input/` ディレクトリに素材画像を配置してください：

```
input/
├── 01.jpg
├── 02.png
├── 03.jpg
└── texts.json
```

(注: 処理が成功した画像とテキスト設定ファイルは、`archive/[タイムスタンプ]` フォルダに移動されます)

### 3. テキスト設定ファイル

`input/texts.json` でテキストの設定を行います：

```json
[
  {
    "text": "１行目のテキスト\\n２行目のテキスト",
    "font_size": 120,
    "color": "#FFFFFF",
    "stroke_width": 8,
    "stroke_fill": "#000000",
    "position": "center"
  },
  {
    "text": "サブタイトル",
    "font_size": 90,
    "color": "#FFD700",
    "stroke_width": 6,
    "stroke_fill": "#000000",
    "position": "top"
  }
]
```

(注: `\\n` を使うと、テキスト内で改行できます)

### 4. 設定オプション

| パラメータ | 説明 | デフォルト値 |
|-----------|------|-------------|
| `text` | 表示するテキスト | 必須 |
| `font_size` | フォントサイズ | 100 |
| `color` | 文字色 (16進数) | #FFFFFF |
| `stroke_width` | 縁取りの太さ | 5 |
| `stroke_fill` | 縁取りの色 | #000000 |
| `position` | テキストの位置 | center |

### 5. 位置指定オプション

- `center`: 中央
- `top`: 上部中央
- `bottom`: 下部中央
- `top-left`: 左上
- `top-right`: 右上
- `bottom-left`: 左下
- `bottom-right`: 右下
- `x,y`: 具体的な座標指定 (例: "100,200")

## フォントについて

### 日本語フォントの取得

1. Google Fonts から Noto Sans JP をダウンロード:
   - https://fonts.google.com/noto/specimen/Noto+Sans+JP
   
2. `fonts/` ディレクトリに配置:
   ```
   fonts/
   └── NotoSansJP-Regular.otf
   ```

### macOS システムフォントの使用

macOS標準のフォントも使用できます：

```bash
# ヒラギノ角ゴシックを使用する場合
python make_carousel.py \
  --font_path "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc" \
  --img_dir input \
  --text_json input/texts.json
```

### 英語テキストのフォント設定例

英語のテキストをメインに使う場合は、視認性が高く、インパクトのあるフォントがおすすめです。

**おすすめのGoogleフォント:**
- **Montserrat**: モダンで読みやすい
- **Poppins**: 親しみやすく、丸みがある
- **Oswald / Bebas Neue**: 縦長でインパクトの強い見出し向け

**スタイル設定のヒント:**
- **色**: 基本は白 (`#FFFFFF`)
- **縁取り**: 必ず設定しましょう。黒 (`#000000`) の縁取りが可読性を大きく向上させます。
- **太さ**: フォントサイズの5-8%がおすすめです (`font_size: 100` なら `stroke_width: 8`)

`input/texts-en.json` にサンプル設定を用意しています。利用する際は、実行スクリプトの `--text_json` の値を変更してください。

## 例：学習法カルーセルの作成

1. 画像を準備（6枚）
2. `input/texts.json` を編集
3. 実行：
   ```bash
   python make_carousel.py \
     --img_dir input \
     --text_json input/texts.json \
     --font_path fonts/NotoSansJP-Regular.otf
   ```
4. `output/` ディレクトリに生成された画像を確認
5. TikTokアプリで画像を選択してカルーセル投稿

## トラブルシューティング

### よくある問題

1. **Pillowがインストールできない**
   ```bash
   pip install --upgrade pip
   pip install pillow
   ```

2. **フォントが見つからない**
   - フォントファイルのパスを確認
   - デフォルトフォントで実行される

3. **画像とテキストの数が合わない**
   - 画像ファイル数とJSONエントリ数を確認
   - ファイル名の順序を確認

4. **画像が読み込めない**
   - 対応形式: JPG, PNG, BMP, TIFF
   - ファイル名に日本語が含まれていないか確認

## ライセンス

MIT License

## 作者

カルーセル投稿自動作成ツール 
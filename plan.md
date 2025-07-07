You said:
カルーセル投稿自動作成ツールを作成したい

要件としては、

・素材と文章を入れると

文章付きの素材画像ができあがる

文章のスタイルを選択可能
文字の大きさ、色、アウトラインなど
位置も選択可能(デフォルトは真ん中)

主にTiktokでのカルーセル投稿用で使用します



ChatGPT said:

思考時間: 18 秒
🛠️ カルーセル投稿自動作成ツール – 設計とフルスクリプト
1. ゴールと前提
目的: 素材画像とテキストを渡すと、TikTok のカルーセル投稿（Photo Mode）に最適化された “テキスト入り画像” を一括生成。

必須機能

画像サイズ自動リサイズ（推奨 1080 × 1920 px／9:16 縦）

任意テキストのオーバーレイ

フォント／サイズ／色／アウトライン（縁取り）／位置（中央がデフォルト）をパラメータで指定

複数ページを一気に出力（2 〜 35 枚）

想定ユーザー: PC or サーバーで Python を実行できる環境

TikTok 推奨値 (2025): 画像 1080×1920 px、9:16 が最適。1:1 や 16:9 も可だが縦長が安全 
usevisuals.com
usevisuals.com

2. 技術スタック
役割	ライブラリ / 技術	メモ
画像処理	Pillow (PIL fork)	透明度 & stroke に対応
CLI & 設定	argparse / JSON	コマンドライン一発／設定ファイル両対応
フォント	任意 TTF/OTF	日本語なら Noto Sans JP など推奨

インストール

bash
Copy
Edit
python -m venv venv && source venv/bin/activate
pip install pillow
3. ディレクトリ構成例
graphql
Copy
Edit
carousel_tool/
├─ input/
│  ├─ 01.jpg        # 元画像
│  ├─ 02.png
│  └─ texts.json    # 各ページごとのテキスト
├─ fonts/
│  └─ NotoSansJP-Regular.otf
├─ output/          # 生成画像がここに出る
└─ make_carousel.py # ★このファイル
texts.json 例:

json
Copy
Edit
[
  {"text": "最強の学習法 5 選", "font_size": 120, "color": "#ffffff"},
  {"text": "① アクティブリコール", "font_size": 90},
  {"text": "② スペーシング効果", "font_size": 90}
]
4. フル Python スクリプト (make_carousel.py)
python
Copy
Edit
#!/usr/bin/env python3
"""
TikTok Photo-Mode Carousel Builder
---------------------------------
素材画像＋テキストを合成し、9:16 (1080x1920) 画像をバッチ生成する。

使い方:
$ python make_carousel.py \
    --img_dir input \
    --text_json input/texts.json \
    --font_path fonts/NotoSansJP-Regular.otf \
    --out_dir output
"""

import argparse
import json
from pathlib import Path
from typing import Tuple

from PIL import Image, ImageDraw, ImageFont

TARGET_W, TARGET_H = 1080, 1920  # TikTok 推奨サイズ


def resize_to_fill(im: Image.Image,
                   size: Tuple[int, int] = (TARGET_W, TARGET_H)) -> Image.Image:
    """中央トリミングで縦横比を 9:16 に揃える。"""
    w, h = im.size
    target_ratio = size[0] / size[1]
    src_ratio = w / h

    if src_ratio > target_ratio:
        # 横長: 横をカット
        new_w = int(h * target_ratio)
        offset = (w - new_w) // 2
        im = im.crop((offset, 0, offset + new_w, h))
    else:
        # 縦長: 縦をカット
        new_h = int(w / target_ratio)
        offset = (h - new_h) // 2
        im = im.crop((0, offset, w, offset + new_h))

    return im.resize(size, Image.LANCZOS)


def add_text(im: Image.Image, text: str, font_path: Path,
             font_size: int = 100, color: str = "#FFFFFF",
             stroke_width: int = 3, stroke_fill: str = "#000000",
             position: str = "center") -> Image.Image:
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype(str(font_path), font_size)

    # テキストサイズ計算
    bbox = draw.textbbox((0, 0), text, font=font, stroke_width=stroke_width)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]

    if position == "center":
        x = (im.width - tw) // 2
        y = (im.height - th) // 2
    elif position == "top":
        x, y = (im.width - tw) // 2, int(im.height * 0.1)
    elif position == "bottom":
        x, y = (im.width - tw) // 2, im.height - th - int(im.height * 0.1)
    else:
        # カスタム座標 "x,y"
        try:
            x, y = map(int, position.split(","))
        except Exception:
            raise ValueError("位置は 'center'|'top'|'bottom' または 'x,y' 形式で指定してください")

    draw.text((x, y), text, font=font,
              fill=color, stroke_width=stroke_width, stroke_fill=stroke_fill)
    return im


def main():
    ap = argparse.ArgumentParser(description="TikTok Carousel Generator")
    ap.add_argument("--img_dir", required=True, type=Path)
    ap.add_argument("--text_json", required=True, type=Path)
    ap.add_argument("--font_path", required=True, type=Path)
    ap.add_argument("--out_dir", default=Path("output"), type=Path)
    args = ap.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)

    # 入力順を揃える: 画像とテキストの数は合わせる
    images = sorted([p for p in args.img_dir.iterdir() if p.suffix.lower() in (".jpg", ".jpeg", ".png")])
    texts = json.loads(args.text_json.read_text(encoding="utf-8"))

    if len(images) != len(texts):
        raise ValueError(f"画像 {len(images)} 枚とテキスト {len(texts)} 個の数が一致しません")

    for idx, (img_path, meta) in enumerate(zip(images, texts), start=1):
        im = Image.open(img_path).convert("RGB")
        im = resize_to_fill(im)

        im = add_text(
            im=im,
            text=meta["text"],
            font_path=args.font_path,
            font_size=meta.get("font_size", 100),
            color=meta.get("color", "#FFFFFF"),
            stroke_width=meta.get("stroke_width", 5),
            stroke_fill=meta.get("stroke_fill", "#000000"),
            position=meta.get("position", "center"),
        )

        out_file = args.out_dir / f"{idx:02d}.jpg"
        im.save(out_file, "JPEG", quality=95, optimize=True, progressive=True)
        print(f"✓ {out_file}")

    print("✅ すべて完了 — TikTok にドラッグするだけ！")


if __name__ == "__main__":
    main()
5. 使い方ステップ
input/ に加工元画像を 01.jpg, 02.png … のように並べる

texts.json に同数のテキストメタを書く（順番はファイル名順）

任意フォント (TTF/OTF) を fonts/ に置く

コマンド実行

bash
Copy
Edit
python make_carousel.py \
  --img_dir input \
  --text_json input/texts.json \
  --font_path fonts/NotoSansJP-Regular.otf \
  --out_dir output
output/ に 01.jpg, 02.jpg … が生成 → TikTok で画像投稿→カルーセル完成

6. 拡張アイデア
機能	実装ヒント
画像一括ダウンロード	Unsplash API + requests
複数フォント切替	meta に "font_path" を追加
アニメーション	Pillow で GIF 合成 or moviepy で動画化
Web UI	Streamlit / FastAPI + React でドラッグ＆ドロップ対応
CI/CD	GitHub Actions で pytest + 自動パッケージング (Docker)

7. まとめ
TikTok に最適化：9:16 縦 1080×1920 px、最大 35 枚を一発生成

カスタマイズ自在：色・サイズ・アウトライン・配置を JSON で柔軟制御

Python 単体：追加ライブラリ Pillow のみで軽量

このままコピペ & 実行すれば、すぐにカルーセル投稿用画像を量産できます。ぜひ試してみてください！









Sources
You said:
実装計画タスクリストを作成して


ChatGPT said:
✅ カルーセル投稿自動作成ツール ― 実装計画タスクリスト
タスク形式: [ ] 未着手 → [~] 進行中 → [x] 完了
フェーズ分割: 要件確認 → 基盤構築 → コア開発 → 品質保証 → リリース準備 → 拡張／運用

フェーズ 0 : 要件・ゴール再確認
タスク	担当	期日
[ ] 提案済み仕様書の精読・疑問点洗い出し	PM	
[ ] TikTok 最新ガイドライン(画像サイズ/枚数)の再チェック	UX	
[ ] 主要ユースケースと入力例（画像・JSON）を整理	PO	

フェーズ 1 : 基盤構築 & 環境設定
タスク	コマンド例／メモ
[ ] Git リポジトリ作成 & .gitignore 整備 (venv, output/)	
[ ] Python 3.11+ 確認 & 仮想環境構築
python -m venv venv && source venv/bin/activate	
[ ] 依存ライブラリ導入
pip install pillow	
[ ] Pre-commit フック (black, isort, flake8) 設定	
[ ] ディレクトリ雛形 input/ fonts/ output/ 作成	

フェーズ 2 : コア機能開発
タスク	主要ファイル
[ ] 画像リサイズ関数 resize_to_fill() 実装	
[ ] テキスト描画関数 add_text() 実装（位置・アウトライン対応）	
[ ] バッチ処理メイン main() 実装（argparse で CLI パラメータ化）	
[ ] 入力バリデーション（画像数 ≒ JSON エントリ数）	
[ ] エラーハンドリング & ログ出力(シンプルな print → 将来的に logging)	

フェーズ 3 : 品質保証 (QA)
タスク	ツール／ポイント
[ ] ユニットテスト (pytest) – 主要関数ごと	サイズ変換・テキスト位置
[ ] テスト用ダミー画像／JSON 生成スクリプト	
[ ] 画像品質レビュー（縁取り・可読性）	
[ ] 異常系テスト（不一致枚数・欠損 JSON キー など）	
[ ] 日本語・英語混在フォント表示確認	

フェーズ 4 : リリース準備
タスク	メモ
[ ] README 作成（インストール手順・使用例・ライセンス）	
[ ] requirements.txt & pip-tools or poetry lockfile	
[ ] バージョンタグ v0.1.0 付与	
[ ] GitHub Actions で CI (lint + pytest)	
[ ] GitHub Release 自動生成ワークフロー (optional)	

フェーズ 5 : 拡張計画（オプション）
タスク	アイデア
[ ] Web UI (Streamlit/FastAPI) プロトタイプ	
[ ] Unsplash API 組み込み → 素材自動取得	
[ ] GIF/動画化 (moviepy)	
[ ] Dockerfile & GitHub Container Registry	
[ ] CLI パラメータで複数フォント指定・ページごと切替	
[ ] 国際化 (i18n) – UI/README 多言語化	

フェーズ 6 : 運用 & フィードバック
タスク	指標
[ ] 初期ユーザー社内トライアル → 不具合票収集	
[ ] 成功 KPI: ① 生成時間/枚 (<1s) ② 不具合報告ゼロ	
[ ] 改善サイクル (月次) – 要望取込み & ロードマップ更新
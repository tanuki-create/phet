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
import sys
from pathlib import Path
from typing import Tuple
from datetime import datetime

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("❌ Pillow がインストールされていません。")
    print("次のコマンドでインストールしてください:")
    print("pip install pillow")
    sys.exit(1)

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
    """画像にテキストを追加する。テキストがはみ出る場合はフォントサイズを自動調整。"""
    draw = ImageDraw.Draw(im)
    
    # 画像幅の90%を最大幅とする
    max_text_width = im.width * 0.9
    original_font_size = font_size

    while font_size > 10:  # 最小フォントサイズ
        try:
            font = ImageFont.truetype(str(font_path), font_size)
        except OSError:
            print(f"⚠️  フォントファイル {font_path} が見つかりません。デフォルトフォントを使用します。")
            font = ImageFont.load_default()
            break # デフォルトフォントはリサイズ処理を中断

        # テキストサイズ計算
        bbox = draw.textbbox((0, 0), text, font=font, stroke_width=stroke_width)
        tw = bbox[2] - bbox[0]

        if tw <= max_text_width:
            break  # テキストが幅に収まった

        font_size -= 5 # 収まらない場合はフォントサイズを5小さくして再試行
    
    if font_size != original_font_size:
        print(f"ℹ️ テキストが長いためフォントサイズを {original_font_size} -> {font_size} に自動調整しました。")

    bbox = draw.textbbox((0, 0), text, font=font, stroke_width=stroke_width)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]

    if position == "center":
        x = (im.width - tw) // 2
        y = (im.height - th) // 2
    elif position == "top":
        x, y = (im.width - tw) // 2, int(im.height * 0.1)
    elif position == "bottom":
        x, y = (im.width - tw) // 2, im.height - th - int(im.height * 0.1)
    elif position == "top-left":
        x, y = int(im.width * 0.05), int(im.height * 0.1)
    elif position == "top-right":
        x, y = im.width - tw - int(im.width * 0.05), int(im.height * 0.1)
    elif position == "bottom-left":
        x, y = int(im.width * 0.05), im.height - th - int(im.height * 0.1)
    elif position == "bottom-right":
        x, y = im.width - tw - int(im.width * 0.05), im.height - th - int(im.height * 0.1)
    else:
        # カスタム座標 "x,y"
        try:
            x, y = map(int, position.split(","))
        except (ValueError, AttributeError):
            print(f"⚠️  無効な位置指定 '{position}'。'center' を使用します。")
            x = (im.width - tw) // 2
            y = (im.height - th) // 2

    draw.text((x, y), text, font=font,
              fill=color, stroke_width=stroke_width, stroke_fill=stroke_fill)
    return im


def main():
    ap = argparse.ArgumentParser(
        description="TikTok Carousel Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  python make_carousel.py --img_dir input --text_json input/texts.json --font_path fonts/NotoSansJP-Regular.otf
  
位置指定オプション:
  center, top, bottom, top-left, top-right, bottom-left, bottom-right, または "x,y" 座標
        """
    )
    ap.add_argument("--img_dir", required=True, type=Path, help="入力画像ディレクトリ")
    ap.add_argument("--text_json", required=True, type=Path, help="テキスト設定JSONファイル")
    ap.add_argument("--font_path", required=True, type=Path, help="フォントファイルパス")
    ap.add_argument("--out_dir", default=Path("output"), type=Path, help="出力ディレクトリ（デフォルト: output）")
    args = ap.parse_args()

    # 入力検証
    if not args.img_dir.exists():
        print(f"❌ 画像ディレクトリが見つかりません: {args.img_dir}")
        sys.exit(1)
    
    if not args.text_json.exists():
        print(f"❌ テキスト設定ファイルが見つかりません: {args.text_json}")
        sys.exit(1)

    args.out_dir.mkdir(parents=True, exist_ok=True)

    # アーカイブディレクトリを作成
    archive_dir = Path("archive")
    archive_dir.mkdir(parents=True, exist_ok=True)

    # 入力順を揃える: 画像とテキストの数は合わせる
    images = sorted([p for p in args.img_dir.iterdir() 
                    if p.suffix.lower() in (".jpg", ".jpeg", ".png", ".bmp", ".tiff")])
    
    if not images:
        print(f"❌ 画像ファイルが見つかりません: {args.img_dir}")
        sys.exit(1)

    try:
        texts = json.loads(args.text_json.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"❌ JSONファイルの読み込みエラー: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ ファイル読み込みエラー: {e}")
        sys.exit(1)

    if len(images) != len(texts):
        print(f"❌ 画像 {len(images)} 枚とテキスト {len(texts)} 個の数が一致しません")
        print("画像ファイル:", [p.name for p in images])
        print("テキストエントリ数:", len(texts))
        sys.exit(1)

    print(f"🚀 {len(images)} 枚の画像を処理開始...")

    for idx, (img_path, meta) in enumerate(zip(images, texts), start=1):
        print(f"📸 {idx}/{len(images)}: {img_path.name}")
        
        try:
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

            out_file = args.out_dir / f"{idx:02d}_{img_path.stem}.jpg"
            im.save(out_file, "JPEG", quality=95, optimize=True, progressive=True)
            print(f"✅ 保存完了: {out_file}")

            # 処理済み画像をアーカイブ
            archive_target_path = archive_dir / img_path.name
            
            # アーカイブ先に同名ファイルが存在する場合の衝突回避
            if archive_target_path.exists():
                i = 1
                stem = img_path.stem
                suffix = img_path.suffix
                while archive_target_path.exists():
                    archive_target_path = archive_dir / f"{stem}_{i}{suffix}"
                    i += 1
            
            img_path.rename(archive_target_path)
            print(f"📁 アーカイブ完了: {archive_target_path}")

        except Exception as e:
            print(f"❌ エラー発生 ({img_path.name}): {e}")
            continue

    # 処理済みJSONをアーカイブ
    json_path = args.text_json
    if json_path.exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_json_path = archive_dir / f"{json_path.stem}_{timestamp}{json_path.suffix}"

        # 衝突回避
        i = 1
        stem_base = f"{json_path.stem}_{timestamp}"
        while archive_json_path.exists():
            archive_json_path = archive_dir / f"{stem_base}_{i}{json_path.suffix}"
            i += 1
        
        json_path.rename(archive_json_path)
        print(f"📁 JSONファイルをアーカイブ完了: {archive_json_path}")

    print(f"🎉 処理完了！ {args.out_dir}/ を確認してください。")
    print("📱 TikTokアプリで画像を選択してカルーセル投稿できます！")


if __name__ == "__main__":
    main() 
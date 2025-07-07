#!/usr/bin/env python3
"""
サンプル画像生成スクリプト
カルーセルツールのテスト用に6枚のサンプル画像を生成します。
"""

from PIL import Image, ImageDraw
import os

def create_sample_image(width, height, color, filename):
    """指定されたサイズと色でサンプル画像を作成"""
    img = Image.new('RGB', (width, height), color)
    draw = ImageDraw.Draw(img)
    
    # グラデーション効果
    for y in range(height):
        alpha = int(255 * (y / height))
        gradient_color = tuple(max(0, c - alpha // 3) for c in color)
        draw.line([(0, y), (width, y)], fill=gradient_color)
    
    # 簡単な図形を追加
    draw.ellipse([width//4, height//4, 3*width//4, 3*height//4], 
                outline=(255, 255, 255), width=5)
    
    img.save(filename)
    print(f"✅ {filename} を作成しました")

def main():
    print("🎨 サンプル画像を生成しています...")
    
    # input ディレクトリを確認
    os.makedirs("input", exist_ok=True)
    
    # 6枚のサンプル画像を作成
    colors = [
        (255, 99, 132),   # ピンク
        (54, 162, 235),   # ブルー
        (255, 206, 86),   # イエロー
        (75, 192, 192),   # グリーン
        (153, 102, 255),  # パープル
        (255, 159, 64),   # オレンジ
    ]
    
    for i, color in enumerate(colors, 1):
        filename = f"input/{i:02d}.jpg"
        create_sample_image(1200, 800, color, filename)
    
    print("🎉 サンプル画像の生成が完了しました！")
    print("次のステップ:")
    print("1. ./setup.sh を実行してセットアップ")
    print("2. ./run_carousel.sh を実行してカルーセル画像を生成")

if __name__ == "__main__":
    main() 
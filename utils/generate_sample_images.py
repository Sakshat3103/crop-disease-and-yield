"""
Sample Leaf Image Generator for AgriVision AI.
Generates realistic leaf demonstration images with distinct pathological lesions
for instant user and academic testing.
"""

import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SAMPLE_DIR = os.path.join(PROJECT_ROOT, "sample_images")


def create_base_leaf(width=500, height=500, leaf_type="oval"):
    """Create a healthy vibrant green leaf canvas with veins."""
    img = Image.new("RGB", (width, height), (245, 247, 250))
    draw = ImageDraw.Draw(img)
    
    if leaf_type == "oval":
        # Draw potato/tomato/apple style broad oval leaf
        draw.pieslice([80, 50, 420, 450], start=0, end=360, fill=(34, 139, 34))
        # Draw pointed tip
        draw.polygon([(250, 30), (220, 90), (280, 90)], fill=(34, 139, 34))
        # Midrib vein
        draw.line([(250, 40), (250, 460)], fill=(124, 252, 0), width=5)
        # Side veins
        for y in range(120, 420, 40):
            draw.line([(250, y), (140, y - 30)], fill=(124, 252, 0), width=2)
            draw.line([(250, y), (360, y - 30)], fill=(124, 252, 0), width=2)
            
    elif leaf_type == "linear":
        # Rice / Corn long blade
        draw.polygon([(220, 40), (280, 40), (330, 460), (170, 460)], fill=(46, 139, 87))
        draw.polygon([(250, 20), (220, 50), (280, 50)], fill=(46, 139, 87))
        # Parallel veins
        for x in [210, 230, 250, 270, 290]:
            draw.line([(x, 40), (x, 460)], fill=(144, 238, 144), width=2)
            
    return img


def generate_all_samples():
    os.makedirs(SAMPLE_DIR, exist_ok=True)
    np.random.seed(42)
    
    # 1. Healthy Leaf
    healthy = create_base_leaf(leaf_type="oval")
    healthy.save(os.path.join(SAMPLE_DIR, "healthy_leaf.png"))
    
    # 2. Rice Bacterial Leaf Blight (Yellow-brown wavy margins)
    rice_blight = create_base_leaf(leaf_type="linear")
    draw = ImageDraw.Draw(rice_blight)
    # Wavy necrotic blights along margins
    for y in range(60, 440, 15):
        # Left margin blight
        w = np.random.randint(25, 55)
        draw.ellipse([160, y, 160 + w, y + 25], fill=(184, 134, 11))
        draw.ellipse([165, y + 5, 160 + w - 10, y + 20], fill=(139, 69, 19))
        # Right margin blight
        w_r = np.random.randint(25, 55)
        draw.ellipse([340 - w_r, y, 340, y + 25], fill=(184, 134, 11))
        draw.ellipse([340 - w_r + 10, y + 5, 335, y + 20], fill=(139, 69, 19))
    rice_blight.save(os.path.join(SAMPLE_DIR, "rice_bacterial_blight.png"))

    # 3. Potato Early Blight (Target-board concentric dark spots)
    potato_eb = create_base_leaf(leaf_type="oval")
    draw = ImageDraw.Draw(potato_eb)
    spot_centers = [(180, 160), (310, 190), (230, 270), (160, 320), (330, 330), (220, 380)]
    for cx, cy in spot_centers:
        r_outer = np.random.randint(28, 42)
        # Yellow chlorotic halo
        draw.ellipse([cx - r_outer - 8, cy - r_outer - 8, cx + r_outer + 8, cy + r_outer + 8], fill=(205, 180, 50))
        # Outer dark ring
        draw.ellipse([cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer], fill=(101, 67, 33))
        # Middle ring
        draw.ellipse([cx - r_outer + 8, cy - r_outer + 8, cx + r_outer - 8, cy + r_outer - 8], fill=(139, 90, 43))
        # Dark necrotic center
        draw.ellipse([cx - r_outer + 16, cy - r_outer + 16, cx + r_outer - 16, cy + r_outer - 16], fill=(50, 30, 15))
    potato_eb.save(os.path.join(SAMPLE_DIR, "potato_early_blight.png"))

    # 4. Potato Late Blight (Large water-soaked dark blights)
    potato_lb = create_base_leaf(leaf_type="oval")
    draw = ImageDraw.Draw(potato_lb)
    # Severe blackish expanding rot
    draw.ellipse([80, 60, 260, 240], fill=(40, 40, 30))
    draw.ellipse([240, 200, 430, 420], fill=(45, 45, 35))
    draw.ellipse([140, 280, 290, 440], fill=(50, 45, 30))
    # Pale greenish-yellow margin
    draw.arc([75, 55, 265, 245], start=0, end=360, fill=(180, 190, 80), width=6)
    potato_lb.save(os.path.join(SAMPLE_DIR, "potato_late_blight.png"))

    # 5. Tomato Leaf Mold (Diffuse chlorotic yellow patches)
    tomato_lm = create_base_leaf(leaf_type="oval")
    draw = ImageDraw.Draw(tomato_lm)
    for _ in range(18):
        x = np.random.randint(120, 380)
        y = np.random.randint(100, 400)
        s = np.random.randint(18, 40)
        draw.ellipse([x - s, y - s, x + s, y + s], fill=(218, 165, 32))
    tomato_lm.save(os.path.join(SAMPLE_DIR, "tomato_leaf_mold.png"))

    # 6. Corn Common Rust (Cinnamon-brown powdery pustules)
    corn_rust = create_base_leaf(leaf_type="linear")
    draw = ImageDraw.Draw(corn_rust)
    for _ in range(60):
        x = np.random.randint(180, 320)
        y = np.random.randint(60, 440)
        w = np.random.randint(4, 9)
        h = np.random.randint(6, 14)
        draw.ellipse([x, y, x + w, y + h], fill=(165, 42, 42))
        draw.ellipse([x + 1, y + 2, x + w - 1, y + h - 2], fill=(205, 92, 92))
    corn_rust.save(os.path.join(SAMPLE_DIR, "corn_common_rust.png"))

    # 7. Apple Scab (Olive-brown velvety scabs)
    apple_scab = create_base_leaf(leaf_type="oval")
    draw = ImageDraw.Draw(apple_scab)
    scabs = [(170, 150), (280, 170), (210, 240), (320, 290), (180, 340)]
    for sx, sy in scabs:
        s = np.random.randint(22, 38)
        draw.ellipse([sx - s, sy - s, sx + s, sy + s], fill=(85, 107, 47))
        draw.ellipse([sx - s + 6, sy - s + 6, sx + s - 6, sy + s - 6], fill=(47, 79, 79))
    apple_scab.save(os.path.join(SAMPLE_DIR, "apple_scab.png"))

    print(f"[+] Successfully generated 7 sample leaf images in: {SAMPLE_DIR}")


if __name__ == "__main__":
    generate_all_samples()

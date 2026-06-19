"""
ORLEN OIL – New Product Image Acquisition & Processing Pipeline
Run: pip install requests rembg Pillow
Then: python fetch_new_product_images.py
Output: public/images/catalog/<SKU>.png (transparent background, 600x600px)
"""

import os
import requests
from pathlib import Path
from PIL import Image
from rembg import remove
from io import BytesIO

OUTPUT_DIR = Path(__file__).parent.parent / "public" / "images" / "catalog"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

TARGET_W, TARGET_H = 600, 600

# ---------------------------------------------------------------------------
# Product → image URL mapping.
# Replace each URL with the official ORLEN OIL branded packaging image URL.
# Source: https://oferta.orlenoil.com/media/  or  https://www.orlenoil.pl/
# ---------------------------------------------------------------------------
PRODUCTS = {
    # Truck – Ultor
    "OR-UEF-5W20":    None,  # Orlen Oil Ultor Effective 5W-20  – obtain from ORLEN CDN
    "PL-UCOM-10W40":  None,  # Platinum Ultor Complete 10W-40   – obtain from ORLEN CDN

    # Agriculture
    "PL-AGRUTTO-10W30": None, # Platinum Agro UTTO 10W-30
    "PL-MPTF":          None, # Platinum Multi PTF

    # Transmission
    "PL-GATF6":       None,  # Platinum Gear ATF VI

    # Industrial – Gear Oils (TRANSOL)
    "OR-TRANSOL-150": None,
    "OR-TRANSOL-220": None,
    "OR-TRANSOL-320": None,
    "OR-TRANSOL-460": None,

    # Industrial – Compressor & Turbine
    "OR-COR-DAB100":  None,  # Coralia L-DAB 100
    "OR-TURB-T46":    None,  # Turbine T-46

    # Greases
    "OR-LTN-4P1":     None,  # Liten LT-4P1 (NLGI 1)
    "OR-LTN-4P2":     None,  # Liten LT-4P2 (NLGI 2)
    "OR-LTN-4P3":     None,  # Liten LT-4P3 (NLGI 3)
    "OR-GRS-STP":     None,  # Greasen STP
    "OR-GRS-GRAF":    None,  # Greasen Grafit
}


def process_image(img_bytes: bytes, sku: str) -> None:
    """Remove background, resize to TARGET_WxTARGET_H, save as PNG."""
    # 1. Remove background -> RGBA
    img_no_bg = remove(img_bytes)
    img = Image.open(BytesIO(img_no_bg)).convert("RGBA")

    # 2. Fit inside TARGET box preserving aspect ratio, pad with transparent
    img.thumbnail((TARGET_W, TARGET_H), Image.LANCZOS)
    canvas = Image.new("RGBA", (TARGET_W, TARGET_H), (0, 0, 0, 0))
    offset_x = (TARGET_W - img.width) // 2
    offset_y = (TARGET_H - img.height) // 2
    canvas.paste(img, (offset_x, offset_y), img)

    # 3. Save
    out_path = OUTPUT_DIR / f"{sku}.png"
    canvas.save(out_path, "PNG", optimize=True)
    print(f"  Saved: {out_path} ({out_path.stat().st_size // 1024} KB)")


def main():
    session = requests.Session()
    session.headers["User-Agent"] = "Mozilla/5.0 ORLEN-ImageBot/1.0"

    for sku, url in PRODUCTS.items():
        if url is None:
            print(f"[SKIP] {sku} – no URL configured. Add the official ORLEN CDN link above.")
            continue

        out_path = OUTPUT_DIR / f"{sku}.png"
        if out_path.exists():
            print(f"[SKIP] {sku} – already exists.")
            continue

        print(f"[FETCH] {sku} <- {url}")
        try:
            resp = session.get(url, timeout=30)
            resp.raise_for_status()
            process_image(resp.content, sku)
        except Exception as e:
            print(f"  ERROR: {e}")


if __name__ == "__main__":
    main()

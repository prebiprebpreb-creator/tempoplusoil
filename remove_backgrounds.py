#!/usr/bin/env python3
"""
Batch background removal for product photos.

Reads every JPG/PNG/WebP in ./input/ , strips the background with `rembg`,
and writes transparent .webp files to ./output/ using the original basename.

Setup:
    pip install rembg[gpu] Pillow    # with CUDA
    # or
    pip install rembg Pillow         # CPU-only

Usage:
    python remove_backgrounds.py
"""

from __future__ import annotations

from pathlib import Path
from io import BytesIO

from PIL import Image
from rembg import remove, new_session

INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")
SUPPORTED = {".jpg", ".jpeg", ".png", ".webp"}
# "isnet-general-use" gives noticeably cleaner edges on product shots than
# the default "u2net"; swap if you prefer speed over quality.
MODEL = "isnet-general-use"


def process_file(src: Path, session) -> Path:
    with Image.open(src) as im:
        im = im.convert("RGBA")
        buf = BytesIO()
        im.save(buf, format="PNG")
        cut = remove(buf.getvalue(), session=session)

    out_img = Image.open(BytesIO(cut)).convert("RGBA")
    dest = OUTPUT_DIR / (src.stem + ".webp")
    out_img.save(dest, format="WEBP", quality=92, method=6)
    return dest


def main() -> None:
    if not INPUT_DIR.exists():
        INPUT_DIR.mkdir(parents=True)
        print(f"Created {INPUT_DIR}/ — drop your source images there and re-run.")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    files = sorted(
        p for p in INPUT_DIR.iterdir()
        if p.is_file() and p.suffix.lower() in SUPPORTED
    )
    if not files:
        print(f"No images found in {INPUT_DIR}/ (looking for {sorted(SUPPORTED)}).")
        return

    print(f"Loading model '{MODEL}'…")
    session = new_session(MODEL)

    for i, src in enumerate(files, 1):
        try:
            dest = process_file(src, session)
            print(f"[{i}/{len(files)}] {src.name}  ->  {dest}")
        except Exception as exc:
            print(f"[{i}/{len(files)}] {src.name}  FAILED: {exc}")

    print(f"Done. Output in {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()

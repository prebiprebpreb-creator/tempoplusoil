"""
Orlen image seeding pipeline.
Downloads official Orlen product images (browser headers to pass the WAF),
removes the background with rembg, trims to content, caps the long side,
and saves a high-quality transparent PNG to public/images/catalog/<SKU>.png.

Usage:  python scripts/seed_orlen_images.py automotive
        python scripts/seed_orlen_images.py industrial
"""
import sys, io, os, time, urllib3
from pathlib import Path
import requests
from PIL import Image
from rembg import remove

urllib3.disable_warnings()
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "public" / "images" / "catalog"
OUT.mkdir(parents=True, exist_ok=True)

HDRS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://oferta.orlenoil.com/",
}

# SKU -> official Orlen source image URL (verified against each product's own page).
AUTOMOTIVE = {
    # --- New passenger products ---
    "PL-MEV-0W30":   "https://oferta.orlenoil.com/media/5xzp20fv/orlen-oil-max-expert-v-0w-30-4l.png",
    "PL-MHYB-0W20":  "https://oferta.orlenoil.com/media/1gfjrcsd/orlen-oil-max-expert-hybrid-0w-20-4l-etykieta-ne231212_qso954b4p_q-20x.png",
    "PL-MHYB-5W20":  "https://oferta.orlenoil.com/media/ae2bosed/orlen-oil-max-expert-hybrid-5w-20-4l-etykieta-ne231212_qso956b4p_q-20x.png",
    # --- New truck product ---
    "PL-UBAS-10W40": "https://oferta.orlenoil.com/media/thqnbnsj/orlen-oil-ultor-basic-10w-40-20l-etykieta-pr-ne240126_qso006k2p_r.png",
    # --- New coolants ---
    "OR-COOLQNEW":   "https://oferta.orlenoil.com/media/43vgomu1/orlen-oil-petrygo-q-new-plyn-do-chlodnic-5l.png",
    "OR-COOLPRIME":  "https://oferta.orlenoil.com/media/qd4aqd0c/orlen-oil-petrygo-prime-plyn-do-chlodnic-5l.png",
    # --- New transmission ---
    "PL-GATF3":      "https://oferta.orlenoil.com/media/bcgn4suy/orlen-oil-gear-atf-iii-20l-etykieta-pr-ne240126_qso830k2r_r.png",

    # --- Image fills for existing products that had no image ---
    "OR-UEF-5W20":     "https://oferta.orlenoil.com/media/q5wneowp/orlen-oil-ultor-effective-5w-20-20l-etykieta-pr-ne240126_qsoxxxk2r_r.png",
    "PL-UCOM-10W40":   "https://oferta.orlenoil.com/media/ig0byphh/orlen-oil-ultor-complete-10w-40-20l-etykieta-pr-ne240126_qso922k2r_r.png",
    "PL-GATF6":        "https://oferta.orlenoil.com/media/lavjs14v/orlen-oil-gear-atf-vi-20l-etykieta-pr-ne240129_qso950k2r_r.png",
    "OR-STOU-10W40":   "https://oferta.orlenoil.com/media/xveaufml/orlen-oil-multi-stou-10w-40-20l-etykieta-pr-ne240109_qso898k2r_q.png",
    "PL-AGRUTTO-10W30":"https://oferta.orlenoil.com/media/satjoohs/orlen-oil-multi-utto-10w-30-20l-etykieta-pr-ne240109_qso899k2r_q-eps.png",
    "PL-MPTF":         "https://oferta.orlenoil.com/media/2y1pa2tn/orlen-oil-multi-ptf-10w-20l-etykieta-pr-ne240109_qso896k2r_q.png",
    "HP-6":            "https://oferta.orlenoil.com/media/xhlbdhxa/orlen-oil-hipol-6-80w-5l.png",
}

# Industrial / grease: official Orlen packaging shots from orlenoil.pl (lower-res, authentic).
INDUSTRIAL = {
    "_generic-drum":  "https://www.orlenoil.pl/PL/NaszaOferta/Produkty/PublishingImages/beczk_szare.jpg",
    "_generic-grease":"https://www.orlenoil.pl/PL/NaszaOferta/Produkty/PublishingImages/226.jpg",
    "OR-GRS-GRAF":    "https://www.orlenoil.pl/PL/NaszaOferta/Produkty/PublishingImages/greasen_grafit_400g_wiz_RGB.jpg",
}

CAP = 1000  # long-side cap in px


def process(sku: str, url: str) -> str:
    try:
        r = requests.get(url, headers=HDRS, timeout=60, verify=False)
        if r.status_code != 200 or "image" not in r.headers.get("content-type", ""):
            return f"[FAIL] {sku}: HTTP {r.status_code} ctype={r.headers.get('content-type')}"
        raw = r.content
        cut = remove(raw)
        im = Image.open(io.BytesIO(cut)).convert("RGBA")
        bbox = im.getbbox()
        if bbox:
            im = im.crop(bbox)
        ratio = min(CAP / im.width, CAP / im.height, 1.0)
        if ratio < 1.0:
            im = im.resize((round(im.width * ratio), round(im.height * ratio)), Image.LANCZOS)
        # pad small industrial images up so they are not tiny on cards
        if max(im.width, im.height) < 360:
            up = 360 / max(im.width, im.height)
            im = im.resize((round(im.width * up), round(im.height * up)), Image.LANCZOS)
        path = OUT / f"{sku}.png"
        im.save(path, "PNG", optimize=True)
        return f"[ OK ] {sku}: {im.width}x{im.height}  {path.stat().st_size // 1024}KB  (src {len(raw)//1024}KB)"
    except Exception as e:
        return f"[FAIL] {sku}: {e}"


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "automotive"
    table = {"automotive": AUTOMOTIVE, "industrial": INDUSTRIAL}[which]
    print(f"=== Processing {which}: {len(table)} images ===")
    for sku, url in table.items():
        print(process(sku, url))
        time.sleep(0.3)


if __name__ == "__main__":
    main()

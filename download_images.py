import requests, time, os

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.orlenoil.pl/",
})

try:
    session.get("https://www.orlenoil.pl/", timeout=15)
    time.sleep(1)
except: pass

URLS = {
    "PL-MAX-5W40":   "https://www.orlenoil.pl/PL/NaszaOferta/Produkty/PublishingImages/PLATINUMMaxExpertC35W-405L-wizual2017-07.jpg",
    "PL-ULT-5W30":   "https://www.orlenoil.pl/PL/NaszaOferta/Produkty/PublishingImages/ORLEN%20OIL%20ULTOR%20PERFECT%205W-30%2020L.jpg",
    "PL-CLA-10W40":  "https://www.orlenoil.pl/PL/NaszaOferta/Produkty/PublishingImages/383.jpg",
    "PL-RID-20W50":  "https://www.orlenoil.pl/PL/NaszaOferta/Produkty/PublishingImages/Rider_4L_vtwin4T_wiz_RGB.jpg",
    "PL-AGR-15W40":  "https://www.orlenoil.pl/PL/NaszaOferta/Produkty/PublishingImages/PLATINUM_AGRO_STOU_10W-40_5L.jpg",
    "PL-GEO-80W90":  "https://www.orlenoil.pl/PL/NaszaOferta/Produkty/PublishingImages/PLATINUM%20GEAR%20GL-5%2080W-90.jpg",
    "PL-ATF-IID":    "https://www.orlenoil.pl/PublishingImages/hipol_ATF-II-D_5L.png",
    "PL-MAX-0W20":   "https://oferta.orlenoil.com/media/dknplm3r/orlen-oil-max-expert-ll-0w-20-4l-etykieta-ne231128_qso947b4p_q-20x.png",
    "PL-DIE-10W40":  "https://www.orlenoil.pl/PL/NaszaOferta/Produkty/PublishingImages/393.jpg",
    "PL-TRU-15W40":  "https://www.orlenoil.pl/PL/NaszaOferta/Produkty/PublishingImages/ORLEN%20OIL%20ULTOR%20PLUS%2015W-40%2020L.jpg",
    "PL-COOL-G12":   "https://www.orlenoil.pl/PL/NaszaOferta/Produkty/PublishingImages/petrygo_5L_prime_g12%2B%2B.png",
    "PL-HYD-46":     "https://www.eoleje.pl/wp-content/uploads/2025/01/hydrolhv4620L.png",
}

OUT = "/c/Users/rronp/Downloads/Tempoplus/input"
os.makedirs(OUT, exist_ok=True)

for sku, url in URLS.items():
    ext = url.split(".")[-1].split("?")[0].lower()
    dest = f"{OUT}/{sku}.{ext}"
    try:
        r = session.get(url, timeout=20)
        ct = r.headers.get("Content-Type","")
        if r.status_code == 200 and "image" in ct:
            with open(dest, "wb") as f:
                f.write(r.content)
            print(f"OK  {sku}  {len(r.content)//1024}KB")
        else:
            print(f"FAIL {sku} status={r.status_code} ct={ct[:60]} size={len(r.content)}")
    except Exception as e:
        print(f"ERR  {sku} {e}")
    time.sleep(0.4)

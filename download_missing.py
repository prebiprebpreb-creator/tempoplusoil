import requests, time

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

# Try multiple URL variants for the two missing products
CANDIDATES = [
    # ATF IID
    ("PL-ATF-IID", "https://www.orlenoil.pl/PL/NaszaOferta/Produkty/PublishingImages/hipol_ATF-II-D_5L.png"),
    ("PL-ATF-IID", "https://www.orlenoil.pl/PL/NaszaOferta/Produkty/PublishingImages/HIPOL_ATF_IID_5L.jpg"),
    ("PL-ATF-IID", "https://www.orlenoil.pl/PL/NaszaOferta/Produkty/PublishingImages/hipol_ATF_IID_5L.png"),
    # Coolant
    ("PL-COOL-G12", "https://www.orlenoil.pl/PL/NaszaOferta/Produkty/PublishingImages/petrygo_5L_prime_g12++.png"),
    ("PL-COOL-G12", "https://www.orlenoil.pl/PL/NaszaOferta/Produkty/PublishingImages/Petrygo_Prime_G12++_5L.jpg"),
    ("PL-COOL-G12", "https://www.orlenoil.pl/PL/NaszaOferta/Produkty/PublishingImages/petrygo_prime_g12++_5L.png"),
]

OUT = "/c/Users/rronp/Downloads/Tempoplus/input"
found = set()

for sku, url in CANDIDATES:
    if sku in found:
        continue
    ext = url.split(".")[-1].split("?")[0].lower()
    dest = f"{OUT}/{sku}.{ext}"
    try:
        r = session.get(url, timeout=15)
        ct = r.headers.get("Content-Type","")
        if r.status_code == 200 and "image" in ct:
            with open(dest, "wb") as f:
                f.write(r.content)
            print(f"OK  {sku}  {len(r.content)//1024}KB  {url}")
            found.add(sku)
        else:
            print(f"FAIL {sku} {r.status_code} {url}")
    except Exception as e:
        print(f"ERR {sku} {e}")
    time.sleep(0.3)

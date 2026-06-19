"""Phase 3: products sourced from other sites. Fill MaxExpert FT and add Platinum Classic Gas."""
import re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")

CAT = Path(__file__).resolve().parent.parent / "public" / "js" / "catalog.js"
text = CAT.read_text(encoding="utf-8")

# Fill MaxExpert FT (existing image-less passenger SKU)
def fill(t, sku, img):
    pat = re.compile(r'(\{[^{}]*?sku:\s*"' + re.escape(sku) + r'"[^{}]*?images:\s*\[)[^\]]*(\])', re.S)
    return pat.subn(r'\g<1>\n      "' + img + r'",\n      null,\n      null\n    \g<2>', t)

text, n = fill(text, "PL-MEFT-5W30", "images/catalog/PL-MEFT-5W30.png")
print("fill PL-MEFT-5W30:", "ok" if n else "NOT FOUND")

def obj(sku, name, category, label, ptype, specs, desc, sizes, badge, img):
    sz = ", ".join(f'"{s}"' for s in sizes)
    return f'''  {{
    sku: "{sku}",
    name: "{name}",
    category: "{category}",
    categoryLabel: "{label}",
    type: "{ptype}",
    specs: "{specs}",
    description: "{desc}",
    sizes: [{sz}],
    badge: "{badge}",
    images: [
      "{img}",
      null,
      null
    ]
  }}'''

NEW = [
    obj("PL-GASSYN-5W40", "Platinum Classic Gas Synthetic 5W-40", "passenger", "Passenger Cars", "Fully Synthetic",
        "Fully synthetic · API SL · for LPG/CNG & petrol engines · gas-installation compatible",
        "Full synthetic engine oil developed specifically for petrol cars fitted with LPG/CNG gas installations. Its additive system is optimised for the higher combustion temperatures and different deposit characteristics of gaseous fuels, providing excellent protection against valve-seat wear and oil oxidation while supporting reliable year-round operation on both petrol and gas.",
        ["1L", "4L", "5L"], "LPG/CNG", "images/catalog/PL-GASSYN-5W40.png"),
    obj("PL-GASSEMI-10W40", "Platinum Classic Gas Semisynthetic 10W-40", "passenger", "Passenger Cars", "Semi-Synthetic",
        "Semi-synthetic · API SL · for LPG/CNG & petrol engines · gas-installation compatible",
        "Semi-synthetic engine oil formulated for petrol vehicles equipped with LPG/CNG gas systems. Balances economy with dependable protection against the elevated thermal loads and valve wear associated with gas combustion, maintaining stable viscosity and oil-film strength for year-round dual-fuel operation in older and modern engines requiring API SL.",
        ["1L", "4L", "5L"], "LPG/CNG", "images/catalog/PL-GASSEMI-10W40.png"),
]

block = "\n\n  // ─── PLATINUM CLASSIC GAS (LPG/CNG line) ─────────────────────────────────────\n\n" + ",\n".join(NEW) + "\n"
idx = text.rstrip().rfind("];")
head = text[:idx].rstrip()
if not head.endswith(","):
    head += ","
text = head + block + "\n];\n"
CAT.write_text(text, encoding="utf-8")
print(f"Appended {len(NEW)} new Platinum Classic Gas products.")

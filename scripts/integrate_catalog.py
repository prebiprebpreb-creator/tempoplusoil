"""Idempotent catalog.js updater: fills images on existing SKUs and appends new product objects."""
import re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")

CAT = Path(__file__).resolve().parent.parent / "public" / "js" / "catalog.js"
text = CAT.read_text(encoding="utf-8")

# --- 1. Image fills: existing SKUs that had images: [null, null, null] ---
FILLS = ["OR-UEF-5W20", "PL-UCOM-10W40", "PL-GATF6", "OR-STOU-10W40",
         "PL-AGRUTTO-10W30", "PL-MPTF", "HP-6",
         "PL-GATF3"]  # already existed (Gear ATF III) -> upgrade CDN image to local bg-removed

def fill_image(t, sku):
    pat = re.compile(r'(\{[^{}]*?sku:\s*"' + re.escape(sku) + r'"[^{}]*?images:\s*\[)[^\]]*(\])', re.S)
    repl = r'\g<1>\n      "images/catalog/' + sku + r'.png",\n      null,\n      null\n    \g<2>'
    new, n = pat.subn(repl, t)
    return new, n

for sku in FILLS:
    text, n = fill_image(text, sku)
    print(f"fill {sku}: {'ok' if n else 'NOT FOUND'}")

# --- 2. New product objects ---
def obj(sku, name, category, label, ptype, specs, desc, sizes, badge):
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
      "images/catalog/{sku}.png",
      null,
      null
    ]
  }}'''

NEW = [
    obj("PL-MEV-0W30", "Platinum MaxExpert V 0W-30", "passenger", "Passenger Cars", "Fully Synthetic",
        "Fully synthetic · ACEA C3 · API SN · BMW LL-04 · MB 229.51/229.31 · VW 504.00/507.00 · GM dexos2",
        "Full synthetic low-SAPS 0W-30 engine oil for the latest BMW, Mercedes-Benz and Volkswagen Group petrol and diesel engines with particulate filters and catalytic converters. The ultra-low 0W cold-start viscosity delivers near-instant oil circulation and improved fuel economy, while the C3 formulation protects DPF/GPF systems and supports extended drain intervals.",
        ["1L", "4L", "20L", "208L"], "0W-30"),
    obj("PL-MHYB-0W20", "Platinum MaxExpert HYBRID 0W-20", "passenger", "Passenger Cars", "Fully Synthetic",
        "Fully synthetic · ACEA C5 · API SP · for hybrid & modern petrol engines · ultra-low viscosity",
        "Ultra-low viscosity full synthetic 0W-20 oil engineered for petrol-electric hybrid and modern low-friction petrol engines. Meets ACEA C5 and API SP, minimising internal friction for measurable fuel savings while fully protecting stop-start systems, Atkinson-cycle cylinders and turbochargers under the frequent cold starts typical of hybrid duty cycles.",
        ["1L", "4L", "20L", "208L"], "Hybrid"),
    obj("PL-MHYB-5W20", "Platinum MaxExpert HYBRID 5W-20", "passenger", "Passenger Cars", "Fully Synthetic",
        "Fully synthetic · ACEA C5 · API SP · for hybrid & modern petrol engines",
        "Full synthetic 5W-20 low-viscosity oil for petrol-electric hybrid and modern petrol engines requiring ACEA C5 / API SP performance. Delivers fuel-economy benefits through reduced friction while maintaining robust wear protection and oxidation stability during the repeated short-trip, low-temperature operation common to hybrid vehicles.",
        ["1L", "4L", "20L", "208L"], "Hybrid"),
    obj("PL-UBAS-10W40", "Platinum Ultor Basic 10W-40", "truck", "Trucks & HGV", "Semi-Synthetic",
        "Semi-synthetic · ACEA E7 · API CI-4 · MB 228.3 · MAN M3275-1 · Volvo VDS-3",
        "Semi-synthetic heavy-duty diesel engine oil for Euro 3 and Euro 5 trucks and buses operating in mixed fleets. ACEA E7 performance with MB 228.3, MAN M3275-1 and Volvo VDS-3 approvals delivers dependable soot control, piston cleanliness and wear protection at standard drain intervals, providing an economical all-round lubricant for distribution and construction vehicles.",
        ["20L", "60L", "208L", "1000L IBC"], "Fleet"),
    obj("OR-COOLQNEW", "Orlen Oil Petrygo Q NEW", "coolant", "Coolants & Radiator Fluids", "OAT Coolant",
        "Ready-to-use long-life coolant · silicate-free OAT · -37°C / +135°C · for car radiators",
        "Ready-to-use silicate-free OAT (Organic Acid Technology) long-life engine coolant providing freeze protection to -37°C and boil protection to +135°C. Compatible with G12-class systems, it protects all cooling-circuit metals including aluminium alloys, cast iron and brass against corrosion, cavitation and scale, and is ready to pour straight into the radiator without dilution.",
        ["1L", "5L", "20L", "208L", "1000L IBC"], "Ready-to-Use"),
    obj("OR-COOLPRIME", "Orlen Oil Petrygo Prime G12++", "coolant", "Coolants & Radiator Fluids", "Si-OAT Coolant",
        "Ready-to-use coolant · G12++ Si-OAT hybrid · long-life · -37°C / +135°C",
        "Premium ready-to-use G12++ (Si-OAT) hybrid long-life engine coolant combining organic acid inhibitors with a trace of silicate for fast aluminium protection. Delivers freeze protection to -37°C and extended service life in modern petrol, diesel and hybrid engines, safeguarding water pumps, radiators and heat exchangers against corrosion and overheating.",
        ["1L", "5L", "20L", "208L", "1000L IBC"], "G12++"),
]

block = "\n\n  // ─── ORLEN OIL CATALOG EXPANSION (new SKUs) ──────────────────────────────────\n\n" + ",\n".join(NEW) + "\n"

# Insert before the final closing "];" of the array.
idx = text.rstrip().rfind("];")
assert idx != -1, "could not find array close"
# ensure previous element ends with a comma
head = text[:idx].rstrip()
if not head.endswith(","):
    head += ","
text = head + block + "\n];\n"

CAT.write_text(text, encoding="utf-8")
print(f"\nAppended {len(NEW)} new products. catalog.js now {text.count('sku:')} SKUs.")

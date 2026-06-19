"""Phase 2: industrial + grease. Fill image-less SKUs with official Orlen drum/cartridge
images and append the real new industrial/grease products."""
import re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")

CAT = Path(__file__).resolve().parent.parent / "public" / "js" / "catalog.js"
text = CAT.read_text(encoding="utf-8")

DRUM = "images/catalog/_generic-drum.png"
LITEN = "images/catalog/OR-GRS-LITEN-EP2.png"  # Liten-brand cartridge (shared across LT-4P grades)

# SKU -> image path to set as images[0]
FILLS = {}
# all image-less industrial oils -> shared Orlen industrial drum
for sku in ["OR-HYD-HVLPD","OR-HYD-LHV15","OR-HYD-LHV22","OR-HYD-LHV32","OR-HYD-LHV68","OR-HYD-LHV100",
            "OR-HYD-HVY15","OR-HYD-HVY32","OR-HYD-HVY46","OR-HYD-HVY68","OR-HYD-HVY100",
            "OR-HYD-POW32","OR-HYD-POW46","OR-HYD-POW68","OR-HYD-LHVP32","OR-HYD-LHVP46","OR-HYD-LHVP68",
            "OR-HYD-EXHLPD","OR-HYD-PHLPD15","OR-HYD-PHLPD32","OR-HYD-HLPD","OR-HYD-PHM15","OR-HYD-HM",
            "OR-HYD-HL","OR-HYD-BHEES","OR-HYD-BHESEL46","OR-HYD-BHETG46","OR-HYD-SPEC","OR-HYD-SYPE46",
            "OR-HYD-XLHV32","OR-HYD-XLHV46","OR-HYD-XLHV68","OR-HYD-ARCT15","OR-HYD-ARCT32",
            "OR-HYD-PLHV15","OR-HYD-PLHV22","OR-HYD-PLHV32","OR-HYD-PLHV46","OR-HYD-PLHV68","OR-HYD-PHVLPD",
            "OR-TRANSOL-150","OR-TRANSOL-220","OR-TRANSOL-320","OR-TRANSOL-460","OR-COR-DAB100",
            "OR-TURB-T46","OR-ADBLUE"]:
    FILLS[sku] = DRUM
# greases -> specific Orlen cartridge renders
FILLS["OR-GRS-GRAF"]   = "images/catalog/OR-GRS-GRAF.png"
FILLS["OR-GRS-STP"]    = "images/catalog/OR-GRS-STP.png"
FILLS["OR-GRS-SYNHT2"] = "images/catalog/OR-GRS-SYNHT2.png"
FILLS["OR-LTN-4P1"]    = LITEN
FILLS["OR-LTN-4P2"]    = LITEN
FILLS["OR-LTN-4P3"]    = LITEN


def fill(t, sku, img):
    pat = re.compile(r'(\{[^{}]*?sku:\s*"' + re.escape(sku) + r'"[^{}]*?images:\s*\[)[^\]]*(\])', re.S)
    repl = r'\g<1>\n      "' + img + r'",\n      null,\n      null\n    \g<2>'
    return pat.subn(repl, t)

ok = miss = 0
for sku, img in FILLS.items():
    text, n = fill(text, sku, img)
    if n: ok += 1
    else:
        miss += 1; print("  NOT FOUND:", sku)
print(f"Industrial/grease fills applied: {ok} (missing {miss})")


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

IND = "Industrial"
GRS = "Greases"
NEW = [
    obj("OR-TRANSOL-SP150", "Transol SP 150", "industrial", IND, "Mineral",
        "Industrial gear oil · ISO VG 150 · CLP · DIN 51517-3 · EP/AW additives",
        "High-quality mineral industrial gear oil (CLP) in ISO VG 150 for enclosed spur, helical and bevel gear drives operating under high loads. The sulphur-phosphorus EP additive system provides outstanding protection against scuffing, micro-pitting and wear, while excellent oxidation and foam resistance ensures long service life in industrial gearboxes and bearings.",
        ["20L", "208L"], "ISO VG 150", DRUM),
    obj("OR-TRANSOL-SP220", "Transol SP 220", "industrial", IND, "Mineral",
        "Industrial gear oil · ISO VG 220 · CLP · DIN 51517-3 · EP/AW additives",
        "Mineral CLP industrial gear oil in ISO VG 220 formulated for heavily loaded enclosed gear systems in industrial machinery. Provides high load-carrying capacity, scuffing protection and thermal-oxidative stability, with reliable demulsibility and anti-foam performance for circulation and splash-lubricated gearboxes.",
        ["20L", "208L"], "ISO VG 220", DRUM),
    obj("OR-TRANSOL-SP320", "Transol SP 320", "industrial", IND, "Mineral",
        "Industrial gear oil · ISO VG 320 · CLP · DIN 51517-3 · EP/AW additives",
        "Mineral CLP industrial gear oil in ISO VG 320 for low-speed, high-torque enclosed gear drives. Its robust EP additive package and high viscosity deliver excellent wear and scuffing protection under shock loading, while maintaining oxidation stability and corrosion protection over extended drain intervals.",
        ["20L", "208L"], "ISO VG 320", DRUM),
    obj("OR-TRANSOL-SP460", "Transol SP 460", "industrial", IND, "Mineral",
        "Industrial gear oil · ISO VG 460 · CLP · DIN 51517-3 · EP/AW additives",
        "Heavy-grade mineral CLP industrial gear oil in ISO VG 460 for the most heavily loaded slow-speed industrial gearboxes. Maintains a strong lubricating film under extreme pressure and high operating temperatures, protecting gears and bearings against wear, scuffing and corrosion in demanding heavy-manufacturing applications.",
        ["20L", "208L"], "ISO VG 460", DRUM),
    obj("OR-COR-DAB46", "Coralia L-DAB 46", "industrial", IND, "Mineral",
        "Air compressor oil · ISO VG 46 · DIN 51506 VDL · for reciprocating compressors",
        "Mineral air-compressor oil in ISO VG 46 meeting DIN 51506 VDL for reciprocating and rotary air compressors. Excellent thermal-oxidative stability minimises carbon and varnish deposits on valves and discharge lines, while good demulsibility and anti-corrosion performance protect the compressor throughout extended service intervals.",
        ["20L", "208L"], "ISO VG 46", DRUM),
    obj("OR-HYD-HLP32", "Hydrol L-HM/HLP 32", "industrial", IND, "Mineral",
        "Hydraulic oil · HLP · ISO VG 32 · DIN 51524-2 · anti-wear",
        "Anti-wear hydraulic oil (HLP) in ISO VG 32 meeting DIN 51524-2 for hydraulic systems operating at moderate temperatures and pressures. The zinc-based anti-wear additive system protects pumps, valves and actuators, while excellent demulsibility, air release and anti-foam properties ensure stable, reliable operation of industrial and mobile hydraulics.",
        ["20L", "208L", "1000L IBC"], "HLP 32", DRUM),
    obj("OR-HYD-HLP46", "Hydrol L-HM/HLP 46", "industrial", IND, "Mineral",
        "Hydraulic oil · HLP · ISO VG 46 · DIN 51524-2 · anti-wear",
        "Anti-wear hydraulic oil (HLP) in ISO VG 46, the most widely used industrial hydraulic grade, meeting DIN 51524-2. Delivers excellent wear protection for vane, gear and piston pumps along with strong oxidation resistance, water separation and air release for dependable performance in industrial hydraulic power units.",
        ["20L", "208L", "1000L IBC"], "HLP 46", DRUM),
    obj("OR-HYD-HLP68", "Hydrol L-HM/HLP 68", "industrial", IND, "Mineral",
        "Hydraulic oil · HLP · ISO VG 68 · DIN 51524-2 · anti-wear",
        "Anti-wear hydraulic oil (HLP) in ISO VG 68 meeting DIN 51524-2 for hydraulic systems operating under higher temperatures or loads requiring a heavier viscosity grade. Provides robust pump protection, oxidation stability and clean operation, with reliable demulsibility and foam control for heavy-duty industrial hydraulics.",
        ["20L", "208L", "1000L IBC"], "HLP 68", DRUM),
    obj("OR-HYD-HLP100", "Hydrol L-HM/HLP 100", "industrial", IND, "Mineral",
        "Hydraulic oil · HLP · ISO VG 100 · DIN 51524-2 · anti-wear",
        "Heavy-grade anti-wear hydraulic oil (HLP) in ISO VG 100 meeting DIN 51524-2 for high-temperature, high-load hydraulic and circulation systems. The thicker film maintains pump protection and pressure stability in demanding applications, with excellent oxidation resistance and contaminant separation.",
        ["20L", "208L", "1000L IBC"], "HLP 100", DRUM),
    obj("OR-HYD-LHV150", "Hydrol L-HV 150", "industrial", IND, "Mineral",
        "Hydraulic oil · HVLP · high VI · ISO VG 150 · DIN 51524-3",
        "High viscosity-index hydraulic oil (HVLP) in ISO VG 150 meeting DIN 51524-3 for hydraulic systems exposed to wide temperature variations. The high VI maintains a stable lubricating film across a broad operating range, while the anti-wear and shear-stable additive package protects heavily loaded pumps and motors in mobile and outdoor equipment.",
        ["20L", "208L", "1000L IBC"], "HVLP 150", DRUM),
    obj("OR-HYD-PHLPD46", "Hydrol Premium HLP-D 46", "industrial", IND, "Mineral",
        "Detergent hydraulic oil · HLP-D · ISO VG 46 · with detergent/dispersant",
        "Premium detergent-dispersant hydraulic oil (HLP-D) in ISO VG 46 for hydraulic systems prone to water and contaminant ingress. The detergent additive system keeps dirt and condensation finely dispersed and carries them to the filter, preventing valve sticking and deposit formation while providing full anti-wear protection for precision hydraulics.",
        ["20L", "208L", "1000L IBC"], "HLP-D 46", DRUM),
    obj("OR-VELOL-9", "Velol 9", "industrial", IND, "Mineral",
        "Spindle & machine oil · light viscosity · for high-speed spindles",
        "Light mineral spindle and machine oil designed for high-speed textile and machine-tool spindles, light hydraulic systems and precision mechanisms requiring a low-viscosity lubricant. Provides reliable anti-wear and anti-corrosion protection with good oxidation stability for sustained high-speed operation.",
        ["20L", "208L"], "Spindle", DRUM),
    obj("OR-VELOL-19", "Velol 19", "industrial", IND, "Mineral",
        "Precision spindle & machine oil · medium-light viscosity",
        "Mineral precision spindle and machine oil of medium-light viscosity for machine-tool spindles, slideways and light hydraulic and circulation systems. Combines good anti-wear and anti-rust performance with thermal stability to ensure smooth, accurate operation of precision machinery.",
        ["20L", "208L"], "Spindle", DRUM),
    obj("OR-VELOL-29", "Velol 29", "industrial", IND, "Mineral",
        "Heavy spindle & machine oil · medium viscosity",
        "Mineral spindle and machine oil of medium viscosity for machine-tool bearings, spindles and light gearing requiring a slightly heavier lubricant. Provides dependable wear protection, corrosion inhibition and oxidation resistance for industrial precision equipment.",
        ["20L", "208L"], "Spindle", DRUM),
    obj("OR-SUCD30", "Orlen Oil Superol CD 30", "truck", "Trucks & HGV", "Mineral",
        "Mineral monograde · API CD · SAE 30 · for turbocharged diesel engines",
        "Monograde mineral engine oil to API CD in SAE 30 for naturally aspirated and turbocharged diesel engines in older trucks, buses, agricultural and stationary machinery. Provides effective protection against high-temperature deposits, corrosion and wear for compression-ignition engines operating on higher-sulphur fuel.",
        ["20L", "60L", "208L", "1000L IBC"], "SAE 30 CD", DRUM),
    obj("OR-SUCD40", "Orlen Oil Superol CD 40", "truck", "Trucks & HGV", "Mineral",
        "Mineral monograde · API CD · SAE 40 · for turbocharged diesel engines",
        "Monograde mineral engine oil to API CD in SAE 40 for turbocharged and naturally aspirated diesel engines operating at elevated temperatures. The heavier viscosity grade maintains oil-film strength and pressure in worn or hot-running engines, protecting bearings, pistons and liners in heavy-duty commercial and industrial diesel applications.",
        ["20L", "60L", "208L", "1000L IBC"], "SAE 40 CD", DRUM),
    obj("OR-TRAFO-EN", "Trafo EN", "industrial", IND, "Mineral",
        "Transformer insulating oil · inhibited · IEC 60296 · electrical equipment",
        "Inhibited mineral electrical insulating oil meeting IEC 60296 for power and distribution transformers, switchgear and other oil-filled electrical apparatus. Its high dielectric strength, low dissipation factor and excellent oxidation stability provide reliable insulation and heat transfer, extending the service life of electrical equipment.",
        ["20L", "208L"], "Dielectric", DRUM),
    obj("OR-ACP-1E", "ACP-1E Cutting Fluid", "industrial", IND, "Mineral",
        "Neat cutting oil · for light machining & general metalworking",
        "Neat (non-emulsifiable) mineral cutting oil for light to medium machining operations including turning, milling and drilling of ferrous and non-ferrous metals. Provides good lubrication and cooling at the cutting edge for improved surface finish and tool life, with corrosion protection for workpieces and machine tools.",
        ["20L", "208L"], "Cutting", DRUM),
    obj("OR-ACP-2E", "ACP-2E Cutting Fluid", "industrial", IND, "Mineral",
        "Neat cutting oil · EP · for heavy machining, tapping & threading",
        "EP-fortified neat cutting oil for demanding machining operations such as deep-hole drilling, tapping, threading and broaching of alloy steels. The extreme-pressure additive package reduces friction and welding at the tool tip, delivering superior tool life and surface finish in severe metal-cutting applications.",
        ["20L", "208L"], "Cutting EP", DRUM),
    obj("OR-ACP-3E", "ACP-3E Cutting Fluid", "industrial", IND, "Mineral",
        "Neat cutting oil · high-EP · for automated threading & severe operations",
        "High-EP neat cutting oil for automated and severe metalworking operations including thread cutting, gear shaping and heavy broaching of hard alloys. Its reinforced additive chemistry withstands extreme tool-tip pressures and temperatures, protecting tooling and ensuring consistent precision in CNC and transfer-line machining.",
        ["20L", "208L"], "Cutting EP", DRUM),
    obj("OR-GRS-BENTOR2", "Bentor 2", "grease", GRS, "Bentonite Grease",
        "Bentonite grease · NLGI 2 · high-temperature · for hot bearings",
        "High-temperature bentonite (clay-thickened) grease in NLGI grade 2 for plain and rolling bearings exposed to sustained high temperatures where conventional soap greases would melt or run. The non-melting thickener maintains consistency and lubrication in kiln cars, furnace conveyors, hot-rolling equipment and other hot operating environments.",
        ["0.4kg", "4.5kg", "18kg", "180kg"], "NLGI 2", "images/catalog/OR-GRS-BENTOR2.png"),
    obj("OR-GRS-SEP00", "Greasen S-EP 00", "grease", GRS, "Semi-Fluid Grease",
        "Semi-fluid EP grease · NLGI 00 · for central lubrication & gearboxes",
        "Semi-fluid lithium EP grease in NLGI grade 00 for centralised lubrication systems and grease-lubricated enclosed gearboxes. The fluid consistency pumps readily through long lines at low temperatures while the EP additive package protects gears and bearings under heavy and shock loads against wear and scuffing.",
        ["0.4kg", "4.5kg", "18kg", "180kg"], "NLGI 00", "images/catalog/OR-GRS-STP.png"),
    obj("OR-GRS-LITEN-EP2", "Liten Premium EP-2", "grease", GRS, "Lithium EP Grease",
        "Lithium EP grease · NLGI 2 · multipurpose · for bearings & chassis",
        "Multipurpose lithium extreme-pressure grease in NLGI grade 2 for rolling and plain bearings, chassis points, joints and general industrial and automotive lubrication. The EP additive system provides excellent load-carrying capacity and wear protection, with good water resistance, mechanical stability and corrosion protection across a wide temperature range.",
        ["0.4kg", "4.5kg", "18kg", "180kg"], "NLGI 2 EP", "images/catalog/OR-GRS-LITEN-EP2.png"),
]

block = "\n\n  // ─── INDUSTRIAL / GREASE EXPANSION (new SKUs) ────────────────────────────────\n\n" + ",\n".join(NEW) + "\n"
idx = text.rstrip().rfind("];")
head = text[:idx].rstrip()
if not head.endswith(","):
    head += ","
text = head + block + "\n];\n"

CAT.write_text(text, encoding="utf-8")
print(f"Appended {len(NEW)} new industrial/grease products.")

import re

catalog_path = r"C:\Users\rronp\Downloads\Tempoplus\public\js\catalog.js"

with open(catalog_path, "r", encoding="utf-8") as f:
    content = f.read()

image_map = {
    "PL-RRAC-5W40": "https://oferta.orlenoil.com/media/hmzhwzg5/orlen-oil-rider-racing-4t-5w-40-1l-etykieta-ne231113_qso902b1p_q-20x.png",
    "PL-RID4T-10W40": "https://oferta.orlenoil.com/media/by1emtt4/orlen-oil-rider-4t-10w-40-1l-etykieta-ne231113_qso900b1p_q-20x.png",
    "PL-RSPT-10W50": "https://www.orlenoil.pl/PL/NaszaOferta/Produkty/PublishingImages/Rider_4L_sport4T_wiz_RGB.jpg",
    "PL-RCRU-15W50": "https://oferta.orlenoil.com/media/jpbl2ppj/orlen-oil-rider-cruiser-4t-15w-50-1l-etykieta-ne231113_qso901b1p_q-20x.png",
    "PL-RVTW-20W50": "https://oferta.orlenoil.com/media/vhaagpoe/orlen-oil-rider-v-twin-4t-20w-50-1l-etykieta-ne231113_qso905b1p_q-20x.png",
    "PL-RRAC2T": "https://www.orlenoil.pl/PL/NaszaOferta/Produkty/PublishingImages/Rider_4L_racing2T_wiz_RGB.jpg",
    "PL-RSC2T": "https://oferta.orlenoil.com/media/tafjv24t/orlen-oil-rider-scooter-2t-1l-etykieta-ne231117_qso903b1p-_q-20x.png",
    "PL-MOTO2T": "https://www.orlenoil.pl/PL/NaszaOferta/Produkty/PublishingImages/168.jpg",
    "OR-2TSEMI": "https://oferta.orlenoil.com/media/xq0f0yf1/orlen-oil-2t-semisynthetic-1l.png",
    "OR-MIXOLS": "https://oferta.orlenoil.com/media/herl33f0/orlen-oil-mixol-s-1l-komplet-ne240104_qso842b1p_qso842b1t_q-20x.png",
    "OR-TRAW-10W30": "https://oferta.orlenoil.com/media/ikai1z2a/orlen-oil-trawol-sg-cd-10w-30-1l.png",
    "OR-TRAW-30": "https://oferta.orlenoil.com/media/yvjecnok/orlen-oil-trawol-sg-cd-30-1l.png",
    "OR-PIL-VG140": "https://www.orlenoil.pl/PL/NaszaOferta/Produkty/PublishingImages/411.jpg",
    "OR-PIL-VG150": "https://oferta.orlenoil.com/media/ck4i5s4k/orlen-oil-pilarol-5l-komplet-ne231220_qso933b5p_qso933b5p_q-20x.png",
    "OR-PIL-EKO": "https://www.orlenoil.pl/PL/NaszaOferta/Produkty/PublishingImages/PILAROL-EKO-Olej.jpg",
    "OR-PIL-Z": "https://www.orlenoil.pl/PL/NaszaOferta/Produkty/PublishingImages/PILAROL_5L.png",
    "OR-DGA-15W40": "https://www.orlenoil.pl/PL/NaszaOferta/Produkty/PublishingImages/beczk_szare.jpg",
    "OR-DGA-40": "https://www.orlenoil.pl/PL/NaszaOferta/Produkty/PublishingImages/beczk_szare.jpg",
    "OR-DGL-40": "https://www.orlenoil.pl/PL/NaszaOferta/Produkty/PublishingImages/beczk_szare.jpg",
    "OR-DGM-40": "https://www.orlenoil.pl/PL/NaszaOferta/Produkty/PublishingImages/beczk_szare.jpg",
    "OR-DGPL-40": "https://www.orlenoil.pl/PL/NaszaOferta/Produkty/PublishingImages/beczk_szare.jpg",
    "OR-ITRM-30MF": "https://egrando.pl/3269-large_default/orlen-iterm-30-mf-kanister-20l.jpg",
    "OR-SMPTFE": "https://buwar24.pl/img/large/42123/1.jpg",
    "OR-NP-32": "https://www.orlenoil.pl/PL/NaszaOferta/Produkty/PublishingImages/beczk_szare.jpg",
    "OR-NP-68": "https://www.orlenoil.pl/PL/NaszaOferta/Produkty/PublishingImages/beczk_szare.jpg",
    "OR-NP-100": "https://www.orlenoil.pl/PL/NaszaOferta/Produkty/PublishingImages/beczk_szare.jpg",
    "PL-IMP-APC": "https://euronaft.pl/media/products/65be5320d61a85cd3ee2d4a7b3c3f226/images/thumbnail/large_Impact-uniwersalny-do-czyszczenia-JPG.jpg",
    "PL-IMP-COCK": "https://www.orlen.pl/pl/dla-biznesu/produkty/plyny-i-chemia-motoryzacyjna/chemia-i-kosmetyki-samochodowe/platinum-impact-cockpit-spray/_jcr_content/root/container/container/container/container/container/image.coreimg.png/1706286600581/platinumimpactspraylesny400ml2019-04.png",
    "PL-IMP-DEIW": "https://www.orlen.pl/pl/dla-biznesu/produkty/plyny-i-chemia-motoryzacyjna/chemia-i-kosmetyki-samochodowe/platinum-impact-odmrazacz-do-szyb/_jcr_content/root/container/container/container/container_4621932/container/image.coreimg.png/1706207668676/impact-odmrazacz-do-szyb-500ml.png",
    "PL-IMP-DEIL": "https://www.orlen.pl/pl/dla-biznesu/produkty/plyny-i-chemia-motoryzacyjna/chemia-i-kosmetyki-samochodowe/platinum-impact-odmrazacz-do-zamkow/_jcr_content/root/container/container/container/container_1607449556/container/image.coreimg.jpeg/1706207664276/20190430platinumimpactodnrazaczdozamkow30mlwizual2019-04.jpeg",
    "PL-IMP-PEN2000": "https://www.orlen.pl/pl/dla-biznesu/produkty/plyny-i-chemia-motoryzacyjna/chemia-i-kosmetyki-samochodowe/platinum-impact-penetrol-2000/_jcr_content/root/container/container/container/container_392034022/container/image.coreimg.jpeg/1706207654420/20190430platinumimpactpenetrol2000100mlwizual2019-04.jpeg",
    "PL-IMP-WNCLN": "https://www.orlen.pl/pl/dla-biznesu/produkty/plyny-i-chemia-motoryzacyjna/chemia-i-kosmetyki-samochodowe/platinum-impact-plyn-do-mycia-szyb/_jcr_content/root/container/container/container/container_1069146863/container/image.coreimg.png/1706207660043/impact-do-mycia-szyb-500ml.png",
    "PL-IMP-UPHOL": "https://www.orlen.pl/pl/dla-biznesu/produkty/plyny-i-chemia-motoryzacyjna/chemia-i-kosmetyki-samochodowe/platinum-impact-plyn-do-usuwania-owadow/_jcr_content/root/container/container/container/container_1843220613/container/image.coreimg.png/1706207657860/impact-do-owadow-500ml.png",
    "PL-IMP-SIL": "https://www.orlen.pl/pl/dla-biznesu/produkty/plyny-i-chemia-motoryzacyjna/chemia-i-kosmetyki-samochodowe/platinum-impact-silikon-do-uszczelek/_jcr_content/root/container/container/container/container_2134188116/container/image.coreimg.png/1706207649752/platinumimpactsilikonsilikonx2.png",
    "PL-IMP-SHAMP": "https://www.orlen.pl/pl/dla-biznesu/produkty/plyny-i-chemia-motoryzacyjna/chemia-i-kosmetyki-samochodowe/platinum-impact-cockpit-spray/_jcr_content/root/container/container/container/container/container/image.coreimg.png/1706286600581/platinumimpactspraylesny400ml2019-04.png",
    "PL-IMP-WAXM": "https://www.orlen.pl/pl/dla-biznesu/produkty/plyny-i-chemia-motoryzacyjna/chemia-i-kosmetyki-samochodowe/platinum-impact-cockpit-spray/_jcr_content/root/container/container/container/container/container/image.coreimg.png/1706286600581/platinumimpactspraylesny400ml2019-04.png",
    "PL-IMP-RIM": "https://www.orlen.pl/pl/dla-biznesu/produkty/plyny-i-chemia-motoryzacyjna/chemia-i-kosmetyki-samochodowe/platinum-impact-plyn-do-czyszczenia-felg/_jcr_content/root/container/container/container/container_1634406930/container/image.coreimg.png/1706207646188/impact-do-felg-500ml.png",
    "PL-IMP-TYRE": "https://www.orlen.pl/pl/dla-biznesu/produkty/plyny-i-chemia-motoryzacyjna/chemia-i-kosmetyki-samochodowe/platinum-impact-silikon-do-uszczelek/_jcr_content/root/container/container/container/container_2134188116/container/image.coreimg.png/1706207649752/platinumimpactsilikonsilikonx2.png",
    "HP-G4-80W90": "https://oferta.orlenoil.com/media/ftybpve0/orlen-oil-hipol-gl-4-80w-90-5l.png",
    "HP-G4-85W140": "https://www.orlenoil.pl/PL/NaszaOferta/Produkty/PublishingImages/beczkaorlenoil205l.jpg",
    "HP-MF-80W90": "https://oferta.orlenoil.com/media/jlhd2iyc/mockup_orlen-oil-hipol-mf-80w-90-1l-komplet-ne240109_qso828b1p_qso828b1r-01.png",
    "HP-ATFIID": "https://oferta.orlenoil.com/media/igkfihly/orlen-oil-hipol-atf-ii-d-5l.png",
    "HP-ATFIIE": "https://www.orlenoil.pl/PL/NaszaOferta/Produkty/PublishingImages/hipol_ATF-II-E_5L.png",
    "OR-HYD-LAN32": "https://techmot24.eu/13796-large_default/hydrol-l-hv-32-ka-p-20l.jpg",
    "OR-HYD-LAN46": "https://techmot24.eu/13796-large_default/hydrol-l-hv-32-ka-p-20l.jpg",
    "OR-HYD-LAN68": "https://techmot24.eu/13796-large_default/hydrol-l-hv-32-ka-p-20l.jpg",
    "OR-HYD-LAN100": "https://techmot24.eu/13796-large_default/hydrol-l-hv-32-ka-p-20l.jpg",
    "OR-HYD-LHM32": "https://techmot24.eu/13796-large_default/hydrol-l-hv-32-ka-p-20l.jpg",
    "OR-HYD-LHM46": "https://techmot24.eu/13796-large_default/hydrol-l-hv-32-ka-p-20l.jpg",
    "OR-HYD-LHM68": "https://techmot24.eu/13796-large_default/hydrol-l-hv-32-ka-p-20l.jpg",
    "OR-HYD-LHM100": "https://techmot24.eu/13796-large_default/hydrol-l-hv-32-ka-p-20l.jpg",
    "OR-HYD-LHV32": "https://techmot24.eu/13796-large_default/hydrol-l-hv-32-ka-p-20l.jpg",
    "OR-HYD-LHV46": "https://techmot24.eu/13796-large_default/hydrol-l-hv-32-ka-p-20l.jpg",
    "OR-HYD-LHV68": "https://techmot24.eu/13796-large_default/hydrol-l-hv-32-ka-p-20l.jpg",
    "OR-HYD-LHV100": "https://techmot24.eu/13796-large_default/hydrol-l-hv-32-ka-p-20l.jpg",
    "OR-HYD-LHS32": "https://techmot24.eu/13796-large_default/hydrol-l-hv-32-ka-p-20l.jpg",
    "OR-HYD-LHS46": "https://techmot24.eu/13796-large_default/hydrol-l-hv-32-ka-p-20l.jpg",
    "OR-HYD-LHS68": "https://techmot24.eu/13796-large_default/hydrol-l-hv-32-ka-p-20l.jpg",
    "OR-HYD-LHS100": "https://techmot24.eu/13796-large_default/hydrol-l-hv-32-ka-p-20l.jpg",
    "OR-HYD-LHL32": "https://techmot24.eu/13796-large_default/hydrol-l-hv-32-ka-p-20l.jpg",
    "OR-HYD-LHL46": "https://techmot24.eu/13796-large_default/hydrol-l-hv-32-ka-p-20l.jpg",
    "OR-HYD-LHL68": "https://techmot24.eu/13796-large_default/hydrol-l-hv-32-ka-p-20l.jpg",
    "OR-HYD-LHL100": "https://techmot24.eu/13796-large_default/hydrol-l-hv-32-ka-p-20l.jpg",
    "OR-HYD-LHG32": "https://techmot24.eu/13796-large_default/hydrol-l-hv-32-ka-p-20l.jpg",
    "OR-HYD-LHG46": "https://techmot24.eu/13796-large_default/hydrol-l-hv-32-ka-p-20l.jpg",
    "OR-HYD-LHG68": "https://techmot24.eu/13796-large_default/hydrol-l-hv-32-ka-p-20l.jpg",
    "OR-HYD-LHG100": "https://techmot24.eu/13796-large_default/hydrol-l-hv-32-ka-p-20l.jpg",
    "OR-HYD-LHFA32": "https://techmot24.eu/13796-large_default/hydrol-l-hv-32-ka-p-20l.jpg",
    "OR-HYD-LHFA46": "https://techmot24.eu/13796-large_default/hydrol-l-hv-32-ka-p-20l.jpg",
    "OR-HYD-LHFA68": "https://techmot24.eu/13796-large_default/hydrol-l-hv-32-ka-p-20l.jpg",
    "OR-HYD-LHFA100": "https://techmot24.eu/13796-large_default/hydrol-l-hv-32-ka-p-20l.jpg",
    "OR-HYD-LHFB32": "https://techmot24.eu/13796-large_default/hydrol-l-hv-32-ka-p-20l.jpg",
    "OR-HYD-LHFB46": "https://techmot24.eu/13796-large_default/hydrol-l-hv-32-ka-p-20l.jpg",
    "OR-HYD-LHFB68": "https://techmot24.eu/13796-large_default/hydrol-l-hv-32-ka-p-20l.jpg",
    "OR-HYD-LHFB100": "https://techmot24.eu/13796-large_default/hydrol-l-hv-32-ka-p-20l.jpg",
    "OR-HYD-LHFC32": "https://techmot24.eu/13796-large_default/hydrol-l-hv-32-ka-p-20l.jpg",
    "OR-HYD-LHFC46": "https://techmot24.eu/13796-large_default/hydrol-l-hv-32-ka-p-20l.jpg",
    "OR-HYD-LHFC68": "https://techmot24.eu/13796-large_default/hydrol-l-hv-32-ka-p-20l.jpg",
    "OR-HYD-LHFC100": "https://techmot24.eu/13796-large_default/hydrol-l-hv-32-ka-p-20l.jpg",
    "OR-HYD-LHFD32": "https://techmot24.eu/13796-large_default/hydrol-l-hv-32-ka-p-20l.jpg",
    "OR-HYD-LHFD46": "https://techmot24.eu/13796-large_default/hydrol-l-hv-32-ka-p-20l.jpg",
    "OR-HYD-LHFD68": "https://techmot24.eu/13796-large_default/hydrol-l-hv-32-ka-p-20l.jpg",
    "OR-HYD-LHFD100": "https://techmot24.eu/13796-large_default/hydrol-l-hv-32-ka-p-20l.jpg",
}

updated = 0
not_found = []

for sku, img_url in image_map.items():
    pattern = r'(sku:\s*"' + re.escape(sku) + r'".*?images:\s*\[)\s*null,\s*null,\s*null(\s*\])'
    replacement = r'\1\n      "' + img_url + r'",\n      null,\n      null\n    \2'
    new_content, n = re.subn(pattern, replacement, content, flags=re.DOTALL)
    if n > 0:
        content = new_content
        updated += 1
        print(f"Updated: {sku}")
    else:
        not_found.append(sku)
        print(f"NOT FOUND or already has image: {sku}")

with open(catalog_path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"\nDone! Updated {updated} products.")
if not_found:
    print(f"Not found/skipped: {not_found}")

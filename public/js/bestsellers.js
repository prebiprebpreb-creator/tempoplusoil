// Best sellers showcase + order-form prefill.
// Exposes window.prefillProduct(name, qty?) so any "Add to Order" button on the
// site — or a ?product=...&qty=... URL param — can populate the Store form.
(function () {
  'use strict';

  const BESTSELLERS = [
    {
      name: "Platinum MaxExpert C3 5W-40",
      category: "passenger", categoryLabel: "Passenger Cars",
      image: "images/catalog/PL-MAX-5W40.webp",
      blurb: "Full synthetic ACEA C3 oil for BMW, Mercedes-Benz and VW Group engines — low-SAPS formula protects DPF and catalysts."
    },
    {
      name: "Orlen Oil Platinum MaxExpert F 5W-30",
      category: "passenger", categoryLabel: "Passenger Cars",
      image: "https://oferta.orlenoil.com/media/vqxd5xjc/orlen-oil-max-expert-f-5w-30-4l-etykieta-ne231128_qso893b4p_q-20x.png",
      blurb: "Low-SAPS synthetic engineered for Euro 5 / Euro 6 vehicles with DPF and three-way catalysts."
    },
    {
      name: "Orlen Oil Platinum Ultor Progress 10W-40",
      category: "truck", categoryLabel: "Trucks & HGV",
      image: "https://oferta.orlenoil.com/media/ywskeqkb/et-ooil-ultor-progress-10w-40-20l_ne250609.png",
      blurb: "Heavy-duty semi-synthetic for trucks and fleet vehicles — extended drain intervals under hard use."
    },
    {
      name: "Hydrol L-HV 46",
      category: "industrial", categoryLabel: "Industrial",
      image: "images/catalog/PL-HYD-46.webp",
      blurb: "High-VI hydraulic oil for industrial and mobile machinery — excellent anti-wear, anti-foam and wide temperature performance."
    },
    {
      name: "Orlen Oil Platinum Gear SX 75W-90",
      category: "transmission", categoryLabel: "Transmission",
      image: "https://oferta.orlenoil.com/media/nqnbtjgo/orlen-oil-gear-sx-75w-90-20l-etykieta-pr-ne240126_qso888k2r_r.png",
      blurb: "Full synthetic gear oil for manual transmissions — smooth shifting and shock-load protection."
    },
    {
      name: "Orlen Oil Agro Supreme 10W-40",
      category: "agri", categoryLabel: "Agriculture",
      image: "https://oferta.orlenoil.com/media/f02htut0/orlen-oil-agro-supreme-10w-40-5l.png",
      blurb: "Premium semi-synthetic STOU for modern tractors — engine, transmission, hydraulics and wet brakes."
    }
  ];

  // SVG bottle fallback (same palette / layout as catalog cards).
  const CATEGORY_COLORS = {
    passenger:    { top:'#c4541a', body:'#ea6a1f', accent:'#fff7ee' },
    truck:        { top:'#3a1c08', body:'#6b3410', accent:'#f4e6d4' },
    motorcycle:   { top:'#8a1f1f', body:'#c62828', accent:'#ffe4e4' },
    agri:         { top:'#1f5e2e', body:'#2e8b3e', accent:'#e4f5e6' },
    industrial:   { top:'#0f3a5c', body:'#1e6091', accent:'#e1eef9' },
    transmission: { top:'#3d1f5e', body:'#6b2c91', accent:'#efe4f9' }
  };
  function extractGrade(name) {
    const m = name.match(/\b(\d+W[-‐]?\d+|ISO\s*VG\s*\d+|EP\s*\d+|L[-‐]?H[MV]?\s*\d+)\b/i);
    return m ? m[0].toUpperCase().replace(/\s+/g, ' ') : '';
  }
  function productSvg(p, idx) {
    const c = CATEGORY_COLORS[p.category] || CATEGORY_COLORS.passenger;
    const grade = extractGrade(p.name);
    const id = 'bs-' + idx;
    return `
<svg viewBox="0 0 160 200" xmlns="http://www.w3.org/2000/svg" class="bottle-svg" aria-hidden="true">
  <defs>
    <linearGradient id="b-${id}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="${c.body}"/><stop offset="1" stop-color="${c.top}"/>
    </linearGradient>
    <linearGradient id="s-${id}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="rgba(255,255,255,.3)"/><stop offset=".5" stop-color="rgba(255,255,255,0)"/>
    </linearGradient>
  </defs>
  <rect x="62" y="4" width="36" height="22" rx="3" fill="${c.top}"/>
  <rect x="62" y="4" width="36" height="5" rx="2" fill="rgba(0,0,0,.25)"/>
  <rect x="68" y="24" width="24" height="10" fill="${c.top}"/>
  <path d="M 40 34 Q 40 30 44 30 L 116 30 Q 120 30 120 34 L 126 58 Q 130 62 130 70 L 130 184 Q 130 194 120 194 L 40 194 Q 30 194 30 184 L 30 70 Q 30 62 34 58 Z"
        fill="url(#b-${id})" stroke="rgba(0,0,0,.15)" stroke-width="1"/>
  <rect x="40" y="82" width="80" height="88" rx="3" fill="${c.accent}" stroke="rgba(0,0,0,.08)"/>
  <text x="80" y="102" text-anchor="middle" font-family="Barlow Condensed, Arial, sans-serif"
        font-weight="800" font-size="13" fill="${c.top}" letter-spacing="1.2">ORLEN OIL</text>
  <line x1="48" y1="108" x2="112" y2="108" stroke="${c.body}" stroke-width="1.2"/>
  ${grade
    ? `<text x="80" y="138" text-anchor="middle" font-family="Barlow Condensed, Arial, sans-serif"
             font-weight="800" font-size="20" fill="${c.top}">${grade}</text>`
    : `<text x="80" y="136" text-anchor="middle" font-family="Barlow Condensed, Arial, sans-serif"
             font-weight="800" font-size="14" fill="${c.top}">PREMIUM</text>`}
  <text x="80" y="158" text-anchor="middle" font-family="Inter, Arial, sans-serif"
        font-weight="600" font-size="7" fill="${c.body}" letter-spacing=".8">${(p.categoryLabel || '').toUpperCase()}</text>
  <rect x="34" y="36" width="16" height="152" rx="6" fill="url(#s-${id})"/>
</svg>`;
  }

  // ---------- Render grid ----------
  const grid = document.getElementById('bestsellerGrid');
  if (grid) {
    grid.innerHTML = BESTSELLERS.map((p, i) => `
      <article class="bestseller-card">
        <div class="bestseller-img">
          ${p.image
            ? `<img src="${p.image}" alt="${p.name}" loading="lazy"
                   onerror="this.outerHTML=this.dataset.fallback;" data-fallback='${productSvg(p, i).replace(/'/g, "&#39;")}' />`
            : productSvg(p, i)}
        </div>
        <div class="bestseller-body">
          <h3>${p.name}</h3>
          <p>${p.blurb}</p>
          <button type="button" class="btn btn-primary bestseller-add"
                  data-name="${p.name.replace(/"/g, '&quot;')}">Add to Order</button>
        </div>
      </article>
    `).join('');

    grid.querySelectorAll('.bestseller-add').forEach(btn => {
      btn.addEventListener('click', () => {
        window.prefillProduct(btn.dataset.name);
      });
    });
  }

  // ---------- Prefill helper ----------
  window.prefillProduct = function (name, qty) {
    const productField = document.getElementById('productField');
    const quantityField = document.getElementById('quantityField');
    if (productField) {
      productField.value = name || '';
      productField.classList.add('prefill-flash');
      setTimeout(() => productField.classList.remove('prefill-flash'), 1600);
    }
    if (qty && quantityField) quantityField.value = qty;

    const order = document.getElementById('order');
    if (order) order.scrollIntoView({ behavior: 'smooth', block: 'start' });

    // Optional: focus the product field shortly after scroll
    setTimeout(() => productField && productField.focus({ preventScroll: true }), 600);
  };

  // ---------- URL query param ----------
  const params = new URLSearchParams(window.location.search);
  const qpProduct = params.get('product');
  const qpQty = params.get('qty') || params.get('quantity');
  if (qpProduct) {
    // small delay so layout is ready before scrolling
    window.addEventListener('load', () => window.prefillProduct(qpProduct, qpQty));
  }
})();

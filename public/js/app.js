// Tempo Plus — client-side app: catalog rendering, filters, cart, order submit.
(function () {
  'use strict';

  const catalog = window.ORLEN_CATALOG || [];
  const cart = loadCart();

  // ---------- DOM ----------
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));

  const grid = $('#productGrid');
  const filters = $$('.cat-link');
  const searchInput = $('#shopSearch');
  const resultsCount = $('#resultsCount');
  const noResults = $('#noResults');
  const sidebar = document.querySelector('.shop-sidebar');
  const filterToggle = $('#shopFilterToggle');
  const cartCountEl = $('#cartCount');
  const cartBody = $('#cartBody');
  const cartSummary = $('#cartSummary');
  const drawer = $('#cartDrawer');
  const overlay = $('#overlay');
  const orderForm = $('#orderForm');
  const formStatus = $('#formStatus');
  const submitBtn = $('#submitBtn');

  $('#year').textContent = new Date().getFullYear();

  // ---------- Mobile nav ----------
  const hamburgerBtn = $('#hamburger');
  const mainNavEl = $('#mainNav');
  hamburgerBtn.addEventListener('click', () => {
    const isOpen = mainNavEl.classList.toggle('open');
    hamburgerBtn.setAttribute('aria-expanded', isOpen);
  });
  $$('#mainNav a').forEach(a => a.addEventListener('click', () => {
    mainNavEl.classList.remove('open');
    hamburgerBtn.setAttribute('aria-expanded', 'false');
  }));

  // ---------- Render catalog ----------
  let currentFilter = 'all';
  let currentQuery = '';
  let visibleCount = 9;

  function matchesSearch(p, q) {
    if (!q) return true;
    const hay = (p.name + ' ' + p.sku + ' ' + p.specs + ' ' + p.categoryLabel).toLowerCase();
    return q.toLowerCase().split(/\s+/).filter(Boolean).every(tok => hay.includes(tok));
  }

  // Per-category color palette for the SVG bottle fallback.
  const CATEGORY_COLORS = {
    passenger:    { top:'#c4541a', body:'#ea6a1f', accent:'#fff7ee' },
    truck:        { top:'#3a1c08', body:'#6b3410', accent:'#f4e6d4' },
    motorcycle:   { top:'#8a1f1f', body:'#c62828', accent:'#ffe4e4' },
    agri:         { top:'#1f5e2e', body:'#2e8b3e', accent:'#e4f5e6' },
    industrial:   { top:'#0f3a5c', body:'#1e6091', accent:'#e1eef9' },
    transmission: { top:'#3d1f5e', body:'#6b2c91', accent:'#efe4f9' },
    coolant:      { top:'#085f6e', body:'#0e8fa3', accent:'#e0f7fa' },
    brake:        { top:'#7b0000', body:'#b71c1c', accent:'#ffebee' },
    grease:       { top:'#2d2d2d', body:'#555555', accent:'#f5f5f5' },
    cosmetics:    { top:'#5c1a6e', body:'#8e24aa', accent:'#f3e5f5' },
    forestry:     { top:'#1b4d1e', body:'#388e3c', accent:'#e8f5e9' }
  };

  // Extract a short badge (viscosity grade or ISO code) from the product name.
  function extractGrade(name) {
    const m = name.match(/\b(\d+W[-‐]?\d+|ISO\s*VG\s*\d+|G\d+\+?\+?|CI[-‐]?\d+)\b/i)
           || name.match(/\b\d+W\d+\b/);
    return m ? m[0].toUpperCase().replace(/\s+/g, ' ') : '';
  }

  function productSvg(p) {
    const c = CATEGORY_COLORS[p.category] || CATEGORY_COLORS.passenger;
    const grade = extractGrade(p.name);
    return `
<svg viewBox="0 0 160 200" xmlns="http://www.w3.org/2000/svg" class="bottle-svg" aria-hidden="true">
  <defs>
    <linearGradient id="b-${p.sku}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="${c.body}"/>
      <stop offset="1" stop-color="${c.top}"/>
    </linearGradient>
    <linearGradient id="s-${p.sku}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="rgba(255,255,255,.3)"/>
      <stop offset=".5" stop-color="rgba(255,255,255,0)"/>
    </linearGradient>
  </defs>
  <!-- cap -->
  <rect x="62" y="4" width="36" height="22" rx="3" fill="${c.top}"/>
  <rect x="62" y="4" width="36" height="5" rx="2" fill="rgba(0,0,0,.25)"/>
  <!-- neck -->
  <rect x="68" y="24" width="24" height="10" fill="${c.top}"/>
  <!-- body -->
  <path d="M 40 34 Q 40 30 44 30 L 116 30 Q 120 30 120 34 L 126 58 Q 130 62 130 70 L 130 184 Q 130 194 120 194 L 40 194 Q 30 194 30 184 L 30 70 Q 30 62 34 58 Z"
        fill="url(#b-${p.sku})" stroke="rgba(0,0,0,.15)" stroke-width="1"/>
  <!-- label -->
  <rect x="40" y="82" width="80" height="88" rx="3" fill="${c.accent}" stroke="rgba(0,0,0,.08)"/>
  <text x="80" y="102" text-anchor="middle" font-family="Barlow Condensed, Arial, sans-serif"
        font-weight="800" font-size="13" fill="${c.top}" letter-spacing="1.2">ORLEN OIL</text>
  <line x1="48" y1="108" x2="112" y2="108" stroke="${c.body}" stroke-width="1.2"/>
  ${grade
    ? `<text x="80" y="138" text-anchor="middle" font-family="Barlow Condensed, Arial, sans-serif"
             font-weight="800" font-size="22" fill="${c.top}">${grade}</text>`
    : `<text x="80" y="136" text-anchor="middle" font-family="Barlow Condensed, Arial, sans-serif"
             font-weight="800" font-size="14" fill="${c.top}">PREMIUM</text>`}
  <text x="80" y="158" text-anchor="middle" font-family="Inter, Arial, sans-serif"
        font-weight="600" font-size="7" fill="${c.body}" letter-spacing=".8">${(p.categoryLabel || '').toUpperCase()}</text>
  <!-- highlight -->
  <rect x="34" y="36" width="16" height="152" rx="6" fill="url(#s-${p.sku})"/>
</svg>`;
  }

  function makeCard(p) {
    const frontImg = p.images ? p.images[0] : p.image;
    return `
      <article class="product-card" data-category="${p.category}" data-sku="${p.sku}" role="button" tabindex="0" aria-label="View details for ${p.name}">
        <div class="product-img">
          ${frontImg
            ? `<img src="${frontImg}" alt="${p.name}" loading="lazy"
                   onerror="this.outerHTML=this.dataset.fallback;" data-fallback='${productSvg(p).replace(/'/g, "&#39;")}' />`
            : productSvg(p)}
          ${p.badge ? `<span class="product-badge">${p.badge}</span>` : ''}
        </div>
        <div class="product-info">
          <span class="product-category">${p.categoryLabel}</span>
          <h3 class="product-name">${p.name}</h3>
          <div class="product-sku">SKU: ${p.sku}</div>
          <div class="product-spec-tags">
            ${p.specs.split(' · ').map(s => `<span class="spec-tag">${s}</span>`).join('')}
          </div>
          <div class="product-sizes" data-sku="${p.sku}">
            ${p.sizes.map((s, i) => `<span class="size-pill ${i === 0 ? 'active' : ''}" data-size="${s}">${s}</span>`).join('')}
          </div>
          <button class="add-btn" data-sku="${p.sku}">Add to Order</button>
        </div>
      </article>`;
  }

  // Event delegation — wired once, works for all dynamically added cards
  grid.addEventListener('click', e => {
    const sizePill = e.target.closest('.size-pill');
    if (sizePill) {
      e.stopPropagation();
      $$('.size-pill', sizePill.parentElement).forEach(x => x.classList.remove('active'));
      sizePill.classList.add('active');
      return;
    }
    const addBtn = e.target.closest('.add-btn');
    if (addBtn) {
      e.stopPropagation();
      const product = catalog.find(p => p.sku === addBtn.dataset.sku);
      const info = addBtn.closest('.product-info');
      const sz = info ? info.querySelector('.size-pill.active') : null;
      addToCart(product, sz ? sz.dataset.size : product.sizes[0]);
      openDrawer();
      return;
    }
    const card = e.target.closest('.product-card');
    if (card) openProductModal(card.dataset.sku);
  });
  grid.addEventListener('keydown', e => {
    if ((e.key === 'Enter' || e.key === ' ') && e.target.matches('.product-card')) {
      e.preventDefault();
      openProductModal(e.target.dataset.sku);
    }
  });

  function renderCatalog(appendFrom, resetScroll = false) {
    const items = catalog.filter(p =>
      (currentFilter === 'all' || p.category === currentFilter) &&
      matchesSearch(p, currentQuery)
    );
    const visible = items.slice(0, visibleCount);
    const hasMore = items.length > visibleCount;

    if (appendFrom !== undefined) {
      // Append new cards only — no height collapse, no scroll jump
      items.slice(appendFrom, visibleCount).forEach((p, idx) => {
        const tpl = document.createElement('template');
        tpl.innerHTML = makeCard(p).trim();
        const card = tpl.content.firstElementChild;
        card.style.animationDelay = `${idx * 50}ms`;
        card.classList.add('card-anim');
        grid.appendChild(card);
      });
    } else if (resetScroll) {
      // Category filter change: render then scroll to catalog section
      grid.innerHTML = visible.map(makeCard).join('');
      requestAnimationFrame(() => {
        const shopEl = document.getElementById('shop');
        if (shopEl) shopEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
        grid.querySelectorAll('.product-card').forEach((c, i) => {
          c.style.animationDelay = `${Math.min(i * 45, 315)}ms`;
          c.classList.add('card-anim');
        });
      });
    } else {
      // Full replace: lock min-height to prevent collapse, restore scroll
      const savedY = window.scrollY;
      const curH = grid.offsetHeight;
      if (curH > 0) grid.style.minHeight = `${curH}px`;
      grid.innerHTML = visible.map(makeCard).join('');
      requestAnimationFrame(() => {
        grid.style.minHeight = '';
        window.scrollTo(0, savedY);
        grid.querySelectorAll('.product-card').forEach((c, i) => {
          c.style.animationDelay = `${Math.min(i * 45, 315)}ms`;
          c.classList.add('card-anim');
        });
      });
    }

    if (resultsCount) {
      resultsCount.textContent = hasMore
        ? `Showing ${visible.length} of ${items.length} products`
        : `${items.length} product${items.length === 1 ? '' : 's'}`;
    }
    if (noResults) noResults.hidden = items.length > 0;

    // Rebuild See More button
    const oldWrap = document.getElementById('seeMoreWrap');
    if (oldWrap) oldWrap.remove();
    if (hasMore) {
      const wrap = document.createElement('div');
      wrap.id = 'seeMoreWrap';
      wrap.className = 'see-more-wrap';
      wrap.innerHTML = `<button class="see-more-btn">Show More Products <span class="see-more-count">${items.length - visibleCount} remaining</span></button>`;
      grid.after(wrap);
      wrap.querySelector('.see-more-btn').addEventListener('click', () => {
        const prev = visibleCount;
        visibleCount += 9;
        renderCatalog(prev); // append mode — no collapse
      });
    }
  }

  filters.forEach(b => b.addEventListener('click', () => {
    filters.forEach(x => x.classList.remove('active'));
    b.classList.add('active');
    currentFilter = b.dataset.filter;
    visibleCount = 9;
    renderCatalog(undefined, true);
    if (sidebar) sidebar.classList.remove('open');
  }));

  if (searchInput) {
    let searchTimer;
    searchInput.addEventListener('input', () => {
      clearTimeout(searchTimer);
      searchTimer = setTimeout(() => {
        currentQuery = searchInput.value.trim();
        visibleCount = 9;
        renderCatalog();
      }, 120);
    });
  }

  if (filterToggle && sidebar) {
    filterToggle.addEventListener('click', (e) => {
      e.stopPropagation();
      sidebar.classList.toggle('open');
    });
    document.addEventListener('click', (e) => {
      if (sidebar.classList.contains('open') && !sidebar.contains(e.target) && e.target !== filterToggle) {
        sidebar.classList.remove('open');
      }
    });
  }

  // Populate category counts from actual catalog
  $$('.cat-count').forEach(el => {
    const key = el.dataset.count;
    const n = key === 'all' ? catalog.length : catalog.filter(p => p.category === key).length;
    el.textContent = n;
  });

  // ---------- Cart ----------
  function loadCart() {
    try { return JSON.parse(localStorage.getItem('tp_cart') || '[]'); }
    catch { return []; }
  }
  function saveCart() { localStorage.setItem('tp_cart', JSON.stringify(cart)); }

  function addToCart(product, size) {
    const key = product.sku + '|' + size;
    const existing = cart.find(i => i.key === key);
    if (existing) existing.qty += 1;
    else cart.push({ key, sku: product.sku, name: product.name, size, qty: 1 });
    saveCart();
    renderCart();
  }

  function updateQty(key, delta) {
    const item = cart.find(i => i.key === key);
    if (!item) return;
    item.qty = Math.max(1, item.qty + delta);
    saveCart();
    renderCart();
  }
  function setQty(key, qty) {
    const item = cart.find(i => i.key === key);
    if (!item) return;
    const q = Math.max(1, Math.min(10000, parseInt(qty, 10) || 1));
    item.qty = q;
    saveCart();
    renderCart();
  }
  function removeItem(key) {
    const idx = cart.findIndex(i => i.key === key);
    if (idx > -1) cart.splice(idx, 1);
    saveCart();
    renderCart();
  }

  function renderCart() {
    const totalUnits = cart.reduce((s, i) => s + i.qty, 0);
    cartCountEl.textContent = totalUnits;

    const rowsHtml = cart.length === 0
      ? '<p class="empty-cart">Your cart is empty.</p>'
      : cart.map(i => `
        <div class="cart-item">
          <div class="cart-item-info">
            <div class="cart-item-name">${i.name}</div>
            <div class="cart-item-meta">${i.sku} · ${i.size}</div>
          </div>
          <div class="qty-ctrl">
            <button data-act="dec" data-key="${i.key}">−</button>
            <input type="number" min="1" max="10000" value="${i.qty}" data-key="${i.key}" />
            <button data-act="inc" data-key="${i.key}">+</button>
          </div>
          <button class="remove-btn" data-act="rm" data-key="${i.key}" aria-label="Remove">✕</button>
        </div>`).join('') +
      `<div class="cart-total"><span>Total Units</span><span>${totalUnits}</span></div>`;

    cartBody.innerHTML = rowsHtml;
    cartSummary.innerHTML = cart.length === 0
      ? '<p class="empty-cart">Your cart is empty — add products from the catalog above.</p>'
      : rowsHtml;

    // Wire cart controls (in both drawer and summary)
    $$('[data-act]').forEach(el => {
      el.addEventListener('click', () => {
        const key = el.dataset.key;
        const act = el.dataset.act;
        if (act === 'inc') updateQty(key, +1);
        else if (act === 'dec') updateQty(key, -1);
        else if (act === 'rm') removeItem(key);
      });
    });
    $$('input[type=number][data-key]').forEach(inp => {
      inp.addEventListener('change', () => setQty(inp.dataset.key, inp.value));
    });
  }

  // ---------- Drawer ----------
  function openDrawer() { drawer.classList.add('open'); overlay.classList.add('show'); }
  function closeDrawer() { drawer.classList.remove('open'); overlay.classList.remove('show'); }
  $('#openCartBtn').addEventListener('click', openDrawer);
  $('#closeCartBtn').addEventListener('click', closeDrawer);
  $('#gotoOrderBtn').addEventListener('click', closeDrawer);
  overlay.addEventListener('click', closeDrawer);

  // ---------- Order type switch (Individual / Company) ----------
  const businessFields = $('#businessFields');
  const companyField = $('#companyField');
  const vatField = $('#vatField');
  $$('input[name="orderType"]').forEach(radio => {
    radio.addEventListener('change', () => {
      const isCompany = radio.value === 'company';
      if (businessFields) businessFields.hidden = !isCompany;
      if (companyField) companyField.required = isCompany;
      if (vatField) vatField.required = isCompany;
      if (isCompany && companyField) setTimeout(() => companyField.focus(), 50);
    });
  });

  // ---------- Submit order ----------
  orderForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    formStatus.className = 'form-status';
    formStatus.textContent = '';

    if (cart.length === 0) {
      formStatus.className = 'form-status error';
      formStatus.textContent = 'Your cart is empty. Please add at least one product.';
      return;
    }

    const fd = new FormData(orderForm);
    const customer = Object.fromEntries(fd.entries());
    const notes = customer.notes || '';
    delete customer.notes;

    const payload = {
      customer,
      items: cart.map(i => ({ sku: i.sku, name: i.name, size: i.size, qty: i.qty })),
      notes
    };

    submitBtn.disabled = true;
    submitBtn.textContent = 'Sending…';

    try {
      const res = await fetch('/api/order', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      if (!res.ok || !data.ok) throw new Error(data.error || 'Submission failed');

      formStatus.className = 'form-status success';
      formStatus.textContent = '✓ ' + (data.message || 'Order sent successfully!');
      orderForm.reset();
      cart.length = 0;
      saveCart();
      renderCart();
    } catch (err) {
      formStatus.className = 'form-status error';
      formStatus.textContent = '✗ ' + err.message + ' — Please call +383 49 499 507.';
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = 'Submit Order';
    }
  });

  // ---------- Product Modal ----------
  const pmodal        = document.getElementById('pmodal');
  const pmodalClose   = document.getElementById('pmodalClose');
  const pmodalImg     = document.getElementById('pmodalImg');
  const pmodalPH      = document.getElementById('pmodalPlaceholder');
  const pmodalPHText  = document.getElementById('pmodalPlaceholderText');
  const pmodalCat     = document.getElementById('pmodalCat');
  const pmodalType    = document.getElementById('pmodalType');
  const pmodalName    = document.getElementById('pmodalName');
  const pmodalSku     = document.getElementById('pmodalSku');
  const pmodalDesc    = document.getElementById('pmodalDesc');
  const pmodalSpecs   = document.getElementById('pmodalSpecs');
  const pmodalSizes   = document.getElementById('pmodalSizes');
  const pmodalAdd     = document.getElementById('pmodalAdd');

  const THUMB_LABELS = ['Front', 'Back', 'Info Label'];
  const THUMB_ICONS  = ['🖼', '↩', '🏷'];
  let   modalProduct = null;
  let   modalImages  = [];
  let   activeIdx    = 0;

  function setModalImage(idx) {
    activeIdx = idx;
    $$('.pmodal-thumb').forEach((t, i) => t.classList.toggle('active', i === idx));

    const src = modalImages[idx];
    if (src) {
      pmodalImg.src = src;
      pmodalImg.alt = modalProduct.name + ' — ' + THUMB_LABELS[idx];
      pmodalImg.hidden = false;
      pmodalPH.hidden = true;
      pmodalImg.onerror = () => {
        pmodalImg.hidden = true;
        pmodalPH.hidden = false;
        pmodalPHText.textContent = THUMB_LABELS[idx] + ' image not available';
      };
    } else {
      pmodalImg.hidden = true;
      pmodalPH.hidden = false;
      pmodalPHText.textContent = THUMB_LABELS[idx] + ' image not available';
    }
  }

  function openProductModal(sku) {
    const p = catalog.find(x => x.sku === sku);
    if (!p) return;
    modalProduct = p;
    modalImages  = (p.images && p.images.length === 3) ? p.images
                   : [p.image || null, null, null];

    // Badges
    pmodalCat.textContent  = p.categoryLabel;
    pmodalType.textContent = p.type || p.badge || '';
    pmodalName.textContent = p.name;
    pmodalSku.textContent  = 'SKU: ' + p.sku;
    pmodalDesc.textContent = p.description || '';

    // Spec pills — split by " · "
    pmodalSpecs.innerHTML = p.specs.split(' · ').map(s => {
      const isCert = /ACEA|API|SAE|ISO|VW|BMW|MB|MAN|Volvo|John|MF|JASO|FMVSS|DIN|MIL|NLGI|Allison|Dexron|dexos/i.test(s);
      return `<span class="pmodal-spec-pill${isCert ? ' cert' : ''}">${s}</span>`;
    }).join('');

    // Size pills
    pmodalSizes.innerHTML = p.sizes.map((s, i) =>
      `<button class="pmodal-size-pill${i === 0 ? ' active' : ''}" data-sz="${s}">${s}</button>`
    ).join('');
    $$('.pmodal-size-pill', pmodalSizes).forEach(btn => {
      btn.addEventListener('click', () => {
        $$('.pmodal-size-pill', pmodalSizes).forEach(x => x.classList.remove('active'));
        btn.classList.add('active');
      });
    });

    // Thumbnails
    [0, 1, 2].forEach(i => {
      const th = document.getElementById('pmodalThumb' + i);
      const src = modalImages[i];
      th.innerHTML = src
        ? `<img src="${src}" alt="${THUMB_LABELS[i]}" onerror="this.outerHTML='<span class=thumb-placeholder>${THUMB_ICONS[i]}</span>'" />`
        : `<span class="thumb-placeholder">${THUMB_ICONS[i]}</span>`;
    });

    // Add to order button
    pmodalAdd.onclick = () => {
      const activeSz = pmodalSizes.querySelector('.pmodal-size-pill.active');
      const size = activeSz ? activeSz.dataset.sz : p.sizes[0];
      addToCart(p, size);
      closeProductModal();
      openDrawer();
    };

    setModalImage(0);
    pmodal.removeAttribute('hidden');
    requestAnimationFrame(() => pmodal.classList.add('open'));
    document.body.style.overflow = 'hidden';
    pmodalClose.focus();
  }

  function closeProductModal() {
    pmodal.classList.remove('open');
    document.body.style.overflow = '';
    pmodal.addEventListener('transitionend', () => pmodal.setAttribute('hidden', ''), { once: true });
  }

  // Thumbnail click
  $$('.pmodal-thumb').forEach(btn => {
    btn.addEventListener('click', () => setModalImage(+btn.dataset.idx));
  });

  pmodalClose.addEventListener('click', closeProductModal);
  pmodal.addEventListener('click', e => { if (e.target === pmodal) closeProductModal(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && pmodal.classList.contains('open')) closeProductModal(); });

  // ---------- Init ----------
  renderCatalog();
  renderCart();

  // ---------- Scrolled header shadow ----------
  const headerEl = document.querySelector('.site-header');
  const onScroll = () => headerEl.classList.toggle('scrolled', window.scrollY > 20);
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // ---------- Section fade-in ----------
  const fadeObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        fadeObserver.unobserve(entry.target);
      }
    });
  }, { rootMargin: '0px 0px -60px 0px', threshold: 0.05 });
  $$('.section').forEach(el => {
    el.classList.add('fade-init');
    fadeObserver.observe(el);
  });

  // ---------- Active nav link on scroll ----------
  const allNavLinks = [
    ...$$('.nav-left a'),
    ...$$('.nav-right-links a'),
    ...$$('#mainNav a')
  ];
  const navSectionObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = '#' + entry.target.id;
        allNavLinks.forEach(link => {
          link.classList.toggle('active', link.getAttribute('href') === id);
        });
      }
    });
  }, { rootMargin: '-20% 0px -60% 0px' });
  $$('section[id]').forEach(s => navSectionObserver.observe(s));

  // ---------- Offline / online notification ----------
  const offlineBar = document.createElement('div');
  offlineBar.className = 'offline-bar';
  document.body.appendChild(offlineBar);
  window.addEventListener('offline', () => {
    offlineBar.textContent = '⚠ No internet connection';
    offlineBar.classList.add('show');
  });
  window.addEventListener('online', () => {
    offlineBar.textContent = '✓ Connection restored';
    setTimeout(() => offlineBar.classList.remove('show'), 2500);
  });
})();

// Tempo Plus - Orlen Distribution
// Express server + Nodemailer order routing
require('dotenv').config();

const express = require('express');
const path = require('path');
const nodemailer = require('nodemailer');
const rateLimit = require('express-rate-limit');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json({ limit: '100kb' }));
app.use(express.static(path.join(__dirname, 'public')));

// Rate limit: max 5 orders / 10 min per IP to prevent abuse
const orderLimiter = rateLimit({
  windowMs: 10 * 60 * 1000,
  max: 5,
  standardHeaders: true,
  legacyHeaders: false,
  message: { ok: false, error: 'Too many orders from this IP. Please try again later.' }
});

// ---- SMTP transporter ----
const transporter = nodemailer.createTransport({
  host: process.env.SMTP_HOST,
  port: Number(process.env.SMTP_PORT || 587),
  secure: String(process.env.SMTP_SECURE).toLowerCase() === 'true',
  auth: {
    user: process.env.SMTP_USER,
    pass: process.env.SMTP_PASS
  }
});

// Verify transport at startup (non-fatal)
transporter.verify().then(
  () => console.log('[mail] SMTP transporter ready'),
  (err) => console.warn('[mail] SMTP verification failed:', err.message)
);

// ---- Helpers ----
function escapeHtml(str = '') {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

function buildEmail(order) {
  const { customer, items, notes, totals } = order;
  const rows = items.map(it => `
    <tr>
      <td style="padding:8px;border:1px solid #e5d8c9;">${escapeHtml(it.name)}</td>
      <td style="padding:8px;border:1px solid #e5d8c9;">${escapeHtml(it.sku || '-')}</td>
      <td style="padding:8px;border:1px solid #e5d8c9;text-align:center;">${Number(it.qty)}</td>
      <td style="padding:8px;border:1px solid #e5d8c9;">${escapeHtml(it.size || '-')}</td>
    </tr>`).join('');

  const html = `
  <div style="font-family:Arial,sans-serif;color:#2a1d12;max-width:680px;margin:auto;">
    <div style="background:#d2691e;padding:18px 22px;color:#fff;">
      <h2 style="margin:0;">New Order — Tempo Plus (Orlen)</h2>
      <p style="margin:4px 0 0;font-size:13px;opacity:.9;">Received: ${new Date().toUTCString()}</p>
    </div>
    <div style="padding:20px;background:#fffaf3;">
      <h3 style="margin-top:0;color:#8b4513;">Customer</h3>
      <table style="width:100%;border-collapse:collapse;font-size:14px;">
        <tr><td style="padding:4px 0;width:140px;"><b>Name</b></td><td>${escapeHtml(customer.name)}</td></tr>
        <tr><td style="padding:4px 0;"><b>Company</b></td><td>${escapeHtml(customer.company || '-')}</td></tr>
        <tr><td style="padding:4px 0;"><b>Email</b></td><td>${escapeHtml(customer.email)}</td></tr>
        <tr><td style="padding:4px 0;"><b>Phone</b></td><td>${escapeHtml(customer.phone)}</td></tr>
        <tr><td style="padding:4px 0;"><b>Country</b></td><td>${escapeHtml(customer.country)}</td></tr>
        <tr><td style="padding:4px 0;"><b>Address</b></td><td>${escapeHtml(customer.address)}</td></tr>
        <tr><td style="padding:4px 0;"><b>City / Postcode</b></td><td>${escapeHtml(customer.city)} / ${escapeHtml(customer.postcode)}</td></tr>
      </table>

      <h3 style="color:#8b4513;">Items (${items.length})</h3>
      <table style="width:100%;border-collapse:collapse;font-size:14px;">
        <thead>
          <tr style="background:#f4e6d4;">
            <th style="padding:8px;border:1px solid #e5d8c9;text-align:left;">Product</th>
            <th style="padding:8px;border:1px solid #e5d8c9;text-align:left;">SKU</th>
            <th style="padding:8px;border:1px solid #e5d8c9;">Qty</th>
            <th style="padding:8px;border:1px solid #e5d8c9;text-align:left;">Size</th>
          </tr>
        </thead>
        <tbody>${rows}</tbody>
      </table>
      <p style="margin-top:10px;"><b>Total units:</b> ${totals.totalUnits}</p>

      ${notes ? `<h3 style="color:#8b4513;">Notes</h3><p>${escapeHtml(notes)}</p>` : ''}
    </div>
    <div style="background:#2a1d12;color:#f4e6d4;padding:12px 20px;font-size:12px;">
      Tempo Plus — Official Orlen Distributor · Kosovo · Slovakia · Europe-wide delivery
    </div>
  </div>`;

  const text =
`NEW ORDER — Tempo Plus (Orlen)
Received: ${new Date().toUTCString()}

CUSTOMER
Name: ${customer.name}
Company: ${customer.company || '-'}
Email: ${customer.email}
Phone: ${customer.phone}
Country: ${customer.country}
Address: ${customer.address}
City / Postcode: ${customer.city} / ${customer.postcode}

ITEMS (${items.length})
${items.map(i => ` - ${i.name} [${i.sku || '-'}] x ${i.qty} (${i.size || '-'})`).join('\n')}

Total units: ${totals.totalUnits}
${notes ? `\nNotes:\n${notes}` : ''}
`;
  return { html, text };
}

function validate(order) {
  if (!order || typeof order !== 'object') return 'Invalid payload';
  const c = order.customer || {};
  const required = ['name', 'email', 'phone', 'country', 'address', 'city', 'postcode'];
  for (const k of required) {
    if (!c[k] || String(c[k]).trim().length < 2) return `Missing field: ${k}`;
  }
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(c.email)) return 'Invalid email address';
  if (!Array.isArray(order.items) || order.items.length === 0) return 'Cart is empty';
  if (order.items.length > 100) return 'Too many items';
  for (const it of order.items) {
    if (!it.name) return 'Item missing name';
    const q = Number(it.qty);
    if (!Number.isFinite(q) || q < 1 || q > 10000) return 'Invalid quantity';
  }
  return null;
}

// ---- Order endpoint ----
app.post('/api/order', orderLimiter, async (req, res) => {
  try {
    const order = req.body;
    const err = validate(order);
    if (err) return res.status(400).json({ ok: false, error: err });

    const totals = {
      totalUnits: order.items.reduce((s, i) => s + Number(i.qty), 0)
    };
    const payload = { ...order, totals };
    const { html, text } = buildEmail(payload);

    const to = (process.env.ORDER_TO || 'rronprebreza@gmail.com,tempoplus.pr1@gmail.com')
      .split(',').map(s => s.trim()).filter(Boolean);

    await transporter.sendMail({
      from: process.env.MAIL_FROM || process.env.SMTP_USER,
      to,
      replyTo: order.customer.email,
      subject: `New Order — ${order.customer.name} (${order.items.length} items)`,
      html,
      text
    });

    return res.json({ ok: true, message: 'Order received. We will contact you shortly.' });
  } catch (e) {
    console.error('[order] error:', e);
    return res.status(500).json({ ok: false, error: 'Failed to send order. Please call us directly.' });
  }
});

app.get('/api/health', (_req, res) => res.json({ ok: true }));

app.listen(PORT, () => console.log(`Tempo Plus site running: http://localhost:${PORT}`));

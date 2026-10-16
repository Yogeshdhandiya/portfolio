// On-screen motion graphics (D.mg) + extra white-card types (grid, flow) for template_minimal.html.
// Loaded after the main script; every animation is a pure function of t.
const ACC = '#FFC83D';
const IMG = s => s.startsWith('l:') ? `img/logos/${s.slice(2)}.svg` : `img/fluent/${s.slice(2)}_3d.png`;
const mgCss = document.createElement('style');
mgCss.textContent = `
.mg{position:absolute;left:0;right:0;display:flex;flex-direction:column;align-items:center;transform-origin:50% 50%}
.tile{width:150px;height:150px;border-radius:38px;background:rgba(255,255,255,.97);box-shadow:0 14px 34px rgba(0,0,0,.38);display:flex;align-items:center;justify-content:center}
.tile img{width:96px;height:96px;object-fit:contain}
.mlab{margin-top:14px;font:600 32px Body;color:#fff;text-shadow:0 2px 10px rgba(0,0,0,.75);white-space:nowrap}
.pill{margin-top:18px;padding:12px 30px;border-radius:40px;background:#fff;color:#111;font:700 36px Body;box-shadow:0 10px 30px rgba(0,0,0,.32);white-space:nowrap}
.mg-hero img{width:210px;height:210px;filter:drop-shadow(0 18px 30px rgba(0,0,0,.5))}
.row{display:flex;gap:34px;align-items:flex-start}
.it{display:flex;flex-direction:column;align-items:center;width:150px}
.ringv{position:relative;width:250px;height:250px}
.ringv svg{position:absolute;inset:0;filter:drop-shadow(0 8px 20px rgba(0,0,0,.4))}
.ringv .num{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font:400 112px Big;color:#fff;text-shadow:0 4px 16px rgba(0,0,0,.5);letter-spacing:0}
.bars{width:820px}
.brow{margin:8px 0 20px}
.blab{font:600 34px Body;color:#fff;text-shadow:0 2px 10px rgba(0,0,0,.75);display:flex;align-items:center;gap:12px}
.blab img{width:46px;height:46px}
.btrk{margin-top:10px;height:34px;border-radius:17px;background:rgba(0,0,0,.35);overflow:hidden;box-shadow:inset 0 0 0 2px rgba(255,255,255,.18)}
.bfil{height:100%;width:0;border-radius:17px}
.fol{display:flex;align-items:center;gap:22px;padding:22px 26px;border-radius:40px;background:rgba(18,18,22,.82);box-shadow:0 16px 40px rgba(0,0,0,.45)}
.fol .ring{width:96px;height:96px}
.fol .h1{font:700 36px Body;color:#fff}.fol .h2{font:500 26px Body;color:#aaa}
.fbtn{margin-left:18px;width:220px;height:74px;border-radius:20px;background:#0095f6;color:#fff;font:700 32px/74px Body;text-align:center;position:relative;overflow:hidden}
.rip{position:absolute;border-radius:50%;background:rgba(255,255,255,.6);width:40px;height:40px;left:50%;top:50%;margin:-20px 0 0 -20px}
.ntf{width:900px;display:flex;align-items:center;gap:24px;padding:26px 30px;border-radius:44px;background:rgba(245,245,247,.95);box-shadow:0 20px 50px rgba(0,0,0,.38);box-sizing:border-box}
.ntf img{width:84px;height:84px;border-radius:20px}
.ntf .a{font:600 26px Body;color:#777}.ntf .b{font:700 34px Body;color:#111}.ntf .c{font:500 31px Body;color:#333}
.chip{display:flex;align-items:center;gap:14px;padding:14px 32px 14px 18px;border-radius:44px;background:rgba(255,255,255,.97);font:700 38px Body;color:#111;box-shadow:0 10px 28px rgba(0,0,0,.32);margin:9px 0;white-space:nowrap}
.chip img{width:56px;height:56px}
.bdg{width:200px;height:200px;border-radius:50%;background:${ACC};color:#111;font:400 150px/212px Big;text-align:center;box-shadow:0 14px 34px rgba(0,0,0,.42);letter-spacing:0}
.cnt{font:400 200px/0.9 Big;color:#fff;text-shadow:0 6px 26px rgba(0,0,0,.55);letter-spacing:0}
.gt{position:absolute;width:170px;height:240px;border-radius:26px;overflow:hidden;box-shadow:0 12px 30px rgba(0,0,0,.18)}
.gt i{position:absolute;left:50%;top:50%;margin:-26px 0 0 -16px;border-left:44px solid rgba(255,255,255,.95);border-top:26px solid transparent;border-bottom:26px solid transparent}
.gt b{position:absolute;right:12px;bottom:10px;font:600 24px Body;color:#fff;background:rgba(0,0,0,.45);padding:2px 10px;border-radius:10px;letter-spacing:0}
.fn{position:absolute;left:150px;width:780px;height:180px;border-radius:40px;border:5px solid #e6e6e6;box-sizing:border-box;display:flex;align-items:center;gap:34px;padding:0 44px;background:#fff}
.fn img{width:110px;height:110px}
.fn span{font:400 112px/1 Big;color:#cfcfcf;letter-spacing:0}
.fl{position:absolute;left:536px;width:8px;background:#111;border-radius:4px}
`;
document.head.appendChild(mgCss);

const popIn = (e, k, d = 0.32, s0 = 0.4) => { e.style.opacity = cl(k / 0.08); e.style.transform = `scale(${k <= 0 ? s0 : s0 + (1 - s0) * eb(k / d)})` };
const slideUp = (e, k, d = 0.25, px = 24) => { e.style.opacity = cl(k / 0.1); e.style.transform = `translateY(${px * (1 - eo(k / d))}px)` };
const fmt = v => Math.round(v).toLocaleString('en-US');

const MG = (D.mg || []).map(m => {
  const box = el('div', 'mg mg-' + m.type); const o = { m, box };
  if (m.type === 'hero') {
    o.inner = el('div', null, `<img src="${IMG(m.icon)}">`, box); o.img = o.inner.firstChild;
    if (m.label) o.pill = el('div', 'pill', m.label, box);
  } else if (m.type === 'icons') {
    o.row = el('div', 'row', null, box);
    o.items = m.items.map(it => { const w = el('div', 'it', null, o.row); const tile = el('div', 'tile', `<img src="${IMG(it.icon)}">`, w);
      const lab = el('div', 'mlab', it.label || '', w); return { w, tile, lab, t: it.t } });
  } else if (m.type === 'ring') {
    const C = 2 * Math.PI * 105;
    o.rv = el('div', 'ringv', `<svg viewBox="0 0 250 250"><circle cx="125" cy="125" r="105" fill="rgba(0,0,0,.28)" stroke="rgba(255,255,255,.22)" stroke-width="20"/>
      <circle class="pg" cx="125" cy="125" r="105" fill="none" stroke="${ACC}" stroke-width="20" stroke-linecap="round" transform="rotate(-90 125 125)" stroke-dasharray="${C}" stroke-dashoffset="${C}"/></svg><div class="num">0</div>`, box);
    o.C = C; o.pg = o.rv.querySelector('.pg'); o.num = o.rv.querySelector('.num');
    if (m.label) o.pill = el('div', 'pill', m.label, box);
  } else if (m.type === 'bars') {
    o.wrap = el('div', 'bars', null, box);
    o.rows = m.rows.map(r => { const w = el('div', 'brow', null, o.wrap);
      const lab = el('div', 'blab', `<img src="${IMG(r.good ? 'f:check_mark_button' : 'f:cross_mark')}">${r.label}`, w);
      const trk = el('div', 'btrk', null, w); const fil = el('div', 'bfil', null, trk); fil.style.background = r.good ? ACC : 'rgba(255,255,255,.55)';
      return { w, lab, fil, r } });
  } else if (m.type === 'follow') {
    o.p = el('div', 'fol', `<div class=ring><div>${m.initials || 'Y'}</div></div><div><div class=h1>${m.handle}</div><div class=h2>${m.sub || ''}</div></div><div class=fbtn><span>Follow</span><div class=rip></div></div>`, box);
    o.btn = o.p.querySelector('.fbtn'); o.txt = o.btn.querySelector('span'); o.rip = o.btn.querySelector('.rip');
  } else if (m.type === 'notif') {
    o.n = el('div', 'ntf', `<img src="${IMG(m.icon)}" style="background:${m.bg || '#fff'}"><div><div class=a>${m.app || ''} · now</div><div class=b>${m.title}</div><div class=c>${m.body || ''}</div></div>`, box);
  } else if (m.type === 'chips') {
    o.items = m.items.map((it, i) => ({ e: el('div', 'chip', (it.icon ? `<img src="${IMG(it.icon)}">` : '') + it.text, box), t: it.t, i }));
  } else if (m.type === 'badge') {
    o.n = el('div', 'bdg', m.num, box); if (m.label) o.pill = el('div', 'pill', m.label, box);
  } else if (m.type === 'counter') {
    o.n = el('div', 'cnt', '', box); if (m.label) o.pill = el('div', 'pill', m.label, box);
  }
  box.style.top = m.y + 'px'; show(box, false);
  return o;
});

// white-card extras
const XC = cards.filter(o => o.c.type === 'grid' || o.c.type === 'flow').map(o => {
  const c = o.c, f = o.f;
  if (c.lead) { o.lead = mkWords(f, 'k klead', c.lead, { top: (c.type === 'grid' ? 380 : 300) + 'px' }); Object.assign(o.lead.el.style, { position: 'absolute', left: '0', right: '0' }) }
  if (c.type === 'grid') {
    o.big = el('div', 'k kbig', letters(c.big), f); o.big.style.top = '450px'; o.big.style.fontSize = '170px';
    const pal = [['#ff6a3d', '#ffb03d'], ['#5b5bff', '#9b6bff'], ['#00b894', '#55efc4'], ['#e84393', '#fd79a8'], ['#0984e3', '#74b9ff'], ['#2d3436', '#636e72']];
    const n = c.n || 12, cols = 4;
    o.tiles = [...Array(n)].map((_, i) => { const g = el('div', 'gt', `<i></i><b>0:${String(15 + Math.floor(rnd(i) * 44)).padStart(2, '0')}</b>`, f);
      const p = pal[i % pal.length]; g.style.background = `linear-gradient(160deg,${p[0]},${p[1]})`;
      g.style.left = (540 - (cols * 170 + (cols - 1) * 26) / 2 + (i % cols) * 196) + 'px'; g.style.top = (760 + Math.floor(i / cols) * 266) + 'px'; return g });
  } else {
    const n = c.items.length, h = n > 4 ? 150 : 180, gap = n > 4 ? 44 : 70; o.gap = gap;
    const y0 = Math.max(430, 1010 - (n * h + (n - 1) * gap) / 2);
    o.nodes = c.items.map(([label, icon, t], i) => { const y = y0 + i * (h + gap); const e = el('div', 'fn', `<img src="${IMG(icon)}"><span>${label}</span>`, f); e.style.top = y + 'px';
      if (n > 4) { e.style.height = h + 'px'; e.querySelector('span').style.fontSize = '92px'; e.querySelector('img').style.width = e.querySelector('img').style.height = '92px' }
      let ln = null; if (i) { ln = el('div', 'fl', null, f); ln.style.top = (y - gap) + 'px'; ln.style.height = '0px' } return { e, ln, t, img: e.querySelector('img'), sp: e.querySelector('span') } });
  }
  return o;
});

let mgFit = false;
function drawMG(t) {
  if (!mgFit) { for (const o of XC) if (o.lead) { const d = o.f.style.display; o.f.style.display = ''; measure(o.lead); o.f.style.display = d } mgFit = true }
  for (const o of MG) {
    const m = o.m, on = t >= m.t0 && t < m.t1; show(o.box, on); if (!on) continue;
    const a = t - m.t0, out = cl((t - (m.t1 - 0.18)) / 0.18);
    o.box.style.opacity = 1 - out; o.box.style.filter = out > 0 ? `blur(${10 * out}px)` : 'none';
    o.box.style.transform = `translateY(-50%) scale(${(m.s || 1) * (1 - 0.08 * out)})`;
    if (m.type === 'hero') { popIn(o.img, a, 0.38, 0.3); o.inner.style.transform = `translateY(${6 * Math.sin(t * 2.4)}px) rotate(${2 * Math.sin(t * 1.7)}deg)`; if (o.pill) slideUp(o.pill, a - 0.12) }
    if (m.type === 'icons') { const n = o.items.length, Wf = n * 150 + (n - 1) * 34; let vis = -34;
      o.items.forEach(it => { const k = t - it.t; it.w.style.visibility = k >= 0 ? 'visible' : 'hidden'; if (k >= 0) { popIn(it.tile, k); slideUp(it.lab, k - 0.08, 0.2, 14); vis += 184 * eo(k / 0.22) } });
      o.row.style.transform = `translateX(${(Wf - Math.max(vis, 0)) / 2}px)` }
    if (m.type === 'ring') { popIn(o.rv, a, 0.35, 0.5); const p = eo((t - (m.tc ?? m.t0 + 0.2)) / 0.9); o.pg.setAttribute('stroke-dashoffset', o.C * (1 - p * m.value / 100));
      o.num.textContent = Math.round(p * m.value) + (m.suffix || '%'); if (o.pill) slideUp(o.pill, a - 0.2) }
    if (m.type === 'bars') o.rows.forEach(({ w, fil, r }) => { const k = t - r.t; w.style.visibility = k >= 0 ? 'visible' : 'hidden'; if (k >= 0) { slideUp(w, k, 0.25, 20); fil.style.width = r.value * eo((k - 0.1) / 0.7) + '%' } });
    if (m.type === 'follow') { popIn(o.p, a, 0.35, 0.6); const k = t - m.tap; const done = k >= 0.12;
      o.btn.style.background = done ? '#3a3a3c' : '#0095f6'; o.txt.textContent = done ? 'Following' : 'Follow';
      o.btn.style.transform = `scale(${k >= 0 && k < 0.25 ? 1 - 0.08 * Math.sin(Math.PI * k / 0.25) : 1})`;
      o.rip.style.opacity = k >= 0 ? 1 - cl(k / 0.45) : 0; o.rip.style.transform = `scale(${k >= 0 ? 1 + 9 * eo(k / 0.45) : 0})` }
    if (m.type === 'notif') { o.n.style.opacity = cl(a / 0.1); o.n.style.transform = `translateY(${-160 * (1 - eb(a / 0.45))}px)` }
    if (m.type === 'chips') o.items.forEach(({ e, t: ti, i }) => { const k = t - ti; e.style.visibility = k >= 0 ? 'visible' : 'hidden'; if (k >= 0) { e.style.opacity = cl(k / 0.1); e.style.transform = `translateX(${(i % 2 ? 140 : -140) * (1 - eo(k / 0.3))}px)` } });
    if (m.type === 'badge') { popIn(o.n, a, 0.42, 0.2); o.n.style.transform += ` rotate(${-25 * (1 - eo(a / 0.45))}deg)`; if (o.pill) slideUp(o.pill, a - 0.15) }
    if (m.type === 'counter') { popIn(o.n, a, 0.3, 0.6); const p = eo((t - (m.tc ?? m.t0)) / (m.dur || 0.9)); o.n.textContent = (m.prefix || '') + fmt(m.from + (m.to - m.from) * p) + (m.suffix || ''); if (o.pill) slideUp(o.pill, a - 0.15) }
  }
  for (const o of XC) {
    const c = o.c; if (t < c.a - 0.3 || t > c.b + 0.3) continue;
    if (o.lead) buildWords(o.lead, t);
    if (c.type === 'grid') { const k = t - c.big_t; show(o.big, k >= 0); if (k >= 0) revealLetters(o.big, k, c.big_t);
      const n = o.tiles.length; o.tiles.forEach((g, i) => { const k2 = t - (c.tiles_t0 + i * (c.tiles_t1 - c.tiles_t0) / Math.max(n - 1, 1));
        g.style.opacity = cl(k2 / 0.08); g.style.transform = `scale(${k2 <= 0 ? 0.3 : 0.3 + 0.7 * eb(k2 / 0.3)}) rotate(${(rnd(i + 9) - 0.5) * 10 * (1 - eo(k2 / 0.4))}deg)` }) }
    if (c.type === 'flow') o.nodes.forEach((nd, i) => { const k = t - nd.t, on = k >= 0;
      nd.e.style.opacity = cl((t - c.a) / 0.2); nd.e.style.borderColor = on ? '#111' : '#e6e6e6'; nd.sp.style.color = on ? '#0b0b0b' : '#cfcfcf';
      nd.img.style.filter = on ? 'none' : 'grayscale(1) opacity(.35)'; nd.e.style.transform = `scale(${on ? 1 + 0.06 * Math.sin(Math.PI * cl(k / 0.3)) : 1})`;
      if (nd.ln) nd.ln.style.height = o.gap * eo((t - (nd.t - 0.2)) / 0.2) + 'px' });
  }
}
const _seek0 = window.__seek;
window.__seek = t => { _seek0(t); drawMG(t) };
drawMG(0);

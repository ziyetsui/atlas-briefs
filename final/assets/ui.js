(function () {
// Atlas brief UI helpers: sticky top bar with section anchors, cover renderer, number formatting.

const SECTIONS = [
  { id: 'product', label: '我的产品' },
  { id: 'competitors', label: '锁定竞品' },
  { id: 'hits', label: '竞品爆款' },
  { id: 'teardown', label: '爆款拆解' },
  { id: 'playbook', label: '规律与落地' },
];

// One-page brief: anchors to <section id>, scroll-spy marks the section in view.
function topBar() {
  const el = document.createElement('header');
  el.className = 'atlas-top';
  el.innerHTML = `
    <a class="brand" href="#product">Atlas</a>
    <span class="crumb" style="color:var(--ink-3)">/</span>
    <span class="crumb" style="color:var(--ink-2)">${window.ATLAS.product.name} · 竞品爆款 Brief</span>
    <nav class="steps" aria-label="Brief 章节">
      ${SECTIONS.map((s) => `<a href="#${s.id}" data-sec="${s.id}">${s.label}</a>`).join('')}
    </nav>`;
  document.body.prepend(el);

  const nav = el.querySelector('.steps');
  const links = [...nav.querySelectorAll('a')];
  let cur = null;
  const set = (id) => {
    if (id === cur) return;
    cur = id;
    links.forEach((a) => (a.dataset.sec === id ? a.setAttribute('aria-current', 'true') : a.removeAttribute('aria-current')));
    const a = links.find((x) => x.dataset.sec === id);
    // keep the active link visible in the (horizontally scrollable) nav without moving the page
    if (a && nav.scrollWidth > nav.clientWidth) nav.scrollTo({ left: a.offsetLeft - nav.offsetLeft - 8 });
  };
  const secs = SECTIONS.map((s) => document.getElementById(s.id)).filter(Boolean);
  const io = new IntersectionObserver((es) => es.forEach((e) => e.isIntersecting && set(e.target.id)), { rootMargin: '-40% 0px -55% 0px' });
  secs.forEach((s) => io.observe(s));
  addEventListener('scroll', () => {
    if (innerHeight + scrollY >= document.documentElement.scrollHeight - 4) set(secs[secs.length - 1].id);
    else if (scrollY < 40) set(secs[0].id);
  }, { passive: true });
  set(secs[0].id);
}

// Simulated 3:4 note cover. `n` is a note from data.js.
function cover(n, { tag = true } = {}) {
  if (n.img) {
    const label = n.pct != null ? `榜内 ${Math.round(n.pct)}%` : '';
    return `<div class="cover-wrap"><div class="cover cover-photo">
      <img src="${n.img}" alt="${(n.title || '').replace(/"/g, '&quot;')}" loading="lazy" decoding="async">
      ${n.type === '视频' ? '<span class="cover-play" aria-label="视频">▶</span>' : ''}
      ${tag && label ? `<span class="cover-tag num">${label}</span>` : ''}
    </div></div>`;
  }
  const [c1, c2, fg] = window.ATLAS.palettes[n.pal % window.ATLAS.palettes.length];
  return `<div class="cover-wrap"><div class="cover" style="--c1:${c1};--c2:${c2};--cfg:${fg}">
    ${n.person ? '<span class="cover-figure" aria-hidden="true"></span>' : ''}
    <div class="cover-text">${n.cover}</div>
    ${n.type === '视频' ? '<span class="cover-play" aria-label="视频">▶</span>' : ''}
    ${tag ? `<span class="cover-tag num">♥ ${fmt(n.likes)}</span>` : ''}
  </div></div>`;
}

function fmt(v) {
  if (v >= 10000) return (v / 10000).toFixed(v >= 100000 ? 0 : 1).replace(/\.0$/, '') + '万';
  return v.toLocaleString('zh-CN');
}


window.AtlasUI = { topBar, cover, fmt };
})();

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

  // Light / dark toggle. No stored choice → follow the system; a click pins the opposite of what's showing.
  const root = document.documentElement;
  const sys = matchMedia('(prefers-color-scheme: dark)');
  const isDark = () => root.dataset.theme ? root.dataset.theme === 'dark' : sys.matches;
  const SUN = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" aria-hidden="true"><circle cx="8" cy="8" r="3"/><path d="M8 1.5v1.2M8 13.3v1.2M1.5 8h1.2M13.3 8h1.2M3.4 3.4l.85.85M11.75 11.75l.85.85M3.4 12.6l.85-.85M11.75 4.25l.85-.85"/></svg>';
  const MOON = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round" aria-hidden="true"><path d="M13.5 9.6A5.5 5.5 0 0 1 6.4 2.5a5.5 5.5 0 1 0 7.1 7.1Z"/></svg>';
  const btn = document.createElement('button');
  btn.type = 'button';
  btn.className = 'theme-btn';
  const paint = () => {
    const d = isDark();
    btn.innerHTML = d ? SUN : MOON;
    btn.setAttribute('aria-label', d ? '切换到浅色模式' : '切换到深色模式');
    btn.title = d ? '浅色模式' : '深色模式';
  };
  btn.addEventListener('click', () => {
    const next = isDark() ? 'light' : 'dark';
    root.classList.add('theme-switching');
    root.dataset.theme = next;
    try { localStorage.setItem('atlas-theme', next); } catch {}
    paint();
    requestAnimationFrame(() => requestAnimationFrame(() => root.classList.remove('theme-switching')));
  });
  sys.addEventListener('change', paint);
  el.append(btn);
  paint();

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
const attr = (t) => String(t || '').replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;');
const dur = (s) => `${Math.floor(s / 60)}:${String(Math.round(s % 60)).padStart(2, '0')}`;

// `play: false` when the cover sits inside a link — pair it with playLink(n) next to the other actions.
function cover(n, { tag = true, play = true } = {}) {
  if (n.img) {
    const label = n.pct != null ? `榜内 ${Math.round(n.pct)}%` : '';
    const v = n.video;
    const badge = v
      ? (play
        ? `<button type="button" class="cover-playbtn" data-video="${n.id}" aria-label="播放视频（${dur(v.durationSec)}）：${attr(n.title)}"><span class="pb-dot" aria-hidden="true">▶</span><span class="pb-dur num">${dur(v.durationSec)}</span></button>`
        : `<span class="cover-play cover-play-live" aria-label="可播放视频">▶</span>`)
      : (n.type === '视频' ? '<span class="cover-play" aria-label="视频">▶</span>' : '');
    return `<div class="cover-wrap"><div class="cover cover-photo">
      <img src="${n.img}" alt="${attr(n.title)}" loading="lazy" decoding="async">
      ${badge}
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



// Inline player for notes whose video exists in the library (most only have a cover — those keep 看原文).
function playLink(n) {
  return n.video ? `<button type="button" class="play-link" data-video="${n.id}">▶ 播放 <span class="num">${dur(n.video.durationSec)}</span></button>` : '';
}

let dlg = null, lastFocus = null;
function openPlayer(n) {
  if (!dlg) {
    dlg = document.createElement('dialog');
    dlg.className = 'atlas-player';
    dlg.addEventListener('click', (e) => { if (e.target === dlg || e.target.closest('.ap-close')) dlg.close(); });
    dlg.addEventListener('close', () => {
      const v = dlg.querySelector('video');
      if (v) { v.pause(); v.removeAttribute('src'); v.load(); }
      lastFocus?.focus?.();
    });
    document.body.append(dlg);
  }
  lastFocus = document.activeElement;
  dlg.setAttribute('aria-label', `视频：${n.title}`);
  dlg.innerHTML = `<div class="ap-box">
      <video src="${n.video.src}" poster="${n.video.poster || n.img}" controls playsinline autoplay preload="metadata"></video>
      <div class="ap-bar">
        <div class="ap-meta"><p class="ap-t">${attr(n.title)}</p><p class="ap-m">${attr(n.account)} · <span class="num">${dur(n.video.durationSec)}</span></p></div>
        <a class="ap-ext" href="${n.url}" target="_blank" rel="noopener">看原文 ↗</a>
        <button type="button" class="ap-close" aria-label="关闭视频">✕</button>
      </div>
    </div>`;
  // Fit the dialog to the video's own aspect ratio (most are vertical) so there are no side bars.
  const v = dlg.querySelector('video'), box = dlg.querySelector('.ap-box');
  const fit = (ar) => {
    const maxW = Math.min(innerWidth * 0.92, 980), maxH = innerHeight * 0.86 - 64;
    box.style.width = Math.max(Math.min(maxW, maxH * ar), Math.min(maxW, 320)) + 'px';
  };
  fit(n.aspect || 0.5625);
  v.addEventListener('loadedmetadata', () => v.videoWidth && fit(v.videoWidth / v.videoHeight), { once: true });
  dlg.showModal();
  dlg.querySelector('.ap-close').focus({ preventScroll: true });
}

// Capture phase so a play control wins over any card / section click handler around it.
document.addEventListener('click', (e) => {
  const b = e.target.closest('[data-video]');
  if (!b) return;
  const n = window.ATLAS.notes[b.dataset.video];
  if (!n?.video) return;
  e.preventDefault(); e.stopPropagation();
  openPlayer(n);
}, true);

window.AtlasUI = { topBar, cover, fmt, playLink };
})();

// Atlas proto harness: top step bar, cover renderer, and the picker (wiring verbatim from PICKER.md).

const STEPS = [
  { href: 'p0-overview.html', label: '总览' },
  { href: 'p1-competitors.html', label: '锁定竞品' },
  { href: 'p2-hits.html', label: '竞品爆款' },
  { href: 'p3-teardown.html', label: '爆款拆解' },
  { href: 'p4-playbook.html', label: '规律与落地' },
];

function topBar(active) {
  const el = document.createElement('header');
  el.className = 'atlas-top';
  el.innerHTML = `
    <a class="brand" href="index.html">Atlas</a>
    <span class="crumb" style="color:var(--ink-3)">/</span>
    <span class="crumb" style="color:var(--ink-2)">${window.ATLAS.product.name} · 竞品爆款 Brief</span>
    <nav class="steps" aria-label="Brief 步骤">
      ${STEPS.map((s, i) => `<a href="${s.href}${i === active ? location.search : ''}" ${i === active ? 'aria-current="page"' : ''}><b>${i}</b><span>${s.label}</span></a>`).join('')}
    </nav>`;
  document.body.prepend(el);
}

// Simulated 3:4 note cover. `n` is a note from data.js.
function cover(n, { tag = true } = {}) {
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

// variants: [{ name, render: () => htmlString, mount?: (stageEl) => void }]
function picker(variants, { replay = true } = {}) {
  const nav = document.createElement('nav');
  nav.className = 'proto-picker';
  nav.setAttribute('aria-label', 'Prototype variants');
  nav.innerHTML = `<span class="proto-picker-highlight" aria-hidden="true"></span>
    ${variants.map((v) => `<button class="proto-picker-item">${v.name}</button>`).join('')}
    ${replay ? '<span class="proto-picker-divider" aria-hidden="true"></span><button class="proto-picker-item proto-picker-replay" aria-label="Replay animation (R)">↻</button>' : ''}`;
  document.body.append(nav);

  const stage = document.getElementById('stage');
  const highlight = nav.querySelector('.proto-picker-highlight');
  const items = [...nav.querySelectorAll('.proto-picker-item:not(.proto-picker-replay)')];
  const replayBtn = nav.querySelector('.proto-picker-replay');
  let current = 0;

  function moveHighlight() {
    const el = items[current];
    highlight.style.width = el.offsetWidth + 'px';
    highlight.style.transform = `translateX(${el.offsetLeft}px)`;
  }
  function mount(i) {
    stage.innerHTML = '';
    requestAnimationFrame(() => {
      stage.innerHTML = variants[i].render();
      variants[i].mount?.(stage);
    });
  }
  function setActive(i) {
    if (i < 0 || i >= variants.length) return;
    current = i;
    items.forEach((el, j) => {
      el.toggleAttribute('data-active', j === i);
      if (j === i) el.setAttribute('aria-current', 'true');
      else el.removeAttribute('aria-current');
    });
    moveHighlight();
    const url = new URL(location);
    url.searchParams.set('v', i + 1);
    history.replaceState(null, '', url);
    mount(i);
  }

  items.forEach((el, i) => el.addEventListener('click', () => setActive(i)));
  replayBtn?.addEventListener('click', () => mount(current));
  window.addEventListener('resize', moveHighlight);
  document.addEventListener('keydown', (e) => {
    if (/^(INPUT|TEXTAREA|SELECT)$/.test(e.target.tagName) || e.target.isContentEditable) return;
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    const num = parseInt(e.key, 10);
    if (num >= 1 && num <= variants.length) setActive(num - 1);
    else if (e.key === 'ArrowRight') setActive((current + 1) % variants.length);
    else if (e.key === 'ArrowLeft') setActive((current - 1 + variants.length) % variants.length);
    else if (e.key === 'r' || e.key === 'R') mount(current);
  });
  setActive((parseInt(new URLSearchParams(location.search).get('v'), 10) || 1) - 1);
  requestAnimationFrame(() => requestAnimationFrame(() => nav.setAttribute('data-ready', '')));
}

window.AtlasUI = { topBar, cover, fmt, picker };

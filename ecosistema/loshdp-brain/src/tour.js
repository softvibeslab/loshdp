// Recorrido de insights de «El Cerebro del Pueblo» (Los HDP).
// Lee tour.json: pasos con nodo foco, cifras, texto y renglones que abren nodos del grafo.
// También agrega al panel lateral el video original del episodio o clip seleccionado.
const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[c]));
const STATIC = globalThis.BRAIN_STATIC === true;

let tour = null, api = null;

function ytId(url) {
  return url?.match(/youtube\.com\/(?:watch\?v=|shorts\/)([\w-]{11})/)?.[1] || null;
}

// Panel lateral: video incrustado para episodios/shorts de YouTube y enlace al original para el resto.
export function renderEvidence(n, el) {
  if (!el) return;
  el.innerHTML = '';
  const url = tour?.links?.[n.title];
  if (!url) return;
  const id = ytId(url);
  el.innerHTML = (id
    ? `<iframe class="yt" src="https://www.youtube-nocookie.com/embed/${id}?rel=0" title="${esc(n.title)}" loading="lazy" allow="encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe>`
    : '') + `<a class="btn small ver-original" href="${esc(url)}" target="_blank" rel="noopener">Ver original ↗</a>`;
}

export async function initTour(theApi) {
  api = theApi;
  try {
    const t = await fetch(STATIC ? 'tour.json' : '/tour.json');
    if (!t.ok) return;
    tour = await t.json();
  } catch { return; }

  const panel = document.getElementById('tour');
  const btn = document.getElementById('btn-tour');
  btn.hidden = false;
  let step = -1, openRow = -1;

  function render() {
    const s = tour.steps[step];
    const rows = (s.rows || []).map((r, i) => {
      const open = i === openRow;
      return `<li class="tour-row${open ? ' open' : ''}" data-i="${i}">
        <button class="tour-row-head"><i style="background:${esc(r.color || 'var(--accent)')}"></i><span>${esc(r.label || r.title)}</span>${r.meta ? `<em>${esc(r.meta)}</em>` : ''}</button>
        ${open ? `<div class="tour-row-body">${r.body ? `<p>${esc(r.body)}</p>` : ''}${r.url ? `<div class="tour-links"><a class="btn small" href="${esc(r.url)}" target="_blank" rel="noopener">Abrir ↗</a></div>` : ''}</div>` : ''}
      </li>`;
    }).join('');
    panel.innerHTML = `
      <div class="tour-top"><span>${esc(s.section)}</span><span>Paso ${step + 1} de ${tour.steps.length}</span></div>
      <div class="tour-progress"><i style="width:${((step + 1) / tour.steps.length) * 100}%"></i></div>
      <h2>${esc(s.title)}</h2>
      ${(s.kpis || []).length ? `<div class="tour-kpis">${s.kpis.map(([v, l]) => `<div><b>${esc(v)}</b><span>${esc(l)}</span></div>`).join('')}</div>` : ''}
      ${(s.text || []).map((t) => `<p>${esc(t)}</p>`).join('')}
      ${step === 0 && tour.legend ? `<div class="tour-legend">${tour.legend.map((t) => `<span><i style="background:${esc(t.color)}"></i>${esc(t.label)}</span>`).join('')}</div>` : ''}
      ${rows ? `<ul class="tour-rows">${rows}</ul>` : ''}
      <div class="tour-nav">
        <button class="btn small ghost" data-act="exit">Salir</button>
        <span class="tour-hint">← → para navegar</span>
        <button class="btn small" data-act="prev" ${step === 0 ? 'disabled' : ''}>Anterior</button>
        <button class="btn small demo-primary" data-act="next">${step === tour.steps.length - 1 ? 'Terminar' : 'Siguiente'}</button>
      </div>`;
  }

  function go(i) {
    step = Math.max(0, Math.min(tour.steps.length - 1, i));
    openRow = -1;
    const s = tour.steps[step];
    api.setSources(s.sources);
    const foco = api.findByTitle(s.focus);
    if (foco) api.select(foco); else api.clear();
    api.resetHistory();
    render();
    panel.scrollTop = 0;
  }
  function start(i = 0) {
    document.body.classList.add('touring');
    panel.hidden = false;
    btn.setAttribute('aria-pressed', 'true');
    go(i);
  }
  function exit() {
    document.body.classList.remove('touring');
    panel.hidden = true;
    btn.setAttribute('aria-pressed', 'false');
    api.setSources(null);
    api.overview();
  }

  btn.addEventListener('click', () => (panel.hidden ? start(Math.max(step, 0)) : exit()));
  panel.addEventListener('click', (e) => {
    if (e.target.closest('a')) return;
    const act = e.target.closest('[data-act]')?.dataset.act;
    if (act === 'next') return step === tour.steps.length - 1 ? exit() : go(step + 1);
    if (act === 'prev') return go(step - 1);
    if (act === 'exit') return exit();
    const row = e.target.closest('.tour-row');
    if (row && e.target.closest('.tour-row-head')) {
      const i = Number(row.dataset.i), r = tour.steps[step].rows[i];
      openRow = openRow === i ? -1 : i;
      render();
      const n = api.findByTitle(r.title);
      if (n && openRow === i) api.select(n);
      panel.querySelector('.tour-row.open')?.scrollIntoView({block: 'nearest', behavior: 'smooth'});
    }
  });
  document.addEventListener('keydown', (e) => {
    if (panel.hidden || /INPUT|TEXTAREA/.test(document.activeElement?.tagName || '')) return;
    if (e.key === 'ArrowRight') { e.preventDefault(); step === tour.steps.length - 1 ? exit() : go(step + 1); }
    if (e.key === 'ArrowLeft') { e.preventDefault(); go(step - 1); }
  });
  if (new URLSearchParams(location.search).has('tour')) setTimeout(() => start(0), 2400);
}

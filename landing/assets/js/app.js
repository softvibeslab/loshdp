/* Los HDP — lógica del sitio. Datos: window.EPISODIOS (generado por scripts/inventario.py). */
(() => {
  // ── Configuración del cliente (pendientes marcados) ─────────────────────────────
  const CONFIG = {
    correo: "loshdp.elpodcast@gmail.com",
    whatsapp: "527712668105", // WhatsApp de Los HDP (+52 771 266 8105)
    canalWhatsapp: "",       // PENDIENTE: enlace del canal de WhatsApp. Sin él, el botón lleva a Facebook.
    redes: [
      { nombre: "Facebook", url: "https://www.facebook.com/profile.php?id=61552864772878", icono: "M14 8h3V4h-3c-2.8 0-4 1.8-4 4.3V10H7v4h3v8h4v-8h3l1-4h-4V8.6c0-.4.2-.6.6-.6Z" },
      { nombre: "YouTube", url: "https://www.youtube.com/@loshijos_delpueblopodcast", icono: "M23 7.2a3 3 0 0 0-2.1-2.1C19 4.6 12 4.6 12 4.6s-7 0-8.9.5A3 3 0 0 0 1 7.2 31 31 0 0 0 .5 12a31 31 0 0 0 .5 4.8 3 3 0 0 0 2.1 2.1c1.9.5 8.9.5 8.9.5s7 0 8.9-.5a3 3 0 0 0 2.1-2.1c.4-1.6.5-4.8.5-4.8s0-3.2-.5-4.8ZM9.7 15V9l5.8 3-5.8 3Z" },
      { nombre: "Spotify", url: "https://open.spotify.com/show/3rwx7hZbCvJzYxBICuRcuf", icono: "M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20Zm4.6 14.4a.6.6 0 0 1-.9.2c-2.4-1.5-5.4-1.8-9-1a.6.6 0 1 1-.3-1.2c3.9-.9 7.2-.5 9.9 1.1.3.2.4.6.3.9Zm1.2-2.7a.8.8 0 0 1-1 .3c-2.7-1.7-6.9-2.2-10.2-1.2a.8.8 0 0 1-.4-1.5c3.7-1.1 8.4-.6 11.4 1.3.3.2.4.7.2 1.1Zm.1-2.8C14.6 9 9.2 8.8 6.1 9.7a.9.9 0 1 1-.5-1.8c3.6-1.1 9.5-.9 13.2 1.3a.9.9 0 0 1-.9 1.7Z" },
      { nombre: "TikTok", url: "https://www.tiktok.com/@los_hijos_delpueblo", icono: "M16.5 2h-3.3v13.2a2.9 2.9 0 1 1-2-2.8V9a6.3 6.3 0 1 0 5.3 6.2V8.6a7.7 7.7 0 0 0 4.5 1.4V6.7a4.5 4.5 0 0 1-4.5-4.7Z" },
      { nombre: "Instagram", url: "https://www.instagram.com/los.hdp.el.podcast/", icono: "M12 7a5 5 0 1 0 0 10 5 5 0 0 0 0-10Zm0 8.2a3.2 3.2 0 1 1 0-6.4 3.2 3.2 0 0 1 0 6.4ZM17.3 5.5a1.2 1.2 0 1 0 0 2.4 1.2 1.2 0 0 0 0-2.4ZM12 2c-2.7 0-3 0-4.1.1C4.3 2.2 2.2 4.3 2.1 7.9 2 9 2 9.3 2 12s0 3 .1 4.1c.1 3.6 2.2 5.7 5.8 5.8 1.1.1 1.4.1 4.1.1s3 0 4.1-.1c3.6-.1 5.7-2.2 5.8-5.8.1-1.1.1-1.4.1-4.1s0-3-.1-4.1c-.1-3.6-2.2-5.7-5.8-5.8C15 2 14.7 2 12 2Z" }
    ]
  };

  const EPS = window.EPISODIOS || [];
  const $ = (s, c = document) => c.querySelector(s);
  const fmt = n => (n || 0).toLocaleString("es-MX");
  const fecha = f => new Date(f + "T12:00:00").toLocaleDateString("es-MX", { day: "numeric", month: "short", year: "numeric" });
  const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const miniatura = id => `img/ep/${id}.jpg`;
  const nombreEp = e => {
    if (e.invitado) return e.invitado;
    const tema = e.titulo.replace(/^los hdp-?\s*(ep\.?\s*\d+\s*-?)?\s*/i, "").split(/\s+-\s+/).slice(-1)[0].trim();
    return tema || `${e.segmento}${e.ep_titulo ? " Ep " + e.ep_titulo : ""}`;
  };
  const svg = d => `<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path fill-rule="evenodd" d="${d}"/></svg>`;

  const ORIGEN = window.HDP_ORIGEN || { firma: () => "", plataforma: () => "youtube", elegirPlataforma() {} };
  function contacto(mensaje, asunto = "Contacto desde el sitio de Los HDP") {
    mensaje += ORIGEN.firma(); // dice de qué red llegó la persona (atribución sin analítica)
    return CONFIG.whatsapp
      ? `https://wa.me/${CONFIG.whatsapp}?text=${encodeURIComponent(mensaje)}`
      : `mailto:${CONFIG.correo}?subject=${encodeURIComponent(asunto)}&body=${encodeURIComponent(mensaje)}`;
  }

  // ── Video con fachada: solo carga YouTube al hacer clic ─────────────────────────
  function fachada(id, titulo) {
    const b = document.createElement("button");
    b.className = "yt-fachada";
    b.setAttribute("aria-label", `Reproducir: ${titulo}`);
    b.innerHTML = `<img src="${miniatura(id)}" alt="" loading="lazy"><span class="play">${svg("M8 5v14l11-7z")}</span>`;
    b.addEventListener("click", () => b.replaceWith(iframe(id, titulo)));
    return b;
  }
  function iframe(id, titulo) {
    const f = document.createElement("iframe");
    f.className = "yt-marco";
    f.src = `https://www.youtube-nocookie.com/embed/${id}?autoplay=1&rel=0`;
    f.title = titulo;
    f.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share";
    f.allowFullscreen = true;
    return f;
  }

  // ── Redes ───────────────────────────────────────────────────────────────────────
  const plat = $("#plataformas");
  CONFIG.redes.forEach(r => {
    plat.insertAdjacentHTML("beforeend", `<a href="${r.url}" target="_blank" rel="noopener" aria-label="${r.nombre}" title="${r.nombre}">${svg(r.icono)}</a>`);
    $("#pie-redes").insertAdjacentHTML("beforeend", `<li><a href="${r.url}" target="_blank" rel="noopener">${r.nombre}</a></li>`);
  });

  // ── Último episodio ───────────────────────────────────────────────────────────
  const ultimo = EPS.find(e => e.segmento !== "Teaser");
  if (ultimo) {
    $("#ultimo-video").appendChild(fachada(ultimo.youtube_id, ultimo.titulo));
    $("#ultimo-titulo").textContent = nombreEp(ultimo);
    $("#ultimo-meta").textContent = `${ultimo.segmento}${ultimo.ep_titulo ? " · Ep " + ultimo.ep_titulo : ""} · ${fecha(ultimo.fecha)} · ${ultimo.dur_min} min`;
    $("#ultimo-yt").href = `https://www.youtube.com/watch?v=${ultimo.youtube_id}`;
  }

  // ── Cinta de cifras ─────────────────────────────────────────────────────────────
  const invitados = new Set(EPS.filter(e => e.invitado).map(e => e.invitado)).size;
  const munis = new Set(EPS.filter(e => e.municipio).map(e => e.municipio)).size;
  const frases = [
    `<b>${EPS.length}</b> episodios`, `<b>${invitados}</b> adoptados`, `<b>44K</b> en Facebook`,
    `<b>13.5K</b> en TikTok`, `<b>${munis}</b> municipios`, "Sin filtro", "No se sulfuren", "HDTPM"
  ];
  const linea = frases.map(f => `<span>${f}</span><span>✦</span>`).join("");
  $("#cinta").innerHTML = linea + linea;

  // ── Archivo filtrable ───────────────────────────────────────────────────────────
  const estado = { segmento: "", partido: "", municipio: "", texto: "", visibles: 9 };
  const conteoPor = k => EPS.reduce((m, e) => (e[k] && (m[e[k]] = (m[e[k]] || 0) + 1), m), {});
  const segs = conteoPor("segmento");
  delete segs.Teaser;
  const chips = $("#chips");
  const chip = (valor, etiqueta, n) => {
    const b = document.createElement("button");
    b.className = "chip";
    b.type = "button";
    b.setAttribute("aria-pressed", valor === estado.segmento);
    b.innerHTML = `${esc(etiqueta)}<small>${n}</small>`;
    b.addEventListener("click", () => {
      estado.segmento = valor;
      estado.visibles = 9;
      chips.querySelectorAll(".chip").forEach(c => c.setAttribute("aria-pressed", c === b));
      pintar();
    });
    chips.appendChild(b);
  };
  chip("", "Todos", EPS.filter(e => e.segmento !== "Teaser").length);
  Object.entries(segs).sort((a, b) => b[1] - a[1]).forEach(([s, n]) => chip(s, s, n));

  const llenar = (sel, obj) => Object.entries(obj).sort((a, b) => b[1] - a[1])
    .forEach(([k, n]) => sel.insertAdjacentHTML("beforeend", `<option value="${esc(k)}">${esc(k)} (${n})</option>`));
  llenar($("#f-partido"), conteoPor("partido"));
  llenar($("#f-municipio"), conteoPor("municipio"));
  $("#f-partido").addEventListener("change", e => { estado.partido = e.target.value; estado.visibles = 9; pintar(); });
  $("#f-municipio").addEventListener("change", e => { estado.municipio = e.target.value; estado.visibles = 9; pintar(); });
  let t;
  $("#buscar").addEventListener("input", e => {
    clearTimeout(t);
    t = setTimeout(() => { estado.texto = e.target.value.trim().toLowerCase(); estado.visibles = 9; pintar(); }, 160);
  });

  const normal = s => s.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();
  function filtrados() {
    const q = normal(estado.texto);
    return EPS.filter(e => e.segmento !== "Teaser"
      && (!estado.segmento || e.segmento === estado.segmento)
      && (!estado.partido || e.partido === estado.partido)
      && (!estado.municipio || e.municipio === estado.municipio)
      && (!q || normal(`${e.titulo} ${e.rol || ""} ${e.municipio || ""}`).includes(q)));
  }

  function tarjeta(e) {
    const b = document.createElement("button");
    b.className = "tarjeta-ep";
    b.type = "button";
    b.innerHTML = `
      <div class="portada"><img src="${miniatura(e.youtube_id)}" alt="" loading="lazy"><span class="dur">${e.dur_min} min</span></div>
      <div class="cuerpo">
        <span class="seg">${esc(e.segmento)}${e.ep_titulo ? " · Ep " + e.ep_titulo : ""}</span>
        <h3>${esc(nombreEp(e))}</h3>
        <p>${esc(e.rol || e.titulo)}</p>
        <div class="meta">
          <span>${fecha(e.fecha)}</span><span>${fmt(e.vistas)} vistas</span>
          ${e.partido ? `<span class="partido">${esc(e.partido)}</span>` : ""}
          ${e.municipio ? `<span>📍 ${esc(e.municipio)}</span>` : ""}
        </div>
      </div>`;
    b.addEventListener("click", () => abrirModal(e));
    return b;
  }

  function pintar() {
    const lista = filtrados();
    const rejilla = $("#rejilla");
    rejilla.innerHTML = "";
    if (!lista.length) {
      rejilla.innerHTML = `<div class="vacio">No encontramos a ese adoptado… todavía. <a href="#adoptame" style="color:var(--lima)">¿Lo proponemos?</a></div>`;
    }
    lista.slice(0, estado.visibles).forEach(e => rejilla.appendChild(tarjeta(e)));
    $("#conteo").textContent = `${lista.length} episodio${lista.length === 1 ? "" : "s"}`;
    $("#ver-mas").hidden = estado.visibles >= lista.length;
  }
  $("#ver-mas").addEventListener("click", () => { estado.visibles += 9; pintar(); });
  pintar();

  // ── Top 5 ────────────────────────────────────────────────────────────────────────
  [...EPS].sort((a, b) => b.vistas - a.vistas).slice(0, 5).forEach(e => {
    const b = document.createElement("button");
    b.className = "top-item";
    b.type = "button";
    b.innerHTML = `<img src="${miniatura(e.youtube_id)}" alt="" loading="lazy"><b>${esc(nombreEp(e))}</b><small>${fmt(e.vistas)} vistas en YouTube</small>`;
    b.addEventListener("click", () => abrirModal(e));
    $("#top").appendChild(b);
  });

  // ── Modal ───────────────────────────────────────────────────────────────────────
  const modal = $("#modal");
  let foco;
  function abrirModal(e) {
    foco = document.activeElement;
    $("#modal-video").replaceChildren(iframe(e.youtube_id, e.titulo));
    $("#modal-titulo").textContent = nombreEp(e);
    $("#modal-meta").textContent = `${e.segmento}${e.ep_titulo ? " · Ep " + e.ep_titulo : ""} · ${fecha(e.fecha)} · ${e.dur_min} min`;
    const url = `https://www.youtube.com/watch?v=${e.youtube_id}`;
    $("#modal-yt").href = url;
    // se comparte el enlace del sitio (con el episodio directo), no el de YouTube: la visita vuelve a casa
    const propio = `${location.origin}${location.pathname}?ep=${e.youtube_id}&o=wa`;
    $("#modal-wa").href = `https://wa.me/?text=${encodeURIComponent(`Mira a ${nombreEp(e)} en Los HDP 👀 ${propio}`)}`;
    // la plataforma preferida va como botón principal
    const pref = ORIGEN.plataforma();
    $("#modal-yt").className = `boton ${pref === "spotify" ? "fantasma" : ""}`;
    $("#modal-sp").className = `boton ${pref === "spotify" ? "" : "fantasma"}`;
    if (pref === "spotify") $("#modal-sp").after($("#modal-yt"));
    else $("#modal-yt").after($("#modal-sp"));
    history.replaceState(null, "", `${location.pathname}?ep=${e.youtube_id}${location.hash}`);
    modal.classList.add("abierto");
    document.body.style.overflow = "hidden";
    $("#modal-cerrar").focus();
  }
  function cerrarModal() {
    modal.classList.remove("abierto");
    $("#modal-video").replaceChildren();
    document.body.style.overflow = "";
    history.replaceState(null, "", location.pathname + location.hash);
    foco?.focus();
  }
  $("#modal-cerrar").addEventListener("click", cerrarModal);
  modal.addEventListener("click", e => { if (e.target === modal) cerrarModal(); });
  addEventListener("keydown", e => { if (e.key === "Escape" && modal.classList.contains("abierto")) cerrarModal(); });

  // ── Conversiones ────────────────────────────────────────────────────────────────
  $("#form-adopta").addEventListener("submit", ev => {
    ev.preventDefault();
    const d = Object.fromEntries(new FormData(ev.target));
    const msg = `Hola Los HDP 👋 Quiero ser adoptado.\nNombre: ${d.nombre}\nCargo y municipio: ${d.cargo}\nWhatsApp: ${d.tel}`;
    window.open(contacto(msg, `Solicitud de entrevista: ${d.nombre}`), "_blank", "noopener");
  });
  $("#btn-kit").href = contacto("Hola Los HDP, me interesa anunciar mi marca. ¿Me comparten su media kit?", "Media kit Los HDP");
  $("#wa-flotante").href = contacto("Hola Los HDP 👋 Los vi en su sitio y quiero platicar con ustedes.");
  if (CONFIG.canalWhatsapp) $("#btn-canal").href = CONFIG.canalWhatsapp;
  else { $("#btn-canal").href = CONFIG.redes[0].url; $("#btn-canal").textContent = "Síguenos (canal de WhatsApp muy pronto)"; }

  // ── Navegación, menú y apariciones ──────────────────────────────────────────────
  const nav = $("#nav");
  addEventListener("scroll", () => nav.classList.toggle("solida", scrollY > 30), { passive: true });
  const menu = $("#menu"), btn = $("#btn-menu");
  btn.addEventListener("click", () => {
    const abierto = menu.classList.toggle("abierto");
    btn.setAttribute("aria-expanded", abierto);
  });
  menu.querySelectorAll("a").forEach(a => a.addEventListener("click", () => { menu.classList.remove("abierto"); btn.setAttribute("aria-expanded", false); }));
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add("visible"); io.unobserve(e.target); }
  }), { threshold: .12 });
  document.querySelectorAll(".reveal").forEach(el => io.observe(el));
  $("#anio").textContent = new Date().getFullYear();

  // ── Viaje del visitante ─────────────────────────────────────────────────────────
  $("#modal-sp").addEventListener("click", () => ORIGEN.elegirPlataforma("spotify"));
  $("#modal-yt").addEventListener("click", () => ORIGEN.elegirPlataforma("youtube"));
  window.HDP_APP = { abrirModal: e => e && abrirModal(e) };
  // enlace directo a un episodio (?ep=<id de YouTube> o ?ep=ultimo): se abre solo
  if (ORIGEN.ep) {
    const e = ORIGEN.ep === "ultimo" ? ultimo : EPS.find(x => x.youtube_id === ORIGEN.ep);
    if (e) setTimeout(() => abrirModal(e), 450);
  }
})();

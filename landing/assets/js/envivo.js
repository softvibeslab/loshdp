/* Los HDP — sección "En vivo": reproductor cuando hay transmisión, agenda de próximas y alertas.
   Datos: data/envivo.json (lo genera scripts/envivo.py). Se revisa cada minuto mientras la página está abierta. */
(() => {
  const $ = (s, c = document) => c.querySelector(s);
  const HDP = window.HDP;
  const TZ = "America/Mexico_City";
  const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const base = location.origin + location.pathname.replace(/[^/]*$/, "");
  const calendarioUrl = `${base}data/envivo.ics`;
  let datos = null, claveVivo = "";

  // ── Fechas ───────────────────────────────────────────────────────────────────────
  const fechaLarga = iso => new Date(iso).toLocaleString("es-MX", { timeZone: TZ, weekday: "long", day: "numeric", month: "long" });
  const hora = iso => new Date(iso).toLocaleString("es-MX", { timeZone: TZ, hour: "numeric", minute: "2-digit" });
  const utc = d => d.toISOString().replace(/[-:]/g, "").replace(/\.\d{3}/, "");
  function faltan(iso) {
    const ms = new Date(iso) - Date.now();
    if (ms <= 0) return "¡Empieza ya!";
    const m = Math.floor(ms / 60e3), d = Math.floor(m / 1440), h = Math.floor((m % 1440) / 60);
    return `Faltan ${d ? d + " d " : ""}${d || h ? h + " h " : ""}${m % 60} min`;
  }
  function google(p) {
    const ini = new Date(p.inicio), fin = new Date(ini.getTime() + (p.duracion_min || 90) * 60e3);
    const q = new URLSearchParams({
      action: "TEMPLATE", text: `Los HDP en vivo: ${p.titulo}`, dates: `${utc(ini)}/${utc(fin)}`,
      details: `${[p.invitado, p.plataforma].filter(Boolean).join(" · ")}\nMíralo en vivo: ${p.url || base + "#envivo"}`,
      location: p.plataforma || "Facebook y YouTube", ctz: TZ
    });
    return `https://calendar.google.com/calendar/render?${q}`;
  }

  // ── Reproductor ──────────────────────────────────────────────────────────────────
  function reproductor(t) {
    const marco = document.createElement("iframe");
    marco.className = "yt-marco";
    marco.title = t.titulo || "Transmisión en vivo de Los HDP";
    marco.allow = "autoplay; encrypted-media; picture-in-picture; web-share; clipboard-write";
    marco.allowFullscreen = true;
    if (t.youtube_id) marco.src = `https://www.youtube-nocookie.com/embed/${encodeURIComponent(t.youtube_id)}?rel=0&playsinline=1`;
    else if (/facebook\.com|fb\.watch/.test(t.url || "")) marco.src = `https://www.facebook.com/plugins/video.php?href=${encodeURIComponent(t.url)}&show_text=false&width=1280`;
    else marco.src = `https://www.youtube.com/embed/live_stream?channel=${encodeURIComponent(datos.canal_youtube)}&playsinline=1`;
    return marco;
  }

  function pintarVivo(t) {
    const clave = t.desde || t.youtube_id || t.url;
    if (clave === claveVivo) return;
    claveVivo = clave;
    const pantalla = $("#vivo-pantalla");
    pantalla.innerHTML = `
      <div class="vivo-marco"></div>
      <div class="vivo-pie">
        <div><span class="insignia-vivo">En vivo</span><b>${esc(t.titulo)}</b></div>
        <div class="vivo-botones">
          <a class="boton fantasma" href="${esc(t.url)}" target="_blank" rel="noopener">Abrir en ${esc(t.plataforma || "YouTube")} ↗</a>
          <a class="boton" href="https://wa.me/?text=${encodeURIComponent(`🔴 Los HDP están en vivo: ${t.titulo} ${base}#envivo`)}" target="_blank" rel="noopener">Compartir</a>
        </div>
      </div>`;
    $(".vivo-marco", pantalla).appendChild(reproductor(t));
  }

  function tarjetaProxima(p, principal) {
    return `
      <article class="${principal ? "vivo-proxima" : "vivo-item"}">
        ${principal ? `<span class="etiqueta">Próxima transmisión</span>` : ""}
        <h3>${esc(p.titulo)}</h3>
        ${p.invitado ? `<p class="vivo-invitado">Con ${esc(p.invitado)}</p>` : ""}
        <p class="vivo-cuando"><b>${esc(fechaLarga(p.inicio))}</b> · ${esc(hora(p.inicio))} <small>(hora del centro)</small> · ${esc(p.plataforma || "Facebook y YouTube")}</p>
        ${principal ? `<p class="vivo-cuenta" data-inicio="${esc(p.inicio)}">${faltan(p.inicio)}</p>` : ""}
        <div class="vivo-botones">
          <a class="boton${principal ? "" : " fantasma"}" href="${esc(google(p))}" target="_blank" rel="noopener">Agendar en Google</a>
          <a class="boton fantasma" href="data/ics/${encodeURIComponent(p.id)}.ics">${HDP.disp.ios || HDP.disp.mac ? "Agendar en Calendario" : "Agendar (.ics)"}</a>
        </div>
      </article>`;
  }

  function pintar() {
    const vivo = datos.en_vivo && datos.transmision;
    document.documentElement.classList.toggle("hay-vivo", !!vivo);
    const aviso = $("#aviso-vivo");
    aviso.hidden = !vivo;
    if (vivo) {
      $("#aviso-vivo-titulo").textContent = datos.transmision.titulo || "Los HDP en vivo";
      pintarVivo(datos.transmision);
    } else {
      claveVivo = "";
      const p = datos.proximas?.[0];
      $("#vivo-pantalla").innerHTML = p ? tarjetaProxima(p, true) : `
        <article class="vivo-proxima vivo-vacio">
          <span class="etiqueta oscura">Próxima transmisión</span>
          <h3>Por anunciar</h3>
          <p>Cuando prendamos el micrófono en vivo, aquí mismo podrás verlo sin salir del sitio. Activa las alertas o suscríbete al calendario y te avisamos.</p>
          <a class="boton fantasma" href="#inicio">Mientras, mira el último episodio ↑</a>
        </article>`;
    }
    const resto = vivo ? datos.proximas || [] : (datos.proximas || []).slice(1);
    $("#vivo-proximas").innerHTML = resto.length
      ? `<h3 class="vivo-subtitulo">También en agenda</h3><div class="vivo-lista">${resto.map(p => tarjetaProxima(p, false)).join("")}</div>`
      : "";
  }

  async function cargar() {
    try {
      const r = await fetch(`data/envivo.json?t=${Date.now()}`, { cache: "no-store" });
      if (!r.ok) throw new Error(r.status);
      datos = await r.json();
    } catch {
      if (!datos) datos = { en_vivo: false, proximas: [] };
    }
    pintar();
    if (alertasActivas()) (await HDP.sw)?.active?.postMessage({ tipo: "revisar", datos });
  }

  // ── Alertas ──────────────────────────────────────────────────────────────────────
  const soporta = "Notification" in window && "serviceWorker" in navigator;
  const alertasActivas = () => soporta && Notification.permission === "granted" && localStorage.getItem("hdp_alertas") === "1";

  function pintarBotones() {
    const activas = alertasActivas();
    document.querySelectorAll("[data-alertas]").forEach(b => {
      b.setAttribute("aria-pressed", activas);
      const txt = b.querySelector("[data-texto]") || b;
      txt.textContent = activas ? (b.dataset.corto ? "Activas" : "Alertas activadas ✓") : (b.dataset.corto ? "Alertas" : "Activar alertas");
    });
  }

  const opcionesExtra = `
    <div class="hoja-acciones">
      <a class="boton" href="${HDP.disp.android ? `https://calendar.google.com/calendar/render?cid=${encodeURIComponent(calendarioUrl.replace(/^https?:/, "webcal:"))}` : calendarioUrl.replace(/^https?:/, "webcal:")}">Suscribirme al calendario</a>
      <a class="boton fantasma" href="#canal" data-cerrar-hoja>Canal de WhatsApp y Facebook</a>
    </div>`;

  async function alternarAlertas() {
    if (alertasActivas()) {
      localStorage.removeItem("hdp_alertas");
      (await HDP.sw)?.active?.postMessage({ tipo: "alertas", activo: false });
      return pintarBotones();
    }
    if (!soporta) {
      const iosSinApp = HDP.disp.ios && !HDP.disp.instalada;
      HDP.hoja(`<span class="hoja-ico">🔔</span><h3>Activa tus alertas</h3>
        ${iosSinApp
          ? `<p>En iPhone las alertas funcionan con la app instalada. Primero toca <b>Descargar app</b>, abre Los HDP desde tu pantalla de inicio y activa las alertas ahí.</p><div class="hoja-acciones"><button class="boton" type="button" id="hoja-instalar">Descargar app</button></div><p class="letra-chica">¿Prefieres no instalar nada? Suscríbete al calendario de transmisiones: tu calendario te avisa 15 minutos antes.</p>`
          : `<p>Este navegador no permite notificaciones. Elige otra forma de enterarte:</p>`}
        ${opcionesExtra}`);
      $("#hoja-instalar")?.addEventListener("click", () => { HDP.cerrarHoja(); setTimeout(() => document.querySelector("[data-instalar]")?.click(), 300); });
      return;
    }
    if (Notification.permission === "denied") {
      HDP.hoja(`<span class="hoja-ico">🔕</span><h3>Las notificaciones están bloqueadas</h3>
        <p>Actívalas en los ajustes del navegador para este sitio (ícono del candado junto a la dirección → Notificaciones → Permitir) y vuelve a tocar <b>Activar alertas</b>.</p>${opcionesExtra}`);
      return;
    }
    const permiso = await Notification.requestPermission();
    if (permiso !== "granted") return;
    localStorage.setItem("hdp_alertas", "1");
    const reg = await HDP.sw;
    reg?.active?.postMessage({ tipo: "alertas", activo: true });
    reg?.active?.postMessage({ tipo: "prueba" });
    try {
      if (reg && "periodicSync" in reg) {
        const st = await navigator.permissions.query({ name: "periodic-background-sync" });
        if (st.state === "granted") await reg.periodicSync.register("hdp-envivo", { minInterval: 15 * 60e3 });
      }
    } catch { /* sin revisión en segundo plano en este navegador */ }
    pintarBotones();
    HDP.hoja(`<span class="hoja-ico">✅</span><h3>Alertas activadas</h3>
      <p>Te avisamos cuando Los HDP estén en vivo y 15 minutos antes de cada transmisión agendada.</p>
      <p class="letra-chica">Para no perderte ninguna aunque no abras la app, suscríbete también al calendario.</p>${opcionesExtra}`);
  }

  document.addEventListener("click", e => {
    const b = e.target.closest("[data-alertas]");
    if (b) { e.preventDefault(); alternarAlertas(); }
    if (e.target.closest("[data-cerrar-hoja]")) HDP.cerrarHoja();
  });
  const sus = $("#vivo-calendario");
  sus.href = HDP.disp.android
    ? `https://calendar.google.com/calendar/render?cid=${encodeURIComponent(calendarioUrl.replace(/^https?:/, "webcal:"))}`
    : calendarioUrl.replace(/^https?:/, "webcal:");
  if (HDP.disp.android) sus.target = "_blank";

  // ── Ciclo ────────────────────────────────────────────────────────────────────────
  pintarBotones();
  cargar();
  setInterval(() => { if (!document.hidden) cargar(); }, 60e3);
  setInterval(() => document.querySelectorAll(".vivo-cuenta").forEach(c => { c.textContent = faltan(c.dataset.inicio); }), 30e3);
  document.addEventListener("visibilitychange", () => { if (!document.hidden) cargar(); });
})();

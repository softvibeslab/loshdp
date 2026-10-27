/* Los HDP — viaje del visitante: de dónde llega (Meta, Spotify, YouTube, TikTok, WhatsApp),
   bienvenida a la medida, episodio directo (?ep=) y plataforma preferida para escuchar.
   Corre antes de app.js y expone window.HDP_ORIGEN. Sin cookies ni analítica: todo queda en el navegador. */
(() => {
  const RED = {
    fb: { id: "facebook", nombre: "Facebook" },
    ig: { id: "instagram", nombre: "Instagram" },
    sp: { id: "spotify", nombre: "Spotify" },
    yt: { id: "youtube", nombre: "YouTube" },
    tt: { id: "tiktok", nombre: "TikTok" },
    wa: { id: "whatsapp", nombre: "WhatsApp" },
  };
  const ALIAS = { facebook: "fb", meta: "fb", instagram: "ig", spotify: "sp", youtube: "yt", tiktok: "tt", whatsapp: "wa" };
  const url = new URL(location.href);
  const ua = navigator.userAgent;
  const ref = document.referrer;

  // 1) enlace del kit (?o=) o UTM · 2) navegador interno de la app · 3) página de origen
  let clave = url.searchParams.get("o") || ALIAS[(url.searchParams.get("utm_source") || "").toLowerCase()] || null;
  if (!RED[clave]) clave = null;
  if (!clave) {
    if (/Instagram/i.test(ua)) clave = "ig";
    else if (/FBAN|FBAV|FB_IAB/i.test(ua)) clave = "fb";
    else if (/musical_ly|TikTok|BytedanceWebview/i.test(ua)) clave = "tt";
  }
  if (!clave && ref) {
    if (/(^|\.)facebook\.com|fb\.me/.test(new URL(ref).hostname)) clave = "fb";
    else if (/instagram\.com/.test(ref)) clave = "ig";
    else if (/spotify\.com|spotify\.link/.test(ref)) clave = "sp";
    else if (/youtube\.com|youtu\.be/.test(ref)) clave = "yt";
    else if (/tiktok\.com/.test(ref)) clave = "tt";
  }
  // la primera red de la visita manda (si navega dentro del sitio no se pierde)
  if (clave) sessionStorage.setItem("hdp_origen", clave);
  else clave = sessionStorage.getItem("hdp_origen");

  const ep = url.searchParams.get("ep");
  // limpia ?o y utm para que, si copian la dirección, no arrastren el origen de otra persona
  ["o", "utm_source", "utm_medium", "utm_campaign", "utm_content", "fbclid", "si"].forEach(p => url.searchParams.delete(p));
  history.replaceState(null, "", url.pathname + (url.search || "") + url.hash);

  // plataforma preferida para escuchar: la que eligió, o la red de la que viene
  const PREF = "hdp_plataforma";
  if (!localStorage.getItem(PREF) && (clave === "sp" || clave === "yt" || clave === "fb")) {
    localStorage.setItem(PREF, RED[clave].id);
  }

  const red = clave ? RED[clave] : null;
  window.HDP_ORIGEN = {
    red: red?.id || null,
    nombre: red?.nombre || null,
    ep,
    dentroDeApp: /FBAN|FBAV|FB_IAB|Instagram|musical_ly|TikTok|BytedanceWebview/i.test(ua),
    plataforma: () => localStorage.getItem(PREF) || "youtube",
    elegirPlataforma: p => localStorage.setItem(PREF, p),
    // texto que se agrega a cada WhatsApp para saber qué red trae conversaciones
    firma: () => red ? `\n\n(Llegué desde ${red.nombre})` : "",
  };

  // ── Bienvenida a la medida ──────────────────────────────────────────────────────
  if (!red || sessionStorage.getItem("hdp_bienvenida_cerrada")) return;
  const EPS = window.EPISODIOS || [];
  const elegido = ep && (ep === "ultimo" ? EPS.find(e => e.segmento !== "Teaser") : EPS.find(e => e.youtube_id === ep));
  const quien = elegido ? (elegido.invitado || "este episodio") : null;
  const SPOTIFY = "https://open.spotify.com/show/3rwx7hZbCvJzYxBICuRcuf";
  const YOUTUBE = "https://www.youtube.com/@loshijos_delpueblopodcast?sub_confirmation=1";

  const verEp = elegido ? { texto: "▶ Verlo completo", accion: "episodio" } : { texto: "▶ Ver el último episodio", accion: "ultimo" };
  const textos = {
    facebook: { titulo: "¡Qué onda, banda de Facebook! 👋", cuerpo: quien ? `Aquí tienes completo a ${quien}, sin cortes.` : "Aquí están los 98 episodios completos, ordenados por partido y municipio.", botones: [verEp, { texto: "Únete a la comunidad", accion: "canal" }] },
    instagram: { titulo: "¡Bienvenido desde Instagram! 📸", cuerpo: quien ? `El clip era solo la probadita: aquí está ${quien} completo.` : "Del reel a la plática completa: busca a tu alcalde, diputada o partido.", botones: [verEp, { texto: "Explorar adoptados", accion: "archivo" }] },
    tiktok: { titulo: "¿Te quedaste con ganas después del clip? 👀", cuerpo: quien ? `Aquí está ${quien} completo.` : "Aquí está la entrevista completa: 98 episodios sin cortes.", botones: [verEp, { texto: "Explorar adoptados", accion: "archivo" }] },
    youtube: { titulo: "Gracias por venir desde YouTube 🎬", cuerpo: "Aquí encuentras a cada adoptado por partido y municipio, y te avisamos de cada estreno.", botones: [elegido ? verEp : { texto: "Explorar adoptados", accion: "archivo" }, { texto: "Suscribirme en YouTube", href: YOUTUBE }] },
    spotify: { titulo: "¿Vienes de Spotify? 🎧", cuerpo: quien ? `Aquí puedes ver a ${quien} en video, o seguir escuchando donde quieras.` : "Aquí también puedes ver las entrevistas en video, o seguir escuchando donde quieras.", botones: [verEp, { texto: "Seguir en Spotify", href: SPOTIFY }] },
    whatsapp: { titulo: "Te compartieron un episodio 👀", cuerpo: quien ? `Dale play a ${quien} sin salir de aquí.` : "Dale play al último episodio sin salir de aquí.", botones: [verEp, { texto: "Ver todos", accion: "archivo" }] },
  };
  const t = textos[red.id];
  const caja = document.createElement("aside");
  caja.className = `bienvenida bienvenida-${red.id}`;
  caja.setAttribute("aria-label", "Bienvenida");
  caja.innerHTML = `
    <button class="bienvenida-cerrar" type="button" aria-label="Cerrar bienvenida">×</button>
    <b>${t.titulo}</b><p>${t.cuerpo}</p>
    <div class="bienvenida-acciones">${t.botones.map((b, i) => b.href
      ? `<a class="boton ${i ? "fantasma" : ""}" href="${b.href}" target="_blank" rel="noopener">${b.texto}</a>`
      : `<button class="boton ${i ? "fantasma" : ""}" type="button" data-accion="${b.accion}">${b.texto}</button>`).join("")}</div>`;
  const destino = document.querySelector("#inicio .envoltura > div");
  if (!destino) return;
  destino.prepend(caja);
  caja.querySelector(".bienvenida-cerrar").addEventListener("click", () => {
    sessionStorage.setItem("hdp_bienvenida_cerrada", "1");
    caja.remove();
  });
  caja.addEventListener("click", e => {
    const a = e.target.closest("[data-accion]")?.dataset.accion;
    if (!a) return;
    if (a === "episodio" && elegido) window.HDP_APP?.abrirModal(elegido);
    if (a === "ultimo") window.HDP_APP?.abrirModal(EPS.find(x => x.segmento !== "Teaser"));
    if (a === "archivo") document.getElementById("adoptados")?.scrollIntoView({ behavior: "smooth" });
    if (a === "canal") document.getElementById("canal")?.scrollIntoView({ behavior: "smooth" });
  });
})();

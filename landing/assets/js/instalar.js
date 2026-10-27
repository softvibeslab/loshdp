/* Los HDP — app instalable: service worker, botón "Descargar app" y hoja de instrucciones por dispositivo.
   Expone window.HDP = { hoja, cerrarHoja, sw, disp } para envivo.js. */
(() => {
  const $ = (s, c = document) => c.querySelector(s);
  const ua = navigator.userAgent;
  const disp = {
    ios: /iPhone|iPad|iPod/.test(ua) || (/Macintosh/.test(ua) && navigator.maxTouchPoints > 1),
    android: /Android/.test(ua),
    // navegadores dentro de apps (Facebook, Instagram, TikTok…): ahí no se puede instalar
    dentroDeApp: /FBAN|FBAV|FB_IAB|Instagram|musical_ly|TikTok|BytedanceWebview|Line\/|Twitter|Snapchat/i.test(ua),
    mac: /Macintosh/.test(ua) && navigator.maxTouchPoints <= 1,
    windows: /Windows/.test(ua),
    safari: /Safari/.test(ua) && !/Chrome|CriOS|FxiOS|EdgiOS|Edg\//.test(ua),
    firefox: /Firefox|FxiOS/.test(ua),
    instalada: matchMedia("(display-mode: standalone)").matches || navigator.standalone === true
  };
  disp.movil = disp.ios || disp.android;
  document.documentElement.classList.toggle("modo-app", disp.instalada);

  // ── Hoja inferior reutilizable ──────────────────────────────────────────────────
  const hoja = $("#hoja"), cuerpo = $("#hoja-cuerpo");
  let focoPrevio;
  function abrirHoja(html) {
    focoPrevio = document.activeElement;
    cuerpo.innerHTML = html;
    hoja.hidden = false;
    requestAnimationFrame(() => hoja.classList.add("abierta"));
    document.body.style.overflow = "hidden";
    $("#hoja-cerrar").focus();
  }
  function cerrarHoja() {
    hoja.classList.remove("abierta");
    document.body.style.overflow = "";
    setTimeout(() => { hoja.hidden = true; }, 250);
    focoPrevio?.focus();
  }
  $("#hoja-cerrar").addEventListener("click", cerrarHoja);
  hoja.addEventListener("click", e => { if (e.target === hoja) cerrarHoja(); });
  addEventListener("keydown", e => { if (e.key === "Escape" && !hoja.hidden) cerrarHoja(); });

  // ── Service worker ──────────────────────────────────────────────────────────────
  const sw = "serviceWorker" in navigator
    ? navigator.serviceWorker.register("sw.js").then(() => navigator.serviceWorker.ready).catch(() => null)
    : Promise.resolve(null);

  // ── Instalación ─────────────────────────────────────────────────────────────────
  let aviso = null;
  addEventListener("beforeinstallprompt", e => { e.preventDefault(); aviso = e; });
  addEventListener("appinstalled", () => {
    aviso = null;
    abrirHoja(`<span class="hoja-ico">🎉</span><h3>¡Listo, ya tienes la app!</h3><p>Búscala como <b>Los HDP</b> en tu pantalla de inicio o en tus aplicaciones.</p>`);
  });

  const icoCompartir = `<svg class="ico-paso" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 3v12M7 8l5-5 5 5M5 12v8h14v-8"/></svg>`;
  const icoMenu = `<svg class="ico-paso" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><circle cx="12" cy="5" r="2"/><circle cx="12" cy="12" r="2"/><circle cx="12" cy="19" r="2"/></svg>`;
  const pasos = lista => `<ol class="pasos">${lista.map(p => `<li><span>${p}</span></li>`).join("")}</ol>`;
  const urlSitio = () => location.origin + location.pathname.replace(/[^/]*$/, "");

  function accesoDirecto() {
    const url = urlSitio();
    let nombre, tipo, contenido;
    if (disp.mac) {
      nombre = "Los HDP.webloc"; tipo = "application/x-apple-plist";
      contenido = `<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n<plist version="1.0"><dict><key>URL</key><string>${url}</string></dict></plist>\n`;
    } else if (disp.windows) {
      nombre = "Los HDP.url"; tipo = "application/internet-shortcut";
      contenido = `[InternetShortcut]\r\nURL=${url}\r\n`;
    } else {
      nombre = "los-hdp.desktop"; tipo = "application/x-desktop";
      contenido = `[Desktop Entry]\nType=Link\nName=Los HDP el Podcast\nURL=${url}\nIcon=${url}img/app/icono-192.png\n`;
    }
    const a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([contenido], { type: tipo }));
    a.download = nombre;
    document.body.appendChild(a);
    a.click();
    setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 1000);
  }

  async function copiarEnlace(boton) {
    try { await navigator.clipboard.writeText(urlSitio()); boton.textContent = "¡Enlace copiado!"; }
    catch { prompt("Copia este enlace:", urlSitio()); }
  }

  async function instalar() {
    if (disp.instalada) {
      return compartir();
    }
    if (aviso) {
      aviso.prompt();
      const { outcome } = await aviso.userChoice;
      if (outcome === "accepted") aviso = null;
      return;
    }
    const cabeza = `<span class="hoja-ico"><img src="img/app/icono-192.png" alt=""></span><h3>Lleva Los HDP en tu ${disp.movil ? "celular" : "compu"}</h3>`;
    if (disp.dentroDeApp) {
      abrirHoja(`${cabeza}<p>Estás viendo el sitio dentro de una app (Facebook, Instagram o TikTok). Desde ahí no se puede instalar.</p>
        ${pasos([`Toca el menú ${icoMenu} o <b>···</b> de arriba.`, `Elige <b>Abrir en ${disp.ios ? "Safari" : "el navegador"}</b>.`, `Ya en el navegador, vuelve a tocar <b>Descargar app</b>.`])}
        <button class="boton" type="button" id="hoja-copiar">Copiar enlace</button>`);
      $("#hoja-copiar").addEventListener("click", e => copiarEnlace(e.currentTarget));
    } else if (disp.ios) {
      abrirHoja(`${cabeza}<p>En iPhone y iPad se instala en tres toques, sin pasar por la App Store:</p>
        ${pasos([`Toca <b>Compartir</b> ${icoCompartir} en la barra de ${/CriOS/.test(ua) ? "Chrome" : "Safari"}.`, `Desliza y elige <b>Agregar a pantalla de inicio</b>.`, `Toca <b>Agregar</b>. Listo: el ícono de Los HDP queda junto a tus apps.`])}
        <p class="letra-chica">Con la app instalada puedes activar alertas de transmisiones en vivo (iOS 16.4 o posterior).</p>`);
    } else if (disp.android) {
      abrirHoja(`${cabeza}${pasos([`Toca el menú ${icoMenu} del navegador.`, `Elige <b>Instalar app</b> o <b>Agregar a la pantalla principal</b>.`, `Confirma con <b>Instalar</b>.`])}`);
    } else {
      const guia = disp.mac && disp.safari
        ? [`En la barra de menú elige <b>Archivo → Agregar al Dock</b>.`, `Confirma con <b>Agregar</b>: Los HDP queda en tu Dock como app.`]
        : disp.firefox
          ? [`Firefox no instala sitios como app. Descarga el acceso directo de abajo o abre esta página en Chrome o Edge.`]
          : [`Busca el ícono de instalar <b>⊕</b> a la derecha de la barra de direcciones.`, `O abre el menú ${icoMenu} → <b>Transmitir, guardar y compartir → Instalar página como app</b>.`];
      abrirHoja(`${cabeza}${pasos(guia)}
        <div class="hoja-acciones"><button class="boton" type="button" id="hoja-acceso">Descargar acceso directo</button></div>
        <p class="letra-chica">El acceso directo (${disp.mac ? ".webloc" : disp.windows ? ".url" : ".desktop"}) abre el sitio con doble clic. Ponlo en tu escritorio.</p>`);
      $("#hoja-acceso").addEventListener("click", accesoDirecto);
    }
  }

  async function compartir() {
    const datos = { title: "Los HDP el Podcast", text: "El podcast político de Hidalgo 🎙️", url: urlSitio() };
    if (navigator.share) {
      try { await navigator.share(datos); } catch { /* cancelado */ }
      return;
    }
    abrirHoja(`<span class="hoja-ico">🔗</span><h3>Comparte Los HDP</h3><p>${datos.url}</p><button class="boton" type="button" id="hoja-copiar">Copiar enlace</button>`);
    $("#hoja-copiar").addEventListener("click", e => copiarEnlace(e.currentTarget));
  }

  document.querySelectorAll("[data-instalar]").forEach(b => {
    if (disp.instalada) {
      b.querySelector("[data-texto]")?.replaceChildren("Compartir");
      b.setAttribute("aria-label", "Compartir Los HDP");
    }
    b.addEventListener("click", e => { e.preventDefault(); instalar(); });
  });

  // Enlace directo a la instalación (p. ej. desde /links): ../#app
  if (location.hash === "#app" && !disp.instalada) {
    addEventListener("load", () => setTimeout(() => {
      if (!aviso) return instalar();
      // Chrome/Edge exigen un toque del usuario para mostrar su ventana de instalación
      abrirHoja(`<span class="hoja-ico"><img src="img/app/icono-192.png" alt=""></span><h3>Instala Los HDP</h3><p>Gratis, sin tienda de apps y ocupa casi nada de espacio.</p><div class="hoja-acciones"><button class="boton" type="button" id="hoja-instalar-ya">Instalar ahora</button></div>`);
      $("#hoja-instalar-ya").addEventListener("click", () => { cerrarHoja(); instalar(); });
    }, 900));
  }

  window.HDP = { hoja: abrirHoja, cerrarHoja, sw, disp };
})();

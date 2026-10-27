/* Los HDP — service worker: app instalable, uso sin conexión y avisos de transmisiones en vivo.
   Páginas y datos: red primero (siempre lo más nuevo) con respaldo en caché.
   Imágenes y estilos: caché primero. /mediahub/ (privado) nunca pasa por aquí. */
const VERSION = "hdp-v2";
const BASICO = [
  "./", "index.html", "manifest.json", "assets/css/estilos.css", "assets/js/origen.js", "assets/js/app.js",
  "assets/js/instalar.js", "assets/js/envivo.js", "data/episodios.js",
  "img/marca/logo.jpg", "img/app/icono-192.png"
];
const ESTADO = "hdp-estado"; // caché aparte con las preferencias de alertas y los avisos ya enviados

self.addEventListener("install", e => {
  e.waitUntil(caches.open(VERSION).then(c => c.addAll(BASICO)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", e => {
  e.waitUntil(caches.keys()
    .then(ks => Promise.all(ks.filter(k => k !== VERSION && k !== ESTADO).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});

self.addEventListener("fetch", e => {
  const url = new URL(e.request.url);
  if (e.request.method !== "GET" || url.origin !== location.origin || url.pathname.startsWith("/mediahub/")) return;
  if (url.pathname.endsWith("/data/envivo.json")) return; // el estado en vivo jamás sale de caché
  const esEstatico = /\.(jpg|jpeg|png|webp|svg|css|woff2?)$/i.test(url.pathname);
  e.respondWith(esEstatico ? cachePrimero(e.request) : redPrimero(e.request));
});

async function cachePrimero(req) {
  const enCache = await caches.match(req);
  if (enCache) return enCache;
  const r = await fetch(req);
  if (r.ok) (await caches.open(VERSION)).put(req, r.clone());
  return r;
}
async function redPrimero(req) {
  try {
    const r = await fetch(req);
    if (r.ok) (await caches.open(VERSION)).put(req, r.clone());
    return r;
  } catch {
    return (await caches.match(req)) || (await caches.match("index.html")) || Response.error();
  }
}

// ── Avisos de transmisiones ─────────────────────────────────────────────────────
async function leerEstado() {
  const r = await (await caches.open(ESTADO)).match("estado");
  return r ? r.json() : { alertas: false, avisados: [] };
}
async function guardarEstado(s) {
  s.avisados = s.avisados.slice(-60);
  await (await caches.open(ESTADO)).put("estado", new Response(JSON.stringify(s), { headers: { "Content-Type": "application/json" } }));
}

async function revisar(datos) {
  const s = await leerEstado();
  if (!s.alertas || Notification.permission !== "granted") return;
  if (!datos) {
    const r = await fetch(`data/envivo.json?t=${Date.now()}`, { cache: "no-store" });
    if (!r.ok) return;
    datos = await r.json();
  }
  const avisos = [];
  const t = datos.transmision;
  if (datos.en_vivo && t) {
    avisos.push({
      clave: `vivo:${t.desde || t.youtube_id || t.url || ""}`,
      titulo: "🔴 Los HDP están EN VIVO",
      cuerpo: t.titulo || "Entra ya a la transmisión."
    });
  }
  const ahora = Date.now();
  (datos.proximas || []).forEach(p => {
    const falta = new Date(p.inicio).getTime() - ahora;
    if (falta <= 15 * 60e3 && falta > -10 * 60e3) {
      avisos.push({
        clave: `pronto:${p.id}`,
        titulo: falta > 0 ? `⏰ En ${Math.max(1, Math.round(falta / 60e3))} min: Los HDP en vivo` : "⏰ Los HDP empiezan ahora",
        cuerpo: [p.titulo, p.invitado].filter(Boolean).join(" · ")
      });
    }
  });
  for (const a of avisos) {
    if (s.avisados.includes(a.clave)) continue;
    s.avisados.push(a.clave);
    await self.registration.showNotification(a.titulo, {
      body: a.cuerpo, tag: a.clave, icon: "img/app/icono-192.png", badge: "img/app/icono-192.png",
      data: { url: "./?fuente=alerta#envivo" }
    });
  }
  await guardarEstado(s);
}

self.addEventListener("message", e => {
  const m = e.data || {};
  if (m.tipo === "alertas") {
    e.waitUntil(leerEstado().then(s => { s.alertas = !!m.activo; return guardarEstado(s); }));
  } else if (m.tipo === "revisar") {
    e.waitUntil(revisar(m.datos));
  } else if (m.tipo === "prueba") {
    e.waitUntil(self.registration.showNotification("Alertas activadas ✅", {
      body: "Te avisaremos cuando Los HDP salgan en vivo.", icon: "img/app/icono-192.png", tag: "prueba"
    }));
  }
});

// Android/Chrome con la app instalada: revisión periódica aunque la app esté cerrada.
self.addEventListener("periodicsync", e => {
  if (e.tag === "hdp-envivo") e.waitUntil(revisar());
});

self.addEventListener("notificationclick", e => {
  e.notification.close();
  const destino = new URL(e.notification.data?.url || "./", self.registration.scope).href;
  e.waitUntil(self.clients.matchAll({ type: "window", includeUncontrolled: true }).then(ws => {
    const w = ws.find(c => c.url.startsWith(self.registration.scope));
    return w ? w.navigate(destino).then(c => c?.focus()) : self.clients.openWindow(destino);
  }));
});

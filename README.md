# Los HDP el Podcast (Los Hijos del Pueblo)

Prospecto Softvibes · podcast de análisis político de Hidalgo (Pachuca). Hosts: Robert Leaños y Kuako Islas.

| Qué | Dónde |
|---|---|
| Investigación profunda y fugas | `docs/01-investigacion.md` |
| Estrategia, KPIs y plan 30-60-90 | `docs/02-estrategia.md` |
| Plan de implementación y deploy | `docs/03-plan-implementacion.md` |
| Inventario previo de landings (regla del workspace) | `docs/inventario-previo.md` |
| Inventario de contenido | `inventario/` (episodios.csv, invitados.csv, inventario.json) |
| Ingesta cruda por red | `ingesta/` |
| Sitio (landing + /links + /analisis) | `landing/` |
| Scripts | `scripts/ig_ingesta.py`, `scripts/fb_pagina.py`, `scripts/inventario.py` |
| Marca (logo, banner, hojas de miniaturas) | `assets/marca/` |
| Plan del cerebro, onboarding y grafo | `docs/04-plan-cerebro-onboarding-grafo.md` |
| Viaje del visitante (Meta, Spotify, YouTube → sitio) | `docs/05-viaje-del-visitante.md` · `landing/assets/js/origen.js` · kit en `kit-enlaces/` (`scripts/kit_enlaces.py`) |
| Mediahub (inventario maestro + base de conocimiento) | `mediahub/` (ver su README) · web privada `/mediahub/` |
| El Cerebro del Pueblo (3D + recorrido de insights) | `ecosistema/loshdp-brain` · web estática en `ecosistema/loshdp-brain-web` · https://loshdpbrain.softvibes.art/?tour=1 (alias `/cerebro/`) · `deploy/publicar-cerebro.sh` |
| Grafo de conocimiento (graphify) | `graphify-out/` (graph.html, GRAPH_REPORT.md, graph.json) · corpus en `grafo/corpus/` |

Vista local: `cd landing && python3 -m http.server 8799 --bind 127.0.0.1` → http://127.0.0.1:8799

Reglas: solo material público del prospecto; las cookies de sesión se leen en memoria y nunca se guardan; no se despliega ni se contacta al cliente sin autorización.

## App instalable y transmisiones en vivo

- **App (PWA):** `landing/manifest.json` + `landing/sw.js` + íconos en `landing/img/app/`. El botón "Descargar app" instala en un toque en Android/Chrome/Edge, guía de 3 pasos en iPhone/iPad, "Agregar al Dock" en Safari de Mac y acceso directo descargable (.url/.webloc/.desktop) en escritorio. Si el sitio se abre dentro de Facebook/Instagram/TikTok, pide abrirlo en el navegador. `…/#app` abre la instalación directo (lo usa `/links`).
- **En vivo:** el sitio lee `landing/data/envivo.json` cada minuto. Se opera con `scripts/envivo.py` (hora del centro de México) y se sube solo ese dato con `publicar`:

```bash
python3 scripts/envivo.py agendar --inicio "2026-10-28 19:00" --titulo "El Adoptado en vivo" --invitado "Nombre" --plataforma "Facebook y YouTube"
python3 scripts/envivo.py iniciar --youtube <id_del_live>     # o --facebook <url_del_live>
python3 scripts/envivo.py terminar
python3 scripts/envivo.py publicar
```

- **Alertas:** notificaciones del navegador (aviso al empezar el live y 15 min antes de cada transmisión agendada; en Android con la app instalada también revisa en segundo plano) + calendario suscribible `data/envivo.ics` (webcal), con recordatorio de 15 min. No hay servidor de notificaciones push: con la app cerrada, el aviso garantizado llega por el calendario.
- nginx sirve `*.ics` como `text/calendar` (ver `deploy/loshdp.softvibes.art.conf`).

# Plan de implementación — sitio Los HDP

Estado al 24-oct-2026. Base: `docs/inventario-previo.md` (nicho nuevo; referencia estructural **Bateria – Podcast HTML Template**, ThemeForest, sin compra ni copia de código).

## Arquitectura

```
landing/                  ← raíz del sitio (un solo zip para Hostinger)
├── index.html            landing: hero + último episodio, archivo filtrable, segmentos, top 5, hosts, "¿Quieres ser adoptado?", media kit, canal
├── links/                reemplazo del atom.bio (sin anuncios, con último episodio)
├── analisis/             página de análisis interactiva para el cliente (noindex)
├── assets/css|js/        estilos.css · app.js (CONFIG con los pendientes del cliente)
├── data/episodios.js     generado por scripts/inventario.py (98 episodios)
└── img/ep|marca/         98 miniaturas optimizadas (480 px) + logo, banner y foto de hosts
```

Stack: HTML/CSS/JS estático, sin dependencias. Fuentes Barlow Condensed (titulares en itálica, como sus miniaturas) + Inter. Paleta tomada de su logo: lima `#C0FF72` y carbón `#2F2F2F`.

## Fases

| Fase | Entregable | Estado |
|---|---|---|
| 0. Inventario previo | `docs/inventario-previo.md` | ✅ |
| 1. Ingesta | `ingesta/` (YT 98 + 329 shorts, TikTok, FB, IG básico, Spotify, atom.bio) | ✅ (IG parcial) |
| 2. Inventario | `inventario/` (episodios.csv, invitados.csv, inventario.json) | ✅ |
| 3. Investigación y estrategia | `docs/01-investigacion.md`, `docs/02-estrategia.md` | ✅ |
| 4. Landing + /links | `landing/` | ✅ demo local |
| 5. Página de análisis | `landing/analisis/` | ✅ demo local |
| 6. Datos del cliente | WhatsApp comercial, canal de WhatsApp, dominio | ⏳ pendiente del cliente |
| 7. Deploy demo | Subdominio Hostinger (zip único) | ⏳ requiere tu autorización |
| 8. Outreach | Kit WhatsApp/IG/email (playbook prospecta-mvp, fase 4) | ⏳ |
| 9. CMS (tier Plataforma) | Panel para publicar episodios/adoptados | ⏳ si cierra tier 2 |

## Pendientes antes de publicar

1. `CONFIG.whatsapp` y `CONFIG.canalWhatsapp` en `landing/assets/js/app.js` (hoy el formulario cae al correo `loshdp.elpodcast@gmail.com`, que sí es real).
2. Confirmar nombres y escritura de los hosts (**Robert Leaños**, **Kuako Islas**, tomados de Spotify y de una miniatura).
3. Quitar `noindex` de `landing/index.html` y `links/` cuando haya dominio y aprobación (el análisis se queda en noindex).
4. Regenerar datos con cada episodio nuevo: `python3 -I scripts/inventario.py`.
5. Partido y municipio se infieren del título y la descripción. Revisar los 28 sin partido si se quiere filtrar con precisión.

## Cómo actualizar la ingesta

```bash
# YouTube (público)
yt-dlp --skip-download --write-info-json --write-thumbnail --convert-thumbnails jpg \
  -o "ingesta/youtube/meta_videos/%(upload_date)s_%(id)s.%(ext)s" \
  "https://www.youtube.com/@loshijos_delpueblopodcast/videos"
yt-dlp --flat-playlist -J "https://www.youtube.com/@loshijos_delpueblopodcast/shorts" > ingesta/youtube/yt_shorts.json
# Instagram con la sesión del navegador (cookies en memoria, nunca a disco)
~/.local/share/uv/tools/yt-dlp/bin/python -I scripts/ig_ingesta.py los.hdp.el.podcast ingesta/instagram chrome "Profile 7" 74777619583
# Inventario + datos de la landing
python3 -I scripts/inventario.py
```

## Deploy (cuando lo autorices)

Hostinger vacía `public_html` y aplana los zips de carpeta única (lección del playbook): hay que subir **un solo zip con el contenido de `landing/` en la raíz**.

```bash
cd landing && zip -r ../deploy/los-hdp-sitio.zip . -x '.*'
```

Verificar después: `/`, `/links/`, `/analisis/`, `/data/episodios.js` y una miniatura → 200.

## QA hecha (local)

- Rutas `/`, `/analisis/`, `/links/`, datos, CSS, JS e imágenes → 200 (servidor local).
- DOM renderizado: 97 episodios en el archivo (sin el teaser), 9 tarjetas iniciales y último episodio = Navor Rojas Ep93.
- Capturas de escritorio (1440) y móvil (iframe de 390 px) revisadas: sin desborde horizontal.
- Sintaxis de `app.js` validada con Node.
- Pendiente: probar en un iPhone/Android real una vez desplegado.

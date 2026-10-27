# Mediahub Los HDP — base de conocimiento

Todo el contenido público de **Los HDP el Podcast (Los Hijos del Pueblo)** inventariado en un solo lugar.

## Qué hay

| Carpeta / archivo | Contenido |
|---|---|
| `conocimiento/INDICE.md` | Índice de los 98 episodios (fecha, segmento, invitado, vistas, enlace a su ficha) |
| `conocimiento/episodios/*.md` | Una ficha por episodio: metadata + descripción + **transcripción automática con marcas de tiempo por minuto** |
| `conocimiento/shorts.md` | 329 shorts de YouTube, ordenados por vistas, con transcripción cuando existe |
| `conocimiento/tiktok.md` | 779 TikToks ordenados por vistas, con su texto y métricas |
| `conocimiento/facebook.md` | Muestra reciente de videos de Facebook con reproducciones |
| `inventario/inventario_maestro.csv` / `.json` | **Una fila por pieza** en todas las plataformas: fecha, título, duración, vistas, likes, comentarios, compartidos, invitado vinculado, temas, hashtags, URL original y ruta del archivo en el hub |
| `inventario/resumen.json` | Totales por plataforma, horas, temas y hashtags más usados |
| `miniaturas/youtube/` | Portadas de los 98 episodios |
| `web/` | Visor del hub (se publica en el VPS) |

## Dónde están los archivos pesados

En el VPS, en `/srv/loshdp-mediahub/`, con acceso por el visor privado **https://loshdp.softvibes.art/mediahub/** (usuario y contraseña en `PRIVADO/mediahub-acceso.txt`, fuera de git):

| Media | Formato | Ruta |
|---|---|---|
| Audio de los 98 episodios | Opus mono 32 kbps (~14 MB/h) | `youtube/episodios/` |
| 329 shorts de YouTube | MP4 ≤480p | `youtube/shorts/` |
| 779 TikToks | MP4 540p (el más ligero disponible) + metadata y portada | `tiktok/video/`, `tiktok/meta/` |

La columna `archivo` del inventario es la ruta relativa: `https://loshdp.softvibes.art/mediahub/media/<archivo>`.

## Cómo usarlo como base de conocimiento

- **NotebookLM / Claude Projects / RAG:** sube `conocimiento/` completo. Cada ficha trae su metadata en el encabezado (invitado, partido, municipio, temas) para filtrar y citar con minuto exacto.
- **Buscar declaraciones:** `grep -ri "revocación" conocimiento/episodios/`.
- **Análisis:** abre `inventario/inventario_maestro.csv` en Sheets o Excel y filtra por plataforma, invitado o tema.

## Límites conocidos

- Las transcripciones son subtítulos automáticos de YouTube (`es-orig`): hay errores de reconocimiento, sobre todo en nombres propios y apodos.
- **Instagram:** solo cifras del perfil. La API respondió 429 (límite de tasa) en todos los intentos, incluso con sesión. Sus reels parecen duplicar shorts y TikToks.
- **Facebook:** solo 9 videos recientes con reproducciones. Los episodios completos de FB duplican los de YouTube; para el histórico y sus métricas se necesita acceso a Meta Business Suite.
- **TikTok:** no publica subtítulos; sus textos son las descripciones. Para transcribirlos haría falta Whisper.
- Calidad reducida a propósito (audio 32 kbps, video ≤540p) por espacio. Para producción conviene pedir los **maestros originales** al cliente.
- Invitado, partido y temas se infieren con reglas sobre títulos y descripciones; conviene revisarlos a mano antes de publicar algo derivado.

## Regenerar

```bash
deploy/publicar-mediahub.sh   # lista archivos en el VPS → inventario + conocimiento → publica el visor
```
Descargas: `scripts/vps_tiktok.sh` (corre en el VPS) y `scripts/mac_youtube_a_vps.sh episodios|shorts` (Mac → VPS por lotes).

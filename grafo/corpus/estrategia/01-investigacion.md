# Los HDP el Podcast — Investigación profunda (deep research)

**Corte:** 24-oct-2026 · **Fuentes:** solo material público de sus redes + sesión del navegador del operador para Facebook. Los datos crudos están en `ingesta/`, y el inventario procesado en `inventario/`.

## 1. Quiénes son

| Campo | Dato | Evidencia |
|---|---|---|
| Marca | **Los HDP — Los Hijos del Pueblo** ("el podcast político + chingón") | banner YouTube `assets/marca/yt_banner.jpg` |
| Hosts | **Robert Leaños** (titular en Spotify) y **"Kuako" Islas** | Spotify; miniatura Ep19 |
| Base | Pachuca, Hidalgo | temas, invitados y hashtags |
| Arranque | 27-nov-2023 (Ep1 "Somos los hijos del pueblo") | YouTube |
| Posicionamiento propio | "Podcast y Plataforma Digital de Análisis Político" (FB) · "Decimos lo que no se puede decir y como nadie lo puede decir" (YT/Spotify/TikTok) · "políticamente incorrecto, irreverente y diferente" (atom.bio) | `ingesta/*` |
| Contacto | loshdp.elpodcast@gmail.com — **solo aparece dentro de la imagen del banner** | banner |

## 2. Audiencia por canal

| Canal | Seguidores | Volumen | Lectura |
|---|---|---|---|
| **Facebook** "Los Hijos Del Pueblo" | **44,089** | 12,390 "hablando de esto" | Canal principal. Un episodio completo de *El que Respira… Aspira* (30 min) lleva **17,346 reproducciones** |
| **TikTok** @los_hijos_delpueblo | 13,500 | 780 videos · 94.2K likes | Viraliza la **opinión ciudadana** (tráfico en Pachuca: 340.9K; "¿Es Claudia?": 255.6K), no los clips de entrevista (~300–3,000) |
| **Instagram** @los.hdp.el.podcast | 2,147 | 1,089 posts · sigue a 1,169 | Canal más débil; ratio seguidos/seguidores alto |
| **YouTube** @loshijos_delpueblopodcast | 951 | 98 episodios (72.3K vistas) + 329 shorts (124K) | Archivo completo, pero poca audiencia |
| **Spotify** | — | 5★ (2 calificaciones) | Último episodio: Ep59 del 16-jul-2026 |
| Apple Podcasts | **no existe** | — | Búsqueda iTunes API, 3 variantes del nombre |

**Audiencia sumada: ~60,700 seguidores**, de los cuales el **73% está en Facebook**.

## 3. Inventario de contenido (resumen)

- **98 episodios largos** en YouTube · **107.5 horas** grabadas · **68 invitados únicos**.
- Segmentos: **El Adoptado** (56 episodios; entrevistas de 60–146 min; mediana de 569 vistas en YT) · **Mesa HDP** (27; opinión y coyuntura; mediana de 247) · **El Adoptado Judicial** (12; candidatos a jueces y magistrados 2025) · nuevos: **¿A poco sí?**, **Los Jubilados del Pueblo**, **El que Respira… Aspira**, **ANAL-isis político con Paco "El Acertijo" Cárdenas** (estos dos últimos solo en FB).
- Invitados por cargo: 14 alcaldes, 10 diputaciones locales, 5 federales, 3 del Senado, 6 de gabinete, 5 dirigencias, 12 candidaturas judiciales.
- **Pluralidad real**: MORENA, PRI, PAN, MC, PT y SOMOS. Es un activo de marca: "aquí vienen todos".
- Territorio: 18 municipios; Pachuca concentra 21 menciones.
- Top YouTube: *NOMAMS con Alito Moreno* (7,638) · **Carolina Viggiano** (6,152) · **José Antonio Rojo** (4,493) · Miguel Tello (2,630) · Karla Hernández (2,403) · Jorge Reyes (2,397).

Detalle: `inventario/episodios.csv`, `inventario/invitados.csv`, `inventario/inventario.json`.

## 4. Fugas verificables

| # | Fuga | Evidencia | Impacto |
|---|---|---|---|
| 1 | **Sin sitio propio**: no aparecen en Google. "HDP" compite con ≥4 podcasts homónimos (médico de Mérida, cristiano, argentino, "Hijo del Podcast") | búsqueda web; iTunes API | Un político, patrocinador o periodista que los busca no los encuentra |
| 2 | **Link-in-bio rentado y con anuncios**: atom.bio gratuito con intersticial de anuncio antes de dejar pasar + banner de Amnistía; sin WhatsApp, contacto ni último episodio | `ingesta/atombio/atombio.json` | Fricción y pérdida de control de marca en el único enlace del perfil |
| 3 | **Cero enlaces en las 98 descripciones de YouTube** (ni Spotify, ni FB, ni contacto) | `ingesta/youtube/meta_videos/*.info.json` | El canal no deriva tráfico a nada |
| 4 | **Correo comercial solo dentro de una imagen** | banner YT | No se puede copiar ni tocar; no hay ruta clara para patrocinar o pedir entrevista |
| 5 | **Spotify atrasado ~3 meses y con numeración distinta**: Mendoza es "Ep59" en Spotify (jul-2026) y "Ep80" en YouTube (abr-2026); los Ep81–93 no están | `ingesta/spotify/spotify_show.json` | El oyente de audio se pierde la temporada electoral |
| 6 | **Sin Apple Podcasts** | iTunes API | Fuera de la segunda plataforma de audio |
| 7 | **63% de los shorts (206/329) se titulan solo con la fecha** ("October 21, 2026") | `ingesta/youtube/shorts.json` | Cero búsqueda y cero gancho; mediana de 181 vistas |
| 8 | **Numeración rota**: falta el Ep89, el Ep83 no tiene título, y Mesa/Adoptado usaron series separadas hasta el Ep11 | `inventario/inventario.json` | Archivo difícil de navegar y de citar |
| 9 | **El formato que viraliza no es el que más producen**: en TikTok la opinión ciudadana llega a 340K, mientras los clips de entrevista quedan en 300–3K | `ingesta/tiktok/tiktok_perfil.json` | Esfuerzo concentrado en el formato de menor alcance |
| 10 | **Alcance sin captura**: 17K personas vieron un episodio en FB y no existe ningún lugar al cual invitarlas (lista, canal de WhatsApp, newsletter) | `ingesta/facebook/facebook_videos.json` | Audiencia 100% rentada a Meta |

## 5. Identidad visual actual

- **Paleta:** verde lima `#C0FF72` sobre carbón `#2F2F2F`; blanco para titulares; acentos rojo/naranja en las miniaturas.
- **Logo:** "LOS HDP" con un signo **?** que contiene un micrófono, más "podcast" en píldora y "-LOS HIJOS DEL PUEBLO-" espaciado.
- **Miniaturas 2026** (ya consistentes): nombre del invitado en itálica condensada blanca, píldora lima *"el adoptado DE LOS HDP"*, estudio oscuro con logo en neón.
- 2024–2025: al menos 6 estilos distintos de miniatura (`assets/marca/contacto_miniaturas_2025.jpg`).

## 6. Voz de marca

Irreverente, de cantina política, con cariño burlón hacia el poder: *"Hijos del purísimo pueblo hidalguense"*, *"fue algo mágico y celestial"*, *"exquisitamente monumental"*, *"no se sulfuren"*, *"HDTPM"*. A cada invitado le ponen un apodo ("el Incómodo", "el Colegiado", "el Inmortal", "el Tigre", "el Carretas") y lo **"adoptan"** como hijo del pueblo.

## 7. Benchmark local

En Hidalgo, la conversación política digital está en medios tradicionales (Quadratín Hidalgo, El Huarache, Radar Político, Radio Hidalgo). **No se encontró otro podcast de entrevista política local con este volumen.** Los HDP ya entrevistó al director de Radio Hidalgo (Ep58), así que el hueco de "el podcast donde se sienta toda la clase política de Hidalgo" está libre y ellos lo ocupan de hecho, pero no lo comunican.

Patrones ganadores a copiar de podcasts de entrevista grandes: (1) una página por invitado, indexable; (2) un media kit público con cifras; (3) clips con titular-gancho, no con fecha.

## 8. Limitaciones de la ingesta

- **Instagram:** la API respondió 429 (rate limit) en todos los endpoints, incluso con la sesión. Solo hay cifras de perfil (Nimble). No se insistió para no arriesgar un bloqueo de la cuenta del operador. Pendiente: reintentar en unas horas o exportar con la sesión directamente en el navegador.
- **Facebook:** solo la primera carga de la pestaña Videos (9 videos, 23–24 oct). Para el histórico se necesita paginar GraphQL o Meta Business Suite si los dueños dan acceso.
- **TikTok:** perfil + 20 videos (3 fijados + 17 recientes) vía Nimble. El listado completo de 780 requiere sesión.
- Partido y cargo de cada invitado se **infieren** del título y la descripción; 28 apariciones quedaron sin partido explícito.

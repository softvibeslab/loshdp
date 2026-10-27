# Viaje del visitante: de Meta, Spotify y YouTube al sitio

Corte: 24-oct-2026. Implementado en `landing/assets/js/origen.js`, `app.js` y `links/index.html`; kit en `kit-enlaces/`.

## El problema que resuelve

Hoy cada red manda a la gente a otra red (o a ninguna parte). Quien ve un clip en Facebook no tiene dónde ver la entrevista completa con contexto, quien escucha en Spotify no sabe que hay video, y nadie sabe qué red trae conversaciones. El viaje nuevo hace que **cada red lleve al sitio, al episodio exacto, con una bienvenida que reconoce de dónde viene**, y que el siguiente paso (escuchar, compartir o escribir) quede a un toque.

## Cómo reconoce de dónde viene

1. **Enlace del kit:** `?o=fb | ig | sp | yt | tt | wa` (o `utm_source`).
2. **Navegador interno:** Facebook, Instagram y TikTok se detectan aunque el enlace no traiga `?o=`.
3. **Página de origen:** facebook.com, instagram.com, spotify.com, youtube.com, tiktok.com.

La primera red de la visita se guarda en la sesión. El parámetro `?o=` se borra de la barra de direcciones para que, si la persona copia el enlace, no arrastre su origen. Sin cookies ni analítica: todo vive en el navegador del visitante.

## El viaje por red

| Llega desde | Bienvenida | Acción principal | Segunda acción | Retorno |
|---|---|---|---|---|
| **Facebook** (44K, la plaza) | «¡Qué onda, banda de Facebook!» + el episodio que vio | ▶ Verlo completo | Únete a la comunidad | WhatsApp dice «Llegué desde Facebook» |
| **Instagram** | «El clip era solo la probadita» | ▶ Verlo completo | Explorar adoptados | /links con su origen |
| **TikTok** (3.3M de vistas) | «¿Te quedaste con ganas después del clip?» | ▶ La entrevista completa | Explorar adoptados | /links con su origen |
| **Spotify** | «¿Vienes de Spotify? Aquí también puedes verla en video» | ▶ Ver en video | Seguir en Spotify | Spotify queda como plataforma preferida |
| **YouTube** | «Gracias por venir desde YouTube» | Explorar adoptados (o el episodio) | Suscribirme (abre el aviso de suscripción) | YouTube queda como plataforma preferida |
| **WhatsApp** (alguien lo compartió) | «Te compartieron un episodio» | ▶ Verlo | Ver todos | Al compartir, el ciclo se repite |

Además, en todos los casos:

- **`?ep=<id de YouTube>` abre el episodio directo** (`?ep=ultimo` abre el más reciente). Al abrir cualquier episodio, la barra de direcciones cambia a su enlace propio.
- **Compartir** manda el enlace del sitio con el episodio (`?ep=…&o=wa`), no el de YouTube: quien lo recibe entra a la casa de Los HDP.
- **Plataforma preferida:** en el episodio, el botón principal es Spotify o YouTube según de dónde vino la persona o lo que eligió la última vez.
- **Atribución en WhatsApp:** cada mensaje (adoptarse, media kit, botón flotante, /links) termina con «(Llegué desde Facebook/Spotify/…)». Así, en el propio WhatsApp de Los HDP se ve qué red trae conversaciones, sin herramientas de analítica.

## Kit de enlaces: qué pegar en cada red

| Dónde | Enlace |
|---|---|
| Facebook · botón de la página y campo «Sitio web» | `https://loshdp.softvibes.art/?o=fb` |
| Facebook · comentario fijado en cada episodio o clip | `https://loshdp.softvibes.art/?o=fb&ep=<id>` (columna `enlace_facebook` del CSV) |
| Instagram · link en bio | `https://loshdp.softvibes.art/links/?o=ig` |
| Instagram · historias con sticker de enlace | `https://loshdp.softvibes.art/?o=ig&ep=<id>` |
| TikTok · link en bio | `https://loshdp.softvibes.art/links/?o=tt` |
| Spotify · descripción del show | `https://loshdp.softvibes.art/?o=sp` |
| Spotify · notas de cada episodio | `https://loshdp.softvibes.art/?o=sp&ep=<id>` |
| YouTube · descripción de cada video | bloque listo en `kit-enlaces/youtube_descripciones.md` |
| YouTube · comentario fijado | `https://loshdp.softvibes.art/?o=yt&ep=<id>` |
| YouTube · vínculos del canal (Personalización → Información básica) | `https://loshdp.softvibes.art/?o=yt` |

- **`kit-enlaces/enlaces_por_episodio.csv`:** los 98 episodios con un enlace por red.
- **`kit-enlaces/youtube_descripciones.md`:** un bloque por episodio con enlace directo, Spotify, WhatsApp, «¿Quieres ser adoptado?», media kit y hashtags.
- Regenerar después de cada episodio nuevo: `python3 -I scripts/kit_enlaces.py`.

## Cómo medir sin analítica (primeros 30 días)

1. Contar en el WhatsApp de Los HDP los mensajes con «(Llegué desde …)», por red y por semana.
2. Comparar con las vistas de cada red. Meta: que Facebook y TikTok, donde está el alcance, también traigan conversaciones.
3. Si se necesita más detalle, el siguiente paso es analítica ligera y respetuosa (Plausible o Umami en el VPS), con la autorización de Los HDP.

## Pendientes del cliente

- Pegar los enlaces del kit (son cambios en sus cuentas: lo hacen ellos o nos dan acceso).
- El canal de WhatsApp: hoy «Únete a la comunidad» lleva a la sección de comunidad del sitio.
- Spotify va atrasado (Ep59); el enlace de Spotify abre el show, no el episodio exacto, hasta que estén al día.

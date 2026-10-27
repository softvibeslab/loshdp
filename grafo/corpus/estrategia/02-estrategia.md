# Los HDP — Estrategia y plan

Base: `docs/01-investigacion.md` (fugas 1–10) e `inventario/`.

## 1. Diagnóstico en una frase

Los HDP ya son, de hecho, **el lugar donde se sienta toda la clase política de Hidalgo** (68 invitados de 6 partidos en 107 horas), pero lo comunican como "un podcast más". Su audiencia vive rentada en Facebook (73%), su archivo no se encuentra en buscadores y no existe una ruta para que un patrocinador o un político los contrate.

## 2. Posicionamiento propuesto

> **"El podcast donde Hidalgo se sienta a platicar sin filtro."**
> Todos los partidos, todos los municipios, ninguna línea editorial comprada.

- **Activo diferencial:** pluralidad comprobable (MORENA, PRI, PAN, MC, PT y SOMOS) + formato largo (60–146 min) + voz irreverente.
- **Ritual de marca:** "la adopción". Cada invitado se vuelve "hijo del pueblo" y recibe un apodo. Hay que convertirlo en un activo visible: un archivo de **adoptados** con ficha, apodo y episodio.
- **Mantener la voz** ("no se sulfuren", "mágico y celestial", "HDTPM"). No la suavizaríamos: es lo que los distingue de Quadratín o Radio Hidalgo.

## 3. Audiencias y conversión

| Audiencia | Qué busca | Conversión |
|---|---|---|
| Ciudadano hidalguense | Enterarse "de lo que no se dice"; ver a su alcalde o diputado en confianza | Ver episodio → seguir en FB/TikTok → unirse al **canal de WhatsApp** |
| Político / equipo de comunicación | Exposición, ser "adoptado" | **Solicitar entrevista** (formulario o WhatsApp precargado) |
| Marca local / patrocinador | Alcance hidalguense segmentado | **Descargar media kit** → WhatsApp comercial |
| Periodistas / medios | Citar declaraciones | Página del episodio con fecha, tema y enlace para citar |

## 4. Ecosistema de canales (rol de cada uno)

| Canal | Rol | Acción inmediata |
|---|---|---|
| **Sitio propio** (nuevo) | Casa: archivo buscable de adoptados, media kit y captura | Landing + archivo filtrable (implementado en `landing/`) |
| **Facebook** | Alcance principal (episodio completo + clips) | Fijar post con el enlace al sitio y al canal de WhatsApp |
| **TikTok** | Descubrimiento con opinión ciudadana | Recuperar el formato "opinión de calle/coyuntura" que dio 340K |
| **YouTube** | Archivo y SEO | Plantilla de descripción con enlaces + capítulos + títulos-gancho en shorts |
| **Spotify + Apple** | Oyente fiel de audio | Poner al día los Ep81–93; dar de alta el RSS en Apple Podcasts; unificar numeración |
| **Instagram** | Apoyo visual (carruseles de frases) | Bajar los seguidos (1,169) y reciclar las miniaturas como carrusel |
| **Canal de WhatsApp** (nuevo) | Audiencia **propia** | "Te avisamos cuando adoptemos a alguien nuevo" |

## 5. Sistema de contenido: 1 episodio → 12 piezas

1. Episodio largo: YouTube + FB + Spotify/Apple **el mismo día** y con el **mismo número**.
2. 6–8 clips verticales con **titular-gancho** (nunca la fecha). Fórmula: `[Nombre/apodo] + [declaración polémica entre comillas]`, p. ej. *"Navor Rojas: 'me deslindé del nombramiento de Fayad'"*.
3. 1 carrusel de IG con 3 frases + portada.
4. 1 ficha en el sitio (adoptado + apodo + cargo + partido + municipio + video incrustado).
5. 1 mensaje al canal de WhatsApp.
6. 1 frase para que el invitado la comparta (tarjeta 1080×1350 con logo). Así se aprovecha la audiencia del invitado.

**Plantilla de descripción de YouTube** (resuelve la fuga 3):
```
Adoptamos a [Nombre] "[apodo]", [cargo] de [municipio]. [2 líneas de gancho]

⏱ Capítulos
00:00 …

🎧 Audio: Spotify · Apple Podcasts
📲 Canal de WhatsApp: [link]
🌐 Todos los adoptados: [sitio]/adoptados
🤝 Patrocinios y entrevistas: [WhatsApp comercial] · loshdp.elpodcast@gmail.com

#ElAdoptado #Hidalgo #[Municipio] #[Partido]
```

## 6. Calendario editorial (rumbo a 2027)

El proceso interno de 2027 ya arrancó (Navor Rojas y Jorge Reyes, aspirantes a Pachuca; registros en MORENA). Es la temporada alta natural del podcast.

- **Serie "Rumbo al 2027"**: un aspirante por semana, con el mismo cuestionario base. Así las respuestas se comparan entre sí, y eso es contenido citable por medios.
- **"¿A poco sí?"**: verificador cómico de promesas (el formato ya existe; darle cadencia quincenal).
- **Mesa HDP** semanal y corta (20–30 min), con clips de opinión para TikTok (el formato que viraliza).
- **Mapa de municipios adoptados**: meta de 84/84 municipios de Hidalgo. Hoy van 18.

## 7. Modelo de ingresos

| Línea | Descripción | Precio indicativo* |
|---|---|---|
| Patrocinio de temporada | Mención + logo en el set + en el sitio | Por definir con media kit |
| Patrocinio de segmento | "¿A poco sí? presentado por…" | — |
| Pauta local en clips | Negocio hidalguense en preroll / mención | — |
| Producción para terceros | Usar el set y el equipo para otros creadores | — |

*No proponemos precios sin las métricas privadas de Meta Business Suite (alcance, % Hidalgo, edad).

⚠️ **Ética y cumplimiento electoral:** cobrar a políticos por ser entrevistados, sobre todo en precampaña o campaña, puede contar como propaganda contratada y afecta la credibilidad, que es su activo principal. Recomendamos: (1) entrevistas **siempre gratuitas** para políticos; (2) monetizar con marcas comerciales; (3) etiquetar como "contenido patrocinado" cualquier pieza pagada; (4) consultar con un asesor electoral antes del periodo de campañas 2027.

## 8. KPIs (línea base → meta a 90 días)

| KPI | Base (24-oct-2026) | Meta 90 días |
|---|---|---|
| Seguidores totales | 60,687 | 70,000 |
| Suscriptores del canal de WhatsApp | 0 | 1,500 |
| Episodios en Spotify al día | hasta el Ep59/80 | 100% el día del estreno |
| Presencia en Apple Podcasts | no | sí |
| Shorts con título-gancho | 37% | 100% |
| Mediana de vistas por short (YT) | 181 | 400 |
| Solicitudes de entrevista vía sitio | 0 | 10/mes |
| Leads de patrocinio | 0 | 3 conversaciones |
| Municipios adoptados | 18 | 30 |

## 9. Plan 30-60-90

**Días 1–30 · Casa propia y orden**
- Publicar el sitio (landing + archivo de adoptados + media kit) en dominio propio (sugerencia: `loshdp.mx` o `loshijosdelpueblo.mx`; verificar disponibilidad).
- Reemplazar atom.bio por `/links` del sitio.
- Crear el canal de WhatsApp y fijarlo en FB/IG/TikTok.
- Poner al día Spotify (Ep81–93) y dar de alta Apple Podcasts con el mismo RSS.
- Plantilla de descripción en los 10 episodios más vistos de YouTube.
- Retitular los 206 shorts fechados (empezando por los 30 con más vistas).

**Días 31–60 · Sistema de contenido**
- Arrancar "Rumbo al 2027" (cuestionario base).
- Pipeline 1→12 por episodio, con un checklist en el CMS.
- Tarjetas de frase para que cada invitado las comparta.
- Dos clips semanales de opinión ciudadana para TikTok.

**Días 61–90 · Monetización**
- Media kit con métricas privadas de Meta.
- Tres propuestas a marcas hidalguenses (no partidistas).
- Medir: WhatsApp, solicitudes y leads. Ajustar.

## 10. Siguiente decisión para el cliente

1. ¿Tienen dominio? ¿Quién administra la página de FB y el canal de YouTube? (necesario para métricas privadas)
2. WhatsApp comercial oficial (hoy no hay ninguno público).
3. ¿Aceptan la política de "entrevistas a políticos siempre gratuitas"?

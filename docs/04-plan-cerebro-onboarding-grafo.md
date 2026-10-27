# Plan · El Cerebro del Pueblo, onboarding y grafo de conocimiento

Corte: 24-oct-2026. Complementa `02-estrategia.md` y `03-plan-implementacion.md`.

## Qué se construyó

| Pieza | Dónde | Para qué |
|---|---|---|
| **El Cerebro del Pueblo** (cerebro 3D) | App local `AIS-OS/apps/loshdp-brain` (http://127.0.0.1:4644) · web privada https://loshdpbrain.softvibes.art (también en https://loshdp.softvibes.art/cerebro/) | Ver todo el contenido de Los HDP como un universo conectado: 295 fichas y 1,208 conexiones en 6 categorías |
| **Onboarding de insights** | El mismo cerebro con `?tour=1` → https://loshdpbrain.softvibes.art/?tour=1 | Presentación guiada de 13 pasos para Robert y Kuako o para un patrocinador, apta para pantalla compartida |
| **Base de grafos (graphify)** | `los-hdp-podcast/graphify-out/` (graph.json, graph.html, GRAPH_REPORT.md) | Grafo semántico consultable (`graphify query`) para responder preguntas cruzadas: quién habló de qué, qué temas conectan a qué invitados |
| **Fichas enlazadas** (fuente de ambos) | `mediahub/conocimiento/{episodios,invitados,temas,municipios,clips,insights}` | Base de conocimiento estilo Obsidian: cada ficha con wikilinks reales del inventario |

## Las 6 categorías del cerebro

| Color | Categoría | Fichas | Fuente |
|---|---|---|---|
| Lima | Insights y estrategia | 28 | Canales, 6 insights, 10 fugas, estrategia, plan y entregables |
| Azul | Episodios | 98 | Metadata + transcripción por minuto |
| Rosa | Invitados | 68 | Rol, partido, municipio, episodios y clips |
| Morado | Temas, partidos y formatos | 20 | Detección por palabras clave en títulos y descripciones |
| Ámbar | Municipios | 18 | Municipios de Hidalgo mencionados |
| Coral | Clips virales | 63 | Top 45 de TikTok, 12 shorts y 6 videos de FB |

Conexiones: 639+ enlaces explícitos (inventario) y ~566 menciones (nombres de invitados que aparecen en otras fichas, sobre todo en transcripciones). Ninguna relación es inventada; partido y tema son inferencias por reglas y están marcadas así en cada ficha.

## El onboarding (13 pasos)

1. **El Cerebro del Pueblo** — 98 episodios, 68 invitados, 1,215 piezas, 3.3M de vistas en TikTok.
2. **Quiénes son** — Robert y Kuako, el ritual de «la adopción» y los formatos.
3. **Audiencia** — el 73% está en Facebook.
4. **Insight 1** — TikTok: el alcance llega por golpes virales (el top 10 suma el 33%); lo viral es la opinión, no la entrevista.
5. **Insight 2** — Jorge Reyes, el invitado imán (23 clips, más de 300K vistas).
6. **Insight 3** — Pluralidad: 6 partidos en la cabina.
7. **Insight 4** — 18 de 84 municipios.
8. **Lo más visto** — top 6 de YouTube, con el video dentro del panel.
9. **Diagnóstico** — las 10 fugas.
10. **Estrategia** — posicionamiento, sistema 1→12, «Rumbo al 2027» e ingresos limpios.
11. **Plan 30·60·90** con metas medibles.
12. **Entregables** — sitio, análisis y mediahub.
13. **Lo que necesitamos de ustedes** — dominio, accesos a métricas, horario de transmisiones, política de entrevistas y archivos maestros.

Cada paso enfoca un nodo del cerebro; sus renglones abren la ficha correspondiente (y su video original cuando existe).

## Cómo presentarlo

- **Con Robert y Kuako (30 min):** abrir https://loshdpbrain.softvibes.art/?tour=1 en pantalla compartida. Pasos 1–8 para que se reconozcan en los datos; pasos 9–13 para la conversación comercial. Terminar con **Ver crecimiento** (el cerebro se arma en ~29 s) en modo **Cine**.
- **Con un patrocinador:** pasos 3, 4, 5 y 6 (alcance, viralidad, invitado imán y pluralidad) y después el media kit del sitio.
- **Para uso interno:** buscar (`/`) un invitado o municipio y usar «Enfocar conexiones».

## Plan de siguientes pasos

| # | Acción | Responsable | Cuándo |
|---|---|---|---|
| 1 | Presentar el onboarding a Robert y Kuako; registrar sus correcciones (nombres, apodos, partidos) | Softvibes | Semana 1 |
| 2 | Corregir el inventario con su retroalimentación y regenerar todo con `deploy/publicar-cerebro.sh` | Softvibes | Semana 1 |
| 3 | Completar las descargas del mediahub y volver a correr el pipeline (las fichas ganan audio) | Automático | En curso |
| 4 | Ampliar el grafo con más transcripciones si el primer grafo resulta útil (`graphify --update`) | Softvibes | Semana 2 |
| 5 | Obtener acceso a Meta Business Suite para cargar métricas reales (alcance, % Hidalgo, edades) en el cerebro y el media kit | Cliente | Semana 2 |
| 6 | Agregar la categoría «Patrocinadores y leads» cuando haya conversaciones | Softvibes | Días 61–90 |
| 7 | Actualización semanal: nuevos episodios → inventario → cerebro → grafo | Softvibes (automatizable con cron) | Continuo |

## Regenerar

```bash
cd los-hdp-podcast
deploy/publicar-cerebro.sh          # fichas → grafo 3D → recorrido → export → /cerebro/
# local: cd AIS-OS/apps/loshdp-brain && node serve.mjs   → http://127.0.0.1:4644/?tour=1
# grafo semántico: graphify query "¿qué invitados hablaron de movilidad en Pachuca?"
```

## Límites

- Las transcripciones son automáticas (errores en nombres y apodos).
- Partido, tema y municipio se infieren por reglas; conviene validarlos con los hosts.
- El grafo de graphify cubre la capa estratégica y las transcripciones de los 10 episodios más vistos, no las 98 (decisión de costo).
- El cerebro web es privado (misma contraseña que el mediahub) y no se indexa.

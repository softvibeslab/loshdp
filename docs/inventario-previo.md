# Inventario previo — Los HDP el podcast (Los Hijos del Pueblo)

- **Fecha:** 2026-10-24
- **Skill aplicada:** `landing-inventory-first` (`/Users/rogergv/.codex/skills/landing-inventory-first/SKILL.md`)
- **Workspace revisado:** `/Users/rogergv/Documents/SoftvibesLab/SoftvibesSites`
- **Fuentes del catálogo:** `AGENTS.md`, `index.html` (41 entradas declaradas, última revisión 2026-09-25), `PROMPT-TELEGRAM.md`; contrastado con `ls` del nivel raíz y de las colecciones `clientes/`, `MusicSites/`, `MenuVibes/`.

## Límites de cobertura

- Por proyecto se revisó solo el `<title>`, la meta description, el `<h1>` y los marcadores de funciones (WhatsApp, YouTube, Spotify, `<video>`, CMS) de su portada fuente, o bien su README. En los proyectos Astro cuyo README heredó el texto de la plantilla Vive Mar (blooming-skincare, blestyum-valmadero, frank-hernandez, katya-varela, suemi-garcia), el nicho se confirmó con el título del build local (`dist/index.html`) y con el campo `nicho` de `cliente.config.json`, sin leer los datos de contacto.
- Se buscaron en todo el workspace las cadenas `podcast`, `episodio`, `youtube.com/embed`, `youtube-nocookie` y `open.spotify.com/embed`. No hay ninguna landing de podcast. Solo aparecen menciones sueltas: un enlace a un podcast externo en Ieoushua y un "podcast como invitado" en la documentación de Mario Villanueva.
- **Excluidos como base:** `node_modules/`, `dist/`, `dist-*`, `*.zip` (p. ej. `cisne-negro-cerveceria.zip`, `fabiola-mvp_20260714.zip` y los zips de hopepaoo, malandra y Ieoushua), copias de despliegue, `output/`, `outputs/`, `tmp/`, `media-archivo-vivemar/`, `.playwright-cli/`, `.tools/`, `.ua/` y `graphify-out/`. Tampoco se usan los repositorios externos de herramientas: `agency-agents`, `awesome-cursorrules`, `MoneyPrinterV2`, `codex-design-skill`, `skills`, `scroll-craft`, `scroll-world` y sus `-onboarding` (las demos de onboarding son de ejemplo y no corresponden a clientes).
- No se leyeron `.env`, credenciales, leads ni carpetas `prospectos/`. La revisión de otros proyectos fue de solo lectura. Que exista una página no significa que esté publicada ni probada.

## Nicho del encargo

- **Nicho:** medio digital / podcast de opinión y análisis político.
- **Subnicho:** videopodcast de entrevistas largas a políticos locales ("El Adoptado"), mesas de opinión y shorts/reels; alcance regional en Hidalgo (Pachuca).
- **Audiencias:** (1) ciudadanos hidalguenses interesados en política local; (2) políticos y patrocinadores.
- **Conversiones:** (1) ver o escuchar episodios y seguir en redes (YouTube, Spotify, TikTok, Instagram, Facebook); (2) contacto comercial, patrocinio o agendar entrevista por WhatsApp o correo.
- **Stack:** HTML/CSS/JS estático con despliegue en Hostinger.

## Tabla de proyectos

| Proyecto | Ruta (portada fuente) | Nicho / subnicho | Conversión principal | Landing | Stack | Comparación | Justificación |
|---|---|---|---|---|---|---|---|
| Ieoushua Barragán | `MusicSites/ioushua-barragan/index.html` (variantes `alt-cultura/`, `alternative/`, `hero-propuestas.html`, `analisis/`, `cms/`) | Música / jazz, booking de artista | Escuchar (YouTube/Spotify/Apple) + booking por WhatsApp | Sí | HTML/CSS/JS | **Relacionado** | Tiene una galería de video con fachada YouTube, una fila "listen" hacia plataformas de audio y un CTA de booking. El nicho es un artista y no un medio de opinión. |
| Rhomán (EPK) | `MusicSites/ioushua-barragan/rhoman/index.html` | Música electrónica / EPK de DJ | Contacto y redes | Sí | HTML/JS | **Relacionado** | El formato EPK (perfil de medios + embeds) se parece a un media kit, pero no es un podcast. |
| Hopepaoo (Paola Elizabeth) | `hopepaoo/landing.html` (copias `deploy_*`, `final_*`, `public_html/`) | Cantante / performer | Contacto, agenda de eventos | Sí | HTML/JS + CMS local | **Relacionado** | Marca personal escénica con video, sección de eventos y un CMS en localStorage. No es un medio informativo. |
| Berova Muñoz · Mamá Blog | `berova-mama-blog/v2/public/index.html` | Creadora de contenido (cocina/maternidad) | Consumir contenido, seguir en redes | Sí | Node.js + HTML/CSS + CMS | **Relacionado** | Comparte la lógica de "creador de contenido → biblioteca de piezas" y tiene un CMS con borradores. El tema y la audiencia son otros. |
| Val Madero | `valmadero/src/pages/index.astro` | Inmobiliario / marca personal | WhatsApp, formulario | Sí | Astro + CMS PHP | Distinto | El nicho es inmobiliario. Su sección `#videos`, donde solo se reproduce un reel a la vez, sirve como patrón para shorts. |
| Cervecería Cisne Negro | `cisne-negro-cerveceria/sitio/index.html` | Cervecería artesanal (Pachuca) | Visita, menú QR, Pasaporte/NPS | Sí | HTML/JS + Python/SQLite | Distinto | Comparte la plaza (Pachuca) pero no el nicho. No se transfieren datos ni contenido de ese cliente. |
| Malandra | `malandra-cerveceria/src/pages/index.astro` | Cervecería artesanal / bitácora | Seguir, WhatsApp | Sí | Astro + CMS PHP | Distinto | El formato de bitácora es narrativo, pero el nicho es otro. |
| MenuVibes (+ whitelabel, barber, localito) | `MenuVibes/index.html` | SaaS gastronómico | Pedidos, menú | Sí | HTML/JS + Supabase | Distinto | Restaurantes. |
| MenuVibes Private | `MenuVibes-private/` | Operación interna | — | No (herramienta) | web | Distinto | Herramienta interna. |
| BeerVibes | `BeerVibes/README.md` | Idea cervecera | — | No (idea) | concepto | Distinto | Es una idea sin landing. |
| Caimán Tugurio | `CaimanTugurio/index.html` | Bar / menú digital | Menú, WhatsApp | Sí | HTML/JS | Distinto | Restaurantes. |
| Vivemar / Vivemar Alt | `vivemar/`, `vivemar-alt/` (+ `redirect-vivemar/`, `analisis-vivemar/`) | Inmobiliario | Catálogo, contacto | Sí | Astro/TS/PHP | Distinto | Inmobiliario. |
| Plantilla inmobiliaria | `plantilla-inmobiliaria-astro-cms/` | Plantilla inmobiliaria | Leads | Sí (demo) | Astro + CMS PHP | Distinto | Inmobiliario. |
| Blestyum / ValmaderoAnalysis | `clientes/blestyum-valmadero/sitio/`, `ValmaderoAnalysis/landing/` | Inmobiliario | WhatsApp | Sí | Astro / HTML | Distinto | Inmobiliario. |
| Katya Varela · Frank Hernández · Suemi García | `katya-varela/sitio/`, `frank-hernandez/sitio/`, `suemi-garcia/sitio/` | Inmobiliario / inversión | WhatsApp | Sí | Astro | Distinto | Inmobiliario (confirmado con build + `nicho`). |
| Ivy Loya | `ivy-loya-real-estate/` | Inmobiliario | WhatsApp | Sí | Astro | Distinto | Inmobiliario. |
| KLH Hub de rentas | `klh-hub-rentas/index.html` | Rentas | WhatsApp contextual | Sí | HTML/JS | Distinto | Inmobiliario. |
| Laura Luna | `laura-luna-broker/index.html` | Inmobiliario / marca personal | WhatsApp atribuible | Sí | HTML/JS | Distinto | Inmobiliario. Tiene un patrón de WhatsApp con tracking reutilizable. |
| Mónica Arteaga × DK del Karibe | `monica-arteaga-dkdelkaribe/index.html` | Inmobiliario | WhatsApp atribuible | Sí | HTML/JS | Distinto | Inmobiliario. `script.js` tiene `whatsappUrl()` y la colocación con `data-wa` y tracking. |
| Ocean Caribbean Playacar | `ocean-caribbean-playacar/index.html` | Inmobiliario premium | WhatsApp | Sí | HTML/JS | Distinto | Inmobiliario. |
| Tania G.O. | `tania-go-inventario/index.html` | Inmobiliario | WhatsApp | Sí | HTML/JS | Distinto | Inmobiliario. |
| Colegios 875 (+ análisis, propuesta) | `colegios-875/index.html` | Desarrollo residencial (no es un colegio) | WhatsApp, contacto | Sí | HTML/JS + Vapi | Distinto | Inmobiliario. |
| Smooth Group | `smooth-group/index.html` | Arquitectura | Contacto | Sí | HTML | Distinto | Arquitectura. |
| Fabiola MVP (+ análisis, contenido) | `fabiola-mvp/index.html` | Desarrollo personal femenino | Aplicar al programa | Sí | HTML/PHP | Distinto | Programa de acompañamiento. |
| Mario Villanueva (+ archivos `mario-*.html` y `landing-mario-eco.html` en la raíz) | `mario-villanueva/sitio/index.html` | Formación en ventas / speaker | WhatsApp | Sí | HTML/JS | Distinto | Es un formador de ventas. El podcast solo aparece como idea de visibilidad. |
| Karla Duarte | `karla-duarte-cirujana/sitio/index.html` | Médico cirujano | Cita por WhatsApp | Sí | HTML/PHP | Distinto | Salud. |
| Blooming | `blooming-skincare/sitio/` | Estética / skincare | WhatsApp | Sí | Astro | Distinto | Estética. |
| Mystic Nails Art | `mystic-nails-art/sitio/index.html` | Uñas | WhatsApp | Sí | HTML | Distinto | Belleza. |
| Diana Yoga Life | `diana-yoga-life/index.html` | Yoga | WhatsApp | Sí | HTML | Distinto | Bienestar. |
| Diana Velas Love | `diana-velas-love/` | Artesanía / velas | WhatsApp por artículo | Sí | Astro + CMS PHP | Distinto | Catálogo artesanal. |
| Emir24 Fit | `emir24-fit/` | Coach fitness | WhatsApp | Sí | Astro + CMS PHP | Distinto | Fitness. |
| Atelier Noisette | `atelier-noisette/site/index.html` | Repostería | Contacto | Sí | HTML | Distinto | Repostería. |
| Detailbox Academy | `detailbox-academy/index.html` | Capacitación automotriz | WhatsApp | Sí | HTML | Distinto | Educación técnica. |
| Áurea Corporativa | `auerea/index.html` | Vehículos recuperados | Agendar recorrido | Sí | HTML | Distinto | Automotriz. |
| Viva Aerobus | `viva-aerobus/public/` | Aerolínea (propuesta) | Planear viaje | Sí | Node.js + HTML + CMS | Distinto | Aerolínea. Su landing editorial con CMS es un precedente de proceso con Envato. |
| Resortes Momo | `resortes-momo/site/index.html` | Industrial B2B | Cotización WhatsApp | Sí | HTML/JS | Distinto | Industrial. |
| Softvibes Funnel | `softvibes-funnel/site/index.html` | Servicios digitales (propio) | Test/embudo | Sí | HTML | Distinto | Marca propia. |
| Softvibes Corporativo | `softvibes-corporativo/site/index.html` | Agencia / software (propio) | WhatsApp | Sí | HTML | Distinto | Marca propia. |
| Softvibes Flow · Skills Dashboard · Hermes specialist · Softvibes Agentes · Playbook MVP | `softvibes-flow/`, `skills-dashboard/`, `hermes-softvibes-specialist/`, `softvibes-agentes/`, `playbook-mvp/` | Herramientas / documentación internas | — | No | varios | Distinto | Herramientas internas; no son landings de un nicho. |

## Conclusión

**Nicho nuevo.** Ninguna landing del workspace corresponde a un podcast, un medio digital o un creador de contenido de opinión o noticias. Los cuatro proyectos *Relacionados* (Ieoushua/Rhomán, Hopepaoo y Berova) comparten patrones de medios o de creador, pero no prueban que el nicho ya esté desarrollado. Por eso se investigó Envato.

### Componentes reutilizables (copiar de forma selectiva, como patrón y sin datos del cliente fuente)

| Componente | Ruta de origen | Uso en Los HDP |
|---|---|---|
| Fachada YouTube ligera (`.yt-facade` → iframe `youtube-nocookie` al hacer clic) | `MusicSites/ioushua-barragan/assets/site.js` (aprox. l. 34-42; marcado en `index.html` l. 154-165) | Grilla de episodios "El Adoptado" sin cargar iframes al inicio |
| Modal de video con `data-yt` | `MusicSites/ioushua-barragan/alt-cultura/index.html` (sección `#musica` l. 232+, script l. 425+) | Reproductor en overlay para mesas de opinión |
| Fila de plataformas ("listen-row") | `MusicSites/ioushua-barragan/index.html` (l. ~176-190) | Botones "Escúchanos en Spotify / Apple / YouTube" |
| CTA de booking por WhatsApp (`#booking`) | `MusicSites/ioushua-barragan/index.html` (l. ~352) | "Agenda tu entrevista / patrocinio" |
| `whatsappUrl()` + `data-wa` por sección + evento `whatsapp_click` | `monica-arteaga-dkdelkaribe/script.js` (l. 235-296); variante con formulario calificado en `laura-luna-broker/script.js` (l. 263-289) | WhatsApp atribuible por intención: entrevista, patrocinio o prensa |
| Galería de reels con un solo video activo (`[data-reel]`) | `valmadero/src/pages/index.astro` (sección `#videos` l. 172, script l. 217) | Carrusel de shorts/reels verticales (portar de Astro a JS plano) |

Hay que reemplazar los teléfonos, IDs de video, textos, marca y tracking de los proyectos fuente. No se copian assets de clientes.

## Investigación Envato (consultada el 2026-10-24)

Las previews `preview.themeforest.net` devolvieron **403** al consultarlas de forma automatizada. Las demos se revisaron en los dominios de cada autor cuando fue posible.

| Candidato | URL oficial | Producto / stack | Secciones útiles | Verificación | Decisión |
|---|---|---|---|---|---|
| **Bateria – Podcast HTML Site Template** (liviu_cerchez) | https://themeforest.net/item/bateria-podcast-html-site-template/45421904 · demo: https://html.liviucerchez.com/bateria/ | HTML/CSS/JS sin jQuery, variables CSS, mobile-first, modo oscuro persistente. Ficha: $15 licencia regular, 26 ventas, última actualización 23-may-2023. | Episodio destacado, lista y grilla de episodios, episodio individual de audio y de video (`single-episode-video.html`), episodios con embed, links a plataformas, RSS/Apple, newsletter, feed de Instagram. | Ficha y demo (home y episodio de video) revisadas. No incluye secciones de hosts, patrocinio ni formulario de contacto en la home. El contenido de la demo es de relleno. | **Elegida como referencia estructural.** Es la que más se acerca al stack previsto (estático, ligero, sin dependencias) y su arquitectura está centrada en episodios. Desventaja: no se actualiza desde 2023. |
| **Audicast – Podcast, Video & Music HTML Template** (vecuro_themes) | https://themeforest.net/item/audicast-podcast-video-music-html-template/52632985 · demo: https://html.vecurosoft.com/audicast/ | HTML5, Bootstrap 5, SASS, jQuery + Slick. Ficha: $19 regular, 27 ventas, actualizada 12-feb-2026. También en Envato Elements. | Hero con Spotify/Apple/Soundcloud, último episodio, grilla de episodios, temporadas, sección "Watch featured episodes", hosts y detalle de host, blog, newsletter, contacto AJAX. | Ficha y demo `demo/index.html` revisadas. Los "videos" de la home solo enlazan a la página de detalle (sin reproductor). No tiene sección de sponsors y el texto es de relleno. | Referencia secundaria para las secciones **Hosts / Temporadas / Videos destacados**. Se descarta como paquete por depender de jQuery y Bootstrap. |
| **Magzin – Creative Magazine & Blog HTML Template** (alithemes) | https://themeforest.net/item/magzin-creative-magazine-blog-html-template/58969258 | HTML5, Bootstrap 5.3, Gulp/SCSS, Figma. Ficha: $19 regular, 60 ventas, actualizada 6-sep-2025. | 4 homes editoriales, archivos, 3 layouts de post, autor, modo oscuro. Los listados de búsqueda dicen "Podcast, Music and Video live play", pero la ficha no lo detalla. | Solo se revisó la ficha. La demo no fue accesible (403). **No se verificó la función de podcast.** | Descartada como base. Puede servir como referencia del ángulo de "medio/revista" (portada de notas y análisis) si después se agrega un blog. |
| News5 – News & Magazine HTML5 Template (reacthemes) | https://themeforest.net/item/news5-news-magazine-html5-template/53645565 | Bootstrap 5, jQuery, Swiper. $17, 300 ventas, actualizada 9-ene-2026. | Portal de noticias con 10 demos. | Solo se revisó la ficha. No describe funciones de video ni de podcast. | Descartada: es un portal de noticias puro y no un videopodcast. |

**Base elegida:** Bateria como referencia de estructura y flujo (home centrada en el episodio destacado → lista de episodios → plataformas → newsletter/redes), complementada con el patrón de **Hosts** y **Videos destacados** de Audicast. Ninguna de las plantillas resuelve la segunda conversión, por lo que la sección **"Patrocina / Agenda tu entrevista"** (media kit, formatos, WhatsApp y correo) se diseñará desde cero. La implementación será original en HTML/CSS/JS estático para Hostinger. Se reutilizarán los patrones internos listados arriba (fachada YouTube, WhatsApp atribuible, galería de reels).

**Licencia y compras:** no se compró ni descargó ningún paquete. Las licencias regulares revisadas cubren un producto final para un cliente sin cobro a usuarios finales. No se copia código, imágenes ni texto de las demos. Si después se decide incorporar el paquete comercial, se necesita la autorización y la licencia del usuario.

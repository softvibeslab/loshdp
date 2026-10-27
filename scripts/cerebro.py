"""Genera las fichas enlazadas de «El Cerebro del Pueblo» dentro de mediahub/conocimiento/.

Corre después de scripts/mediahub.py. Todas las conexiones salen del inventario
(invitado, partido, municipio, temas y formato inferidos de títulos y descripciones)
o de la evidencia citada en cada insight; no se inventan relaciones.

Salidas:
  conocimiento/episodios/*.md     + title/description/type y sección «Conexiones»
  conocimiento/invitados/          una ficha por invitado
  conocimiento/temas/              temas, partidos y formatos
  conocimiento/municipios/         municipios de Hidalgo con presencia
  conocimiento/clips/              clips con más alcance (TikTok, shorts, Facebook)
  conocimiento/insights/           hallazgos, fugas, estrategia y entregables
  cerebro/enlaces.json             título de nodo → URL original (para el recorrido)
"""
import csv
import json
import re
import statistics
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KB = ROOT / "mediahub/conocimiento"
CARPETAS = ["invitados", "temas", "municipios", "clips", "insights"]


def slug(s):
    s = unicodedata.normalize("NFD", s or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:60]


def sin_comillas(v):
    """El parser del grafo no desescapa \\": las comillas internas pasan a simples."""
    return str(v).replace('"', "'")


def nota(carpeta, nombre, fm, cuerpo):
    lineas = ["---"] + [f'{k}: "{sin_comillas(v)}"' for k, v in fm.items() if v not in (None, "", [])] + ["---", ""]
    (KB / carpeta / f"{nombre}.md").write_text("\n".join(lineas) + cuerpo.strip() + "\n")


def lista(enlaces):
    return "\n".join(f"- [[{e}]]" + (f" · {d}" if d else "") for e, d in enlaces) or "_Sin conexiones._"


def fmt(n):
    return f"{n:,}".replace(",", ",")


def main():
    for c in CARPETAS:
        d = KB / c
        d.mkdir(parents=True, exist_ok=True)
        for f in d.glob("*.md"):
            f.unlink()  # se regeneran completas
    items = json.loads((ROOT / "mediahub/inventario/inventario_maestro.json").read_text())
    invitados_csv = {r["invitado"]: r for r in csv.DictReader(open(ROOT / "inventario/invitados.csv"))}
    inv_global = json.loads((ROOT / "inventario/inventario.json").read_text())

    # ── episodios: localizar su ficha por URL ─────────────────────────────────────
    ep_file = {}
    for f in (KB / "episodios").glob("*.md"):
        m = re.search(r'^url: "([^"]+)"', f.read_text(), re.M)
        if m:
            ep_file[m.group(1)] = f
    episodios = [i for i in items if i["tipo"] == "Episodio" and i["url"] in ep_file]

    def ep_slug(i):
        return ep_file[i["url"]].stem

    def ep_titulo(i):
        n = f"Ep{int(re.search(r'Ep\.?\s?(\d+)', i['titulo'], re.I).group(1))}" if re.search(r"Ep\.?\s?(\d+)", i["titulo"], re.I) else i["fecha"]
        if i["invitado"]:
            return f"{n} · {i['invitado']}"
        tema = re.sub(r"^los hdp-?\s*(ep\.?\s*\d+\s*-?)?\s*", "", i["titulo"], flags=re.I).strip(" -") or i["segmento"]
        return f"{i['segmento']} {n} · {tema[:60]}"

    # ── clips: los de mayor alcance + evidencia de títulos con fecha ──────────────
    tt = sorted((i for i in items if i["plataforma"] == "TikTok"), key=lambda x: -x["vistas"])
    sh = sorted((i for i in items if i["tipo"] == "Short"), key=lambda x: -x["vistas"])
    fb = sorted((i for i in items if i["plataforma"] == "Facebook"), key=lambda x: -x["vistas"])
    clips = tt[:45] + sh[:12] + fb[:6]

    def clip_slug(i):
        return f"clip-{i['plataforma'].lower()}-{i['id']}"

    def clip_titulo(i):
        t = (i["descripcion"] or i["titulo"] or "").replace("\n", " ")
        t = re.sub(r"(\s*#\w+)+\s*$", "", t)        # quita el bloque de hashtags del final
        t = re.sub(r"#(\w+)", r"\1", t).strip(" .")  # los hashtags dentro de la frase se quedan como palabra
        t = re.sub(r"\s+", " ", t).strip()
        if len(t) > 70:
            t = t[:70].rsplit(" ", 1)[0].rstrip(" ,.;:") + "…"
        if not t or re.match(r"^[A-Z][a-z]+ \d{1,2}, \d{4}$", t):
            t = f"Short sin título ({i['titulo']})"
        return f"{t} · {fmt(i['vistas'])} vistas"

    # índices inversos para enlazar
    por_inv = defaultdict(list)
    for i in episodios + clips:
        if i["invitado"]:
            por_inv[i["invitado"]].append(i)

    # ── fichas de clips ───────────────────────────────────────────────────────────
    enlaces_url = {}
    for i in clips:
        conex = []
        if i["invitado"]:
            conex.append((f"invitado-{slug(i['invitado'])}", "invitado"))
        conex += [(f"tema-{slug(t)}", "tema") for t in i["temas"] if t not in PARTIDOS]
        conex += [(f"partido-{slug(t)}", "partido") for t in i["temas"] if t in PARTIDOS]
        conex.append((f"canal-{i['plataforma'].lower()}", "canal"))
        titulo = sin_comillas(clip_titulo(i))
        enlaces_url[titulo] = i["url"]
        nota("clips", clip_slug(i), {
            "title": titulo, "type": "clip",
            "description": f"{i['plataforma']} · {i['fecha'] or 's/f'} · {fmt(i['vistas'])} vistas" + (f" · {fmt(i['likes'])} likes" if i["likes"] else ""),
            "created": i["fecha"], "url": i["url"],
        }, f"""# {titulo}

| Plataforma | Fecha | Vistas | Likes | Comentarios | Compartidos | Duración |
|---|---|---|---|---|---|---|
| {i['plataforma']} {i['tipo']} | {i['fecha'] or '—'} | {fmt(i['vistas'])} | {fmt(i['likes']) if i['likes'] else '—'} | {fmt(i['comentarios']) if i['comentarios'] else '—'} | {fmt(i['compartidos']) if i['compartidos'] else '—'} | {round(i['duracion_seg'] or 0)} s |

## Texto publicado

{(i['descripcion'] or i['titulo'] or '').strip()}

[Ver original]({i['url']})

## Conexiones

{lista(conex)}
""")

    # ── episodios: título corto + conexiones ──────────────────────────────────────
    for i in episodios:
        f = ep_file[i["url"]]
        texto = f.read_text()
        texto = re.sub(r"\n## Conexiones\n[\s\S]*$", "\n", texto)  # idempotente
        titulo = sin_comillas(ep_titulo(i))
        enlaces_url[titulo] = i["url"]
        extra = f'title: {json.dumps(titulo, ensure_ascii=False)}\ntype: "episodio"\ndescription: {json.dumps(f"{i["segmento"]} · {i["fecha"]} · {fmt(i["vistas"])} vistas en YouTube" + (f" · {i["invitado"]}" if i["invitado"] else ""), ensure_ascii=False)}\ncreated: "{i["fecha"]}"\n'
        texto = re.sub(r"^---\n(?:title: .*\ntype: .*\ndescription: .*\ncreated: .*\n)?", "---\n" + extra, texto, count=1)
        conex = []
        if i["invitado"]:
            conex.append((f"invitado-{slug(i['invitado'])}", "invitado"))
        conex.append((f"formato-{slug(i['segmento'])}", "formato"))
        if i["partido"]:
            conex.append((f"partido-{slug(i['partido'])}", "partido"))
        if i["municipio"]:
            conex.append((f"municipio-{slug(i['municipio'])}", "municipio"))
        conex += [(f"tema-{slug(t)}", "tema") for t in i["temas"] if t not in PARTIDOS]
        f.write_text(texto.rstrip() + "\n\n## Conexiones\n\n" + lista(conex) + "\n")

    # ── invitados ─────────────────────────────────────────────────────────────────
    for nombre, piezas in por_inv.items():
        r = invitados_csv.get(nombre, {})
        eps = [p for p in piezas if p["tipo"] == "Episodio"]
        cl = [p for p in piezas if p["tipo"] != "Episodio"]
        todos_clips = [x for x in items if x["invitado"] == nombre and x["tipo"] != "Episodio"]
        conex = [(ep_slug(p), f"{p['fecha']} · {fmt(p['vistas'])} vistas") for p in eps]
        conex += [(clip_slug(p), f"{p['plataforma']} · {fmt(p['vistas'])} vistas") for p in cl]
        if r.get("partido"):
            conex.append((f"partido-{slug(r['partido'])}", "partido"))
        if r.get("municipio"):
            conex.append((f"municipio-{slug(r['municipio'])}", "municipio"))
        nota("invitados", f"invitado-{slug(nombre)}", {
            "title": nombre, "type": "invitado",
            "description": " · ".join(x for x in [r.get("rol"), r.get("partido"), r.get("municipio")] if x) or "Invitado de Los HDP",
        }, f"""# {nombre}

- **Rol:** {r.get('rol') or '—'}
- **Cargo (inferido):** {r.get('cargo') or '—'} · **Partido (inferido):** {r.get('partido') or '—'} · **Municipio:** {r.get('municipio') or '—'}
- **Episodios:** {len(eps)} · **Clips en todas las redes:** {len(todos_clips)} · **Vistas sumadas de sus clips:** {fmt(sum(x['vistas'] for x in todos_clips))}

## Conexiones

{lista(conex)}
""")

    # ── temas, partidos y formatos ────────────────────────────────────────────────
    con_tema = defaultdict(list)
    for i in episodios + clips:
        for t in i["temas"]:
            con_tema[t].append(i)
    for t, piezas in con_tema.items():
        pref = "partido" if t in PARTIDOS else "tema"
        eps = [p for p in piezas if p["tipo"] == "Episodio"]
        conex = [(ep_slug(p), p["fecha"]) for p in sorted(eps, key=lambda x: -x["vistas"])[:25]]
        conex += [(clip_slug(p), f"{fmt(p['vistas'])} vistas") for p in piezas if p["tipo"] != "Episodio"]
        if pref == "partido":
            conex += [(f"invitado-{slug(n)}", "invitado") for n, r in invitados_csv.items() if r.get("partido") == t and n in por_inv]
        total = sum(1 for x in items if t in x["temas"])
        nota("temas", f"{pref}-{slug(t)}", {
            "title": t if pref == "tema" else f"Partido · {t}", "type": pref,
            "description": f"{total} piezas del inventario lo mencionan · {len(eps)} episodios",
        }, f"""# {t if pref == 'tema' else 'Partido · ' + t}

Aparece en **{total}** piezas del inventario ({len(eps)} episodios). Detección por palabras clave en títulos y descripciones: es una lectura aproximada.

## Conexiones (los 25 episodios más vistos y los clips del cerebro)

{lista(conex)}
""")
    # partidos que solo aparecen en el inventario de invitados (p. ej. SOMOS)
    for partido in {r["partido"] for r in invitados_csv.values() if r.get("partido")} - set(con_tema):
        invs = [n for n, r in invitados_csv.items() if r.get("partido") == partido and n in por_inv]
        eps = [p for p in episodios if p["partido"] == partido]
        nota("temas", f"partido-{slug(partido)}", {
            "title": f"Partido · {partido}", "type": "partido",
            "description": f"{len(invs)} invitados · {len(eps)} episodios",
        }, f"""# Partido · {partido}

Partido inferido del título o la descripción de sus episodios.

## Conexiones

{lista([(ep_slug(p), p['fecha']) for p in eps] + [(f'invitado-{slug(n)}', 'invitado') for n in invs])}
""")
    medianas = inv_global["mediana_vistas_por_segmento"]
    for seg, n in Counter(i["segmento"] for i in episodios).items():
        eps = [p for p in episodios if p["segmento"] == seg]
        nota("temas", f"formato-{slug(seg)}", {
            "title": f"Formato · {seg}", "type": "formato",
            "description": f"{n} episodios · mediana de {fmt(int(medianas.get(seg, 0)))} vistas en YouTube",
        }, f"""# Formato · {seg}

{FORMATOS.get(seg, '')}

- **Episodios:** {n} · **Mediana de vistas en YouTube:** {fmt(int(medianas.get(seg, 0)))}

## Episodios

{lista([(ep_slug(p), p['fecha']) for p in sorted(eps, key=lambda x: x['fecha'])])}
""")

    # ── municipios ────────────────────────────────────────────────────────────────
    por_mun = defaultdict(list)
    for i in episodios:
        if i["municipio"]:
            por_mun[i["municipio"]].append(i)
    for mun, eps in por_mun.items():
        invs = sorted({p["invitado"] for p in eps if p["invitado"]})
        nota("municipios", f"municipio-{slug(mun)}", {
            "title": f"{mun}, Hidalgo", "type": "municipio",
            "description": f"{len(eps)} episodios · {len(invs)} invitados",
        }, f"""# {mun}, Hidalgo

{len(eps)} episodios y {len(invs)} invitados vinculados (detectado en título o descripción).

## Conexiones

{lista([(ep_slug(p), p['fecha']) for p in eps] + [(f'invitado-{slug(n)}', 'invitado') for n in invs])}
""")

    # ── insights, canales, fugas y estrategia ─────────────────────────────────────
    ctx = contexto(items, tt, sh, clips, clip_slug, ep_slug, episodios, por_inv, inv_global)
    for s, d in INSIGHTS(ctx).items():
        nota("insights", s, {"title": d["title"], "type": d["type"], "description": d["desc"]},
             f"# {d['title']}\n\n{d['body'].strip()}\n\n## Conexiones\n\n{lista(d['links'])}\n")

    (ROOT / "cerebro").mkdir(exist_ok=True)
    (ROOT / "cerebro/enlaces.json").write_text(json.dumps(enlaces_url, ensure_ascii=False, indent=1))
    conteo = {c: len(list((KB / c).glob("*.md"))) for c in ["episodios"] + CARPETAS}
    print(json.dumps(conteo, ensure_ascii=False))


PARTIDOS = {"MORENA", "PRI", "PAN", "MC", "PT"}
FORMATOS = {
    "El Adoptado": "La entrevista insignia: de una a dos horas y media con alcaldes, diputados, senadores, dirigentes y personajes de Hidalgo. Al final, el invitado queda «adoptado» y con apodo.",
    "Mesa HDP": "Robert y Kuako comentan la semana política hidalguense.",
    "El Adoptado Judicial": "Candidatas y candidatos a jueces y magistrados de Hidalgo antes de la elección judicial de 2025.",
    "¿A poco sí?": "Las promesas y declaraciones, puestas a prueba.",
    "Los Jubilados del Pueblo": "Spin-off con voces de experiencia.",
    "Teaser": "Avance promocional.",
}


def contexto(items, tt, sh, clips, clip_slug, ep_slug, episodios, por_inv, inv_global):
    meses = defaultdict(list)
    for i in tt:
        meses[(i["fecha"] or "")[:7]].append(i["vistas"])
    v = [i["vistas"] for i in tt]
    top_ep = sorted(episodios, key=lambda x: -x["vistas"])
    fecha_sh = [i for i in sh if re.match(r"^[A-Z][a-z]+ \d{1,2}, \d{4}$", i["titulo"] or "")]
    return {
        "tt_total": sum(v), "tt_n": len(v), "tt_top10": round(sum(sorted(v, reverse=True)[:10]) / sum(v) * 100, 1),
        "tt_100k": sum(1 for x in v if x >= 100000), "tt_10k": sum(1 for x in v if x >= 10000),
        "dic25": (len(meses["2025-12"]), int(statistics.median(meses["2025-12"]))),
        "oct26": (len(meses["2026-10"]), int(statistics.median(meses["2026-10"]))),
        "top_tt": [clip_slug(i) for i in tt[:3]],
        "reyes": [clip_slug(i) for i in clips if i["invitado"] == "Jorge Reyes"],
        "top_ep": [ep_slug(i) for i in top_ep[:5]],
        "fecha_sh": [clip_slug(i) for i in clips if i in fecha_sh],
        "n_fecha_sh": len(fecha_sh), "n_sh": len(sh),
        "invitados": len(por_inv), "canales": inv_global["canales"],
        "municipios": len(inv_global["municipios"]),
    }


def INSIGHTS(c):
    k = c["canales"]
    hub = "cerebro-del-pueblo"
    I = {}

    def add(s, title, typ, desc, body, links):
        I[s] = {"title": title, "type": typ, "desc": desc, "body": body, "links": links}

    add(hub, "El Cerebro del Pueblo", "inicio",
        "Mapa de todo lo que Los HDP han dicho, a quién han entrevistado y dónde los ven.",
        f"""Los HDP — Los Hijos del Pueblo: podcast de análisis político de Hidalgo conducido por Robert Leaños y Kuako Islas desde noviembre de 2023.

- 98 episodios largos (107 horas) · {c['invitados']} invitados con ficha · {c['municipios']} municipios.
- ~60,700 seguidores sumados · {fmt(c['tt_total'])} vistas en TikTok.
- Corte de datos: 24 de octubre de 2026, solo material público.""",
        [("canal-facebook", "canal principal"), ("canal-tiktok", "mayor alcance"), ("canal-youtube", "archivo"),
         ("canal-instagram", ""), ("canal-spotify", ""), ("insight-pluralidad", ""), ("insight-tiktok-alcance", ""),
         ("estrategia-posicionamiento", ""), ("estrategia-plan-30-60-90", ""), ("entregables", "")])

    canales = {
        "facebook": ("Facebook · 44,089 seguidores", f"{fmt(k['facebook']['seguidores'])} seguidores · {fmt(k['facebook']['hablando_de_esto'])} hablando de esto",
                     "Canal principal: 73% de la audiencia sumada. Un episodio completo de *El que Respira… Aspira* (30 min) llevaba 17,346 reproducciones al corte."),
        "tiktok": ("TikTok · 13,500 seguidores", f"{fmt(c['tt_n'])} videos · {fmt(c['tt_total'])} vistas",
                   "El canal de mayor alcance real: más de 3.3 millones de vistas en 22.6 horas de clips."),
        "youtube": ("YouTube · 951 suscriptores", f"98 episodios ({fmt(k['youtube']['vistas_episodios'])} vistas) + {k['youtube']['shorts']} shorts",
                    "El archivo completo, con poca audiencia. Ninguna descripción tiene enlaces."),
        "instagram": ("Instagram · 2,147 seguidores", f"{fmt(k['instagram']['posts'])} publicaciones · sigue a {fmt(k['instagram']['siguiendo'])}",
                      "El canal más débil. No se pudo descargar su feed (límite de la API)."),
        "spotify": ("Spotify · 5★ (2 calificaciones)", "Último episodio publicado: Ep59 del 16-jul-2026",
                    "Atrasado unos tres meses frente a YouTube y con otra numeración. No están en Apple Podcasts."),
    }
    for s, (t, d, b) in canales.items():
        add(f"canal-{s}", t, "canal", d, b, [(hub, "")])

    add("insight-tiktok-alcance", f"TikTok: {fmt(c['tt_total'])} vistas, concentradas en pocos videos", "insight",
        f"El top 10 suma el {c['tt_top10']}% de las vistas; {c['tt_100k']} videos pasan de 100K y {c['tt_10k']} de 10K.",
        f"""- {fmt(c['tt_n'])} videos, {fmt(c['tt_total'])} vistas en total.
- El top 10 concentra el **{c['tt_top10']}%**: el alcance llega por golpes virales, no por constancia.
- Solo {c['tt_100k']} videos superan 100K y {c['tt_10k']} superan 10K.
- Los clips largos no se castigan: los de más de 5 minutos tienen la mediana más alta.""",
        [("canal-tiktok", ""), *[(s, "récord") for s in c["top_tt"]], ("insight-opinion-viraliza", "")])
    add("insight-opinion-viraliza", "Lo que se viraliza es la opinión de coyuntura, no la entrevista", "insight",
        "Los tres récords de TikTok no tienen invitado: tráfico en Pachuca, «¿Es Claudia?» y el bastón al Presidente.",
        """Los tres videos más vistos (340.9K, 255.6K y 142.7K) son opinión de los hosts sobre un tema que le duele a la gente. Los clips de entrevista quedan, en mediana, en el mismo rango que el resto (~1.4K).

**Implicación:** la entrevista da credibilidad y relaciones; la opinión ciudadana da alcance. Hay que producir las dos a propósito.""",
        [*[(s, "") for s in c["top_tt"]], ("estrategia-sistema-1-a-12", "")])
    add("insight-jorge-reyes", "Jorge Reyes, el invitado imán", "insight",
        "Sus clips de diciembre de 2025 llegaron a 89.6K, 63.1K y 39.2K vistas.",
        "El alcalde de Pachuca es el invitado con más piezas y el de mejor rendimiento en TikTok. Pachuca concentra 21 menciones en el archivo: la capital es el tema más rentable.",
        [("invitado-jorge-reyes", ""), ("municipio-pachuca", ""), *[(s, "") for s in c["reyes"]]])
    add("insight-volumen-vs-alcance", "Más volumen, menos alcance por video", "insight",
        f"Dic-2025: {c['dic25'][0]} clips con mediana de {fmt(c['dic25'][1])} vistas. Oct-2026: {c['oct26'][0]} clips con mediana de {fmt(c['oct26'][1])}.",
        "Desde agosto de 2026 publican más de 60 clips al mes en TikTok, pero cada uno rinde menos. Muchos clips del mismo episodio salen el mismo día con títulos parecidos y compiten entre sí.\n\n**Implicación:** menos clips por episodio, mejor gancho en cada uno, y espaciarlos.",
        [("canal-tiktok", ""), ("estrategia-sistema-1-a-12", "")])
    add("insight-pluralidad", f"{c['invitados']} invitados de todos los partidos", "insight",
        "MORENA, PRI, PAN, MC, PT y SOMOS se han sentado en la cabina.",
        "La pluralidad es comprobable y es su activo más valioso frente a los medios tradicionales: «aquí vienen todos». Hoy no lo comunican en ninguna parte.",
        [("partido-morena", ""), ("partido-pri", ""), ("partido-pan", ""), ("partido-mc", ""), ("partido-pt", ""), ("formato-el-adoptado", ""), ("estrategia-posicionamiento", "")])
    add("insight-territorio", f"{c['municipios']} de 84 municipios de Hidalgo", "insight",
        "Pachuca domina; el resto del estado casi no aparece.",
        "Meta propuesta: «mapa de municipios adoptados», de 18 a 30 en 90 días. Es una serie natural rumbo a 2027.",
        [("municipio-pachuca", ""), ("municipio-huejutla", ""), ("municipio-ixmiquilpan", ""), ("estrategia-rumbo-2027", "")])

    fugas = [
        ("fuga-01-sin-sitio", "Fuga 1 · Nadie los encuentra fuera de las redes", "Sin sitio propio; «HDP» compite con al menos cuatro podcasts homónimos.", [("entregables", "resuelto con el sitio")]),
        ("fuga-02-link-rentado", "Fuga 2 · Link en bio rentado y con anuncios", "atom.bio gratuito: anuncio intersticial, banner de Amnistía, botones fuera de su paleta.", [("entregables", "/links propio")]),
        ("fuga-03-youtube-sin-enlaces", "Fuga 3 · 98 descripciones de YouTube sin enlaces", "El canal no manda tráfico a ningún lado.", [("canal-youtube", ""), ("estrategia-sistema-1-a-12", "plantilla de descripción")]),
        ("fuga-04-contacto-en-imagen", "Fuga 4 · El contacto comercial vive dentro de una imagen", "loshdp.elpodcast@gmail.com solo aparece en el banner de YouTube.", [("canal-youtube", ""), ("entregables", "WhatsApp conectado")]),
        ("fuga-05-spotify-atrasado", "Fuga 5 · Spotify tres meses atrás y sin Apple Podcasts", "Último episodio en Spotify: Ep59 (jul-2026); YouTube va en el Ep93.", [("canal-spotify", "")]),
        ("fuga-06-shorts-con-fecha", f"Fuga 6 · {c['n_fecha_sh']} de {c['n_sh']} shorts titulados con la fecha", "«21 de octubre de 2026» no es un título: cero búsqueda, cero gancho.", [("canal-youtube", ""), *[(s, "") for s in c["fecha_sh"]]]),
        ("fuga-07-numeracion", "Fuga 7 · Numeración rota", "Falta el Ep89, el Ep83 no tiene título y Spotify numera distinto.", [("canal-youtube", ""), ("canal-spotify", "")]),
        ("fuga-08-formato-equivocado", "Fuga 8 · Se produce más lo que menos viraliza", "La opinión ciudadana llega a 340K; los clips de entrevista, a ~1.4K de mediana.", [("insight-opinion-viraliza", "")]),
        ("fuga-09-alcance-sin-captura", "Fuga 9 · Alcance sin audiencia propia", "17K personas vieron un episodio en FB y no hay lista, canal ni newsletter.", [("canal-facebook", ""), ("estrategia-plan-30-60-90", "canal de WhatsApp")]),
        ("fuga-10-instagram", "Fuga 10 · Instagram estancado", "2,147 seguidores siguiendo a 1,169 cuentas.", [("canal-instagram", "")]),
    ]
    for s, t, d, links in fugas:
        add(s, t, "fuga", d, d, links)

    add("estrategia-posicionamiento", "Posicionamiento: «el podcast donde Hidalgo se sienta a platicar sin filtro»", "estrategia",
        "Todos los partidos, todos los municipios, ninguna línea comprada.",
        "Activo diferencial: pluralidad comprobable + formato largo + voz irreverente («no se sulfuren», «mágico y celestial»). El ritual de «la adopción» se vuelve archivo público de adoptados.",
        [("insight-pluralidad", ""), ("formato-el-adoptado", ""), (hub, "")])
    add("estrategia-sistema-1-a-12", "Sistema: 1 episodio → 12 piezas", "estrategia",
        "Mismo día y mismo número en todas las plataformas, 6–8 clips con titular-gancho, carrusel, ficha web, tarjeta para el invitado.",
        "Fórmula de título: apodo + frase polémica entre comillas. Plantilla de descripción con capítulos, enlaces y contacto. Menos clips por episodio, mejor espaciados.",
        [("fuga-03-youtube-sin-enlaces", ""), ("fuga-06-shorts-con-fecha", ""), ("insight-volumen-vs-alcance", ""), ("insight-opinion-viraliza", "")])
    add("estrategia-rumbo-2027", "Serie «Rumbo al 2027»", "estrategia",
        "Un aspirante por semana con el mismo cuestionario base: comparable y citable.",
        "El proceso interno ya arrancó (aspirantes a Pachuca, registros en MORENA). Es la temporada alta natural del podcast.",
        [("tema-elecciones-2027", ""), ("insight-territorio", ""), ("invitado-navor-rojas", "aspirante a Pachuca")])
    add("estrategia-ingresos", "Modelo de ingresos limpio", "estrategia",
        "Patrocinio de marcas hidalguenses; entrevistas a políticos siempre gratuitas.",
        "Cobrar a políticos por ser entrevistados (sobre todo en precampaña o campaña) es un riesgo electoral y destruye la credibilidad, que es el activo principal. Etiquetar todo contenido pagado y consultar a un asesor electoral antes de 2027.",
        [("estrategia-posicionamiento", ""), ("canal-facebook", "")])
    add("estrategia-plan-30-60-90", "Plan 30 · 60 · 90", "estrategia",
        "Casa propia y orden → sistema de contenido → monetización.",
        "- **Días 1–30:** sitio y /links, canal de WhatsApp, Spotify al día + Apple, descripciones con enlaces.\n- **Días 31–60:** «Rumbo al 2027», sistema 1→12, tarjetas para invitados, opinión ciudadana en TikTok.\n- **Días 61–90:** media kit con métricas de Meta, 3 propuestas a marcas locales, medición.",
        [("estrategia-rumbo-2027", ""), ("estrategia-sistema-1-a-12", ""), ("estrategia-ingresos", ""), ("fuga-09-alcance-sin-captura", "")])
    add("entregables", "Lo que ya construimos", "entregable",
        "Sitio en loshdp.softvibes.art, análisis, mediahub privado y este cerebro.",
        "- **Sitio:** archivo filtrable de los 98 episodios, «¿Quieres ser adoptado?» con WhatsApp, media kit, /links, app instalable y sección En vivo.\n- **Análisis interactivo:** /analisis.\n- **Mediahub:** 1,215 piezas inventariadas, audio de episodios, shorts y TikToks, transcripciones.\n- **El Cerebro del Pueblo:** este mapa.",
        [("fuga-01-sin-sitio", ""), ("fuga-02-link-rentado", ""), ("fuga-04-contacto-en-imagen", ""), (hub, "")])
    return I


if __name__ == "__main__":
    main()

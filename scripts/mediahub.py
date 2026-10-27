"""Construye el mediahub de Los HDP: inventario maestro + base de conocimiento.

Entradas (locales):
  ingesta/youtube/meta_videos/*.info.json   metadata completa de los episodios
  ingesta/youtube/shorts.json               shorts (id, título, vistas)
  mediahub/tiktok/tt_flat.json              779 TikToks con métricas
  ingesta/facebook/facebook_videos.json     videos recientes de FB
  inventario/episodios.csv                  segmento/invitado/partido ya clasificados
  mediahub/youtube/*/transcripciones/*.vtt  subtítulos automáticos (es-orig)
  mediahub/archivos_vps.txt                 listado de archivos en el VPS (opcional)

Salidas:
  mediahub/inventario/inventario_maestro.{csv,json}
  mediahub/conocimiento/episodios/*.md, shorts.md, tiktok.md, INDICE.md
  mediahub/web/data.js                      (visor web privado)
"""
import csv
import html
import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MH = ROOT / "mediahub"
URL_MEDIA = "media"  # relativo al visor /mediahub/

TEMAS = {
    "Elecciones 2027": r"2027|candidatur|aspirant|encuesta|registr[oé]|coalici",
    "MORENA": r"morena|4t|transformaci",
    "PRI": r"\bpri\b|priista|alito",
    "PAN": r"\bpan\b|panista",
    "MC": r"movimiento ciudadano|\bmc\b",
    "PT": r"\bpt\b|petista",
    "Poder Judicial": r"judicial|juez|jueza|magistrad|suprema corte",
    "Seguridad": r"seguridad|narco|violencia|polic[ií]a|delincuen",
    "Movilidad y obras": r"tr[aá]fico|vial|bache|carretera|obra|transporte|sem[aá]foro",
    "Presupuesto y dinero público": r"presupuest|recurso|dinero|gasto|deuda|moches|corrupci",
    "Pachuca": r"pachuca",
    "Gobierno de Hidalgo": r"menchaca|gobernador|gobierno del estado|secretar[ií]a de gobierno",
    "Federal": r"claudia|sheinbaum|amlo|presidente de la rep[uú]blica|senado",
}


def norm(s):
    s = unicodedata.normalize("NFD", s or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9 ]", " ", s)


def temas(texto):
    t = (texto or "").lower()
    return [k for k, rx in TEMAS.items() if re.search(rx, t)]


def hashtags(texto):
    return sorted(set(h.lower() for h in re.findall(r"#(\w+)", texto or "")))


def fecha_iso(d):
    return f"{d[:4]}-{d[4:6]}-{d[6:]}" if d and len(d) == 8 else d


# ── VTT → texto con marcas de tiempo ────────────────────────────────────────────
def leer_vtt(path, cada_seg=60):
    """YouTube repite líneas en subtítulos automáticos; se deduplican y se agrupan por minuto."""
    bloques, actual_ini, vistas = [], None, []
    t_rx = re.compile(r"^(\d+):(\d+):(\d+)\.\d+ -->")
    ultimo = ""
    seg = 0
    for linea in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        m = t_rx.match(linea)
        if m:
            h, mi, s = map(int, m.groups())
            seg = h * 3600 + mi * 60 + s
            continue
        if not linea.strip() or linea.startswith(("WEBVTT", "Kind:", "Language:")) or "-->" in linea:
            continue
        txt = html.unescape(re.sub(r"<[^>]+>", "", linea)).strip()
        if not txt or txt == ultimo:
            continue
        ultimo = txt
        if actual_ini is None or seg - actual_ini >= cada_seg:
            if vistas:
                bloques.append((actual_ini, " ".join(vistas)))
            actual_ini, vistas = seg, []
        # evita repetir la cola de la línea anterior (subtítulos "rodantes")
        if vistas and txt.startswith(vistas[-1]):
            vistas[-1] = txt
        elif not (vistas and vistas[-1].endswith(txt)):
            vistas.append(txt)
    if vistas:
        bloques.append((actual_ini or 0, " ".join(vistas)))
    return bloques


def mmss(s):
    return f"{s // 3600:d}:{s % 3600 // 60:02d}:{s % 60:02d}" if s >= 3600 else f"{s // 60:02d}:{s % 60:02d}"


def transcripciones(carpeta):
    out = {}
    for f in (MH / carpeta).glob("*.vtt"):
        vid = re.match(r"\d{8}_(.+?)\.es", f.name)
        if vid:
            out[vid.group(1)] = f
    return out


def archivos_vps():
    """id → ruta relativa del archivo multimedia en el VPS (de `find` en /srv/loshdp-mediahub)."""
    p = MH / "archivos_vps.txt"
    res = {}
    if not p.exists():
        return res
    for linea in p.read_text().splitlines():
        rel = linea.strip().removeprefix("/srv/loshdp-mediahub/")
        m = re.search(r"\d{8}_([\w-]+)\.(opus|mp4|m4a|webm|mp3)$", rel)
        if m:
            res[m.group(1)] = rel
    return res


def main():
    vps = archivos_vps()
    inv_eps = {r["youtube_id"]: r for r in csv.DictReader(open(ROOT / "inventario/episodios.csv"))}
    invitados = sorted({r["invitado"] for r in inv_eps.values() if r["invitado"]}, key=len, reverse=True)

    def vincula_invitado(texto):
        t = norm(texto).replace(" ", "")
        for nombre in invitados:
            base = re.sub(r'"[^"]*"', "", nombre)
            partes = norm(base).split()
            if len(partes) >= 2 and "".join(partes[:2]) in t:
                return nombre
        return None

    items = []
    tr_eps = transcripciones("youtube/episodios/transcripciones")
    tr_sh = transcripciones("youtube/shorts/transcripciones")

    # Episodios de YouTube
    for f in sorted((ROOT / "ingesta/youtube/meta_videos").glob("2*.info.json")):
        d = json.loads(f.read_text())
        r = inv_eps.get(d["id"], {})
        texto = f"{d['title']} {d.get('description') or ''}"
        items.append({
            "plataforma": "YouTube", "tipo": "Episodio", "id": d["id"],
            "fecha": fecha_iso(d.get("upload_date")), "titulo": d["title"],
            "descripcion": d.get("description") or "", "duracion_seg": d.get("duration") or 0,
            "vistas": d.get("view_count") or 0, "likes": d.get("like_count") or 0,
            "comentarios": d.get("comment_count") or 0, "compartidos": None,
            "segmento": r.get("segmento"), "invitado": r.get("invitado") or None,
            "partido": r.get("partido") or None, "municipio": r.get("municipio") or None,
            "temas": temas(texto), "hashtags": hashtags(texto),
            "url": f"https://www.youtube.com/watch?v={d['id']}",
            "miniatura": f"miniaturas/youtube/{d['id']}.jpg",
            "archivo": vps.get(d["id"]), "transcripcion": d["id"] in tr_eps,
        })

    # Shorts de YouTube
    for s in json.loads((ROOT / "ingesta/youtube/shorts.json").read_text()):
        items.append({
            "plataforma": "YouTube", "tipo": "Short", "id": s["id"], "fecha": None,
            "titulo": s["titulo"], "descripcion": "", "duracion_seg": None,
            "vistas": s["vistas"] or 0, "likes": None, "comentarios": None, "compartidos": None,
            "segmento": None, "invitado": vincula_invitado(s["titulo"]), "partido": None, "municipio": None,
            "temas": temas(s["titulo"]), "hashtags": hashtags(s["titulo"]),
            "url": f"https://www.youtube.com/shorts/{s['id']}", "miniatura": None,
            "archivo": vps.get(s["id"]), "transcripcion": s["id"] in tr_sh,
        })
        # la fecha real viene en el nombre del archivo / transcripción
        f = tr_sh.get(s["id"])
        if f:
            items[-1]["fecha"] = fecha_iso(f.name[:8])
        elif vps.get(s["id"]):
            items[-1]["fecha"] = fecha_iso(Path(vps[s["id"]]).name[:8])

    # TikTok
    tt_flat = MH / "tiktok/tt_flat.json"
    if tt_flat.exists():
        for e in json.loads(tt_flat.read_text())["entries"]:
            desc = e.get("description") or e.get("title") or ""
            import datetime as dt
            fecha = dt.datetime.fromtimestamp(e["timestamp"], dt.UTC).strftime("%Y-%m-%d") if e.get("timestamp") else None
            items.append({
                "plataforma": "TikTok", "tipo": "Video", "id": e["id"], "fecha": fecha,
                "titulo": desc[:140], "descripcion": desc, "duracion_seg": e.get("duration"),
                "vistas": e.get("view_count") or 0, "likes": e.get("like_count") or 0,
                "comentarios": e.get("comment_count") or 0, "compartidos": e.get("repost_count"),
                "segmento": None, "invitado": vincula_invitado(desc), "partido": None, "municipio": None,
                "temas": temas(desc), "hashtags": hashtags(desc),
                "url": f"https://www.tiktok.com/@los_hijos_delpueblo/video/{e['id']}",
                "miniatura": None, "archivo": vps.get(e["id"]), "transcripcion": False,
            })

    # Facebook (muestra reciente)
    fb = ROOT / "ingesta/facebook/facebook_videos.json"
    for i, v in enumerate(json.loads(fb.read_text())["videos"] if fb.exists() else []):
        t = v.get("texto") or ""
        items.append({
            "plataforma": "Facebook", "tipo": "Video", "id": f"fb{i}", "fecha": v.get("fecha"),
            "titulo": t.split("\n")[0][:140], "descripcion": t, "duracion_seg": v.get("dur_seg"),
            "vistas": v["reproducciones"], "likes": None, "comentarios": None, "compartidos": None,
            "segmento": None, "invitado": vincula_invitado(t), "partido": None, "municipio": None,
            "temas": temas(t), "hashtags": hashtags(t),
            "url": "https://www.facebook.com/profile.php?id=61552864772878&sk=videos",
            "miniatura": None, "archivo": None, "transcripcion": False,
        })

    # ── Inventario maestro ──────────────────────────────────────────────────────
    out = MH / "inventario"
    out.mkdir(parents=True, exist_ok=True)
    (out / "inventario_maestro.json").write_text(json.dumps(items, ensure_ascii=False, indent=1))
    campos = [k for k in items[0] if k != "descripcion"]
    with open(out / "inventario_maestro.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=campos, extrasaction="ignore")
        w.writeheader()
        for it in items:
            w.writerow({**it, "temas": "; ".join(it["temas"]), "hashtags": " ".join(it["hashtags"])})

    resumen = {
        "piezas": len(items),
        "por_plataforma_tipo": Counter(f"{i['plataforma']} · {i['tipo']}" for i in items),
        "vistas_por_plataforma": defaultdict(int),
        "horas": defaultdict(float),
        "con_archivo": sum(1 for i in items if i["archivo"]),
        "con_transcripcion": sum(1 for i in items if i["transcripcion"]),
        "con_invitado_vinculado": sum(1 for i in items if i["invitado"]),
        "temas": Counter(t for i in items for t in i["temas"]),
        "hashtags_top": Counter(h for i in items for h in i["hashtags"]).most_common(30),
    }
    for i in items:
        resumen["vistas_por_plataforma"][i["plataforma"]] += i["vistas"] or 0
        resumen["horas"][f"{i['plataforma']} · {i['tipo']}"] += (i["duracion_seg"] or 0) / 3600
    resumen["horas"] = {k: round(v, 1) for k, v in resumen["horas"].items()}
    (out / "resumen.json").write_text(json.dumps(resumen, ensure_ascii=False, indent=1, default=dict))

    # ── Base de conocimiento ────────────────────────────────────────────────────
    kb = MH / "conocimiento"
    (kb / "episodios").mkdir(parents=True, exist_ok=True)
    for viejo in (kb / "episodios").glob("*.md"):
        viejo.unlink()  # evita fichas huérfanas si cambia el nombre de un episodio
    indice = ["# Los HDP — Base de conocimiento\n",
              "Un archivo por episodio con metadata y transcripción automática (puede tener errores de reconocimiento de voz).\n",
              "| Fecha | Segmento | Episodio | Invitado | Vistas YT | Transcripción |", "|---|---|---|---|---|---|"]
    for it in sorted((i for i in items if i["tipo"] == "Episodio"), key=lambda x: x["fecha"]):
        slug = re.sub(r"[^a-z0-9]+", "-", norm(it["invitado"] or it["titulo"]))[:60].strip("-")
        nombre = f"{it['fecha']}_{slug}.md"
        bloques = leer_vtt(tr_eps[it["id"]]) if it["id"] in tr_eps else []
        fm = {
            "titulo": it["titulo"], "fecha": it["fecha"], "segmento": it["segmento"],
            "invitado": it["invitado"], "partido": it["partido"], "municipio": it["municipio"],
            "duracion_min": round(it["duracion_seg"] / 60), "vistas_youtube": it["vistas"],
            "url": it["url"], "audio": it["archivo"], "temas": it["temas"],
        }
        cuerpo = ["---"] + [f"{k}: {json.dumps(v, ensure_ascii=False)}" for k, v in fm.items()] + ["---", "",
                  f"# {it['titulo']}", "", "## Descripción", "", it["descripcion"].strip() or "_Sin descripción._", "",
                  "## Transcripción", ""]
        if bloques:
            cuerpo += [f"**[{mmss(s)}]** {t}\n" for s, t in bloques]
        else:
            cuerpo.append("_Sin subtítulos automáticos disponibles._")
        (kb / "episodios" / nombre).write_text("\n".join(cuerpo))
        it["kb"] = f"conocimiento/episodios/{nombre}"
        indice.append(f"| {it['fecha']} | {it['segmento']} | [{it['titulo'][:70]}](episodios/{nombre}) | "
                      f"{it['invitado'] or '—'} | {it['vistas']:,} | {'sí' if bloques else 'no'} |")
    (kb / "INDICE.md").write_text("\n".join(indice) + "\n")

    # Shorts y TikTok: un archivo consolidado cada uno (texto breve por pieza)
    def consolidado(nombre, titulo, filtro, con_tr=None):
        lineas = [f"# {titulo}\n"]
        for it in sorted(filter(filtro, items), key=lambda x: -(x["vistas"] or 0)):
            lineas.append(f"## {it['titulo'][:100] or it['id']}")
            lineas.append(f"- Fecha: {it['fecha'] or '—'} · Vistas: {it['vistas']:,} · Invitado: {it['invitado'] or '—'} · [Ver]({it['url']})")
            if it["descripcion"] and it["descripcion"] != it["titulo"]:
                lineas.append(f"- Texto: {it['descripcion'].strip()}")
            if con_tr and it["id"] in con_tr:
                texto = " ".join(t for _, t in leer_vtt(con_tr[it["id"]], 9999))
                lineas.append(f"- Transcripción: {texto}")
            lineas.append("")
        (kb / nombre).write_text("\n".join(lineas))

    consolidado("shorts.md", "Shorts de YouTube (ordenados por vistas)", lambda i: i["tipo"] == "Short", tr_sh)
    consolidado("tiktok.md", "TikToks (ordenados por vistas)", lambda i: i["plataforma"] == "TikTok")
    consolidado("facebook.md", "Facebook — muestra reciente", lambda i: i["plataforma"] == "Facebook")

    # ── Datos del visor web ─────────────────────────────────────────────────────
    web = MH / "web"
    web.mkdir(exist_ok=True)
    ligero = [{k: v for k, v in i.items() if k != "descripcion"} | {"texto": (i["descripcion"] or "")[:300]} for i in items]
    (web / "data.js").write_text("window.MEDIAHUB=" + json.dumps({"items": ligero, "resumen": json.loads((out / "resumen.json").read_text())}, ensure_ascii=False) + ";")

    print(json.dumps({k: v for k, v in json.loads((out / "resumen.json").read_text()).items() if k != "hashtags_top"}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()

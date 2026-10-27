"""Construye el inventario de contenido de Los HDP a partir de la ingesta.

Entradas: ingesta/youtube/episodios.json, shorts.json, ingesta/{tiktok,facebook,instagram,spotify}/*.json
Salidas: inventario/episodios.csv, inventario/invitados.csv, inventario/inventario.json,
         landing/data/episodios.json (lo que consume la landing)
"""
import csv
import json
import re
import statistics
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ING = ROOT / "ingesta"
OUT = ROOT / "inventario"

PARTIDOS = [
    ("MORENA", r"\bmorena\b|bienestar|4t|transformaci"),
    ("PRI", r"\bpri\b|cde del pri"),
    ("PAN", r"\bpan\b"),
    ("MC", r"movimiento ciudadano|\bmc\b|naranjas"),
    ("PT", r"\bpt\b"),
    ("SOMOS", r"\bsomos\b"),
]
CARGOS = [
    ("Senado", r"senador"),
    ("Diputación federal", r"diputad[oa] federal"),
    ("Diputación local", r"diputad[oa] local|diputad[oa] presidente|diputad[oa] .*distrito|diputada local"),
    ("Presidencia municipal", r"presidente municipal|presidenta municipal|alcalde|ex presidente de"),
    ("Gabinete estatal/federal", r"secretari[oa]|delegado|sub secretaria|subsecretaria"),
    ("Dirigencia partidista", r"presidente de|presidente del cde|dirigente|coordinador|comisionado|secretario general|secretario nacional|secretaria nacional"),
    ("Regiduría", r"regidor"),
    ("Poder Judicial (candidatura)", r"candidat[oa] a (juez|jueza|magistrad)"),
    ("Periodismo / sociedad civil", r"periodista|comentarista|luchador social|grupo "),
]
MUNICIPIOS = ["Pachuca", "Huejutla", "Ixmiquilpan", "Zimapán", "Cardonal", "Huichapan", "Mineral de la Reforma",
              "Mineral del Monte", "Tepeji del Río", "Singuilucan", "Zacualtipán", "Molango", "Acaxochitlán",
              "Epazoyucan", "Villa de Tezontepec", "Tulancingo", "Actopan", "Tlanchinol"]


def segmento(t):
    tl = t.lower()
    if "teaser" in tl:
        return "Teaser"
    # la mesa va primero: sus temas pueden mencionar "judicial" o "adoptado"
    if re.match(r"los hdp-ep|los hdp-nomams", tl):
        return "Mesa HDP"
    if "judicial" in tl:
        return "El Adoptado Judicial"
    if "a poco si" in tl:
        return "¿A poco sí?"
    if "jubilados" in tl:
        return "Los Jubilados del Pueblo"
    if "adoptad" in tl:
        return "El Adoptado"
    if re.match(r"los hdp-ep|los hdp-nomams", tl):
        return "Mesa HDP"
    return "Otro"


def episodio_num(t):
    m = re.search(r"Ep\.?\s?(\d+)", t, re.I)
    return int(m.group(1)) if m else None


def invitado_y_rol(t, seg):
    if seg in ("Mesa HDP", "Teaser", "Los Jubilados del Pueblo"):
        return None, None
    base = re.split(r"\s*-\s*(?:el adoptad|la adoptad|¿a poco)", t, flags=re.I)[0]
    partes = re.split(r",\s*|\s+-\s+", base, maxsplit=1)
    nombre = partes[0].strip()
    rol = partes[1].strip() if len(partes) > 1 else None
    # "Marco Antonio Mendoza Presidente del CDE..." sin coma
    m = re.match(r"^(.*?)\s+(Presidente|Presidenta|Secretario|Diputad[oa]|Senador|Regidor|Candidat[oa])\b(.*)$", nombre)
    if m and not rol:
        nombre, rol = m.group(1).strip(), (m.group(2) + m.group(3)).strip()
    return nombre, rol


def clasifica(texto, reglas):
    tl = texto.lower()
    return next((k for k, rx in reglas if re.search(rx, tl)), None)


def main():
    OUT.mkdir(exist_ok=True)
    eps = json.loads((ING / "youtube/episodios.json").read_text())
    filas = []
    for e in eps:
        t = e["titulo"]
        seg = segmento(t)
        inv, rol = invitado_y_rol(t, seg)
        ctx = f"{t} {e['desc']}"
        vistas, likes, com = e["vistas"] or 0, e["likes"] or 0, e["coments"] or 0
        filas.append({
            "fecha": f"{e['fecha'][:4]}-{e['fecha'][4:6]}-{e['fecha'][6:]}",
            "youtube_id": e["id"],
            "url": f"https://www.youtube.com/watch?v={e['id']}",
            "ep_titulo": episodio_num(t),
            "segmento": seg,
            "invitado": inv,
            "rol": rol,
            "cargo": clasifica(ctx, CARGOS) if inv else None,
            "partido": clasifica(ctx, PARTIDOS) if inv else None,
            "municipio": next((m for m in MUNICIPIOS if m.lower() in ctx.lower()), None),
            "dur_min": e["dur_min"],
            "vistas": vistas,
            "likes": likes,
            "comentarios": com,
            "engagement_pct": round(100 * (likes + com) / vistas, 2) if vistas else 0,
            "titulo": t,
        })

    campos = list(filas[0].keys())
    with open(OUT / "episodios.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        w.writerows(filas)

    # invitados únicos
    inv = defaultdict(lambda: {"apariciones": 0, "vistas": 0, "episodios": []})
    for r in filas:
        if r["invitado"]:
            k = r["invitado"]
            inv[k]["apariciones"] += 1
            inv[k]["vistas"] += r["vistas"]
            inv[k]["episodios"].append(r["youtube_id"])
            for c in ("rol", "cargo", "partido", "municipio"):
                inv[k][c] = inv[k].get(c) or r[c]
    with open(OUT / "invitados.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["invitado", "rol", "cargo", "partido", "municipio", "apariciones", "vistas_yt"])
        for k, v in sorted(inv.items(), key=lambda x: -x[1]["vistas"]):
            w.writerow([k, v.get("rol"), v.get("cargo"), v.get("partido"), v.get("municipio"), v["apariciones"], v["vistas"]])

    # números repetidos / faltantes
    # hasta el Ep11 Mesa y Adoptado se numeraban por separado; desde ahí comparten serie
    nums = Counter(r["ep_titulo"] for r in filas if r["ep_titulo"] and r["ep_titulo"] > 10
                   and r["segmento"] not in ("Los Jubilados del Pueblo", "Teaser"))
    repetidos = sorted(n for n, c in nums.items() if c > 1)
    faltantes = sorted(set(range(11, max(nums) + 1)) - set(nums))

    shorts = json.loads((ING / "youtube/shorts.json").read_text())
    sv = [s["vistas"] or 0 for s in shorts]
    fecha_rx = re.compile(r"^[A-Z][a-z]+ \d{1,2}, \d{4}$")
    tt = json.loads((ING / "tiktok/tiktok_perfil.json").read_text())
    fb = json.loads((ING / "facebook/facebook_perfil.json").read_text())
    fbv = json.loads((ING / "facebook/facebook_videos.json").read_text())
    ig = json.loads((ING / "instagram/instagram_perfil_basico.json").read_text())
    sp = json.loads((ING / "spotify/spotify_show.json").read_text())

    por_seg = Counter(r["segmento"] for r in filas)
    vistas_seg = defaultdict(list)
    for r in filas:
        vistas_seg[r["segmento"]].append(r["vistas"])
    resumen = {
        "fecha_corte": "2026-10-24",
        "canales": {
            "facebook": {"seguidores": fb["followers"], "hablando_de_esto": fb["talking_about"]},
            "tiktok": {"seguidores": tt["followers"], "likes": tt["likes"], "videos": tt["videos_count"]},
            "instagram": {"seguidores": ig["followers"], "posts": ig["posts_count"], "siguiendo": ig["following"]},
            "youtube": {"suscriptores": 951, "episodios": len(filas), "shorts": len(shorts),
                        "vistas_episodios": sum(r["vistas"] for r in filas), "vistas_shorts": sum(sv)},
            "spotify": {"rating": sp["rating"], "num_ratings": sp["num_ratings"], "ultimo_ep": sp["ultimo_episodio"]},
        },
        "audiencia_total_seguidores": fb["followers"] + tt["followers"] + ig["followers"] + 951,
        "episodios_por_segmento": dict(por_seg),
        "mediana_vistas_por_segmento": {k: statistics.median(v) for k, v in vistas_seg.items()},
        "invitados_unicos": len(inv),
        "partidos": dict(Counter(r["partido"] for r in filas if r["invitado"])),
        "cargos": dict(Counter(r["cargo"] for r in filas if r["invitado"])),
        "municipios": dict(Counter(r["municipio"] for r in filas if r["municipio"])),
        "horas_grabadas": round(sum(r["dur_min"] for r in filas) / 60, 1),
        "numeracion": {"repetidos": repetidos, "faltantes": faltantes},
        "shorts_titulo_solo_fecha": sum(1 for s in shorts if fecha_rx.match(s["titulo"] or "")),
        "shorts_mediana_vistas": statistics.median(sv),
        "top_episodios": sorted(filas, key=lambda r: -r["vistas"])[:10],
        "top_tiktok": tt["top_videos"][:3],
        "facebook_videos_recientes": fbv["videos"],
    }
    (OUT / "inventario.json").write_text(json.dumps(resumen, ensure_ascii=False, indent=1))

    # datos para la landing (solo lo necesario)
    land = ROOT / "landing/data"
    land.mkdir(parents=True, exist_ok=True)
    pub = [{k: r[k] for k in ("fecha", "youtube_id", "segmento", "invitado", "rol", "partido", "municipio",
                              "dur_min", "vistas", "titulo", "ep_titulo")} for r in sorted(filas, key=lambda r: r["fecha"], reverse=True)]
    (land / "episodios.json").write_text(json.dumps(pub, ensure_ascii=False))
    # versión .js para que el sitio funcione también abierto como archivo local
    (land / "episodios.js").write_text("window.EPISODIOS=" + json.dumps(pub, ensure_ascii=False) + ";")
    print(json.dumps({k: v for k, v in resumen.items() if k not in ("top_episodios", "top_tiktok", "facebook_videos_recientes")}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()

"""Genera el recorrido de insights (onboarding) de «El Cerebro del Pueblo».

Toma los títulos reales de las fichas en mediahub/conocimiento/ para que cada paso
apunte a un nodo existente; si un título no existe, falla en vez de publicar un paso roto.

Uso: python3 scripts/tour_cerebro.py [--app <carpeta de la app 3D>]
Salida: cerebro/tour.json (y copia en la app si se indica)
"""
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KB = ROOT / "mediahub/conocimiento"
COLOR = {"insights": "#C0FF72", "episodios": "#38BDF8", "invitados": "#F472B6",
         "temas": "#A78BFA", "municipios": "#FBBF24", "clips": "#FB7185"}


def titulos():
    """slug de archivo → (título, carpeta, descripción)."""
    out = {}
    for carpeta in COLOR:
        for f in (KB / carpeta).glob("*.md"):
            t = f.read_text()
            g = lambda k: (re.search(rf'^{k}: "(.*)"$', t, re.M) or [None, ""])[1]
            # el grafo colapsa espacios en los títulos: se normalizan igual para que coincidan
            out[f.stem] = (" ".join(json.loads(f'"{g("title")}"').split()), carpeta, g("description"))
    return out


def main():
    T = titulos()
    items = json.loads((ROOT / "mediahub/inventario/inventario_maestro.json").read_text())
    enlaces = json.loads((ROOT / "cerebro/enlaces.json").read_text())

    def t(s):
        if s not in T:
            sys.exit(f"Nodo inexistente en el recorrido: {s}")
        return T[s][0]

    def row(s, label=None, body=None, meta=None, url=None):
        titulo, carpeta, desc = T.get(s) or sys.exit(f"Nodo inexistente en el recorrido: {s}")
        return {"title": titulo, "label": label or titulo, "body": body if body is not None else desc,
                "meta": meta, "color": COLOR[carpeta], "url": url}

    clips = sorted((s for s in T if s.startswith("clip-tiktok")), key=lambda s: -int(re.sub(r"\D", "", T[s][2].split("·")[2]) or 0))
    eps = {s: T[s] for s in T if T[s][1] == "episodios"}
    top_eps = sorted(eps, key=lambda s: -int(re.search(r"([\d,]+) vistas", eps[s][2]).group(1).replace(",", "")))[:6]
    reyes_clips = [s for s in clips if "[[invitado-jorge-reyes]]" in open(KB / "clips" / f"{s}.md").read()][:3]
    tt_total = sum(i["vistas"] for i in items if i["plataforma"] == "TikTok")

    pasos = [
        {"section": "Inicio", "title": "El Cerebro del Pueblo", "focus": t("cerebro-del-pueblo"), "sources": None,
         "kpis": [["98", "episodios · 107 horas"], ["68", "invitados con ficha"], ["1,215", "piezas inventariadas"], [f"{tt_total / 1e6:.1f} M", "vistas en TikTok"]],
         "text": ["Este mapa conecta todo lo que Los HDP han publicado: cada episodio, cada invitado, cada clip viral, y los temas y municipios que tocan.",
                  "Cada punto es una ficha real con su transcripción o su texto publicado. Las líneas son conexiones del inventario: invitado, partido, municipio, tema y formato.",
                  "Corte: 24 de octubre de 2026, solo con material público."],
         "rows": []},
        {"section": "Quiénes son", "title": "Robert y Kuako, los Hijos del Pueblo", "focus": t("formato-el-adoptado"), "sources": ["insights", "temas", "episodios"],
         "text": ["Podcast de análisis político de Hidalgo desde noviembre de 2023. Su ritual: «adoptar» a cada invitado y ponerle apodo.",
                  "Su voz es su marca: irreverente, de cantina política, con cariño burlón hacia el poder. «No se sulfuren.»"],
         "rows": [row("formato-el-adoptado", meta="56 ep."), row("formato-mesa-hdp", meta="27 ep."), row("formato-el-adoptado-judicial", meta="12 ep."), row("formato-a-poco-si")]},
        {"section": "Audiencia", "title": "El 73% de su gente está en Facebook", "focus": t("canal-facebook"), "sources": ["insights"],
         "kpis": [["44,089", "Facebook"], ["13,500", "TikTok"], ["2,147", "Instagram"], ["951", "YouTube"]],
         "text": ["Facebook es la plaza pública: allí un episodio completo llega a 17 mil reproducciones. YouTube es el archivo, no el escenario."],
         "rows": [row(f"canal-{c}") for c in ["facebook", "tiktok", "youtube", "instagram", "spotify"]]},
        {"section": "Insight 1", "title": "TikTok: el alcance llega por golpes virales", "focus": t("insight-tiktok-alcance"), "sources": ["insights", "clips"],
         "text": ["Un tercio de las vistas de TikTok viene de solo 10 videos. Los récords no son entrevistas: son opinión de los hosts sobre lo que le duele a la gente."],
         "rows": [row(s, url=enlaces.get(T[s][0])) for s in clips[:3]] + [row("insight-opinion-viraliza"), row("insight-volumen-vs-alcance")]},
        {"section": "Insight 2", "title": "Jorge Reyes, el invitado imán", "focus": t("invitado-jorge-reyes"), "sources": ["insights", "invitados", "clips", "municipios", "episodios"],
         "text": ["El alcalde de Pachuca es el invitado con más clips (23) y el de mejor rendimiento: más de 300 mil vistas sumadas. La capital es el tema más rentable."],
         "rows": [row("insight-jorge-reyes")] + [row(s, url=enlaces.get(T[s][0])) for s in reyes_clips] + [row("municipio-pachuca")]},
        {"section": "Insight 3", "title": "Aquí vienen todos los partidos", "focus": t("insight-pluralidad"), "sources": ["insights", "temas", "invitados"],
         "text": ["MORENA, PRI, PAN, MC, PT y SOMOS se han sentado en la cabina. Esa pluralidad comprobable es su activo más valioso frente a los medios tradicionales, y hoy no la comunican."],
         "rows": [row(f"partido-{p}") for p in ["morena", "pri", "pan", "mc", "pt", "somos"] if f"partido-{p}" in T]},
        {"section": "Insight 4", "title": "18 de 84 municipios", "focus": t("insight-territorio"), "sources": ["insights", "municipios", "invitados"],
         "text": ["Pachuca domina el archivo. El resto de Hidalgo casi no aparece: es la oportunidad editorial rumbo a 2027."],
         "rows": [row(s) for s in sorted((s for s in T if s.startswith("municipio-")), key=lambda s: -int(T[s][2].split()[0]))[:6]]},
        {"section": "Lo más visto", "title": "Los episodios que más se vieron en YouTube", "focus": eps[top_eps[0]][0], "sources": ["episodios", "invitados"],
         "text": ["Cada ficha trae la transcripción completa por minuto. Abre una y dale play: el video se carga en el panel."],
         "rows": [row(s, url=enlaces.get(eps[s][0])) for s in top_eps]},
        {"section": "Diagnóstico", "title": "10 fugas que se pueden comprobar", "focus": t("fuga-01-sin-sitio"), "sources": ["insights", "clips"],
         "text": ["Cada fuga tiene evidencia en el inventario. Varias ya están resueltas con el sitio."],
         "rows": [row(s) for s in sorted(s for s in T if s.startswith("fuga-"))]},
        {"section": "Estrategia", "title": "El podcast donde Hidalgo se sienta a platicar sin filtro", "focus": t("estrategia-posicionamiento"), "sources": ["insights", "temas"],
         "rows": [row(s) for s in ["estrategia-posicionamiento", "estrategia-sistema-1-a-12", "estrategia-rumbo-2027", "estrategia-ingresos"]]},
        {"section": "Plan", "title": "Plan 30 · 60 · 90", "focus": t("estrategia-plan-30-60-90"), "sources": ["insights"],
         "kpis": [["0 → 1,500", "canal de WhatsApp"], ["37% → 100%", "shorts con título-gancho"], ["18 → 30", "municipios adoptados"], ["0 → 3", "conversaciones con patrocinadores"]],
         "text": ["Casa propia y orden → sistema de contenido → monetización limpia (con marcas, nunca cobrando a políticos)."],
         "rows": [row("estrategia-plan-30-60-90")]},
        {"section": "Entregables", "title": "Lo que ya está construido", "focus": t("entregables"), "sources": None,
         "text": ["Todo vive en loshdp.softvibes.art. El mediahub y este cerebro son de acceso privado."],
         "rows": [
             {"title": t("entregables"), "label": "Sitio: episodios, «¿Quieres ser adoptado?», media kit", "body": "Archivo filtrable de los 98 episodios, WhatsApp conectado, /links, app instalable y sección En vivo.", "color": COLOR["insights"], "url": "https://loshdp.softvibes.art/"},
             {"title": t("entregables"), "label": "Análisis interactivo", "body": "Las fugas, el antes y el después, y los planes.", "color": COLOR["insights"], "url": "https://loshdp.softvibes.art/analisis/"},
             {"title": t("entregables"), "label": "El Cerebro del Pueblo (este mapa)", "body": "Cerebro 3D con el recorrido de insights, para presentar en pantalla compartida.", "color": COLOR["insights"], "url": "https://loshdpbrain.softvibes.art/?tour=1"},
             {"title": t("entregables"), "label": "Mediahub privado", "body": "1,215 piezas inventariadas, audio de episodios, shorts y TikToks, transcripciones.", "color": COLOR["insights"], "url": "https://loshdp.softvibes.art/mediahub/"},
         ]},
        {"section": "Siguiente", "title": "Lo que necesitamos de ustedes", "focus": t("cerebro-del-pueblo"), "sources": None,
         "text": ["1. Dominio propio y quién administra la página de Facebook y el canal de YouTube (para métricas reales).",
                  "2. El horario real de sus transmisiones y el enlace del canal de WhatsApp.",
                  "3. Acordar la política de «entrevistas a políticos siempre gratuitas».",
                  "4. Los archivos maestros de video, para producción en calidad completa."],
         "rows": []},
    ]
    tour = {"name": "El Cerebro del Pueblo", "corte": "24 oct 2026",
            "legend": [{"label": l, "color": COLOR[k]} for k, l in [("insights", "Insights y estrategia"), ("episodios", "Episodios"), ("invitados", "Invitados"), ("temas", "Temas, partidos y formatos"), ("municipios", "Municipios"), ("clips", "Clips virales")]],
            "links": {" ".join(k.split()): v for k, v in enlaces.items()}, "steps": pasos}
    destino = ROOT / "cerebro/tour.json"
    destino.write_text(json.dumps(tour, ensure_ascii=False, indent=1))
    if "--app" in sys.argv:
        shutil.copy(destino, Path(sys.argv[sys.argv.index("--app") + 1]) / "tour.json")
    print(f"{len(pasos)} pasos · {sum(len(p['rows']) for p in pasos)} renglones · {len(enlaces)} enlaces a originales")


if __name__ == "__main__":
    main()

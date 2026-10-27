"""Kit de enlaces del viaje del visitante: un enlace por red y por episodio + descripciones de YouTube.

Cada enlace lleva ?o=<red> (el sitio da la bienvenida a la medida y el WhatsApp dice de dónde llegó)
y ?ep=<id> (abre ese episodio directo). Salidas en kit-enlaces/:
  enlaces_por_episodio.csv     id, episodio y un enlace por red
  youtube_descripciones.md     bloque listo para pegar en la descripción de cada video
"""
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITIO = "https://loshdp.softvibes.art/"
SPOTIFY = "https://open.spotify.com/show/3rwx7hZbCvJzYxBICuRcuf"
WHATSAPP = "https://wa.me/527712668105"
REDES = {"youtube": "yt", "facebook": "fb", "instagram": "ig", "tiktok": "tt", "spotify": "sp"}


def enlace(o, ep=None):
    return f"{SITIO}?o={o}" + (f"&ep={ep}" if ep else "")


def hashtag(s):
    return "#" + re.sub(r"[^A-Za-z0-9ÁÉÍÓÚÑáéíóúñ]", "", (s or "").title())


def main():
    out = ROOT / "kit-enlaces"
    out.mkdir(exist_ok=True)
    items = json.loads((ROOT / "mediahub/inventario/inventario_maestro.json").read_text())
    eps = sorted((i for i in items if i["tipo"] == "Episodio"), key=lambda x: x["fecha"], reverse=True)

    with open(out / "enlaces_por_episodio.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["fecha", "youtube_id", "episodio"] + [f"enlace_{r}" for r in REDES])
        for e in eps:
            w.writerow([e["fecha"], e["id"], e["titulo"]] + [enlace(o, e["id"]) for o in REDES.values()])

    bloques = ["# Descripciones de YouTube listas para pegar\n",
               "Una por episodio, del más reciente al más antiguo. Pega el bloque **al final** de la descripción actual de cada video (YouTube Studio → Contenido → Detalles). El primer enlace abre ese mismo episodio en el sitio con la bienvenida para quien llega de YouTube.\n"]
    for e in eps:
        etiquetas = " ".join(dict.fromkeys(
            ["#LosHDP", "#Hidalgo"]
            + ([hashtag(e["segmento"])] if e["segmento"] else [])
            + ([hashtag(e["invitado"].split('"')[0].split("'")[0])] if e["invitado"] else [])
            + ([hashtag(e["municipio"])] if e["municipio"] else [])
            + ([hashtag(e["partido"])] if e["partido"] else [])))
        bloques.append(f"""## {e['fecha']} · {e['titulo']}

```
🌐 Este episodio y todos los adoptados, por partido y municipio: {enlace('yt', e['id'])}
🎧 Escúchalo en Spotify: {SPOTIFY}
📲 Escríbenos por WhatsApp: {WHATSAPP}
🙋 ¿Quieres ser adoptado? {SITIO}?o=yt#adoptame
🤝 Patrocinios y media kit: {SITIO}?o=yt#patrocinio

{etiquetas}
```
""")
    (out / "youtube_descripciones.md").write_text("\n".join(bloques))
    print(f"{len(eps)} episodios → {out}/enlaces_por_episodio.csv y youtube_descripciones.md")


if __name__ == "__main__":
    main()

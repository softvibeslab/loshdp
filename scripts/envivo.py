"""Transmisiones en vivo de Los HDP: agenda, estado "en vivo" y calendarios .ics del sitio.

Escribe landing/data/envivo.json (lo lee el sitio cada minuto), landing/data/envivo.ics (calendario
suscribible) y landing/data/ics/<id>.ics (un evento por transmisión). Las fechas se capturan en hora
del centro de México.

  python3 scripts/envivo.py listar
  python3 scripts/envivo.py agendar --inicio "2026-10-28 19:00" --titulo "El Adoptado en vivo" \
      --invitado "Nombre" --duracion 90 --plataforma "Facebook y YouTube" --url https://...
  python3 scripts/envivo.py quitar <id>
  python3 scripts/envivo.py iniciar --youtube <id_video>      # o --facebook <url_del_live>, o sin nada
  python3 scripts/envivo.py terminar
  python3 scripts/envivo.py publicar                          # sube solo los datos en vivo al VPS
"""
import argparse
import json
import re
import subprocess
import sys
import unicodedata
from datetime import datetime, timedelta, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DATOS = RAIZ / "landing" / "data"
JSON_PATH = DATOS / "envivo.json"
TZ = timezone(timedelta(hours=-6))  # America/Mexico_City (sin horario de verano desde 2022)
SITIO = "https://loshdp.softvibes.art"
CANAL_YT = "UC8_bvhq1cv1PAm7kws4ZGNA"
FB = "https://www.facebook.com/profile.php?id=61552864772878"
VPS = "root@31.220.63.211"
LLAVE = Path.home() / ".ssh" / "rovi_vps_deploy"


def ahora():
    return datetime.now(TZ)


def cargar():
    if JSON_PATH.exists():
        return json.loads(JSON_PATH.read_text(encoding="utf-8"))
    return {"canal_youtube": CANAL_YT, "facebook": FB, "en_vivo": False, "transmision": None, "proximas": []}


def slug(texto):
    t = unicodedata.normalize("NFD", texto).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")[:40] or "transmision"


def ics_texto(s):
    return s.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def ics_fecha(iso):
    return datetime.fromisoformat(iso).astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def vevento(p, sello):
    fin = datetime.fromisoformat(p["inicio"]) + timedelta(minutes=p.get("duracion_min", 90))
    desc = " · ".join(x for x in [p.get("invitado"), p.get("plataforma")] if x)
    desc = f"{desc}\nMíralo en vivo: {p.get('url') or SITIO + '/#envivo'}".strip()
    return [
        "BEGIN:VEVENT",
        f"UID:{p['id']}@loshdp.softvibes.art",
        f"DTSTAMP:{sello}",
        f"DTSTART:{ics_fecha(p['inicio'])}",
        f"DTEND:{ics_fecha(fin.isoformat())}",
        f"SUMMARY:{ics_texto('Los HDP en vivo: ' + p['titulo'])}",
        f"DESCRIPTION:{ics_texto(desc)}",
        f"URL:{p.get('url') or SITIO + '/#envivo'}",
        f"LOCATION:{ics_texto(p.get('plataforma') or 'Facebook y YouTube')}",
        "BEGIN:VALARM", "ACTION:DISPLAY", "TRIGGER:-PT15M",
        f"DESCRIPTION:{ics_texto('En 15 min: ' + p['titulo'])}", "END:VALARM",
        "END:VEVENT",
    ]


def calendario(eventos, nombre):
    sello = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    lineas = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Softvibes//Los HDP//ES", "CALSCALE:GREGORIAN",
              "METHOD:PUBLISH", f"X-WR-CALNAME:{ics_texto(nombre)}", "X-WR-TIMEZONE:America/Mexico_City",
              "REFRESH-INTERVAL;VALUE=DURATION:PT6H", "X-PUBLISHED-TTL:PT6H"]
    for p in eventos:
        lineas += vevento(p, sello)
    lineas.append("END:VCALENDAR")
    return "\r\n".join(lineas) + "\r\n"


def guardar(d):
    corte = ahora()
    d["proximas"] = sorted(
        (p for p in d.get("proximas", [])
         if datetime.fromisoformat(p["inicio"]) + timedelta(minutes=p.get("duracion_min", 90)) > corte),
        key=lambda p: p["inicio"])
    d["actualizado"] = corte.isoformat(timespec="seconds")
    DATOS.mkdir(parents=True, exist_ok=True)
    JSON_PATH.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (DATOS / "envivo.ics").write_text(calendario(d["proximas"], "Los HDP · Transmisiones en vivo"), encoding="utf-8")
    carpeta = DATOS / "ics"
    carpeta.mkdir(exist_ok=True)
    vigentes = set()
    for p in d["proximas"]:
        archivo = carpeta / f"{p['id']}.ics"
        archivo.write_text(calendario([p], "Los HDP"), encoding="utf-8")
        vigentes.add(archivo.name)
    for viejo in carpeta.glob("*.ics"):
        if viejo.name not in vigentes:
            viejo.unlink()


def listar(d):
    print("EN VIVO ahora:", "sí → " + json.dumps(d["transmision"], ensure_ascii=False) if d.get("en_vivo") else "no")
    if not d.get("proximas"):
        print("Sin transmisiones agendadas.")
    for p in d.get("proximas", []):
        print(f"- {p['id']}: {p['inicio']} · {p['titulo']} · {p.get('invitado') or ''}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("listar")
    a = sub.add_parser("agendar")
    a.add_argument("--inicio", required=True, help='"AAAA-MM-DD HH:MM", hora del centro de México')
    a.add_argument("--titulo", required=True)
    a.add_argument("--invitado", default="")
    a.add_argument("--duracion", type=int, default=90, help="minutos")
    a.add_argument("--plataforma", default="Facebook y YouTube")
    a.add_argument("--url", default="", help="enlace del live si ya existe (Facebook o YouTube)")
    q = sub.add_parser("quitar")
    q.add_argument("id")
    i = sub.add_parser("iniciar")
    i.add_argument("--youtube", default="", help="id del video en vivo de YouTube")
    i.add_argument("--facebook", default="", help="URL del video en vivo de Facebook")
    i.add_argument("--titulo", default="")
    sub.add_parser("terminar")
    sub.add_parser("publicar")
    args = ap.parse_args()

    d = cargar()
    if args.cmd == "listar":
        return listar(d)
    if args.cmd == "publicar":
        guardar(d)
        destino = f"{VPS}:/var/www/loshdp/data/"
        ssh = f"ssh -i {LLAVE}"
        subprocess.run(["rsync", "-az", "--delete", "-e", ssh, str(DATOS / "ics") + "/", destino + "ics/"], check=True)
        subprocess.run(["rsync", "-az", "-e", ssh, str(JSON_PATH), str(DATOS / "envivo.ics"), destino], check=True)
        subprocess.run(["ssh", "-i", str(LLAVE), VPS, "chmod -R a+rX /var/www/loshdp/data"], check=True)
        print(f"publicado → {SITIO}/#envivo")
        return
    if args.cmd == "agendar":
        inicio = datetime.strptime(args.inicio, "%Y-%m-%d %H:%M").replace(tzinfo=TZ)
        base = f"{inicio:%Y%m%d-%H%M}-{slug(args.titulo)}"
        d.setdefault("proximas", []).append({
            "id": base, "inicio": inicio.isoformat(timespec="minutes"), "duracion_min": args.duracion,
            "titulo": args.titulo, "invitado": args.invitado, "plataforma": args.plataforma, "url": args.url})
        print("agendada:", base)
    elif args.cmd == "quitar":
        antes = len(d.get("proximas", []))
        d["proximas"] = [p for p in d.get("proximas", []) if p["id"] != args.id]
        if len(d["proximas"]) == antes:
            sys.exit(f"no existe la transmisión {args.id}")
    elif args.cmd == "iniciar":
        prox = (d.get("proximas") or [{}])[0]
        d["en_vivo"] = True
        d["transmision"] = {
            "titulo": args.titulo or prox.get("titulo") or "Los HDP en vivo",
            "plataforma": "Facebook" if args.facebook else "YouTube",
            "youtube_id": args.youtube,
            "url": args.facebook or (f"https://www.youtube.com/watch?v={args.youtube}" if args.youtube
                                     else f"https://www.youtube.com/channel/{CANAL_YT}/live"),
            "desde": ahora().isoformat(timespec="seconds"),
        }
    elif args.cmd == "terminar":
        d["en_vivo"] = False
        d["transmision"] = None
    guardar(d)
    listar(d)
    print("Recuerda: python3 scripts/envivo.py publicar")


if __name__ == "__main__":
    main()

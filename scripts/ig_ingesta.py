"""Ingesta de Instagram usando la sesión abierta del navegador (en memoria).

Las cookies se leen del navegador con yt-dlp y nunca se escriben a disco;
solo se guardan las respuestas del perfil y del feed.

Uso: python3 ig_ingesta.py <usuario> <dir_salida> [navegador] [perfil] [user_id]
"""
import json
import sys
import time
import urllib.request
from pathlib import Path

from yt_dlp.cookies import extract_cookies_from_browser

APP_ID = "936619743392459"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")


def find_jar(browser, profile):
    profiles = [profile] if profile else ["Default"] + [f"Profile {i}" for i in range(2, 17)]
    for p in profiles:
        try:
            jar = extract_cookies_from_browser(browser, p)
        except Exception:
            continue
        names = {c.name for c in jar if c.domain.endswith("instagram.com")}
        if "sessionid" in names:
            print(f"sesión de Instagram encontrada en {browser}:{p}")
            return jar
    sys.exit("no se encontró sesión de Instagram")


def get(opener, jar, url):
    csrf = next((c.value for c in jar if c.name == "csrftoken" and c.domain.endswith("instagram.com")), "")
    req = urllib.request.Request(url, headers={
        "User-Agent": UA, "x-ig-app-id": APP_ID, "x-csrftoken": csrf,
        "x-requested-with": "XMLHttpRequest", "Referer": "https://www.instagram.com/",
    })
    with opener.open(req, timeout=30) as r:
        return json.loads(r.read())


def main():
    user, out = sys.argv[1], Path(sys.argv[2])
    browser = sys.argv[3] if len(sys.argv) > 3 else "chrome"
    profile = sys.argv[4] if len(sys.argv) > 4 else None
    out.mkdir(parents=True, exist_ok=True)
    jar = find_jar(browser, profile)
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))

    uid = sys.argv[5] if len(sys.argv) > 5 else None
    if uid:
        prof = get(opener, jar, f"https://www.instagram.com/api/v1/users/{uid}/info/")
    else:
        prof = get(opener, jar, f"https://www.instagram.com/api/v1/users/web_profile_info/?username={user}")
        uid = prof["data"]["user"]["id"]
    (out / "perfil.json").write_text(json.dumps(prof, ensure_ascii=False, indent=1))

    items, max_id, page = [], None, 0
    while True:
        url = f"https://www.instagram.com/api/v1/feed/user/{uid}/?count=33"
        if max_id:
            url += f"&max_id={max_id}"
        d = get(opener, jar, url)
        items += d.get("items", [])
        page += 1
        print(f"página {page}: {len(items)} publicaciones")
        if not d.get("more_available") or not d.get("next_max_id"):
            break
        max_id = d["next_max_id"]
        time.sleep(2.5)
    (out / "feed_raw.json").write_text(json.dumps(items, ensure_ascii=False))
    print(f"total {len(items)}")


if __name__ == "__main__":
    main()

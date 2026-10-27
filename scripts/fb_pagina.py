"""Descarga el HTML de una página de Facebook con la sesión abierta (en memoria).

Uso: python3 fb_pagina.py <url> <salida.html> [navegador] [perfil]
"""
import sys
import urllib.request

from yt_dlp.cookies import extract_cookies_from_browser

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")

url, out = sys.argv[1], sys.argv[2]
browser = sys.argv[3] if len(sys.argv) > 3 else "chrome"
profile = sys.argv[4] if len(sys.argv) > 4 else None
jar = extract_cookies_from_browser(browser, profile)
if not any(c.name == "c_user" and c.domain.endswith("facebook.com") for c in jar):
    sys.exit("sin sesión de Facebook en ese perfil")
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
req = urllib.request.Request(url, headers={
    "User-Agent": UA, "Accept-Language": "es-MX,es;q=0.9",
    "Accept": "text/html,application/xhtml+xml", "Sec-Fetch-Mode": "navigate",
})
with opener.open(req, timeout=40) as r:
    open(out, "wb").write(r.read())
print("ok", out)

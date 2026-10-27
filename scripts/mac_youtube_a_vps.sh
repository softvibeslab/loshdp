#!/usr/bin/env bash
# YouTube bloquea la IP del VPS, así que se descarga en la Mac por lotes pequeños,
# se sube al VPS y se borra lo local (la Mac tiene poco espacio). Reanudable (--download-archive).
# Uso: scripts/mac_youtube_a_vps.sh episodios|shorts
set -uo pipefail
TIPO=${1:?episodios|shorts}
cd "$(dirname "$0")/.."
VPS=root@31.220.63.211
KEY=~/.ssh/rovi_vps_deploy
CANAL="https://www.youtube.com/@loshijos_delpueblopodcast"
STAGE=mediahub/_staging/$TIPO
ARCHIVO=mediahub/youtube/$TIPO/descargados.txt
MIN_MAC_GB=2
mkdir -p "$STAGE" "$(dirname "$ARCHIVO")"
ssh -i "$KEY" "$VPS" "mkdir -p /srv/loshdp-mediahub/youtube/$TIPO"

if [[ $TIPO == episodios ]]; then
  URL="$CANAL/videos"; LOTE=2
  # Audio para la base de conocimiento: Opus mono 32 kbps (~14 MB por hora)
  FORMATO=(-f "251/250/249/bestaudio" -x --audio-format opus)
else
  URL="$CANAL/shorts"; LOTE=10
  FORMATO=(-f "bv*[height<=480]+ba/b[height<=480]/b" -S "+size" --merge-output-format mp4)
fi
TOTAL=$(yt-dlp --flat-playlist --print id "$URL" 2>/dev/null | wc -l | tr -d ' ')
echo "$TIPO: $TOTAL elementos"

libre_mac() { df -g . | tail -1 | awk '{print $4}'; }
for ((ini=1; ini<=TOTAL; ini+=LOTE)); do
  if (( $(libre_mac) < MIN_MAC_GB )); then echo "FRENO: la Mac tiene menos de $MIN_MAC_GB GB libres"; exit 2; fi
  yt-dlp ${COOKIES_BROWSER:+--cookies-from-browser "$COOKIES_BROWSER"} --js-runtimes node "${FORMATO[@]}" --playlist-items "$ini-$((ini+LOTE-1))" \
    --download-archive "$ARCHIVO" --sleep-requests 1 --sleep-interval 3 --max-sleep-interval 8 \
    --no-progress --ignore-errors -o "$STAGE/%(upload_date)s_%(id)s.%(ext)s" "$URL"
  if [[ $TIPO == episodios ]]; then
    # yt-dlp copia el Opus original sin recomprimir; aquí se baja a mono 32 kbps antes de subir
    for f in "$STAGE"/*.opus; do
      [[ -e $f ]] || continue
      ffmpeg -v error -y -i "$f" -vn -ac 1 -c:a libopus -b:a 32k -application voip "${f%.opus}.tmp.opus" && mv "${f%.opus}.tmp.opus" "$f"
    done
  fi
  rsync -a --remove-source-files -e "ssh -i $KEY" "$STAGE/" "$VPS:/srv/loshdp-mediahub/youtube/$TIPO/"
  echo "$(date '+%T') lote $ini · $(wc -l < "$ARCHIVO" | tr -d ' ')/$TOTAL subidos · Mac libre $(libre_mac) GB"
done
echo "TERMINADO $TIPO"

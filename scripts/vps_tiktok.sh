#!/usr/bin/env bash
# Descarga los TikToks de Los HDP en el VPS (la IP del VPS sí puede bajar de TikTok).
# Por lotes de 40, con freno de disco y baja prioridad para no afectar producción.
# Uso (en el VPS): nohup bash vps_tiktok.sh > tiktok.log 2>&1 &
set -uo pipefail
BASE=/srv/loshdp-mediahub
YTDLP=$BASE/.venv/bin/yt-dlp
DEST=$BASE/tiktok
SEC_UID="MS4wLjABAAAAPhc3nEWBwu93eijDBdMWR-fQCzzhNW53t1t6mJD0OSnJOHSsC36ngQ4iu6Hzud2H"
MIN_LIBRE_GB=10
LOTE=40
mkdir -p "$DEST/video" "$DEST/meta"

libre_gb() { df --output=avail -BG / | tail -1 | tr -dc '0-9'; }

total=$(wc -l < "$DEST/ids.txt")
for ((ini=1; ini<=total; ini+=LOTE)); do
  if (( $(libre_gb) < MIN_LIBRE_GB )); then
    echo "$(date '+%F %T') FRENO: quedan $(libre_gb) GB libres (< $MIN_LIBRE_GB). Me detengo."
    exit 2
  fi
  sed -n "${ini},$((ini+LOTE-1))p" "$DEST/ids.txt" | sed 's|^|https://www.tiktok.com/@los_hijos_delpueblo/video/|' > "$DEST/lote.txt"
  nice -n 15 ionice -c3 "$YTDLP" -a "$DEST/lote.txt" \
    -f "b[vcodec!=none]" -S "+size,+br" \
    --download-archive "$DEST/archivo.txt" \
    --write-info-json --write-thumbnail --convert-thumbnails jpg \
    --sleep-requests 1 --sleep-interval 2 --max-sleep-interval 5 \
    --no-progress --ignore-errors \
    -o "$DEST/video/%(upload_date)s_%(id)s.%(ext)s" \
    -o "infojson:$DEST/meta/%(upload_date)s_%(id)s.%(ext)s" \
    -o "thumbnail:$DEST/meta/%(upload_date)s_%(id)s.%(ext)s"
  echo "$(date '+%F %T') lote $ini listo · $(wc -l < "$DEST/archivo.txt") descargados · $(libre_gb) GB libres"
done
rm -f "$DEST/lote.txt"
echo "$(date '+%F %T') TERMINADO"

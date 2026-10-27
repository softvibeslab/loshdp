#!/usr/bin/env bash
# Regenera el inventario del mediahub con lo que ya está en el VPS y publica el visor privado.
set -euo pipefail
cd "$(dirname "$0")/.."
VPS=root@31.220.63.211
KEY=~/.ssh/rovi_vps_deploy
ssh -i "$KEY" "$VPS" "find /srv/loshdp-mediahub/youtube /srv/loshdp-mediahub/tiktok/video -type f \( -name '*.opus' -o -name '*.mp4' -o -name '*.m4a' -o -name '*.webm' \) 2>/dev/null" > mediahub/archivos_vps.txt
python3 -I scripts/inventario.py > /dev/null
python3 -I scripts/mediahub.py > /dev/null
mkdir -p mediahub/web/miniaturas
cp landing/img/marca/logo.jpg mediahub/web/miniaturas/logo.jpg
ssh -i "$KEY" "$VPS" "mkdir -p /srv/loshdp-mediahub/web"
rsync -az --delete -e "ssh -i $KEY" mediahub/web/ "$VPS:/srv/loshdp-mediahub/web/" --exclude conocimiento
rsync -az --delete -e "ssh -i $KEY" mediahub/conocimiento/ "$VPS:/srv/loshdp-mediahub/web/conocimiento/"
ssh -i "$KEY" "$VPS" "find /srv/loshdp-mediahub/web -type d -exec chmod 755 {} + ; find /srv/loshdp-mediahub/web -type f -exec chmod 644 {} +"
echo "mediahub publicado: $(wc -l < mediahub/archivos_vps.txt | tr -d ' ') archivos en el VPS → https://loshdp.softvibes.art/mediahub/"

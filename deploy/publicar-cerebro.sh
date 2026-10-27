#!/usr/bin/env bash
# Regenera «El Cerebro del Pueblo» (fichas → grafo → recorrido) y lo publica en /cerebro/ (privado).
set -euo pipefail
cd "$(dirname "$0")/.."
APP=/Users/rogergv/Documents/SoftvibesLab/AIS-OS/apps/loshdp-brain
VPS=root@31.220.63.211
KEY=~/.ssh/rovi_vps_deploy
python3 -I scripts/mediahub.py > /dev/null
python3 -I scripts/cerebro.py
python3 -I scripts/tour_cerebro.py --app "$APP"
(cd "$APP" && node build.mjs && node export-static.mjs)
ssh -i "$KEY" "$VPS" "mkdir -p /srv/loshdp-mediahub/cerebro"
rsync -az --delete -e "ssh -i $KEY" "$APP/../loshdp-brain-web/" "$VPS:/srv/loshdp-mediahub/cerebro/"
ssh -i "$KEY" "$VPS" "find /srv/loshdp-mediahub/cerebro -type d -exec chmod 755 {} + ; find /srv/loshdp-mediahub/cerebro -type f -exec chmod 644 {} +"
echo "cerebro publicado → https://loshdpbrain.softvibes.art/?tour=1 (y /cerebro/)"

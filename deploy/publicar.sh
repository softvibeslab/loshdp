#!/usr/bin/env bash
# Publica landing/ en https://loshdp.softvibes.art (VPS rovicrm). Respaldo previo en el servidor.
set -euo pipefail
cd "$(dirname "$0")/.."
VPS=root@31.220.63.211
KEY=~/.ssh/rovi_vps_deploy
TS=$(date +%Y%m%d-%H%M%S)
ssh -i "$KEY" "$VPS" "mkdir -p /var/www/loshdp /var/backups/loshdp-web && cp -a /var/www/loshdp /var/backups/loshdp-web/$TS"
rsync -az --delete --exclude '.*' -e "ssh -i $KEY" landing/ "$VPS:/var/www/loshdp/"
ssh -i "$KEY" "$VPS" "find /var/www/loshdp -type d -exec chmod 755 {} + && find /var/www/loshdp -type f -exec chmod 644 {} +"
echo "$TS publicado" >> deploy/DESPLIEGUES.log
echo "ok → https://loshdp.softvibes.art (respaldo /var/backups/loshdp-web/$TS)"

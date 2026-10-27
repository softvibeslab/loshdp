# El Cerebro del Pueblo · Los HDP

Cerebro 3D del podcast Los HDP (Los Hijos del Pueblo) con recorrido de insights para presentar. Proyecto fuente: `SoftvibesSites/los-hdp-podcast/` (ver `docs/04-plan-cerebro-onboarding-grafo.md`).

- Local: `node serve.mjs` → http://127.0.0.1:4644 · recorrido: http://127.0.0.1:4644/?tour=1
- Web privada: https://loshdpbrain.softvibes.art/?tour=1 (alias https://loshdp.softvibes.art/cerebro/; vhost en `los-hdp-podcast/deploy/loshdpbrain.softvibes.art.conf`) (misma contraseña que el mediahub, `los-hdp-podcast/PRIVADO/mediahub-acceso.txt`)
- Fuentes: `los-hdp-podcast/mediahub/conocimiento/{insights,episodios,invitados,temas,municipios,clips}`
- Diferencias con la plantilla: `src/tour.js` (recorrido + video en el panel), `src/app.js` y `index.html` en español (base Wappy·Entrega), acento lima, `tour.json` y `export-static.mjs` (modo `BRAIN_STATIC`).

Regenerar y publicar todo: `los-hdp-podcast/deploy/publicar-cerebro.sh`. Si cambias `src/`: `npm run build:js`.

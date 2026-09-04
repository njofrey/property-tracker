# AGENTS.md

Instrucciones para cualquier agente que trabaje en este repositorio.

## Proyecto

`Property Tracker` monitorea una búsqueda de Portal Inmobiliario Chile y avisa por Telegram cuando aparece una publicación nueva. También puede avisar bajas de precio.

## Estado actual

- Scaffold creado el 2026-09-02.
- Cadencia decidida: cada 30 minutos mediante GitHub Actions.
- Stack: Python 3.12, requests, BeautifulSoup, estado JSON en una rama dedicada de GitHub y Telegram Bot API.
- Búsquedas confirmadas: arriendo de departamentos en Providencia y Vitacura, entre 1 y 2 dormitorios, hasta $850.000, sin exigir estacionamiento.
- El extractor se validó con HTML real el 2026-09-04.
- GitHub tiene `PORTAL_SEARCH_URLS` y `ALERT_PRICE_DROPS=true` configurados.
- La rama `tracker-state` contiene el baseline inicial de 63 publicaciones.
- Falta un bot de Telegram propio. El cron continúa apagado.

## Al retomar

Si Nico escribe «sigamos»:

1. Leer `README.md` y `MEMORY.md`.
2. No volver a pedir filtros ni URLs: ya están confirmados y validados.
3. Verificar que exista la rama `tracker-state` y que el baseline esté creado.
4. Configurar `TELEGRAM_TOKEN` y `TELEGRAM_CHAT_ID` cuando Nico tenga el bot propio.
5. Confirmar una alerta controlada y luego activar/verificar el cron.

## Reglas

- Secrets nunca en código ni commits.
- Telegram siempre usa `parse_mode: "HTML"`.
- Primera ejecución crea baseline y no bombardea Telegram con publicaciones antiguas.
- Una publicación se identifica por su ID estable `MLC...`, nunca por título ni posición.
- Si Portal falla o cambia HTML, terminar con error sin modificar el baseline.
- El estado vive exclusivamente en `tracker-state`; no usar la base Upstash de Flights.
- No usar Playwright/Selenium en producción salvo que se demuestre que el HTML no contiene los resultados.
- Mensajes en español chileno directo, sin marketing ni ruido.

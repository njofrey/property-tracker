# AGENTS.md

Instrucciones para cualquier agente que trabaje en este repositorio.

## Proyecto

`Property Tracker` monitorea una búsqueda de Portal Inmobiliario Chile y avisa por Telegram cuando aparece una publicación nueva. También puede avisar bajas de precio.

## Estado actual

- Scaffold creado el 2026-09-02.
- Cadencia decidida: cada 30 minutos mediante GitHub Actions.
- Stack decidido: Python 3.12, requests, BeautifulSoup, Upstash Redis y Telegram Bot API.
- La URL y los filtros concretos todavía están pendientes; Nico los recibirá después.
- El extractor HTML es deliberadamente defensivo, pero debe validarse con la URL real antes de desplegar.

## Al retomar

Si Nico escribe «sigamos»:

1. Leer `README.md` y `MEMORY.md`.
2. Pedir o recibir solamente estos datos pendientes: compra/arriendo, casa/departamento, comunas, precio máximo y moneda, dormitorios mínimos, estacionamiento y si quiere alertas de bajas de precio.
3. Pedir la URL de Portal Inmobiliario con esos filtros aplicados.
4. Probar `portal_source.py` contra esa URL y ajustar la extracción con evidencia real.
5. Configurar los secrets en GitHub, ejecutar manualmente una vez para crear el baseline y luego activar/verificar el cron.

## Reglas

- Secrets nunca en código ni commits.
- Telegram siempre usa `parse_mode: "HTML"`.
- Primera ejecución crea baseline y no bombardea Telegram con publicaciones antiguas.
- Una publicación se identifica por su ID estable `MLC...`, nunca por título ni posición.
- Si Portal falla o cambia HTML, terminar con error sin modificar el baseline.
- No usar Playwright/Selenium en producción salvo que se demuestre que el HTML no contiene los resultados.
- Mensajes en español chileno directo, sin marketing ni ruido.


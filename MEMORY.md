# MEMORY.md

## Decisiones confirmadas

- Nombre del proyecto: **Property Tracker**.
- Vive como proyecto separado y hermano de `Flights`.
- Revisión: cada **30 minutos**.
- Canal de alertas: Telegram.
- Estado/deduplicación: Upstash Redis.
- Runtime: GitHub Actions con Python 3.12.
- Alertar solamente después del baseline inicial.
- El cron de 30 minutos está preparado pero pausado hasta configurar URL y secrets.

## Objetivo

Detectar publicaciones nuevas en una búsqueda definida de Portal Inmobiliario Chile. Opcionalmente detectar bajas de precio de avisos ya conocidos.

## Búsqueda confirmada

- Arriendo de departamentos.
- Comunas: Providencia y Vitacura.
- Precio máximo: $850.000 CLP (Nico indicó también su referencia de 20,79 UF).
- Entre 1 y 2 dormitorios.
- Estacionamiento no obligatorio.
- Alertar publicaciones nuevas y bajas de precio.

## URLs validadas el 2026-09-04

- Providencia: `https://www.portalinmobiliario.com/arriendo/departamento/providencia-metropolitana/_PriceRange_0CLP-850000CLP_BEDROOMS_1-2_NoIndex_True` (48 resultados).
- Vitacura: `https://www.portalinmobiliario.com/arriendo/departamento/vitacura-metropolitana/_PriceRange_0CLP-850000CLP_BEDROOMS_1-2_NoIndex_True` (15 resultados).

La primera URL recibida contenía solamente Providencia, máximo $900.000 y rango
`*-2`. El tracker ahora acepta varias URLs mediante `PORTAL_SEARCH_URLS` y deduplica
la unión por ID `MLC`.

## Configuración de GitHub

- Secret `PORTAL_SEARCH_URLS`: configurado el 2026-09-04.
- Variable `ALERT_PRICE_DROPS=true`: configurada el 2026-09-04.
- Secrets pendientes: `TELEGRAM_TOKEN`, `TELEGRAM_CHAT_ID`,
  `UPSTASH_REDIS_REST_URL` y `UPSTASH_REDIS_REST_TOKEN`.

## Próximo paso exacto

Configurar los secrets, ejecutar manualmente para crear el baseline y confirmar una alerta controlada.

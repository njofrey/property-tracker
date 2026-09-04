# CLAUDE.md

Este repositorio es **Property Tracker**, un bot personal que monitorea Portal Inmobiliario Chile cada 30 minutos y avisa por Telegram sobre publicaciones nuevas y, opcionalmente, bajas de precio.

Antes de trabajar:

1. Lee `AGENTS.md` completo: contiene arquitectura, reglas y el procedimiento para retomar.
2. Lee `MEMORY.md` completo: contiene decisiones confirmadas, datos pendientes y el próximo paso exacto.
3. Lee `README.md` para ejecución y configuración.

Si Nico escribe solamente **«sigamos»**, continúa desde `MEMORY.md`; no rediseñes el proyecto ni repitas preguntas ya respondidas.

Estado al 2026-09-04: búsquedas de Providencia y Vitacura validadas, estado migrado desde Upstash a la rama `tracker-state` y GitHub parcialmente configurado. Falta conectar un bot de Telegram propio y activar el cron.

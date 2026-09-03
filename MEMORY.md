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

## Información pendiente de Nico

1. Compra o arriendo.
2. Casa o departamento.
3. Comunas.
4. Precio máximo y moneda: UF, CLP o USD.
5. Dormitorios mínimos.
6. Si necesita estacionamiento.
7. Si quiere alertas por bajas de precio además de avisos nuevos.
8. URL final de Portal Inmobiliario con filtros aplicados.

## Próximo paso exacto

Validar el extractor con la URL real, crear repositorio Git, configurar secrets, ejecutar manualmente para crear baseline y confirmar una alerta controlada.

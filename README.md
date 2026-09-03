# Property Tracker

Tracker personal de Portal Inmobiliario Chile. Consulta una búsqueda cada 30 minutos, recuerda los IDs vistos en Upstash y envía a Telegram solamente publicaciones nuevas o bajas de precio.

## Estado

El proyecto base está listo. Falta definir la búsqueda real y validar el extractor con su HTML.

## Configuración

1. Copiar `.env.example` a `.env` para una prueba local.
2. Completar la URL y los secrets.
3. Instalar dependencias:

```bash
python -m pip install -r requirements.txt
```

4. Probar solamente la extracción:

```bash
PORTAL_SEARCH_URL='https://www.portalinmobiliario.com/...' python portal_source.py
```

5. Ejecutar el tracker:

```bash
python check_properties.py
```

6. Ejecutar las pruebas:

```bash
python -m unittest discover -s tests -v
```

La primera ejecución crea un baseline y no envía avisos antiguos. Las ejecuciones siguientes notifican IDs nuevos. Para recibir mensajes, el chat debe haber enviado `/start` al bot.

## Variables

- `PORTAL_SEARCH_URL`: URL completa con filtros aplicados.
- `SEARCH_KEY`: nombre estable de la búsqueda, por ejemplo `depto-providencia`.
- `ALERT_PRICE_DROPS`: `true` o `false`.
- `TELEGRAM_TOKEN` y `TELEGRAM_CHAT_ID`.
- `UPSTASH_REDIS_REST_URL` y `UPSTASH_REDIS_REST_TOKEN`.

## GitHub Actions

El workflow permite ejecución manual. El cron de 30 minutos está preparado pero comentado hasta configurar la búsqueda y los secrets. Una vez activado, GitHub puede retrasarlo durante periodos de alta carga; la cadencia no es una garantía de minuto exacto.

Secrets requeridos en GitHub:

- `PORTAL_SEARCH_URL`
- `TELEGRAM_TOKEN`
- `TELEGRAM_CHAT_ID`
- `UPSTASH_REDIS_REST_URL`
- `UPSTASH_REDIS_REST_TOKEN`

Variable opcional del repositorio:

- `ALERT_PRICE_DROPS=true`

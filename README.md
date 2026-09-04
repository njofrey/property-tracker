# Property Tracker

Tracker personal de Portal Inmobiliario Chile. Consulta las búsquedas cada 30 minutos, recuerda los IDs vistos en la rama `tracker-state` y envía a Telegram solamente publicaciones nuevas o bajas de precio.

## Estado

Las búsquedas de Providencia y Vitacura están validadas. Falta conectar un bot de Telegram propio y activar el cron.

## Configuración

1. Copiar `.env.example` a `.env` para una prueba local.
2. Completar Telegram; las URLs reales ya están en el ejemplo.
3. Instalar dependencias:

```bash
python -m pip install -r requirements.txt
```

4. Probar solamente la extracción:

```bash
PORTAL_SEARCH_URLS='https://www.portalinmobiliario.com/...' python3 portal_source.py
```

5. Ejecutar el tracker:

```bash
python3 check_properties.py
```

6. Ejecutar las pruebas:

```bash
python3 -m unittest discover -s tests -v
```

La primera ejecución crea un baseline y no envía avisos antiguos. Las ejecuciones siguientes notifican IDs nuevos. Para recibir mensajes, el chat debe haber enviado `/start` al bot.

## Variables

- `PORTAL_SEARCH_URLS`: una URL completa por comuna, separadas por saltos de línea.
  Para una sola búsqueda también se acepta la variable antigua `PORTAL_SEARCH_URL`.
- `ALERT_PRICE_DROPS`: `true` o `false`.
- `STATE_FILE`: ruta del JSON persistente; GitHub Actions usa la rama `tracker-state`.
- `TELEGRAM_TOKEN` y `TELEGRAM_CHAT_ID`.

## GitHub Actions

El workflow permite ejecución manual. Usa `main` para el código y `tracker-state` para `state.json`. El cron de 30 minutos está preparado pero comentado hasta configurar Telegram. Una vez activado, GitHub puede retrasarlo durante periodos de alta carga; la cadencia no es una garantía de minuto exacto.

Secrets requeridos en GitHub:

- `PORTAL_SEARCH_URLS`
- `TELEGRAM_TOKEN`
- `TELEGRAM_CHAT_ID`

Variable opcional del repositorio:

- `ALERT_PRICE_DROPS=true`

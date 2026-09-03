import sys
import traceback
from dataclasses import asdict

from config import Settings
from portal_source import fetch_properties
from property_state import PropertyState
from telegram_notify import TelegramNotifier


def is_price_drop(current: dict, previous: dict | None) -> bool:
    if not previous:
        return False
    return (
        current.get("currency") is not None
        and current.get("currency") == previous.get("currency")
        and current.get("price_value") is not None
        and previous.get("price_value") is not None
        and current["price_value"] < previous["price_value"]
    )


def main() -> int:
    settings = Settings.from_env()
    state = PropertyState(settings.upstash_url, settings.upstash_token, settings.search_key)
    notifier = TelegramNotifier(settings.telegram_token, settings.telegram_chat_id)

    # Si la extracción falla, no tocamos estado: la próxima corrida puede reintentar.
    properties = fetch_properties(settings.search_url)
    items = {item.id: asdict(item) for item in properties}
    print(f"Extraídas {len(items)} publicaciones")

    if not state.initialized():
        for item in items.values():
            state.save_item(item)
            state.mark_seen(item["id"])
        state.mark_initialized()
        print(f"Baseline creado con {len(items)} publicaciones; no se enviaron alertas")
        return 0

    seen = state.seen_ids()
    new_count = 0
    drop_count = 0

    for property_id, item in items.items():
        previous = state.get_item(property_id)
        try:
            if property_id not in seen:
                notifier.send_new(item)
                state.mark_seen(property_id)
                new_count += 1
            elif settings.alert_price_drops and is_price_drop(item, previous):
                notifier.send_price_drop(item, previous)
                drop_count += 1
            state.save_item(item)
        except Exception as exc:
            # No actualizamos el item si Telegram falla: así la alerta se reintenta.
            print(f"[{property_id}] error procesando: {exc}", file=sys.stderr)
            traceback.print_exc()

    print(f"Alertas: {new_count} nuevas, {drop_count} bajas de precio")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


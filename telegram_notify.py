import html

import requests


class TelegramNotifier:
    def __init__(self, token: str, chat_id: str):
        self.url = f"https://api.telegram.org/bot{token}/sendMessage"
        self.chat_id = chat_id

    def send_new(self, item: dict):
        lines = [
            "🏠 <b>Nueva propiedad</b>",
            "",
            f"<b>{html.escape(item['title'])}</b>",
        ]
        if item.get("price_label"):
            lines.append(f"Precio: <b>{html.escape(item['price_label'])}</b>")
        if item.get("location"):
            lines.append(f"Ubicación: {html.escape(item['location'])}")
        lines.extend(["", f'<a href="{html.escape(item["url"], quote=True)}">Ver publicación</a>'])
        self._send("\n".join(lines))

    def send_price_drop(self, item: dict, previous: dict):
        text = (
            "📉 <b>Bajó de precio</b>\n\n"
            f"<b>{html.escape(item['title'])}</b>\n"
            f"Antes: {html.escape(previous.get('price_label') or '—')}\n"
            f"Ahora: <b>{html.escape(item.get('price_label') or '—')}</b>\n\n"
            f'<a href="{html.escape(item["url"], quote=True)}">Ver publicación</a>'
        )
        self._send(text)

    def _send(self, text: str):
        response = requests.post(
            self.url,
            json={
                "chat_id": self.chat_id,
                "text": text,
                "parse_mode": "HTML",
                "disable_web_page_preview": False,
            },
            timeout=30,
        )
        response.raise_for_status()


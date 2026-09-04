import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


def _required(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"Falta la variable {name}")
    return value


def _boolean(name: str, default: bool = False) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "si", "sí", "on"}


def _search_urls() -> tuple[str, ...]:
    raw = os.environ.get("PORTAL_SEARCH_URLS", "").strip()
    if raw:
        urls = tuple(line.strip() for line in raw.splitlines() if line.strip())
    else:
        urls = (_required("PORTAL_SEARCH_URL"),)
    if not all(url.startswith("https://www.portalinmobiliario.com/") for url in urls):
        raise RuntimeError("Todas las URLs deben pertenecer a www.portalinmobiliario.com")
    return urls


@dataclass(frozen=True)
class Settings:
    search_urls: tuple[str, ...]
    alert_price_drops: bool
    state_file: str
    telegram_token: str | None
    telegram_chat_id: str | None

    def telegram_credentials(self) -> tuple[str, str]:
        if not self.telegram_token or not self.telegram_chat_id:
            raise RuntimeError("Faltan TELEGRAM_TOKEN y TELEGRAM_CHAT_ID")
        return self.telegram_token, self.telegram_chat_id

    @classmethod
    def from_env(cls):
        return cls(
            search_urls=_search_urls(),
            alert_price_drops=_boolean("ALERT_PRICE_DROPS", True),
            state_file=os.environ.get("STATE_FILE", "state.json").strip() or "state.json",
            telegram_token=os.environ.get("TELEGRAM_TOKEN", "").strip() or None,
            telegram_chat_id=os.environ.get("TELEGRAM_CHAT_ID", "").strip() or None,
        )

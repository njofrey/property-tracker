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


@dataclass(frozen=True)
class Settings:
    search_url: str
    search_key: str
    alert_price_drops: bool
    telegram_token: str
    telegram_chat_id: str
    upstash_url: str
    upstash_token: str

    @classmethod
    def from_env(cls):
        return cls(
            search_url=_required("PORTAL_SEARCH_URL"),
            search_key=os.environ.get("SEARCH_KEY", "busqueda-principal").strip(),
            alert_price_drops=_boolean("ALERT_PRICE_DROPS", True),
            telegram_token=_required("TELEGRAM_TOKEN"),
            telegram_chat_id=_required("TELEGRAM_CHAT_ID"),
            upstash_url=_required("UPSTASH_REDIS_REST_URL"),
            upstash_token=_required("UPSTASH_REDIS_REST_TOKEN"),
        )


"""Extracción defensiva de resultados públicos de Portal Inmobiliario."""

import json
import os
import re
from dataclasses import asdict, dataclass
from urllib.parse import urldefrag, urljoin

import requests
from bs4 import BeautifulSoup


ID_RE = re.compile(r"\bMLC-?(\d{6,})\b", re.IGNORECASE)
PRICE_RE = re.compile(r"(?P<currency>UF|US\$|\$)\s*(?P<amount>[\d][\d.,]*)", re.IGNORECASE)
CARD_SELECTORS = (
    "li.ui-search-layout__item",
    ".poly-card",
    "article",
)


class ExtractionError(RuntimeError):
    pass


@dataclass(frozen=True)
class Property:
    id: str
    title: str
    url: str
    price_label: str | None = None
    price_value: int | float | None = None
    currency: str | None = None
    location: str | None = None


def extract_property_id(value: str) -> str | None:
    match = ID_RE.search(value or "")
    return f"MLC{match.group(1)}" if match else None


def _parse_chilean_number(value: str) -> int | float:
    """Interpreta punto de miles y coma decimal usados en Chile."""
    normalized = value.replace(".", "").replace(",", ".")
    number = float(normalized) if "." in normalized else int(normalized)
    return int(number) if isinstance(number, float) and number.is_integer() else number


def parse_price(text: str):
    match = PRICE_RE.search(text or "")
    if not match:
        return None, None, None
    raw_currency = match.group("currency").upper()
    currency = {"UF": "UF", "US$": "USD", "$": "CLP"}[raw_currency]
    label = match.group(0).strip()
    amount = match.group("amount")
    return label, _parse_chilean_number(amount), currency


def _card_for(anchor):
    for parent in anchor.parents:
        if getattr(parent, "name", None) in {"body", "html"}:
            break
        classes = " ".join(parent.get("class", []))
        if parent.name == "article" or "ui-search-layout__item" in classes or "poly-card" in classes:
            return parent
    return anchor.parent


def parse_results(html_text: str, base_url: str):
    lower = html_text.lower()
    if "captcha" in lower or "robot" in lower and "verific" in lower:
        raise ExtractionError("Portal respondió con una verificación anti-bot")

    soup = BeautifulSoup(html_text, "html.parser")
    found = {}

    for anchor in soup.find_all("a", href=True):
        url = urldefrag(urljoin(base_url, anchor["href"])).url
        property_id = extract_property_id(url)
        if not property_id or property_id in found:
            continue

        card = _card_for(anchor)
        card_text = " ".join(card.stripped_strings) if card else ""
        title_node = card.select_one("h2, h3, .poly-component__title") if card else None
        title = (
            anchor.get("title")
            or (title_node.get_text(" ", strip=True) if title_node else None)
            or anchor.get_text(" ", strip=True)
            or property_id
        )
        price_label, price_value, currency = parse_price(card_text)
        location_node = card.select_one(
            ".poly-component__location, .ui-search-item__location, [class*='location']"
        ) if card else None

        found[property_id] = Property(
            id=property_id,
            title=title[:300],
            url=url,
            price_label=price_label,
            price_value=price_value,
            currency=currency,
            location=location_node.get_text(" ", strip=True)[:300] if location_node else None,
        )

    if not found:
        raise ExtractionError(
            "No se encontraron IDs MLC. El HTML cambió, la URL es inválida o Portal bloqueó la consulta"
        )
    return list(found.values())


def fetch_properties(search_url: str):
    response = requests.get(
        search_url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; PropertyTracker/1.0)",
            "Accept-Language": "es-CL,es;q=0.9",
        },
        timeout=30,
    )
    response.raise_for_status()
    return parse_results(response.text, search_url)


def fetch_all_properties(search_urls: tuple[str, ...]):
    """Extrae varias búsquedas y elimina duplicados por ID estable."""
    found = {}
    for search_url in search_urls:
        for item in fetch_properties(search_url):
            found.setdefault(item.id, item)
    return list(found.values())


if __name__ == "__main__":
    raw_urls = os.environ.get("PORTAL_SEARCH_URLS", "").strip()
    if raw_urls:
        urls = tuple(line.strip() for line in raw_urls.splitlines() if line.strip())
    else:
        url = os.environ.get("PORTAL_SEARCH_URL", "").strip()
        if not url:
            raise SystemExit("Falta PORTAL_SEARCH_URLS o PORTAL_SEARCH_URL")
        urls = (url,)
    items = fetch_all_properties(urls)
    print(json.dumps([asdict(item) for item in items[:5]], ensure_ascii=False, indent=2))
    print(f"Total extraído: {len(items)}")

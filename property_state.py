"""Estado persistente del tracker en un archivo JSON."""

import json
import os
from pathlib import Path


class PropertyState:
    def __init__(self, path: str):
        self.path = Path(path)
        self._initialized = False
        self._seen: set[str] = set()
        self._items: dict[str, dict] = {}
        self._dirty = False
        self._load()

    def _load(self):
        if not self.path.exists():
            return
        data = json.loads(self.path.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or data.get("version") != 1:
            raise RuntimeError(f"Estado inválido en {self.path}")
        seen = data.get("seen")
        items = data.get("items")
        if not isinstance(seen, list) or not all(isinstance(item, str) for item in seen):
            raise RuntimeError(f"Lista de IDs inválida en {self.path}")
        if not isinstance(items, dict):
            raise RuntimeError(f"Publicaciones inválidas en {self.path}")
        self._initialized = data.get("initialized") is True
        self._seen = set(seen)
        self._items = items

    def initialized(self) -> bool:
        return self._initialized

    def mark_initialized(self):
        if not self._initialized:
            self._initialized = True
            self._dirty = True

    def seen_ids(self):
        return set(self._seen)

    def mark_seen(self, property_id: str):
        if property_id not in self._seen:
            self._seen.add(property_id)
            self._dirty = True

    def get_item(self, property_id: str):
        return self._items.get(property_id)

    def save_item(self, item: dict):
        if self._items.get(item["id"]) != item:
            self._items[item["id"]] = item
            self._dirty = True

    def flush(self) -> bool:
        if not self._dirty:
            return False
        payload = {
            "version": 1,
            "initialized": self._initialized,
            "seen": sorted(self._seen),
            "items": dict(sorted(self._items.items())),
        }
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_name(f".{self.path.name}.tmp")
        temporary.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        os.replace(temporary, self.path)
        self._dirty = False
        return True

import json

from upstash_redis import Redis


class PropertyState:
    def __init__(self, url: str, token: str, search_key: str):
        self.redis = Redis(url=url, token=token, rest_retries=1, rest_retry_interval=1.0)
        self.prefix = f"property-tracker:{search_key}"

    @property
    def seen_key(self):
        return f"{self.prefix}:seen"

    @property
    def items_key(self):
        return f"{self.prefix}:items"

    @property
    def initialized_key(self):
        return f"{self.prefix}:initialized"

    def initialized(self) -> bool:
        return bool(self.redis.get(self.initialized_key))

    def mark_initialized(self):
        self.redis.set(self.initialized_key, "1")

    def seen_ids(self):
        return set(self.redis.smembers(self.seen_key) or [])

    def mark_seen(self, property_id: str):
        self.redis.sadd(self.seen_key, property_id)

    def get_item(self, property_id: str):
        raw = self.redis.hget(self.items_key, property_id)
        return json.loads(raw) if raw else None

    def save_item(self, item: dict):
        self.redis.hset(self.items_key, item["id"], json.dumps(item, ensure_ascii=False))


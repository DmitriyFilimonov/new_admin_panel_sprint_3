import json
import abc
import redis
from redis import Redis, commands
from typing import Any, Dict


class RedisStorage():
    KEY = "data"

    def __init__(self, redis_client: redis.Redis):
        self.redis_client = redis_client

    def save_state(self, state: Dict[str, Any]) -> None:
        json_str = json.dumps(state)
        self.redis_client.set(self.KEY, json_str)

    def retrieve_state(self) -> Dict[str, Any]:
        raw = self.redis_client.get(self.KEY)

        if raw is None:
            return {}

        try:
            return json.load(raw)
        except json.JSONDecodeError:
            raise

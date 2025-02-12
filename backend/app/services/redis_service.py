from typing import Dict, Optional, List
import json
import redis
from app.models import TruckData

class RedisService:
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url)
        self.key_prefix = "truck:"
        self.expiry_seconds = 5 * 60 * 60  # 5 hours

    def store_truck_data(self, truck_data: TruckData) -> None:
        """Store truck data in Redis with expiration"""
        key = f"{self.key_prefix}{truck_data.id}"
        self.redis.setex(
            key,
            self.expiry_seconds,
            truck_data.model_dump_json()
        )

    def get_truck_data(self, truck_id: str) -> Optional[TruckData]:
        """Retrieve truck data from Redis"""
        key = f"{self.key_prefix}{truck_id}"
        data = self.redis.get(key)
        if data:
            return TruckData.model_validate_json(data)
        return None

    def get_all_trucks(self) -> List[TruckData]:
        """Get all active trucks"""
        keys = self.redis.keys(f"{self.key_prefix}*")
        if not keys:
            return []

        data = self.redis.mget(keys)
        return [TruckData.model_validate_json(d) for d in data if d]

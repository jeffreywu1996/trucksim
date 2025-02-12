import asyncio
import json
import random
import websockets
from datetime import datetime, timezone
import math

# NYC area boundaries
NYC_BOUNDS = {
    'min_lat': 40.4774,
    'max_lat': 40.9176,
    'min_lng': -74.2591,
    'max_lng': -73.7004
}

class Truck:
    def __init__(self, truck_id):
        self.id = f"truck-{truck_id}"
        self.latitude = random.uniform(NYC_BOUNDS['min_lat'], NYC_BOUNDS['max_lat'])
        self.longitude = random.uniform(NYC_BOUNDS['min_lng'], NYC_BOUNDS['max_lng'])
        self.speed = 0
        self.fuel_level = 100.0
        self.engine_status = "running"
        self.running_time = 0
        self.miles_accumulated = 0.0
        self.direction = random.uniform(0, 2 * math.pi)  # Random direction in radians

    def update(self):
        # Update speed (randomly accelerate or decelerate)
        self.speed += random.uniform(-5, 5)
        self.speed = max(0, min(65, self.speed))  # Keep speed between 0 and 65 mph

        # Move truck based on speed and direction
        speed_lat_lng = self.speed * 0.000008  # Rough conversion from mph to lat/lng
        self.latitude += math.sin(self.direction) * speed_lat_lng
        self.longitude += math.cos(self.direction) * speed_lat_lng

        # Bounce off boundaries
        if self.latitude < NYC_BOUNDS['min_lat'] or self.latitude > NYC_BOUNDS['max_lat']:
            self.direction = -self.direction
        if self.longitude < NYC_BOUNDS['min_lng'] or self.longitude > NYC_BOUNDS['max_lng']:
            self.direction = math.pi - self.direction

        # Update other metrics
        self.running_time += 1
        self.miles_accumulated += self.speed / 3600  # Convert mph to miles per second
        self.fuel_level = max(0, self.fuel_level - random.uniform(0, 0.1))

    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "latitude": self.latitude,
            "longitude": self.longitude,
            "speed": round(self.speed, 2),
            "fuel_level": round(self.fuel_level, 2),
            "engine_status": self.engine_status,
            "running_time": self.running_time,
            "miles_accumulated": round(self.miles_accumulated, 2)
        }

async def simulate_fleet():
    uri = "ws://backend:8000/ws"
    trucks = [Truck(i) for i in range(10)]  # Create 10 trucks

    while True:
        try:
            async with websockets.connect(uri) as websocket:
                while True:
                    # Update all trucks
                    for truck in trucks:
                        truck.update()

                    # Create update message
                    update = {
                        "type": "trucks_update",
                        "data": [truck.to_dict() for truck in trucks]
                    }

                    # Send update
                    await websocket.send(json.dumps(update))
                    await asyncio.sleep(1)  # Update every second

        except websockets.ConnectionClosed:
            print("Connection lost. Retrying...")
            await asyncio.sleep(5)
        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(simulate_fleet())

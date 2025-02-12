import asyncio
import json
import random
import websockets
import time
from datetime import datetime
from typing import Dict, List
import os

class Truck:
    def __init__(self, truck_id: str):
        self.id = truck_id
        self.latitude = random.uniform(40.0, 41.0)  # Example: NYC area
        self.longitude = random.uniform(-74.0, -73.0)
        self.speed = 0
        self.fuel_level = 100
        self.engine_status = "running"
        self.start_time = time.time()
        self.miles_accumulated = 0

    def update(self):
        # Simulate movement
        self.latitude += random.uniform(-0.001, 0.001)
        self.longitude += random.uniform(-0.001, 0.001)
        self.speed = random.uniform(0, 65)  # mph
        self.fuel_level = max(0, self.fuel_level - random.uniform(0, 0.1))
        self.miles_accumulated += self.speed / 3600  # Convert to miles per second

    def to_dict(self) -> dict:
        running_time = int(time.time() - self.start_time)
        return {
            "id": self.id,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "speed": round(self.speed, 2),
            "fuel_level": round(self.fuel_level, 2),
            "engine_status": self.engine_status,
            "running_time": running_time,
            "miles_accumulated": round(self.miles_accumulated, 2),
            "timestamp": datetime.utcnow().isoformat()
        }

class TruckFleetSimulator:
    def __init__(self, num_trucks: int, websocket_url: str):
        self.trucks: Dict[str, Truck] = {
            f"truck-{i}": Truck(f"truck-{i}")
            for i in range(num_trucks)
        }
        self.websocket_url = websocket_url

    async def update_and_send(self):
        async with websockets.connect(self.websocket_url) as websocket:
            while True:
                try:
                    # Update all trucks
                    for truck in self.trucks.values():
                        truck.update()

                    # Send updates
                    payload = {
                        "type": "trucks_update",
                        "data": [truck.to_dict() for truck in self.trucks.values()]
                    }
                    await websocket.send(json.dumps(payload))
                    await asyncio.sleep(1)  # 1Hz update frequency

                except websockets.exceptions.ConnectionClosed:
                    print("Connection lost. Attempting to reconnect...")
                    break
                except Exception as e:
                    print(f"Error: {e}")
                    break

    async def run(self):
        while True:
            try:
                await self.update_and_send()
            except Exception as e:
                print(f"Error in run loop: {e}")
                await asyncio.sleep(5)  # Wait before reconnecting

def main():
    num_trucks = int(os.getenv("NUM_TRUCKS", "20"))
    websocket_url = os.getenv("BACKEND_URL", "ws://localhost:8000/ws")

    simulator = TruckFleetSimulator(num_trucks, websocket_url)
    asyncio.run(simulator.run())

if __name__ == "__main__":
    main()

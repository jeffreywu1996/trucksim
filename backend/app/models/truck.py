from datetime import datetime
from pydantic import BaseModel
from typing import List

class TruckData(BaseModel):
    id: str
    timestamp: datetime
    latitude: float
    longitude: float
    speed: float
    fuel_level: float
    engine_status: str
    running_time: int
    miles_accumulated: float

class TruckUpdate(BaseModel):
    type: str = "trucks_update"
    data: List[TruckData]

from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Literal

class TruckData(BaseModel):
    id: str
    latitude: float
    longitude: float
    speed: float
    fuel_level: float
    engine_status: str
    running_time: int
    miles_accumulated: float
    timestamp: datetime

class TruckUpdate(BaseModel):
    type: Literal["trucks_update"]
    data: List[TruckData]

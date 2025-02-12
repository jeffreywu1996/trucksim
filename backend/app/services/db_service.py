from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from typing import List
from app.models.database import TruckHistory
from app.models import TruckData

class DatabaseService:
    def store_truck_history(self, db: Session, truck_data: TruckData) -> None:
        """Store truck data in the persistent database"""
        history = TruckHistory(
            id=truck_data.id,
            timestamp=truck_data.timestamp,
            latitude=truck_data.latitude,
            longitude=truck_data.longitude,
            speed=truck_data.speed,
            fuel_level=truck_data.fuel_level,
            engine_status=truck_data.engine_status,
            running_time=truck_data.running_time,
            miles_accumulated=truck_data.miles_accumulated
        )
        db.add(history)
        db.commit()

    def get_truck_history(
        self,
        db: Session,
        truck_id: str,
        start_time: datetime,
        end_time: datetime
    ) -> List[TruckHistory]:
        """Get historical data for a specific truck within a time range"""
        return db.query(TruckHistory)\
            .filter(
                TruckHistory.id == truck_id,
                TruckHistory.timestamp.between(start_time, end_time)
            )\
            .order_by(TruckHistory.timestamp.desc())\
            .all()

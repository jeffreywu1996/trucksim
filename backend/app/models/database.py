from sqlalchemy import create_engine, Column, Float, String, DateTime, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/truckdb")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class TruckHistory(Base):
    __tablename__ = "truck_history"

    id = Column(Text, primary_key=True)
    timestamp = Column(DateTime(timezone=True), primary_key=True)
    latitude = Column(Float)
    longitude = Column(Float)
    speed = Column(Float)
    fuel_level = Column(Float)
    engine_status = Column(Text)
    running_time = Column(Integer)
    miles_accumulated = Column(Float)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

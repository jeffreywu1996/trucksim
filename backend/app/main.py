from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from typing import List, Set
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models import TruckUpdate, TruckData
from app.services.redis_service import RedisService
from app.models.database import get_db
from app.services.db_service import DatabaseService
import uvicorn
from .db import init_db

app = FastAPI(title="Truck Fleet Monitor")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Redis service
redis_service = RedisService(os.getenv("REDIS_URL", "redis://localhost:6379"))

# Initialize PostgreSQL service
db_service = DatabaseService()

# A simple connection manager to handle multiple WebSocket connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print("New client connected. Total:", len(self.active_connections))

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print("Client disconnected. Total:", len(self.active_connections))

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                print("Failed to send message:", e)

manager = ConnectionManager()

@app.on_event("startup")
async def startup_event():
    init_db()
    # ... rest of your startup code ...

@app.get("/")
async def root():
    return {"status": "ok"}

@app.get("/api/trucks", response_model=List[TruckData])
async def get_all_trucks():
    """Get all active trucks"""
    return redis_service.get_all_trucks()

@app.get("/api/trucks/{truck_id}", response_model=TruckData)
async def get_truck(truck_id: str):
    """Get specific truck data"""
    truck = redis_service.get_truck_data(truck_id)
    if truck is None:
        raise HTTPException(status_code=404, detail="Truck not found")
    return truck

@app.get("/api/trucks/{truck_id}/history")
async def get_truck_history(
    truck_id: str,
    hours: int = 1,
    db: Session = Depends(get_db)
):
    """Get historical data for a specific truck"""
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours)
    return db_service.get_truck_history(db, truck_id, start_time, end_time)

# WebSocket endpoint for both simulator and UI clients
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print("Received data:", data)  # For debugging purposes
            # Broadcast the received update to all connected clients
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("WebSocket client disconnected")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

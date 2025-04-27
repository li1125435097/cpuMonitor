# app/api/api_v1/endpoints/monitoring.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
import asyncio
from app.services.system_metrics import SystemMetrics

router = APIRouter()
active_connections: List[WebSocket] = []
system_metrics = SystemMetrics()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            metrics = system_metrics.get_all_metrics()
            await websocket.send_json(metrics)
            await asyncio.sleep(1)  # Send updates every second
    except WebSocketDisconnect:
        active_connections.remove(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        if websocket in active_connections:
            active_connections.remove(websocket)

@router.get("/health")
async def health_check():
    """
    Health check endpoint for the monitoring service
    """
    return {"status": "healthy"}
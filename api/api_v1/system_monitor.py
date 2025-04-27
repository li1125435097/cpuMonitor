# app/api/api_v1/system_monitor.py
from fastapi import APIRouter, WebSocket
from typing import List
import json
import asyncio
from app.services.system_metrics import SystemMetrics

router = APIRouter()
active_connections: List[WebSocket] = []
system_metrics = SystemMetrics()

@router.websocket("/ws/metrics")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            metrics = system_metrics.get_all_metrics()
            await websocket.send_json(metrics)
            await asyncio.sleep(1)  # Send updates every second
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        active_connections.remove(websocket)
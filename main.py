from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import psutil
import asyncio
import json
from datetime import datetime

app = FastAPI()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def get_system_stats():
    # CPU信息
    cpu_percent = psutil.cpu_percent(interval=1)
    
    # 内存信息
    memory = psutil.virtual_memory()
    memory_percent = memory.percent
    
    # 网络信息
    net = psutil.net_io_counters()
    bytes_sent = net.bytes_sent
    bytes_recv = net.bytes_recv
    
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cpu": {
            "percent": cpu_percent,
        },
        "memory": {
            "percent": memory_percent,
            "total": memory.total,
            "used": memory.used
        },
        "network": {
            "bytes_sent": bytes_sent,
            "bytes_recv": bytes_recv
        }
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            stats = await get_system_stats()
            await websocket.send_text(json.dumps(stats))
            await asyncio.sleep(2)
    except Exception:
        await websocket.close()

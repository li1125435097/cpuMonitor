# app/api/api_v1/api.py
from fastapi import APIRouter
from app.api.api_v1.endpoints import monitoring

api_router = APIRouter()
api_router.include_router(monitoring.router, prefix="/monitoring", tags=["monitoring"])
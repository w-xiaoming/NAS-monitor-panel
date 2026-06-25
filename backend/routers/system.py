"""System information routes"""
from fastapi import APIRouter
from services.collector import SystemCollector

router = APIRouter()
collector = SystemCollector()


@router.get("/system/info")
async def get_system_info():
    return collector.get_system_info()


@router.get("/system/uptime")
async def get_uptime():
    import psutil
    return {"uptime": psutil.boot_time()}

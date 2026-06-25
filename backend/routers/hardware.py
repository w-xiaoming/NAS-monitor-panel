"""Hardware status routes"""
from fastapi import APIRouter
from services.collector import HardwareCollector

router = APIRouter()
collector = HardwareCollector()


@router.get("/hardware/cpu")
async def get_cpu_info():
    return collector.get_cpu_info()


@router.get("/hardware/memory")
async def get_memory_info():
    return collector.get_memory_info()


@router.get("/hardware/temperature")
async def get_temperature():
    return collector.get_temperature()

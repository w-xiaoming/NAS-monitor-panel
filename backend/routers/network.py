"""Network status routes"""
from fastapi import APIRouter
from services.collector import NetworkCollector

router = APIRouter()
collector = NetworkCollector()


@router.get("/network/interfaces")
async def get_interfaces():
    return collector.get_interfaces()


@router.get("/network/io")
async def get_io_counters():
    return collector.get_io_counters()

"""Storage routes"""
from fastapi import APIRouter
from services.collector import StorageCollector

router = APIRouter()
collector = StorageCollector()


@router.get("/storage/partitions")
async def get_partitions():
    return collector.get_partitions()


@router.get("/storage/io")
async def get_io_counters():
    return collector.get_io_counters()

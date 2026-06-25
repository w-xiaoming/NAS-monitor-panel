"""Process routes"""
from fastapi import APIRouter, Query
from services.collector import ProcessCollector

router = APIRouter()
collector = ProcessCollector()


@router.get("/process/list")
async def get_processes(limit: int = Query(default=50, le=200)):
    return collector.get_processes(limit=limit)


@router.get("/process/connections")
async def get_connections():
    return collector.get_connections()

"""NAS Monitor Panel - FastAPI Backend"""
import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse

sys.path.insert(0, os.path.dirname(__file__))
from config import settings

_BASE = os.path.dirname(os.path.dirname(__file__))
_FRONTEND_DIST = os.path.join(_BASE, "frontend", "dist")
_INDEX_HTML = os.path.join(_FRONTEND_DIST, "index.html")

app = FastAPI(title=settings.title, version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

from routers.system import router as system_router
from routers.hardware import router as hardware_router
from routers.network import router as network_router
from routers.process import router as process_router
from routers.storage import router as storage_router

app.include_router(system_router, prefix="/api", tags=["system"])
app.include_router(hardware_router, prefix="/api", tags=["hardware"])
app.include_router(network_router, prefix="/api", tags=["network"])
app.include_router(process_router, prefix="/api", tags=["process"])
app.include_router(storage_router, prefix="/api", tags=["storage"])

if os.path.isfile(_INDEX_HTML):
    @app.get("/")
    async def index():
        return FileResponse(_INDEX_HTML)

if os.path.isdir(os.path.join(_FRONTEND_DIST, "assets")):
    app.mount("/assets", StaticFiles(directory=os.path.join(_FRONTEND_DIST, "assets")), name="assets")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.host, port=settings.port, reload=False)
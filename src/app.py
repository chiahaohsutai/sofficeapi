from contextlib import asynccontextmanager
from os import environ, system

from fastapi import APIRouter, FastAPI

from .conversions.router import router as conversions_router
from .conversions.service import LibreOfficeManager

XMLRPC_PORTS = environ.get("XMLRPC_PORTS", "2000,2001,2002,2003")
SOFFICE_PORTS = environ.get("SOFFICE_PORTS", "3000,3001,3002,3003")
CONVERSION_TIMEOUT = environ.get("CONVERSION_TIMEOUT", "60")


@asynccontextmanager
async def lifespan(_: FastAPI):
    system("pkill -f unoserver.server")
    system("pkill -f soffice")

    xmlrpc_ports = [int(p) for p in XMLRPC_PORTS.split(",") if p.isdigit()]
    soffice_ports = [int(p) for p in SOFFICE_PORTS.split(",") if p.isdigit()]

    if len(xmlrpc_ports) != len(soffice_ports):
        raise ValueError("Mismatched number of XMLRPC and SOFFICE ports")

    manager = LibreOfficeManager(
        xmlrpc_ports=xmlrpc_ports,
        soffice_ports=soffice_ports,
        conversion_timeout=int(CONVERSION_TIMEOUT),
    )
    await manager.start_all()
    yield
    manager.stop_all()


app = FastAPI(
    lifespan=lifespan,
    title="sofficeapi",
    description="API for converting files to PDF",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

api_router = APIRouter(prefix="/api")
app.include_router(conversions_router)

from contextlib import asynccontextmanager
import os
import subprocess

from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI

from conversions.router import router as conversions_router

load_dotenv()

PORTS = os.environ.get("SOFFICE_PORTS")
UNO_PORTS = os.environ.get("SOFFICE_UNO_PORTS")
SOFFICE_PYTHOPATH = os.environ.get("SOFFICE_PYTHONPATH")

assert PORTS, "SOFFICE_PORTS not set in .env file"
assert UNO_PORTS, "SOFFICE_UNO_PORTS not set in .env file"
assert SOFFICE_PYTHOPATH, "SOFFICE_PYTHONPATH not set in .env file"

processes: list[subprocess.Popen[bytes]] = []

PORTS = PORTS.split(",")
UNO_PORTS = UNO_PORTS.split(",")


@asynccontextmanager
async def lifespan(app: FastAPI):
    os.system("pkill -f unoserver.server")
    os.system("pkill -f soffice")

    for port, uno_port in zip(PORTS, UNO_PORTS):
        process = subprocess.Popen(
            [
                SOFFICE_PYTHOPATH,
                "-m",
                "unoserver.server",
                "--port",
                port,
                "--uno-port",
                uno_port,
                "--quiet",
            ]
        )
        processes.append(process)

    yield

    for process in processes:
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()


app = FastAPI(
    lifespan=lifespan,
    title="sofficeapi",
    description="A simple API for converting documents using LibreOffice",
    version="0.1.0",
)
api_router = APIRouter(prefix="/api")

app.include_router(conversions_router)

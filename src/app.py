from fastapi import FastAPI, APIRouter
from conversions.router import router as conversions_router

app = FastAPI(
    title="sofficeapi",
    description="A simple API for converting documents using LibreOffice",
    version="0.1.0",
)
api_router = APIRouter(prefix="/api")

app.include_router(conversions_router)

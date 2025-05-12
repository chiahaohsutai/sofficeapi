import json
from base64 import b64decode, b64encode
from logging import getLogger
from pathlib import Path

from fastapi import APIRouter, Response

from .schemas import Base64File
from .service import convert_file

router = APIRouter(prefix="/conversions", tags=["conversions"])
logger = getLogger("sofficeapi")


@router.post("/pdf")
def convert_to_pdf(file: Base64File):
    try:
        pdf = convert_file(b64decode(file.content), "pdf")
        new_filename = Path(file.filename).with_suffix(".pdf").name
        new_file = b64encode(pdf).decode("utf-8")
        return Response(
            content=json.dumps(
                {
                    "filename": new_filename,
                    "content": new_file,
                }
            ),
            status_code=200,
            media_type="application/json",
        )
    except Exception as e:
        logger.error(f"Error converting file: {e}")
        return Response(
            content=json.dumps({"error": str(e)}),
            status_code=500,
            media_type="application/json",
        )

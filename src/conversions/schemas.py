from pydantic import BaseModel, Field


class Base64File(BaseModel):
    filename: str = Field(..., description="The name of the file.")
    content: str = Field(..., description="The base64-encoded file.")

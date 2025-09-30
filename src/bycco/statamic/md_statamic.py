from pydantic import BaseModel
from typing import Any


class ReadRequest(BaseModel):
    name: str
    binary: bool | None = False


class WriteRequest(BaseModel):
    name: str
    content: Any
    binary: bool | None = False

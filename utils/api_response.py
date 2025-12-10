from typing import Any
from pydantic import BaseModel


class ApiResponse(BaseModel):
    status: str
    data: Any
    http_code: int

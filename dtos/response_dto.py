from typing import Optional, List

from pydantic import BaseModel


class ResponseDto(BaseModel):
    company_name: str
    tags: List[str]

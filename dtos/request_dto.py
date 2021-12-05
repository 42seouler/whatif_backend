from typing import List

from pydantic import BaseModel


class RequestDto(BaseModel):
    company_name: dict
    tags: List[dict]

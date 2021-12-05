from typing import List

from pydantic import BaseModel


class SearchResponseDto(BaseModel):
    companies: List[dict]

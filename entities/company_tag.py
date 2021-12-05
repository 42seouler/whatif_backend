from typing import Optional

from sqlmodel import Field, SQLModel


class CompanyTag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tag_id: Optional[int] = Field(default=None, foreign_key="tag.id")
    company_id: Optional[int] = Field(default=None, foreign_key="company.id")
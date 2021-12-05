from typing import Optional

from sqlmodel import Field, SQLModel


class CompanyTranslation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    company_id: Optional[int] = Field(default=None, foreign_key="company.id")
    locales_id: Optional[int] = Field(default=None, foreign_key="locales.id")
    name: str

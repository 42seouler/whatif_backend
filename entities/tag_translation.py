from typing import Optional

from sqlmodel import Field, SQLModel


class TagTranslation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tag_id: Optional[int] = Field(default=None, foreign_key="tag.id")
    locales_id: Optional[int] = Field(default=None, foreign_key="locales.id")
    name: str

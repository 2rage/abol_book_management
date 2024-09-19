from pydantic import BaseModel
from datetime import date


class BookCreate(BaseModel):
    title: str
    author: str
    publication_date: date


class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    publication_date: date | None = None


class BookOut(BaseModel):
    id: int
    title: str
    author: str
    publication_date: date

    class Config:
        orm_mode = True

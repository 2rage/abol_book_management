from pydantic import BaseModel, EmailStr
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


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None

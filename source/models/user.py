from pydantic import BaseModel, EmailStr
from sqlmodel import Field, SQLModel


class UserMainSchema(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: EmailStr
    first_name: str
    last_name: str
    avatar: str


class ListUserMainPaginationSchema(BaseModel):
    items: list[UserMainSchema]
    total: int
    page: int
    size: int
    pages: int

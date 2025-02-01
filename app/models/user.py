from pydantic import BaseModel, EmailStr, HttpUrl
from sqlmodel import Field, SQLModel


class UserModel(SQLModel, table=True):
    __tablename__ = 'users'
    id: int | None = Field(default=None, primary_key=True)
    email: EmailStr
    first_name: str
    last_name: str
    avatar: str


class UserCreateModel(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    avatar: HttpUrl


class UserUpdateModel(BaseModel):
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None
    avatar: str | None = None


class ListUserPaginationModel(BaseModel):
    items: list[UserModel]
    total: int
    page: int
    size: int
    pages: int

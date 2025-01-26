from pydantic import BaseModel, EmailStr, HttpUrl


class UserMainSchema(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    avatar: HttpUrl


class ListUserMainPaginationSchema(BaseModel):
    items: list[UserMainSchema]
    total: int
    page: int
    size: int
    pages: int

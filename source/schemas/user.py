from pydantic import BaseModel


class UserMainSchema(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    avatar: str


class UserSupportSchema(BaseModel):
    url: str
    text: str


class UserResponseSchemaGet(BaseModel):
    data: UserMainSchema
    support: UserSupportSchema

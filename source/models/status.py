from pydantic import BaseModel


class StatusSchema(BaseModel):
    database: bool


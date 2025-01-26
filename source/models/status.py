from pydantic import BaseModel


class StatusSchema(BaseModel):
    message: str = 'serving'

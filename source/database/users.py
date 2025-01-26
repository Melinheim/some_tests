from typing import Iterable
from sqlmodel import Session, select
from database._engine import engine
from models.user import UserMainSchema


def get_user(user_id: int) -> UserMainSchema | None:
    with Session(engine) as session:
        return session.get(UserMainSchema, user_id)


def get_users() -> Iterable[UserMainSchema] | None:
    with Session(engine) as session:
        return session.exec(select(UserMainSchema)).all()

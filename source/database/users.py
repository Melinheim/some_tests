import logging
from typing import Iterable, Type

from fastapi import HTTPException
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate
from sqlalchemy.orm.exc import UnmappedInstanceError
from sqlmodel import Session, select

from database._engine import engine
from models.user import UserModel


def get_user(user_id: int) -> UserModel | None:
    """Получить пользователя по id"""
    with Session(engine) as session:
        return session.get(UserModel, user_id)


def get_users() -> Iterable[UserModel]:
    """Получить всех пользователей"""
    with Session(engine) as session:
        return session.exec(select(UserModel)).all()


def get_users_paginated() -> Page[UserModel]:
    """Получить всех пользователей постранично"""
    with Session(engine) as session:
        return paginate(session, select(UserModel))


def create_user(user: UserModel) -> UserModel:
    """Создать пользователя"""
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


def update_user(user_id: int, user: UserModel) -> Type[UserModel]:
    """Изменить пользователя"""
    with Session(engine) as session:
        db_user = session.get(UserModel, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail='User not found')
        user_data = user.model_dump(exclude_unset=True)
        db_user.sqlmodel_update(user_data)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user


def delete_user(user_id: int):
    """Удалить пользователя"""
    with Session(engine) as session:
        user = session.get(UserModel, user_id)
        try:
            session.delete(user)
            session.commit()
        except UnmappedInstanceError:
            logging.info('On user %s deletion', user_id)

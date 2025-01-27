import logging
import os

from sqlalchemy.orm import Session
from sqlmodel import SQLModel, create_engine, text


engine = create_engine(
    url=os.getenv('DATABASE_ENGINE'),
    pool_size=int(os.getenv('DATABASE_POOL_SIZE', 10))
)


def db_init():
    """Инициализация БД"""
    SQLModel.metadata.create_all(engine)


def check_availability() -> bool:
    """Проверка доступности БД"""
    try:
        with Session(engine) as session:
            session.execute(text('SELECT 1'))
        return True
    except Exception as e:
        print(e)
        return False

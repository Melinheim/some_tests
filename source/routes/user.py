from http import HTTPStatus

from fastapi import APIRouter, HTTPException, status
from fastapi_pagination import Page

from database import users
from database.users import get_user as get_user_db
from database.users import get_users_paginated
from models.user import UserCreateModel, UserModel, UserUpdateModel

router = APIRouter(prefix='/api/users', tags=['Users API'])


@router.get('/{user_id}', status_code=HTTPStatus.OK)
def get_user_by_id(user_id: int) -> UserModel:
    """Получить пользователя по user_id"""
    if user_id < 1:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='Invalid user id')
    user = get_user_db(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return user


@router.get('', status_code=HTTPStatus.OK)
def get_users() -> Page[UserModel]:
    """Получить всех пользователей"""
    return get_users_paginated()


@router.post('', status_code=HTTPStatus.CREATED)
def create_user(user: UserModel) -> UserModel:
    """Создать пользователя"""
    UserCreateModel.model_validate(user.model_dump())
    return users.create_user(user)


@router.patch('/{user_id}', status_code=HTTPStatus.OK)
def update_user(user_id: int, user: UserModel) -> UserModel:
    """Изменить пользователя"""
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail='Invalid user id')
    UserUpdateModel.model_validate(user.model_dump())
    return users.update_user(user_id, user)


@router.delete('/{user_id}', status_code=HTTPStatus.OK)
def delete_user(user_id: int):
    """Удалить пользователя"""
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail='Invalid user id')
    users.delete_user(user_id)
    return {'message': 'User deleted'}

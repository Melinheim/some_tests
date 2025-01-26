from fastapi import APIRouter, HTTPException, status
from fastapi_pagination import Page, paginate
from mimesis import Locale, Person

from schemas.user import UserMainSchema

router = APIRouter(prefix='/api/users', tags=['Users API'])

person = Person(Locale.EN)

users: list[UserMainSchema] = [
    UserMainSchema(
        id=i,
        email=person.email(),
        first_name=person.name(),
        last_name=person.surname(),
        avatar=f'https://reqres.in/img/faces/{i}-image.jpg'
    ) for i in range(1, 116)
]


@router.get('/{user_id}')
def get_user_by_id(user_id: int) -> UserMainSchema:
    """Получить пользователя по user_id"""
    if user_id < 1:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='Invalid user id')
    try:
        return users[user_id - 1]
    except IndexError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found') from exc


@router.get('')
def get_users() -> Page[UserMainSchema]:
    """Получить всех пользователей"""
    return paginate(users)

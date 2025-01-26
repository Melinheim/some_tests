from fastapi import APIRouter, HTTPException, status
from fastapi_pagination import Page, paginate
from mimesis import Locale, Person

from models.user import UserMainSchema
from database.users import get_user as get_user_db
from database.users import get_users as get_users_db

router = APIRouter(prefix='/api/users', tags=['Users API'])

# person = Person(Locale.EN)

# users: list[UserMainSchema] = [
#     UserMainSchema(
#         id=i,
#         email=person.email(),
#         first_name=person.name(),
#         last_name=person.surname(),
#         avatar=f'https://reqres.in/img/faces/{i}-image.jpg'
#     ) for i in range(1, 116)
# ]


@router.get('/{user_id}')
def get_user_by_id(user_id: int) -> UserMainSchema:
    """Получить пользователя по user_id"""
    if user_id < 1:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='Invalid user id')
    user = get_user_db(user_id)
    if not user: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return user


@router.get('')
def get_users() -> Page[UserMainSchema]:
    return paginate(get_users_db())

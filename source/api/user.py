from fastapi import APIRouter, HTTPException

from schemas.user import UserResponseSchemaGet

router = APIRouter(prefix='/api/users', tags=['Users API'])

users = {
    2: {
        'id': 2,
        'email': 'janet.weaver@reqres.in',
        'first_name': 'Janet',
        'last_name': 'Weaver',
        'avatar': 'https://reqres.in/img/faces/2-image.jpg',
    }
}

support_info = {
    'url': 'https://contentcaddy.io?utm_source=reqres&utm_medium=json&utm_campaign=referral',
    'text': 'Tired of writing endless social media content? Let Content Caddy generate it.',
}


@router.get('/{user_id}', response_model=UserResponseSchemaGet)
def get_user_by_id(user_id: int):
    """Получить пользователя по user_id"""
    user = users.get(user_id)
    if not user:
        raise HTTPException(status_code=404)
    return {
        'data': user,
        'support': support_info,
    }

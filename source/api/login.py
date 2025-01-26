from fastapi import APIRouter, HTTPException

from schemas.login import LoginResponseSchema, LoginSchema

router = APIRouter(prefix='/api/login', tags=['Login API'])

login_info_db = {
    'eve.holt@reqres.i': 'cityslicka'
}


@router.post('', response_model=LoginResponseSchema | dict)
def post_login(login_data: LoginSchema):
    """Получить пользователя по id"""
    try:
        if login_data.password == login_info_db[login_data.email]:
            return LoginResponseSchema(token='QpwL5tke4Pnpja7X4')
        raise HTTPException(status_code=401)
    except KeyError as exc:
        raise HTTPException(status_code=404) from exc

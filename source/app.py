from fastapi import FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi_pagination import add_pagination
from dotenv import load_dotenv

load_dotenv()

from database._engine import db_init
from routes.login import router as router_login
from routes.user import router as router_user
from routes.status import router as router_status

app = FastAPI()


@app.exception_handler(HTTPException)
def http_exception_handler(request, exc: HTTPException):
    response_content = {
        'message': exc.detail,
    }
    if exc.status_code == status.HTTP_404_NOT_FOUND:
        response_content = {}
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(response_content),
    )


@app.exception_handler(RequestValidationError)
def request_validation_exception_handler(request, exc: RequestValidationError):
    errors = [
        f'{".".join(str(l) for l in i["loc"])}: {i["msg"]}'
        for i in exc.errors()
    ]
    error = ' '.join(errors)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({'error': error})
    )


app.include_router(router_status)
app.include_router(router_user)
app.include_router(router_login)

add_pagination(app)


if __name__ == '__main__':
    db_init()
    import uvicorn
    uvicorn.run(app)

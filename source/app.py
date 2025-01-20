from fastapi import FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from inflection import humanize

from api.login import router as router_login
from api.user import router as router_user

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
def http_exception_handler(request, exc: RequestValidationError):
    errors = [
        humanize(f'{i["type"]} {l}.')
        for i in exc.errors()
        for l in i['loc']
        if l != 'body'
    ]
    error = ' '.join(errors)
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({'error': error})
    )


app.include_router(router_user)
app.include_router(router_login)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)

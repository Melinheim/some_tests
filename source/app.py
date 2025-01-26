from fastapi import FastAPI
from fastapi_pagination import add_pagination

from api.login import router as router_login
from api.status import router as router_status
from api.user import router as router_user

app = FastAPI()


app.include_router(router_status)
app.include_router(router_user)
app.include_router(router_login)

add_pagination(app)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)

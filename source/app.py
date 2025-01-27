# pylint: disable=wrong-import-position
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi_pagination import add_pagination

load_dotenv()

from database._engine import db_init
from routes.login import router as router_login
from routes.status import router as router_status
from routes.user import router as router_user

app = FastAPI()


app.include_router(router_status)
app.include_router(router_user)
app.include_router(router_login)

add_pagination(app)


if __name__ == '__main__':
    db_init()
    import uvicorn
    uvicorn.run(app)

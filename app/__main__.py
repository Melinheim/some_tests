# pylint: disable=wrong-import-position
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi_pagination import add_pagination

load_dotenv()

from app.database._engine import db_init
from app.routes.login import router as router_login
from app.routes.status import router as router_status
from app.routes.user import router as router_user


@asynccontextmanager
async def lifespan(_: FastAPI):
    db_init()
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(router_status)
app.include_router(router_user)
app.include_router(router_login)

add_pagination(app)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)

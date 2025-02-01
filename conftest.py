from fastapi.testclient import TestClient
from pytest import fixture

from app.__main__ import app

pytest_plugins = [
    'tests.fixtures'
]


@fixture(scope='session')
def client():
    """Тестовый клиент"""
    yield TestClient(app)

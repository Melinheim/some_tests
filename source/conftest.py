from fastapi.testclient import TestClient
from pytest import fixture

from app import app

pytest_plugins = [
    'tests.fixtures'
]


@fixture(scope='session')
def client():
    """Тестовый клиент"""
    yield TestClient(app)

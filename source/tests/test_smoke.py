from http import HTTPStatus
from fastapi import Response
from fastapi.testclient import TestClient
from pytest import mark
from api.user import users
from schemas.status import StatusSchema
from schemas.user import UserMainSchema


def test_smoke(client: TestClient):
    """Доступсноть сервиса"""

    response = client.get(url='/status')

    status_code_expected = HTTPStatus.OK
    assert response.status_code == status_code_expected, (
        f'Expected status code {status_code_expected}, but got {response.status_code}')
    StatusSchema.model_validate(response.json())

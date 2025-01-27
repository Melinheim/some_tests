from http import HTTPStatus

from fastapi.testclient import TestClient

from models.status import StatusSchema


def test_smoke(client: TestClient):
    """Доступсноть сервиса"""

    response = client.get(url='/status')

    assert response.status_code == HTTPStatus.OK
    StatusSchema.model_validate(response.json())

from http import HTTPStatus
from fastapi.testclient import TestClient
from models.status import StatusSchema


def test_smoke(client: TestClient):
    """Доступсноть сервиса"""

    response = client.get(url='/status')

    status_code_expected = HTTPStatus.OK
    assert response.status_code == status_code_expected, (
        f'Expected status code {status_code_expected}, but got {response.status_code}')
    StatusSchema.model_validate(response.json())

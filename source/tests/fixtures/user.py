from http import HTTPStatus

from fastapi import Response
from fastapi.testclient import TestClient
from pytest import fixture


@fixture
def get_all_users(client: TestClient):
    response: Response = client.get(url=f'/api/users')
    assert response.status_code == HTTPStatus.OK
    return response.json()

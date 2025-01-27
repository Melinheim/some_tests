from http import HTTPStatus

from fastapi import Response
from fastapi.testclient import TestClient
from pytest import fixture


@fixture
def get_all_users(client: TestClient):
    """Получить всех пользователей"""
    all_users = []
    params = {'page': 1, 'pageSize': 100}

    def _get_users_and_extend():
        response: Response = client.get(url='/api/users', params=params)
        assert response.status_code == HTTPStatus.OK
        all_users.extend(response.json().get('items', []))
        return response

    response = _get_users_and_extend()

    for i in range(2, response.json().get('pages') + 1):
        params['page'] = i
        _get_users_and_extend()

    return all_users

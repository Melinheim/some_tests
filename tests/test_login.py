from http import HTTPStatus

from fastapi import Response
from fastapi.testclient import TestClient
from pytest import mark


class TestLogin:
    """Запросы логина /api/login"""
    def test_login_successful(self, client: TestClient, any_user_credentials):
        """Успешный запрос логина пользователя
        
        1. Запросить логин пользователя по действующей паре email и password.
        2. Проверить: ответ содержит token не нулевой длины.
        """

        response: Response = client.post(
            url='/api/login',
            json=any_user_credentials
        )

        assert response.status_code == HTTPStatus.OK
        body = response.json()
        assert 'token' in body, 'Response body does not contain "token" key'
        assert len(body['token']) > 0, 'Token is too short'

    @mark.parametrize(
        'missing',
        [
            'email',
            'password'
        ]
    )
    def test_login_bad_request(self, client: TestClient, any_user_credentials, missing):
        """Успешный запрос логина пользователя
        
        1. Запросить логин пользователя по действующей паре email и password.
        2. Проверить: ответ содержит информацию об ошибке.
        """
        credentials = {k: v for k, v in any_user_credentials.items() if k != missing}

        response: Response = client.post(
            url='/api/login',
            json=credentials
        )

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

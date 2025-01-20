from fastapi import Response
from fastapi.testclient import TestClient
from pytest import mark


@mark.parametrize('user_id, expected_email', [
    (2, 'janet.weaver@reqres.in'),
])
def test_user_data(client: TestClient, user_id, expected_email):
    """Успешный запрос пользователя по id
    
    1. Запросить пользователя по id.
    2. Проверить: ответ содержит искомые id и email в разделе data.
    """

    response: Response = client.get(
        url=f'/api/users/{user_id}'
    )

    assert response.status_code == 200, f'Expected status code 200, but got {response.status_code}'

    body = response.json()
    assert 'data' in body, 'Response body does not contain "data" key'

    data = body['data']

    assert data['id'] == user_id, f'Expected id {user_id}, but got {data["id"]}'
    assert data['email'] == expected_email, f'Expected email {expected_email}, but got {data["email"]}'

from http import HTTPStatus
from fastapi import Response
from fastapi.testclient import TestClient
from pytest import mark
from routes.user import users
from models.user import UserMainSchema


class TestUser:
    """Запросы пользователя /api/users/{user_id}"""
    @mark.parametrize('user_id, expected_email', [
        (1, users[1 - 1].email),
        (20, users[20 - 1].email),
        (51, users[51 - 1].email),
    ])
    def test_user(self, client: TestClient, user_id, expected_email):
        """Успешный запрос пользователя по id
        
        1. Запросить пользователя по id.
        2. Проверить: ответ содержит искомые id и email в разделе data.
        """

        response: Response = client.get(
            url=f'/api/users/{user_id}'
        )

        assert response.status_code == HTTPStatus.OK, (
            f'Expected status code 200, but got {response.status_code}')
        response_json = response.json()
        UserMainSchema.model_validate(response_json)
        assert response_json['id'] == user_id, (
            f'Expected id {user_id}, but got {response_json["id"]}')
        assert response_json['email'] == expected_email, (
            f'Expected email {expected_email}, but got {response_json["email"]}')

    def test_user_not_found(self, client: TestClient):
        """Запросы пользователя с несуществующими значениями возвращают статус NOT_FOUND
        
        1. Запросить пользователя по несуществующему id.
        2. Проверить: код ответа соответствует ожидаемому
        """

        response: Response = client.get(
            url=f'/api/users/{len(users) + 1}'
        )

        status_code_expected = HTTPStatus.NOT_FOUND
        assert response.status_code == status_code_expected, (
            f'Expected status code {status_code_expected}, but got {response.status_code}')

    @mark.parametrize('user_id', [-1, 0, 'aaa'])
    def test_user_unprocessable_entity(self, client: TestClient, user_id):
        """Запросы пользователя с невалидными значениями возвращают статус UNPROCESSABLE_ENTITY
        
        1. Запросить пользователя по невалидному id.
        2. Проверить: код ответа соответствует ожидаемому
        """

        response: Response = client.get(
            url=f'/api/users/{user_id}'
        )

        status_code_expected = HTTPStatus.UNPROCESSABLE_ENTITY
        assert response.status_code == status_code_expected, (
            f'Expected status code {status_code_expected}, but got {response.status_code}')


class TestUsers:
    """Запросы списка пользователкй /api/users"""
    max_pagination_count = 100
    default_pagination_count = 50

    def test_users(client: TestClient, get_all_users):
        """Успешный запрос всех пользователей
        
        1. Запросить вскх пользователей.
        2. Проверить: ответ содержит список с валидными моделями UserMainSchema.
        """
        for user in get_all_users['items']:
            UserMainSchema.model_validate(user)

    def test_users_no_duplicates(client: TestClient, get_all_users):
        """Запрос всех пользователей не возвращает повторяющиеся id
        
        1. Запросить всех пользователей.
        2. Проверить: в ответе только уникальные id.
        """
        users_ids = [user['id'] for user in get_all_users['items']]
        assert len(users_ids) == len(set(users_ids))

    @mark.parametrize(
        'page_size_request',
        [
            default_pagination_count,
            1,
            15,
            max_pagination_count
        ]
    )
    def test_users_pagination(self, client: TestClient, page_size_request):
        """Пагинация возвращает возвращает запрошенное количество элементов
        и рассчитывает количество страниц
        
        1. Запросить всех пользователей с параметрами пагинации.
        2. Проверить: в ответе запрошенное количество элементов.
        3. Проверить: в ответе правильно рассчитано количество страниц пагинации.
        """
        users_len = len(users)
        pages_count = (
            users_len // page_size_request + 1
            if users_len % page_size_request
            else users_len // page_size_request
        )

        response: Response = client.get(
            url=f'/api/users',
            params={'size': page_size_request}
        )

        status_code_expected = HTTPStatus.OK
        assert response.status_code == status_code_expected, (
            f'Expected status code {status_code_expected}, but got {response.status_code}')
        response_items_len = len(response.json().get('items', []))
        assert response_items_len == page_size_request, (
            f'Expected {page_size_request} items, but got {response_items_len}')
        pages = response.json().get('pages')
        assert pages == pages_count, f'Expected {pages_count} pages count, but got {pages}'

    def test_users_pagination_no_duplicate(self, client: TestClient):
        """Страницы возвращают уникальные элементы
        
        1. Запросить пользователей постранично.
        2. Проверить: повторяющиеся элементы не встречатся.
        """
        users_len = len(users)
        pages_count = (
            3 if users_len < (self.max_pagination_count * 3)
            else users_len // self.max_pagination_count + 1
        )

        all_ids = []
        for i in range(pages_count):
            response: Response = client.get(
                url=f'/api/users',
                params={'page': i + 1}
            )
            status_code_expected = HTTPStatus.OK
            assert response.status_code == status_code_expected, (
                f'Expected status code {status_code_expected}, but got {response.status_code}')
            all_ids.extend([u['id'] for u in response.json().get('items', [])])
        
        assert len(all_ids) == len(set(all_ids)), 'В пагинации вернулись повторяющиеся элементы'

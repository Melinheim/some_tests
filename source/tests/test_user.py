from http import HTTPStatus

from fastapi import Response
from fastapi.testclient import TestClient
from pytest import mark
from models.user import UserMainSchema


class TestUser:
    """Запросы пользователя /api/users/{user_id}"""
    @mark.parametrize('user_id', [1, 20, 51,])
    def test_user(self, client: TestClient, get_all_users: list, user_id):
        """Успешный запрос пользователя по id
        
        1. Запросить пользователя по id.
        2. Проверить: ответ содержит искомые id и email в разделе data.
        """
        user = get_all_users[user_id - 1]

        response: Response = client.get(
            url=f'/api/users/{user_id}'
        )

        assert response.status_code == HTTPStatus.OK
        response_json = response.json()
        UserMainSchema.model_validate(response_json)
        assert response_json['id'] == user_id
        assert response_json['email'] == user['email']

    def test_user_not_found(self, client: TestClient, get_all_users: list):
        """Запросы пользователя с несуществующими значениями возвращают статус NOT_FOUND
        
        1. Запросить пользователя по несуществующему id.
        2. Проверить: код ответа соответствует ожидаемому
        """

        response: Response = client.get(
            url=f'/api/users/{len(get_all_users) + 1}'
        )

        status_code_expected = HTTPStatus.NOT_FOUND
        assert response.status_code == status_code_expected

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
        assert response.status_code == status_code_expected


class TestUsers:
    """Запросы списка пользователкй /api/users"""
    max_pagination_count = 100
    default_pagination_count = 50

    def test_users(self, client: TestClient):
        """Успешный запрос всех пользователей
        
        1. Запросить вскх пользователей.
        2. Проверить: ответ содержит список с валидными моделями UserMainSchema.
        """
        response: Response = client.get(
            url='/api/users'
        )
        assert response.status_code == HTTPStatus.OK
        ListUserMainPaginationSchema.model_validate(response.json())

    def test_users_no_duplicates(self, client: TestClient):
        """Запрос всех пользователей не возвращает повторяющиеся id
        
        1. Запросить всех пользователей.
        2. Проверить: в ответе только уникальные id.
        """
        response: Response = client.get(
            url='/api/users'
        )
        assert response.status_code == HTTPStatus.OK
        users_ids = [user['id'] for user in response.json()['items']]
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
    def test_users_pagination(
        self, client: TestClient, page_size_request: int, get_all_users: list
    ):
        """Пагинация возвращает возвращает запрошенное количество элементов
        и рассчитывает количество страниц
        
        1. Запросить всех пользователей с параметрами пагинации.
        2. Проверить: в ответе запрошенное количество элементов.
        3. Проверить: в ответе правильно рассчитано количество страниц пагинации.
        """
        users_len = len(get_all_users)
        pages_count = users_len // page_size_request + int(bool(users_len % page_size_request))

        response: Response = client.get(
            url='/api/users',
            params={'size': page_size_request}
        )

        status_code_expected = HTTPStatus.OK
        assert response.status_code == status_code_expected
        response_items_len = len(response.json().get('items', []))
        assert response_items_len == page_size_request
        pages = response.json().get('pages')
        assert pages == pages_count

    def test_users_pagination_no_duplicate(self, client: TestClient, get_all_users: list):
        """Страницы возвращают уникальные элементы
        
        1. Запросить пользователей постранично.
        2. Проверить: повторяющиеся элементы не встречатся.
        """
        users_len = len(get_all_users)
        pages_count = (
            users_len // self.default_pagination_count
            + int(bool(users_len % self.default_pagination_count))
        )

        all_ids = []
        for i in range(pages_count):
            response: Response = client.get(
                url='/api/users',
                params={
                    'page': i + 1,
                    'pageSize': self.default_pagination_count
                }
            )

            assert response.status_code == HTTPStatus.OK
            all_ids.extend([u['id'] for u in response.json().get('items', [])])

        assert len(all_ids) == len(set(all_ids)), 'В пагинации вернулись повторяющиеся элементы'

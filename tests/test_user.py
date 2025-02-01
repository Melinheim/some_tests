from http import HTTPStatus

from fastapi import Response
from fastapi.testclient import TestClient
from pytest import mark

from app.models.user import ListUserPaginationModel, UserModel, UserUpdateModel


class TestGetUsersId:
    """Запросы пользователя GET /api/users/{user_id}"""
    @mark.parametrize('user_position', [0, 1, -1])
    def test_get_users_id(self, client: TestClient, fill_users: list[UserModel], user_position):
        """Успешный запрос пользователя по id
        
        1. Запросить пользователя по id.
        2. Проверить: ответ содержит искомые id и email в разделе data.
        """
        user: UserModel = fill_users[user_position]

        response: Response = client.get(
            url=f'/api/users/{user.id}'
        )

        assert response.status_code == HTTPStatus.OK
        response_json = response.json()
        UserModel.model_validate(response_json)
        assert response_json['id'] == user.id
        assert response_json['email'] == user.email

    def test_get_users_id_not_found(self, client: TestClient, fill_users: list[UserModel]):
        """Запросы пользователя с несуществующими значениями возвращают статус NOT_FOUND
        
        1. Запросить пользователя по несуществующему id.
        2. Проверить: код ответа соответствует ожидаемому
        """

        response: Response = client.get(
            url=f'/api/users/{fill_users[-1].id + 1}'
        )

        status_code_expected = HTTPStatus.NOT_FOUND
        assert response.status_code == status_code_expected

    @mark.parametrize('user_id', [-1, 0, 'aaa'])
    def test_get_users_id_unprocessable_entity(self, client: TestClient, user_id):
        """Запросы пользователя с невалидными значениями возвращают статус UNPROCESSABLE_ENTITY
        
        1. Запросить пользователя по невалидному id.
        2. Проверить: код ответа соответствует ожидаемому
        """

        response: Response = client.get(
            url=f'/api/users/{user_id}'
        )

        status_code_expected = HTTPStatus.UNPROCESSABLE_ENTITY
        assert response.status_code == status_code_expected


class TestGetUsers:
    """Запросы списка пользователей GET /api/users"""
    max_pagination_count = 100
    default_pagination_count = 50

    @mark.usefixtures('fill_users')
    def test_get_users(self, client: TestClient):
        """Успешный запрос всех пользователей
        
        1. Запросить вскх пользователей.
        2. Проверить: ответ содержит список с валидными моделями UserModel.
        """
        response: Response = client.get(
            url='/api/users'
        )
        assert response.status_code == HTTPStatus.OK
        ListUserPaginationModel.model_validate(response.json())

    @mark.usefixtures('fill_users')
    def test_get_users_no_duplicates(self, client: TestClient):
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
    def test_get_users_pagination(
        self, client: TestClient, page_size_request: int, fill_users: list[UserModel]
    ):
        """Пагинация возвращает возвращает запрошенное количество элементов
        и рассчитывает количество страниц
        
        1. Запросить всех пользователей с параметрами пагинации.
        2. Проверить: в ответе запрошенное количество элементов.
        3. Проверить: в ответе правильно рассчитано количество страниц пагинации.
        """
        users_len = len(fill_users)
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

    def test_get_users_pagination_no_duplicate(
        self, client: TestClient, fill_users: list[UserModel]
    ):
        """Страницы возвращают уникальные элементы
        
        1. Запросить пользователей постранично.
        2. Проверить: повторяющиеся элементы не встречатся.
        """
        users_len = len(fill_users)
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


class TestPostUsers:
    """Запросы создания пользователей POST /api/users"""
    def test_post_users(self, client: TestClient, user_data_for_create: dict):
        """Успешное создание пользователя
        
        1. Создать пользователя.
        2. Проверить: значения полей в ответе соответствуют значениям полей в запросе.
        """

        response: Response = client.post(
            url='/api/users',
            json=user_data_for_create
        )

        assert response.status_code == HTTPStatus.CREATED
        response_json = response.json()
        client.delete(url=f'/api/users/{response_json['id']}')
        UserModel.model_validate(response_json)
        assert response_json['email'] == user_data_for_create['email']
        assert response_json['first_name'] == user_data_for_create['first_name']
        assert response_json['last_name'] == user_data_for_create['last_name']
        assert response_json['avatar'] == user_data_for_create['avatar']


class TestPatchUsers:
    """Запросы изменения пользователей PATCH /api/users/{user_id}"""
    @mark.parametrize(
        'update_user',
        [
            UserUpdateModel(
                first_name='Updated_first_name',
                last_name='Updated_last_name',
                avatar='http://updated_avatar.com'
            ),
            UserUpdateModel(
                first_name='Updated_first_name',
                last_name='Updated_last_name',
                email='updated_email@email.com'
            ),
            UserUpdateModel(
                last_name='Updated_last_name',
                email='updated_email@email.com',
                avatar='http://updated_avatar.com'
            ),
            UserUpdateModel(
                first_name='Updated_first_name',
                email='updated_email@email.com',
                avatar='http://updated_avatar.com'
            ),
        ]
    )
    def test_patch_users(
        self, client: TestClient, create_user: UserModel, update_user: UserUpdateModel
    ):
        """Успешное изменение пользователя
        
        1. Изменить поля пользователя.
        2. Проверить: значения полей в ответе соответствуют значениям полей в запросе.
        3. Проверить: значения полей, отсутствующих в запросе, остались неизменными.
        """
        body_json = update_user.model_dump(exclude_unset=True)

        response: Response = client.patch(
            url=f'/api/users/{create_user.id}',
            json=body_json
        )

        assert response.status_code == HTTPStatus.OK
        response_json = response.json()
        UserModel.model_validate(response_json)
        for k in body_json.keys():
            assert response_json[k] == getattr(update_user, k), (
                f'Значение поля {k} должно быть изменено')
        for k in (i for i in create_user.model_dump().keys() if i not in body_json.keys()):
            assert response_json[k] == getattr(create_user, k), (
                f'Значение поля {k} не должно быть изменено')


class TestDeleteUsers:
    """Запросы удаления пользователей DELETE /api/users/{user_id}"""
    def test_delete_users(self, client: TestClient, create_user: UserModel):
        """Успешное удаление пользователя
        
        1. Удалть пользователя.
        2. Проверить: в ответе сообщение об успешно удалении пользователя.
        """

        response: Response = client.delete(url=f'/api/users/{create_user.id}')

        assert response.status_code == HTTPStatus.OK
        assert response.json().get('message') == 'User deleted'

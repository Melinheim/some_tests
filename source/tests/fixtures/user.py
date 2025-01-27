from ast import literal_eval
from http import HTTPStatus
from random import randint
from typing import Generator

from fastapi import Response
from fastapi.testclient import TestClient
from mimesis import Locale, Person
from pytest import fixture

from models.user import UserCreateModel, UserModel


def generate_user() -> UserCreateModel:
    """Сгенерировать заполненную модель позльзователя"""
    person = Person(Locale.EN)
    return UserCreateModel(
        email=person.email(),
        first_name=person.name(),
        last_name=person.surname(),
        avatar=f'https://reqres.in/img/faces/{randint}-image.jpg'
    )


def create_user_by_model(client: TestClient, user: UserModel) -> UserModel:
    """Создать пользователя по модели"""
    response = client.post(
        url='/api/users',
        json=literal_eval(user.model_dump_json())
    )
    return UserModel(**response.json())


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


@fixture
def user_data_for_create() -> dict:
    """Данные для создания пользователя"""
    return literal_eval(generate_user().model_dump_json())


@fixture(scope='module', params=[150])
def fill_users(client: TestClient, request) -> Generator[None, list[UserModel], None]:
    """Заполение БД пользователями"""
    users_to_create = [generate_user() for _ in range(request.param)]
    api_users: list[UserModel] = []
    for user in users_to_create:
        api_users.append(create_user_by_model(client=client, user=user))

    yield api_users

    for user in api_users:
        client.delete(url=f'/api/users/{user.id}')


@fixture
def create_user(client: TestClient) -> Generator[None, UserModel, None]:
    """Создать пользователя"""
    user_created: UserModel = create_user_by_model(client=client, user=generate_user())

    yield user_created

    client.delete(url=f'/api/users/{user_created.id}')

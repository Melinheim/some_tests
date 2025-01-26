from pytest import fixture

from routes.login import login_info_db


@fixture
def any_user_credentials():
    """Email и пароль для логина"""
    email, password = next(iter(login_info_db.items()))
    return {
        'email': email,
        'password': password
    }

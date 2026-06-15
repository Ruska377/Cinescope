import pytest

from config.hosts import BASE_URL_AUTH
from data.auth import AuthData
import requests
from models.base_models import RegisterUserResponse
from api.api_manager import ApiManager

def test_register_user(api_manager: ApiManager, registration_user_data):
    response = api_manager.auth_api.register_user(user_data=registration_user_data)
    register_user_response = RegisterUserResponse(**response.json())
    assert register_user_response.email == registration_user_data.email, "Email не совпадает"

"""------------------------------------------------------------------------------------------------"""


class TestAuthAPI:
    def test_register_user(self, api_manager: ApiManager, test_user):

        response = api_manager.auth_api.register_user(test_user)
        response_data = response.json()

        assert response_data["email"] == test_user.email, "Email не совпадает"
        assert "id" in response_data, "ID пользователя отсутствует в ответе"
        assert "roles" in response_data, "Роли пользователя отсутствуют в ответе"
        assert "USER" in response_data["roles"], "Роль USER должна быть у пользователя"

    @pytest.mark.skip(reason="Тест отключен")
    def test_register_and_login_user(self, api_manager: ApiManager, registered_user):
        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }
        response = api_manager.auth_api.login_user(login_data)
        response_data = response.json()

        assert "accessToken" in response_data, "Токен доступа отсутствует в ответе"
        assert response_data["user"]["email"] == registered_user["email"], "Email не совпадает"
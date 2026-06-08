from config.hosts import BASE_URL_AUTH
import requests
from data.auth import AuthData
import pytest

pytestmark = pytest.mark.skip(reason="Тесты надо рефакторить")

class TestPositive:
    def test_login_user(self):
        login_data = AuthData.test_login_data()
        response = requests.post(url=f"{BASE_URL_AUTH}/login", json=login_data)

        assert response.status_code == 200, \
            f"Ожидали статус код 200, получили статус код {response.status_code}"

        response_data = response.json()
        assert "accessToken" in response_data
        assert isinstance(response_data["accessToken"], str)


class TestNegative:
    def test_login_user_invalid_data(self):
        login_data = AuthData.test_invalid_login_data()

        response = requests.post(url=f"{BASE_URL_AUTH}/login", json=login_data)

        assert response.status_code == 401, \
            f"Ожидали статус код 401, получили статус код {response.status_code}"


    def test_login_user_with_wrong_credentials(self):
        login_data = AuthData.test_wrong_login_data()

        response = requests.post(url=f"{BASE_URL_AUTH}/login", json=login_data)

        assert response.status_code == 401, \
            f"Ожидали статус код 401, получили статус код {response.status_code}"
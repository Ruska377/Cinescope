from config.hosts import BASE_URL_AUTH
from data.auth import AuthData
import requests


class TestPositive:
    def test_register_user(self, api_manager):
        user_data = AuthData.data_register_user()
        response = requests.post(url=f"{BASE_URL_AUTH}/register", json=user_data)

        assert response.status_code == 201,\
            f"Ожидали статус код 201, получили статус код {response.status_code}"

        created_user = response.json()

        assert isinstance(created_user['id'], str)
        assert isinstance(created_user['email'], str)
        assert created_user["email"] == user_data["email"]
        assert isinstance(created_user['fullName'], str)
        assert created_user["fullName"] == user_data["fullName"]
        assert isinstance(created_user['roles'], list)
        assert isinstance(created_user['verified'], bool)
        assert isinstance(created_user['createdAt'], str)
        assert isinstance(created_user['banned'], bool)


class TestNegative:
    def test_register_user_with_invalid_email(self):
        user_data = AuthData.data_register_user()
        user_data["email"] = 'dadaddad'
        response = requests.post(url=f"{BASE_URL_AUTH}/register", json=user_data)

        assert response.status_code == 400,\
            f"Ожидали статус код 400, получили статус код {response.status_code}"

    def test_register_user_with_duplicate_email(self):
        user_data = AuthData.data_register_user()
        requests.post(url=f"{BASE_URL_AUTH}/register", json=user_data)
        response = requests.post(url=f"{BASE_URL_AUTH}/register", json=user_data)

        assert response.status_code == 409,\
            f"Ожидали статус код 409, получили статус код {response.status_code}"
        assert "Пользователь с таким email уже зарегистрирован" in response.json()['message']

    def test_register_user_with_short_email(self):
        user_data = AuthData.data_register_user()
        user_data['email'] = "12@mail.ru"
        response = requests.post(url=f"{BASE_URL_AUTH}/register", json=user_data)

        assert response.status_code == 400,\
            f"Ожидали статус код 400, получили статус код {response.status_code}"

    def test_register_user_with_long_email(self):
        user_data = AuthData.data_register_user()
        user_data['email'] = "111111111111111111111111111111111111111111111111111@mail.ru"
        response = requests.post(url=f"{BASE_URL_AUTH}/register", json=user_data)

        assert response.status_code == 400,\
            f"Ожидали статус код 400, получили статус код {response.status_code}"

    def test_register_user_without_fullname(self):
        user_data = AuthData.data_register_user()
        del user_data['fullName']
        response = requests.post(url=f"{BASE_URL_AUTH}/register", json=user_data)

        assert response.status_code == 400,\
            f"Ожидали статус код 400, получили статус код {response.status_code}"

    def test_register_user_with_short_password(self):
        user_data = AuthData.data_register_user()
        user_data['password'] = "12"
        user_data['passwordRepeat'] = "12"
        response = requests.post(url=f"{BASE_URL_AUTH}/register", json=user_data)

        assert response.status_code == 400,\
            f"Ожидали статус код 400, получили статус код {response.status_code}"

        register_response = response.json()
        assert 'Пароль должен содержать хотя бы одну заглавную букву' in register_response["message"]
        assert 'Минимальная длина пароля 8 символов' in register_response["message"]

    def test_register_user_with_wrong_repeat_password(self):
        user_data = AuthData.data_register_user()
        user_data['password'] = "A12222"
        user_data['passwordRepeat'] = "AASdd12"
        response = requests.post(url=f"{BASE_URL_AUTH}/register", json=user_data)

        assert response.status_code == 400,\
            f"Ожидали статус код 400, получили статус код {response.status_code}"

        register_response = response.json()
        assert 'Пароли не совпадают' in register_response["message"]
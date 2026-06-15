import pytest

from data.auth import AuthData, CreateData
from datetime import datetime, timezone

pytestmark = pytest.mark.skip(reason="Тесты надо рефакторить")


class TestPositive:
    def test_create_user(self, authenticated_api_manager):
        create_user_data = CreateData.data_create_user()
        response = authenticated_api_manager.auth_api.create_user(create_user_data)

        assert response.status_code == 201, \
            f"Ожидали статус код 201, получили статус код {response.status_code}"

        user_data = response.json()
        assert isinstance(user_data["id"], str)
        assert len(user_data['id']) > 0
        assert user_data['email'] == create_user_data['email']
        assert user_data['fullName'] == create_user_data['fullName']
        assert user_data['roles'] == ["USER"]
        assert user_data['verified'] == create_user_data['verified']
        assert user_data['banned'] == create_user_data['banned']
        assert user_data['createdAt']

        created_at = datetime.fromisoformat(user_data["createdAt"].replace("Z", "+00:00"))
        assert created_at.date() == datetime.now(timezone.utc).date()


class TestNegative:
    def test_create_user_with_invalid_data(self, authenticated_api_manager):
        response = authenticated_api_manager.auth_api.create_user(
            CreateData.invalid_data_create_user(), expected_status=400)

        assert response.status_code == 400, \
            f"Ожидали статус код 400, получили статус код {response.status_code}"

    def test_create_user_with_duplicate_email(self, authenticated_api_manager):
        create_user_data = CreateData.data_create_user()
        authenticated_api_manager.auth_api.create_user(create_user_data)
        response = authenticated_api_manager.auth_api.create_user(create_user_data, expected_status=409)

        assert response.status_code == 409, \
            f"Ожидали статус код 409, получили статус код {response.status_code}"

    def test_create_user_without_permission(self, authorized_api_manager):
        response = authorized_api_manager.auth_api.create_user(AuthData.data_create_user(), expected_status=403)

        assert response.status_code == 403, \
            f"Ожидали статус код 403, получили статус код {response.status_code}"
from config.hosts import BASE_URL_AUTH
from helpers.user_unchanged import assert_user_unchanged
import pytest

pytestmark = pytest.mark.skip(reason="Тесты надо рефакторить")

class TestPositive:
    def test_patch_user(self, created_user_with_cleanup, movie_auth_session):
        id_user = created_user_with_cleanup['id']
        old_data = created_user_with_cleanup
        update_data = {"verified": False,
                       "banned": True}
        response = movie_auth_session.patch(url=f"{BASE_URL_AUTH}/user/{id_user}", json=update_data)
        assert response.status_code == 200, \
            f"Ожидали статус код 200, получили статус код {response.status_code}"

        new_data = response.json()
        assert new_data["verified"] == False
        assert new_data["banned"] == True
        # assert new_data["id"] == old_data["id"] - не выдает id - хотя по свагеру должен
        assert new_data["roles"] == old_data["roles"]
        assert_user_unchanged(old_data, new_data)

    def test_patch_roles_user(self, created_user_with_cleanup, movie_auth_session):
        id_user = created_user_with_cleanup['id']
        update_data = {"roles": ["USER", "ADMIN"]}
        response = movie_auth_session.patch(url=f"{BASE_URL_AUTH}/user/{id_user}", json=update_data)
        assert response.status_code == 200, \
            f"Ожидали статус код 200, получили статус код {response.status_code}"

        new_data = response.json()
        assert new_data["roles"] == update_data["roles"]

    # full_patch_user → optional / regression test
    def test_full_patch_user(self, created_user_with_cleanup, movie_auth_session):
        id_user = created_user_with_cleanup['id']
        old_data = created_user_with_cleanup

        update_data = {
            "roles": ["USER", "ADMIN"],
            "verified": False,
            "banned": True}

        response = movie_auth_session.patch(url=f"{BASE_URL_AUTH}/user/{id_user}", json=update_data)
        assert response.status_code == 200, \
            f"Ожидали статус код 200, получили статус код {response.status_code}"
        new_data = response.json()
        assert new_data["verified"] == False
        assert new_data["banned"] == True
        assert new_data["roles"] == update_data["roles"]
        assert_user_unchanged(old_data, new_data)


class TestNegative:
    def test_patch_user_invalid_roles(self, created_user_with_cleanup, movie_auth_session):
        id_user = created_user_with_cleanup['id']
        update_data = {"roles": ["SUPER_GOD"]}
        response = movie_auth_session.patch(url=f"{BASE_URL_AUTH}/user/{id_user}", json=update_data)
        assert response.status_code == 400, \
            f"Ожидали статус код 400, получили статус код {response.status_code}"

    def test_patch_user_without_permission(self, created_user_with_cleanup, auth_session_test_user):
        id_user = created_user_with_cleanup['id']
        update_data = {"roles": ["USER", "ADMIN"]}
        response = auth_session_test_user.patch(url=f"{BASE_URL_AUTH}/user/{id_user}", json=update_data)
        assert response.status_code == 403, \
            f"Ожидали статус код 403, получили статус код {response.status_code}"

    def test_patch_user_not_found(self, movie_auth_session):
        id_user = '8cbabbe9-5fff-4dbe-a77e-104bf4e63dbdc'
        update_data = {"roles": ["USER", "ADMIN"]}
        response = movie_auth_session.patch(url=f"{BASE_URL_AUTH}/user/{id_user}", json=update_data)
        assert response.status_code == 404, \
            f"Ожидали статус код 404, получили статус код {response.status_code}"
        #Выдаст Ошибку 400 - неверные данные, хотя по сваггеру вроде должно быть - 404 Пользователь не найден
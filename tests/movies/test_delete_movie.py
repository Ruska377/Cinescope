import pytest

from conftest import super_admin, common_user
import allure

@allure.epic("Cinescop")
@allure.feature("movie_api")
@allure.story("DELETE_movie")
class TestPositive:
    @allure.title("Тест на удаление фильма")
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_delete_movie(self, created_movie_with_cleanup, super_admin):
        movie_id = created_movie_with_cleanup["id"]
        delete_movie = super_admin.api.movies_api.delete_movie(movie_id)

        assert delete_movie.status_code == 200, \
            f"Ожидали статус код 200, получили статус код {delete_movie.status_code}"

    @allure.title("Тест на удаление фильма с параметризацией")
    @pytest.mark.positive
    @pytest.mark.slow
    @pytest.mark.parametrize("role,expected_status", [("super_admin", 200), ("common_user", 403)], indirect=["role"])
    def test_delete_movie(self, created_movie_with_cleanup, role, expected_status):
        movie_id = created_movie_with_cleanup["id"]
        delete_movie = role.api.movies_api.delete_movie(movie_id, expected_status=expected_status)

@allure.epic("Cinescop")
@allure.feature("movie_api")
@allure.story("DELETE_movie")
class TestNegative:
    @allure.title("Тест: Попытка удаления фильма, ID которого нет в базе")
    @pytest.mark.negative
    @pytest.mark.slow
    def test_delete_movie_twice_return_not_found(self, created_movie_with_cleanup, super_admin):
        movie_id = created_movie_with_cleanup["id"]
        delete_movie = super_admin.api.movies_api.delete_movie(movie_id)
        assert delete_movie.status_code == 200, \
            f"Ожидали статус код 200, получили статус код {delete_movie.status_code}"

        delete_movie = super_admin.api.movies_api.delete_movie(movie_id, expected_status=404)
        assert delete_movie.status_code == 404, \
            f"Ожидали статус код 404, получили статус код {delete_movie.status_code}"

    @allure.title("Попытка удаления фильма без авторизации")
    @pytest.mark.negative
    def test_delete_movie_not_auth(self, created_movie_with_cleanup, non_auth_api_manager):
        movie_id = created_movie_with_cleanup["id"]

        delete_movie = non_auth_api_manager.movies_api.delete_movie(movie_id, expected_status=401)
        assert delete_movie.status_code == 401, \
            f"Ожидали статус код 401, получили статус код {delete_movie.status_code}"


from data.movies import MoviesData
import pytest
import allure

@allure.epic("Cinescop")
@allure.feature("movie_api")
@allure.story("PATCH_movie")
class TestPositive:
    @allure.title("Тест на частичное обновление данных фильма")
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_patch_movie(self, super_admin, created_movie_with_cleanup):
        id_created_movie = created_movie_with_cleanup['id']
        original_data = created_movie_with_cleanup
        updated_data = MoviesData.updated_data()
        patch_movie = super_admin.api.movies_api.patch_movie(id_created_movie, updated_data)

        assert patch_movie.status_code == 200, \
            f"Ожидали статус код 200, получил статус код {patch_movie.status_code}"

        new_data_movie = patch_movie.json()
        assert new_data_movie["name"] == updated_data["name"]
        assert new_data_movie["price"] == updated_data["price"]

        for key in original_data:
            if key not in updated_data:
                assert new_data_movie[key] == original_data[key]

        get_movie = super_admin.api.movies_api.get_movie(id_created_movie)

        get_new_data_movie  = get_movie.json()
        assert get_new_data_movie["name"] == updated_data["name"]
        assert get_new_data_movie["price"] == updated_data["price"]

        for key in original_data:
            if key not in updated_data:
                assert original_data[key] == get_new_data_movie[key]

@allure.epic("Cinescop")
@allure.feature("movie_api")
@allure.story("PATCH_movie")
class TestNegative:
    @allure.title("Тест: попытка обновить фильм, отправляя невалидные данные")
    @allure.title("")
    @pytest.mark.negative
    def test_patch_movie_with_invalid_data(self, super_admin, created_movie_with_cleanup):
        id_created_movie = created_movie_with_cleanup['id']
        updated_data = {"name": True, "price": -999}
        patch_movie = super_admin.api.movies_api.patch_movie(id_created_movie, updated_data, expected_status=400)

        assert patch_movie.status_code == 400, \
            f"Ожидали статус код 400, получил статус код {patch_movie.status_code}"
        # Можно добавить тест на сообщение об ошибке?

    @allure.title("Попытка обновить данные у не существующего фильма")
    @pytest.mark.negative
    def test_patch_movie_not_found(self, super_admin, created_movie_with_cleanup):
        id_created_movie = created_movie_with_cleanup['id']
        updated_data = MoviesData.created_movie_data()
        super_admin.api.movies_api.delete_movie(id_created_movie)
        patch_movie = super_admin.api.movies_api.patch_movie(id_created_movie, updated_data, expected_status=404)

        assert  patch_movie.status_code == 404, \
            f"Ожидали статус код 404, получил статус код {patch_movie.status_code}"

        assert patch_movie.json()["message"] == "Фильм не найден"

    @allure.title("Попытка обновить данные фильма без авторизации")
    @pytest.mark.negative
    def test_patch_movie_not_auth(self, non_auth_api_manager, created_movie_with_cleanup):
        id_created_movie = created_movie_with_cleanup['id']
        updated_data = MoviesData.created_movie_data()
        patch_movie = non_auth_api_manager.movies_api.patch_movie(id_created_movie, updated_data, expected_status=401)

        assert patch_movie.status_code == 401, \
            f"Ожидали статус код 401, получил статус код {patch_movie.status_code}"

    @allure.title("Попытка обновления данных с неверным токеном")
    @pytest.mark.negative
    def test_patch_movie_with_wrong_token(self, created_movie_with_cleanup, auth_with_invalid_token_api_manager):
        id_created_movie = created_movie_with_cleanup['id']
        updated_data = MoviesData.created_movie_data()
        patch_movie = auth_with_invalid_token_api_manager.movies_api.patch_movie(id_created_movie, updated_data, expected_status=401)


        assert patch_movie.status_code == 401, \
            f"Ожидали статус код 401, получил статус код {patch_movie.status_code}"

    @allure.title("Попытка обновления данных фильма с пустым телом запроса")
    @pytest.mark.negative
    def test_patch_movie_with_empty_body(self, super_admin, created_movie_with_cleanup):
        id_created_movie = created_movie_with_cleanup['id']
        updated_data = {}
        patch_movie = super_admin.api.movies_api.patch_movie(id_created_movie, updated_data)

        assert patch_movie.status_code == 200, \
            f"Ожидали статус код 200, получил статус код {patch_movie.status_code}"

    @allure.title("Попытка обновить данные фильма, с отправкой в теле запроса неверного поля")
    @pytest.mark.negative
    def test_patch_movie_with_unknown_field(self, super_admin, created_movie_with_cleanup):
        id_created_movie = created_movie_with_cleanup['id']
        updated_data = {"name": "new name", "price": 999, 'unknown': 'field'}
        patch_movie = super_admin.api.movies_api.patch_movie(id_created_movie, updated_data, expected_status=400)

        assert patch_movie.status_code == 400, \
            f"Ожидали статус код 200 или 400, получил статус код {patch_movie.status_code}"
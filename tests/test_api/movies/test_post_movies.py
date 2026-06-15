import allure
from data.movies import MoviesData
import pytest
from PydanticExamples.pydentic_movies import Movie


@allure.epic("Cinescop")
@allure.feature("movie_api")
@allure.story("POST_movie")
class TestPositive:
    @allure.title("Тест на создания фильма")
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_created_movie(self, super_admin):
        with allure.step("Генерируем данные и создаем Фильм"):
            data = MoviesData.created_movie_data()
            created_movie = super_admin.api.movies_api.create_movie(data)

        assert created_movie.status_code == 201, \
            f'Ожидали статус код 201, получили статус код {created_movie.status_code}'

        with allure.step("Валидируем ответ через Pydentic модель"):
            Movie.model_validate(created_movie.json())

        with allure.step("Проверяем, что все данные отправленные в бэк при создание фильма, бэк нам вернул"):
            movie_data = created_movie.json()
            for key in data:
                assert data[key] == movie_data[key]

        with allure.step("Делаем Get запрос на получение созданного нами фильма"):
            get_movie = super_admin.api.movies_api.get_movie(movie_data['id'])
            assert get_movie.status_code == 200, \
                f"Ожидали статуc код 200 (фильм сохранился) получили статус код {get_movie.status_code}"


@allure.epic("Cinescop")
@allure.feature("movie_api")
@allure.story("POST_movie")
class TestNegative:
    @allure.title("Попытка создать фильма без авторизации")
    @pytest.mark.negative
    def test_create_movie_without_auth(self, non_auth_api_manager):
        data = MoviesData.created_movie_data()
        created_movie = non_auth_api_manager.movies_api.create_movie(data, expected_status=401)
        assert created_movie.status_code == 401, \
            f'Ожидали статус код 401, получили статус код {created_movie.status_code}'

    @allure.title("Попытка создать фильм с неверным токеном аутентификации")
    @pytest.mark.negative
    def test_create_movie_with_wrong_token(self, auth_with_invalid_token_api_manager):
        data = MoviesData.created_movie_data()
        created_movie = auth_with_invalid_token_api_manager.movies_api.create_movie(data, expected_status=401)

        assert created_movie.status_code == 401, \
            f'Ожидали статус код 401, получили статус код {created_movie.status_code}'

    @allure.title("Попытка создания дубликата фильма")
    @pytest.mark.negative
    def test_create_movie_with_duplicate_name(self, super_admin):
        data = MoviesData.created_movie_data()
        first_created_movie = super_admin.api.movies_api.create_movie(data)
        second_created_movie = super_admin.api.movies_api.create_movie(data, expected_status=409)

        assert second_created_movie.status_code == 409, \
            f'Ожидали статус код 409, получили статус код {second_created_movie.status_code}'

    @allure.title("Попытка создания фильма с невалидной локацией")
    @pytest.mark.negative
    def test_create_movie_with_wrong_location(self, super_admin):
        data = MoviesData.created_movie_data()
        data['location'] = "USA"
        created_movie = super_admin.api.movies_api.create_movie(data, expected_status=400)
        assert created_movie.status_code == 400, \
            f"Ожидали статус-код 400 (неверные параметры), получили статус-код {created_movie.status_code}"

    @allure.title("Попытка создать фильма не указывая его цену")
    @pytest.mark.negative
    def test_create_movie_without_price(self, super_admin):
        data = MoviesData.created_movie_data()
        del data['price']
        created_movie = super_admin.api.movies_api.create_movie(data, expected_status=400)
        assert created_movie.status_code == 400, \
            f"Ожидали статус-код 400 (неверные параметры), получили статус-код {created_movie.status_code}"

    @allure.title("Попытка создать фильм без прав доступа, авторизовавшись под ролью USER")
    @pytest.mark.negative
    @pytest.mark.slow
    def test_create_movie_with_forbidden(self, common_user):
        data = MoviesData.created_movie_data()
        created_movie = common_user.api.movies_api.create_movie(data, expected_status=403)

        assert created_movie.status_code == 403, \
            f'Ожидали статус код 403, получили статус код {created_movie.status_code}'


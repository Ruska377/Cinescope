import allure
from data.movies import MoviesData
from  PydanticExamples.pydentic_movies import GetMovie
import pytest

@allure.epic("Cinescop")
@allure.feature("movie_api")
@allure.story("GET_movie")
class TestPositive:
    @allure.title("Тест на получения фильма(с предварительным его созданием)")
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_created_and_get_movie(self, super_admin):
        with allure.step("Генерируем данные, создаем фильм, получаем его ID для дальнейшей проверки"):
            data = MoviesData.created_movie_data()
            created_movie = super_admin.api.movies_api.create_movie(data)

            assert created_movie.status_code == 201, \
                f'Ожидали статус код 201, получили статус код {created_movie.status_code}'

            movie_data = created_movie.json()
            movie_id = movie_data['id']

        with allure.step("Делаем GET запрос"):
            get_movie = super_admin.api.movies_api.get_movie(movie_id)

            assert get_movie.status_code == 200, \
                f'Ожидали статус код 200, получили статус код {get_movie.status_code}'

        with allure.step("Валидируем полученные данные с помощью Pydentic модели"):
            GetMovie.model_validate(get_movie.json())

        with allure.step("Проверяем, что все данные сгенерированные при создание фильма присутствуют"):
            get_movie_data = get_movie.json()
            for key in movie_data:
                assert movie_data[key] == get_movie_data[key]

@allure.epic("Cinescop")
@allure.feature("movie_api")
@allure.story("GET_movie")
class TestNegative:
    @allure.title("Попытка получить фильм вводя неверный ID")
    @pytest.mark.negative
    def test_get_movie_with_wrong_id(self, api_manager):
        get_movie = api_manager.movies_api.get_movie(12223, expected_status=404)
        assert get_movie.status_code == 404, \
            f'Ожидали статус код 404, получили статус код {get_movie.status_code}'
    #### Не обробатывает длинный айди или айди через буквы (dadad)


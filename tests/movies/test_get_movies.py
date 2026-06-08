import allure

from conftest import api_manager
from data.movies import MoviesData
import pytest
from PydanticExamples.pydentic_movies import Movies, MoviesResponse

@allure.epic("Cinescop")
@allure.feature("movie_api")
@allure.story("GET_movies")
class TestPositive:
    @allure.title("Тест на парсинг списка фильмов")
    @pytest.mark.smoke
    @pytest.mark.positive
    @pytest.mark.parametrize(
        "price_range,locations,genreId",
        [((1, 1000), ["MSK"], 1), ((100, 300), ["SPB"], 3), ((1000, 500000), ["MSK", "SPB"], 3)],
         ids=["First params", "Second params", "Third params"])
    def test_get_movies_with_locations(self, api_manager, price_range, locations, genreId):
        with allure.step("Генерируем данные для поиска фильмов"):
            data = MoviesData.search_data_movies()

        with allure.step("Параметризуем данные"):
            min_price, max_price = price_range
            data.update({
                "minPrice": min_price,
                "maxPrice": max_price,
                "genreId": genreId,
                "locations": locations
            })

        with allure.step("Валидируем данные через Pydentic model"):
            movies = Movies(**data)

        with allure.step("Отправляем запрос на бэкенд"):
            response = api_manager.movies_api.get_movies(movies)

        with allure.step("Проверяем статус код ответа"):
            assert response.status_code == 200, \
                f"Ожидали статус-код 200, а получили статус код {response.status_code}"

        with allure.step("Валидируем данные, которые вернул нам бэкенд"):
            response_model = MoviesResponse.model_validate(response.json())

        with allure.step("Проводим остальные проверки"):
            assert response_model.page == movies.page
            assert response_model.pageSize == movies.pageSize

            for movie in response_model.movies:
                assert movies.minPrice <= movie.price <= movies.maxPrice
                assert movie.location in movies.locations
                assert movie.genreId == movies.genreId
                assert movie.published == movies.published

    @allure.title("Тест на сортировку при парсинге фильмов")
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_movies_sorted_by_created_at_asc(self, api_manager):
        data = MoviesData.search_data_movies()
        response = api_manager.movies_api.get_movies(data)

        response_data = response.json()
        dates = []
        for movie in response_data['movies']:
            dates.append(movie["createdAt"])
        assert dates == sorted(dates), \
            f'Фильмы отсортированы не верно по createdAt'

    @allure.title("Тест на парсинг фильмов без ввода в поле локации")
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_get_movies_without_locations(self, api_manager):
        data = MoviesData.search_data_movies_without_locations()
        response = api_manager.movies_api.get_movies(data)

        assert response.status_code == 200, \
            f"Ожидали статус-код 200, а получили статус код {response.status_code}"
        response_data = response.json()

        for movie in response_data['movies']:
            assert movie["location"] in ["MSK", "SPB"]


@allure.epic("Cinescop")
@allure.feature("movie_api")
@allure.story("GET_movies")
class TestNegative:
    @allure.title("Минимальная цена равна максимальной")
    @pytest.mark.negative
    def test_get_movies_min_price_equals_max_price(self, api_manager):
        data = MoviesData.search_data_movies()
        data['minPrice'] = data['maxPrice']
        response = api_manager.movies_api.get_movies(data, expected_status=400)

        assert response.status_code == 400, \
            f"Ожидали статус-код 400, а получили статус код {response.status_code}"
        response_data = response.json()

        assert response_data["message"] == "minPrice must be less than maxPrice"
        assert response_data["error"] == "Bad Request"
        assert response_data["statusCode"] == 400

    @allure.title("Минимальная цена имеет отрицательное значение")
    @pytest.mark.negative
    def test_get_movies_with_negative_min_price_(self, api_manager):
        data = MoviesData.search_data_movies()
        data['minPrice'] = -100
        response = api_manager.movies_api.get_movies(data, expected_status=400)

        assert response.status_code == 400, \
            f"Ожидали статус-код 400, а получили статус код {response.status_code}"

        error_body = response.json()
        assert "Поле minPrice имеет минимальную величину 0" in error_body['message']

    @allure.title("Минимальная цена выше Максимавльной")
    @pytest.mark.negative
    def test_get_movies_min_price_over_max_price(self, api_manager):
        data = MoviesData.search_data_movies()
        data['minPrice'] = data['maxPrice'] + 1
        response = api_manager.movies_api.get_movies(data, expected_status=400)

        assert response.status_code == 400, \
            f"Ожидали статус-код 400, а получили статус код {response.status_code}"
        response_data = response.json()

        assert response_data["message"] == "minPrice must be less than maxPrice"
        assert response_data["error"] == "Bad Request"
        assert response_data["statusCode"] == 400

    @allure.title("Поиск фильма с невалидной локацией")
    @pytest.mark.negative
    def test_get_movies_with_bad_location(self, api_manager):
        data = MoviesData.search_data_movies()
        data['locations'] = ["USA"]
        response = api_manager.movies_api.get_movies(data, expected_status=400)

        assert response.status_code == 400, \
            f"Ожидали статус-код 400, а получили статус код {response.status_code}"

    @allure.title("Поиск фильма с вводом невалидной цены")
    @pytest.mark.negative
    def test_get_movies_not_valid_price(self, api_manager):
        data = MoviesData.search_data_movies()
        data['minPrice'] = "abc"
        data['maxPrice'] =  "abcd"
        response = api_manager.movies_api.get_movies(data, expected_status=400)

        assert response.status_code == 400, \
            f"Ожидали статус-код 400, а получили статус код {response.status_code}"
        response_data = response.json()

        assert response_data["error"] == "Bad Request"
        assert response_data["statusCode"] == 400

    @allure.title("Парсинг фильмов с попыткой ввести отрицательное значение размера pageSize")
    @pytest.mark.negative
    def test_pagination_page_size_negative(self, api_manager):
        data = MoviesData.search_data_movies()
        data['pageSize'] = -5
        response = api_manager.movies_api.get_movies(data, expected_status=400)

        assert response.status_code == 400

    @allure.title("Попытка парсинга с вводом очень большого размера страницы")
    @pytest.mark.negative
    def test_pagination_pagesize_over_negative(self, api_manager):
        data = MoviesData.search_data_movies()
        data['pageSize'] = 999
        response = api_manager.movies_api.get_movies(data, expected_status=400)

        assert response.status_code == 400

    @allure.title("Попытка парсинга с вводом очень болього количества страниц")
    @pytest.mark.negative
    def test_pagination_page_over_pagelist_negative(self, api_manager):
        data = MoviesData.search_data_movies()
        data['page'] = 99999999
        response = api_manager.movies_api.get_movies(data, expected_status=200)
        assert response.status_code == 200
        # data['page'] = 9999999999999999999999 status_code = 400
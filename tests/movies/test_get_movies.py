from conftest import api_manager
from data.movies import MoviesData

class TestPositive:
    def test_get_movies_with_locations(self, api_manager):
        data = MoviesData.search_data_movies()
        response = api_manager.movies_api.get_movies(data)

        assert response.status_code == 200, \
            f"Ожидали статус-код 200, а получили статус код {response.status_code}"

        response_data = response.json()
        assert "movies" in response_data
        assert "count" in response_data
        assert "page" in response_data
        assert "pageSize" in response_data
        assert "pageCount" in response_data

        assert response_data['page'] == data['page']
        assert response_data['pageSize'] == data["pageSize"]

        assert isinstance(response_data["movies"], list)
        assert isinstance(response_data["count"], int)
        assert isinstance(response_data["page"], int)
        assert isinstance(response_data["pageSize"], int)
        assert isinstance(response_data["pageCount"], int)

        for movie in response_data['movies']:
            assert "id" in movie
            assert "name" in movie
            assert "price" in movie
            assert data["minPrice"] <= movie["price"] <= data["maxPrice"]
            assert "description" in movie
            assert "imageUrl" in movie
            assert "location" in movie
            assert isinstance(movie["location"], str)
            assert movie["location"] in data["locations"]
            assert "published" in movie
            assert movie["published"] == data["published"]
            assert "genreId" in movie
            assert movie["genreId"] == data['genreId']
            assert "genre" in movie
            assert isinstance(movie["genre"], dict)
            assert "name" in movie["genre"]
            assert "createdAt" in movie
            assert "rating" in movie


    def test_movies_sorted_by_created_at_asc(self, api_manager):
        data = MoviesData.search_data_movies()
        response = api_manager.movies_api.get_movies(data)

        response_data = response.json()
        dates = []
        for movie in response_data['movies']:
            dates.append(movie["createdAt"])
        assert dates == sorted(dates), \
            f'Фильмы отсортированы не верно по createdAt'


    def test_get_movies_without_locations(self, api_manager):
        data = MoviesData.search_data_movies_without_locations()
        response = api_manager.movies_api.get_movies(data)

        assert response.status_code == 200, \
            f"Ожидали статус-код 200, а получили статус код {response.status_code}"
        response_data = response.json()

        for movie in response_data['movies']:
            assert movie["location"] in ["MSK", "SPB"]


class TestNegative:
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

    def test_get_movies_with_negative_min_price_(self, api_manager):
        data = MoviesData.search_data_movies()
        data['minPrice'] = -100
        response = api_manager.movies_api.get_movies(data, expected_status=400)

        assert response.status_code == 400, \
            f"Ожидали статус-код 400, а получили статус код {response.status_code}"

        error_body = response.json()
        assert "Поле minPrice имеет минимальную величину 1" in error_body['message']

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

    def test_get_movies_with_bad_location(self, api_manager):
        data = MoviesData.search_data_movies()
        data['locations'] = ["USA"]
        response = api_manager.movies_api.get_movies(data, expected_status=400)

        assert response.status_code == 400, \
            f"Ожидали статус-код 400, а получили статус код {response.status_code}"

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

    def test_pagination_page_size_negative(self, api_manager):
        data = MoviesData.search_data_movies()
        data['pageSize'] = -5
        response = api_manager.movies_api.get_movies(data, expected_status=400)

        assert response.status_code == 400

    def test_pagination_pagesize_over_negative(self, api_manager):
        data = MoviesData.search_data_movies()
        data['pageSize'] = 999
        response = api_manager.movies_api.get_movies(data, expected_status=400)

        assert response.status_code == 400

    def test_pagination_page_over_pagelist_negative(self, api_manager):
        data = MoviesData.search_data_movies()
        data['page'] = 99999999
        response = api_manager.movies_api.get_movies(data, expected_status=200)
        assert response.status_code == 200
        # data['page'] = 9999999999999999999999 status_code = 400
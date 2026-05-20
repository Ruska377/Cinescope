from data.movies import MoviesData

class TestPositive:
    def test_created_movie(self, authenticated_api_manager):
        data = MoviesData.created_movie_data()
        created_movie = authenticated_api_manager.movies_api.create_movie(data)

        assert created_movie.status_code == 201, \
            f'Ожидали статус код 201, получили статус код {created_movie.status_code}'

        movie_data = created_movie.json()

        assert "id" in movie_data
        assert "name" in movie_data
        assert "price" in movie_data
        assert "description" in movie_data
        assert "imageUrl" in movie_data
        assert "location" in movie_data
        assert "published" in movie_data
        assert "genreId" in movie_data
        assert "genre" in movie_data
        assert "createdAt" in movie_data
        assert "rating" in movie_data

        for key in data:
            assert data[key] == movie_data[key]

        get_movie = authenticated_api_manager.movies_api.get_movie(movie_data['id'])
        assert get_movie.status_code == 200, \
            f"Ожидали статуc код 200 (фильм сохранился) получили статус код {get_movie.status_code}"


class TestNegative:
    def test_create_movie_without_auth(self, non_auth_api_manager):
        data = MoviesData.created_movie_data()
        created_movie = non_auth_api_manager.movies_api.create_movie(data, expected_status=401)
        assert created_movie.status_code == 401, \
            f'Ожидали статус код 401, получили статус код {created_movie.status_code}'

    def test_create_movie_with_wrong_token(self, auth_with_invalid_token_api_manager):
        data = MoviesData.created_movie_data()
        created_movie = auth_with_invalid_token_api_manager.movies_api.create_movie(data, expected_status=401)

        assert created_movie.status_code == 401, \
            f'Ожидали статус код 401, получили статус код {created_movie.status_code}'

    def test_create_movie_with_duplicate_name(self, authenticated_api_manager):
        data = MoviesData.created_movie_data()
        first_created_movie = authenticated_api_manager.movies_api.create_movie(data)
        second_created_movie = authenticated_api_manager.movies_api.create_movie(data, expected_status=409)

        assert second_created_movie.status_code == 409, \
            f'Ожидали статус код 409, получили статус код {second_created_movie.status_code}'

    def test_create_movie_with_wrong_location(self, authenticated_api_manager):
        data = MoviesData.created_movie_data()
        data['location'] = "USA"
        created_movie = authenticated_api_manager.movies_api.create_movie(data, expected_status=400)
        assert created_movie.status_code == 400, \
            f"Ожидали статус-код 400 (неверные параметры), получили статус-код {created_movie.status_code}"

    def test_create_movie_without_price(self, authenticated_api_manager):
        data = MoviesData.created_movie_data()
        del data['price']
        created_movie = authenticated_api_manager.movies_api.create_movie(data, expected_status=400)
        assert created_movie.status_code == 400, \
            f"Ожидали статус-код 400 (неверные параметры), получили статус-код {created_movie.status_code}"



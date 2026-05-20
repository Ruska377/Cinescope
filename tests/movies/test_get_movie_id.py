from data.movies import MoviesData


def test_created_and_get_movie(authenticated_api_manager):
    data = MoviesData.created_movie_data()
    created_movie = authenticated_api_manager.movies_api.create_movie(data)

    assert created_movie.status_code == 201, \
        f'Ожидали статус код 201, получили статус код {created_movie.status_code}'

    movie_data = created_movie.json()
    movie_id = movie_data['id']

    get_movie = authenticated_api_manager.movies_api.get_movie(movie_id)
    assert get_movie.status_code == 200, \
        f'Ожидали статус код 200, получили статус код {get_movie.status_code}'

    get_movie_data = get_movie.json()
    assert "id" in get_movie_data
    assert "name" in get_movie_data
    assert "price" in get_movie_data
    assert "description" in get_movie_data
    assert "imageUrl" in get_movie_data
    assert "location" in get_movie_data
    assert "published" in get_movie_data
    assert "genreId" in get_movie_data
    assert "createdAt" in get_movie_data
    assert "rating" in get_movie_data
    assert "reviews" in get_movie_data


    for key in movie_data:
        assert movie_data[key] == get_movie_data[key]

def test_get_movie_with_wrong_id(api_manager):
    get_movie = api_manager.movies_api.get_movie(12223, expected_status=404)
    assert get_movie.status_code == 404, \
        f'Ожидали статус код 404, получили статус код {get_movie.status_code}'

#### Не обробатывает длинный айди или айди через буквы (dadad)
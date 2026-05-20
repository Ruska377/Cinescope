class TestPositive:
    def test_delete_movie(self, created_movie_with_cleanup, authenticated_api_manager):
        movie_id = created_movie_with_cleanup["id"]
        delete_movie = authenticated_api_manager.movies_api.delete_movie(movie_id)

        assert delete_movie.status_code == 200, \
            f"Ожидали статус код 200, получили статус код {delete_movie.status_code}"


class TestNegative:
    def test_delete_movie_twice_return_not_found(self, created_movie_with_cleanup, authenticated_api_manager):
        movie_id = created_movie_with_cleanup["id"]
        delete_movie = authenticated_api_manager.movies_api.delete_movie(movie_id)
        assert delete_movie.status_code == 200, \
            f"Ожидали статус код 200, получили статус код {delete_movie.status_code}"

        delete_movie = authenticated_api_manager.movies_api.delete_movie(movie_id, expected_status=404)
        assert delete_movie.status_code == 404, \
            f"Ожидали статус код 404, получили статус код {delete_movie.status_code}"


    def test_delete_movie_not_auth(self, created_movie_with_cleanup, non_auth_api_manager):
        movie_id = created_movie_with_cleanup["id"]

        delete_movie = non_auth_api_manager.movies_api.delete_movie(movie_id, expected_status=401)
        #requests.delete(url=f"{BASE_URL}/movies/{movie_id}")
        assert delete_movie.status_code == 401, \
            f"Ожидали статус код 401, получили статус код {delete_movie.status_code}"
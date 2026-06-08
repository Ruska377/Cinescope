from custom_requester.custom_requester import CustomRequester
from config.hosts import BASE_URL, ENDPOINT_MOVIES

class MoviesAPI(CustomRequester):
    def __init__(self, session):
       super().__init__(session=session, base_url=BASE_URL)

    def get_movies(self, movies_data, expected_status=200):
        return self.send_request(
            method="GET",
            endpoint=ENDPOINT_MOVIES,
            params=movies_data,
            expected_status=expected_status
        )

    def create_movie(self, movie_data, expected_status=201):
        return self.send_request(
            method="POST",
            endpoint=ENDPOINT_MOVIES,
            data=movie_data,
            expected_status=expected_status
        )

    def get_movie(self, movie_id, expected_status=200):
        return self.send_request(
            method="GET",
            endpoint=f"{ENDPOINT_MOVIES}/{movie_id}",
            expected_status=expected_status
        )

    def delete_movie(self, movie_id, expected_status=200):
        return self.send_request(
            method="DELETE",
            endpoint=f"{ENDPOINT_MOVIES}/{movie_id}",
            expected_status=expected_status
        )

    def patch_movie(self, movie_id, movie_data, expected_status=200):
        return self.send_request(
            method="PATCH",
            endpoint=f"{ENDPOINT_MOVIES}/{movie_id}",
            data=movie_data,
            expected_status=expected_status
        )
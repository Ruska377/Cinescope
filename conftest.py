import  pytest
import requests
from data.movies import MoviesData
from data.auth import AuthData
from api.api_manager import ApiManager


@pytest.fixture(scope="session")
def session():
    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture(scope="session")
def api_manager(session):
    return ApiManager(session)

@pytest.fixture(scope="session")
def authenticated_api_manager(api_manager):
    api_manager.auth_api.authenticate(AuthData.admin_data())
    return api_manager

@pytest.fixture(scope="session")
def clear_auth_api_manager(api_manager):
    api_manager.auth_api.clear_auth()
    return api_manager

@pytest.fixture(scope="session")
def auth_with_invalid_token_api_manager():
    api_manager = ApiManager(requests.session())
    api_manager.auth_api.auth_with_invalid_token()
    return api_manager


@pytest.fixture(scope="session")
def authorized_api_manager(api_manager):
    api_manager.auth_api.authenticate(AuthData.user_data())
    return api_manager

@pytest.fixture(scope="session")
def created_movie(authenticated_api_manager):
    data = MoviesData.created_movie_data()
    return authenticated_api_manager.movies_api.create_movie(data).json()

@pytest.fixture
def created_movie_with_cleanup(api_manager):
    api_manager.auth_api.authenticate(AuthData.admin_data())
    data = MoviesData.created_movie_data()
    created_movie = api_manager.movies_api.create_movie(data)
    movie_id = created_movie.json()["id"]

    yield created_movie.json()

    # Пытаемся удалить, но игнорируем ошибку 404
    try:
        api_manager.auth_api.authenticate(AuthData.admin_data())
        response = api_manager.movies_api.delete_movie(movie_id)
        if response.status_code == 404:
            # Фильм уже удален - это нормально
            pass
    except Exception as e:
        print(f"Cleanup warning: {e}")

@pytest.fixture
def non_auth_api_manager():
    return ApiManager(requests.session())


"""========================================================================================================="""
# @pytest.fixture
# def created_user_with_cleanup(movie_auth_session):
#     create_user_data = AuthData.data_create_user()
#     response = movie_auth_session.post(url=f"{BASE_URL_AUTH}/user", json=create_user_data)
#     user_id = response.json()["id"]
#     yield response.json()
#     movie_auth_session.delete(url=f"{BASE_URL_AUTH}/user/{user_id}")



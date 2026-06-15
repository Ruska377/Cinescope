import pytest
from data.movies import MoviesData
import allure


@allure.epic("Cinescop")
@allure.feature("user_api")
@allure.story("create_user")
@allure.title("Тест создание юзера в БД")
@pytest.mark.smoke
@pytest.mark.positive
def test_db_requests(super_admin, db_helper, created_test_user):
    assert created_test_user == db_helper.get_user_by_id(created_test_user.id)
    assert db_helper.user_exists_by_email(created_test_user.email)


@allure.epic("Cinescop")
@allure.feature("movie_api")
@allure.story("DB_movies")
@allure.title("Тест на проверку появления и удаления фильма из БД после отправки запросов через API в Бэкенд")
@pytest.mark.smoke
@pytest.mark.positive
def test_db_movie(super_admin, db_helper):
    movie = MoviesData.created_movie_data()
    assert db_helper.get_movie_by_name(movie["name"]) is None

    created_test_movie = super_admin.api.movies_api.create_movie(movie).json()
    assert db_helper.get_movie_by_id(created_test_movie["id"]) is not None

    delete_movie = super_admin.api.movies_api.delete_movie(created_test_movie["id"])
    assert db_helper.get_movie_by_id(created_test_movie["id"]) is None




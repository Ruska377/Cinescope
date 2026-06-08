import  pytest
import requests
from data.movies import MoviesData
from data.auth import CreateData
from api.api_manager import ApiManager
from config.user_creds import SuperAdminCreds
from entities.user import User
from enums.roles import Roles
from data.data_generator import DataGenerator
from models.base_models import TestUser
from db_requester.db_client import get_db_session
from db_requester.db_herlpers import DBHelper


@pytest.fixture
def test_user() -> TestUser:
    random_password = DataGenerator.generate_random_password()

    return TestUser(
        email=DataGenerator.generate_random_email(),
        fullName=DataGenerator.generate_random_name(),
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER.value]
    )

@pytest.fixture
def registration_user_data(test_user):
    return test_user.model_copy()

@pytest.fixture(scope="session")
def session():
    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture(scope="session")
def api_manager(session):
    return ApiManager(session)

@pytest.fixture()
def auth_with_invalid_token_api_manager():
    session = requests.session()
    api_manager = ApiManager(session)
    api_manager.auth_api.auth_with_invalid_token()
    yield api_manager
    session.close()

@pytest.fixture
def created_movie_with_cleanup(super_admin):
    data = MoviesData.created_movie_data()
    created_movie = super_admin.api.movies_api.create_movie(data)
    movie_id = created_movie.json()["id"]

    yield created_movie.json()

    # Пытаемся удалить, но игнорируем ошибку 404
    try:
        response = super_admin.api.movies_api.delete_movie(movie_id)
        if response.status_code == 404:
            # Фильм уже удален - это нормально
            pass
    except Exception as e:
        print(f"Cleanup warning: {e}")

@pytest.fixture
def non_auth_api_manager():
    session = requests.session()
    yield ApiManager(session)
    session.close()


"""========================================================================================================="""


@pytest.fixture
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()

@pytest.fixture
def super_admin(user_session):
    new_session = user_session()

    super_admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        [Roles.SUPER_ADMIN.value],
        new_session)

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin


@pytest.fixture(scope="function")
def creation_user_data():
    return CreateData.creation_user_data()

@pytest.fixture
def creation_user_data_for_pydentic(test_user):
    return test_user.model_copy(update={
        "verified": True,
        "banned": False
    })


@pytest.fixture
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    common_user = User(
        creation_user_data['email'],
        creation_user_data['password'],
        list(Roles.USER.value),
        new_session)

    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user


@pytest.fixture
def admin_superadmin(user_session, super_admin, creation_user_data):
    new_session = user_session()

    admin_superadmin = User(
        creation_user_data['email'],
        creation_user_data['password'],
        [Roles.ADMIN.value, Roles.SUPER_ADMIN.value],
        new_session
    )

    response = super_admin.api.user_api.create_user(creation_user_data)
    user_id = response.json()['id']
    updated_data = {"roles": [Roles.ADMIN.value, Roles.SUPER_ADMIN.value]}
    super_admin.api.user_api.patch_user(updated_data, user_id)
    admin_superadmin.api.auth_api.authenticate(admin_superadmin.creds)
    return admin_superadmin

@pytest.fixture
def role(request, super_admin, common_user):
    if request.param == "super_admin":
        return super_admin
    if request.param == "common_user":
        return common_user


#----------- DB ------------------------
@pytest.fixture(scope="module")
def db_session():
    db_session = get_db_session()
    yield db_session
    db_session.close()

@pytest.fixture(scope="module")
def db_helper(db_session) -> DBHelper:
    db_helper = DBHelper(db_session)
    return db_helper

@pytest.fixture(scope="module")
def created_test_user(db_helper):
    user = db_helper.create_test_user(DataGenerator.generate_user_data())
    yield user
    if db_helper.get_user_by_id(user.id):
        db_helper.delete_user(user)


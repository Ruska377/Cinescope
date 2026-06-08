from faker import Faker
from enums.roles import Roles
from config.user_creds import SuperAdminCreds

fake = Faker(locale='en_US')

class AuthData:
    @staticmethod
    def admin_data():
        return {
            "email": SuperAdminCreds.USERNAME,
            "password":SuperAdminCreds.PASSWORD
        }

    @staticmethod
    def user_data():
        return {
            "email": "test@email.com",
            "password": "12345678Aa"
        }

    @staticmethod
    def data_register_user():
        password = "Test123!"

        return {
            "email": fake.unique.email(),
            "fullName": fake.name(),
            "password": password,
            "passwordRepeat": password
        }

    @staticmethod
    def test_invalid_login_data():
        return {
            "email": 123,
            "password": True
        }

    @staticmethod
    def test_wrong_login_data():
        return {
            "email": "123@mail.ru",
            "password":"wrongpassword"
        }

    @staticmethod
    def data_create_user():
        return {
            "fullName": fake.name(),
            "email": fake.unique.email(),
            "password": "Test1234",
            "verified": True,
            "banned": False
        }

class CreateData:
    @staticmethod
    def creation_user_data():
        return {
            "fullName": fake.name(),
            "email": fake.unique.email(),
            "password": "Test1234",
            "passwordRepeat": "Test1234",
            "roles": [Roles.USER.value],
            "verified": True,
            "banned": False
        }

    @staticmethod
    def invalid_data_create_user():
        return {
            "fullName": fake.name(),
            "email": fake.unique.email(),
            "password": "",
            "verified": True,
            "banned": False
        }

    @staticmethod
    def creation_admin_superadmin_user_data():
        return {
            "fullName": fake.name(),
            "email": fake.unique.email(),
            "password": "Test1234",
            "passwordRepeat": "Test1234",
            "roles": [Roles.ADMIN.value, Roles.SUPER_ADMIN.value],
            "verified": True,
            "banned": False
        }
from custom_requester.custom_requester import CustomRequester
from config.hosts import ENDPOINT_USER, ENDPOINT_LOGIN

class AuthAPI(CustomRequester):
    def __init__(self, session):
        super().__init__(session=session, base_url="https://auth.dev-cinescope.coconutqa.ru")

    def authenticate(self, user_creds):
        login_data = {
            "email": user_creds["email"],
            "password": user_creds["password"]
        }

        response = self.login_user(login_data).json()
        if "accessToken" not in response:
            raise KeyError("token is missing")

        token = response["accessToken"]
        self._update_session_headers(Authorization=f"Bearer {token}")

    def clear_auth(self):
        self.session.headers.pop("Authorization", None)
        self.headers.pop("Authorization", None)

    def auth_with_invalid_token(self):
        self._update_session_headers(Authorization=f"Bearer invalid.token.123")


    def register_user(self, user_data, expected_status=201):

        return self.send_request(
            method="POST",
            endpoint=ENDPOINT_USER,
            data=user_data,
            expected_status=expected_status
        )

    def login_user(self, login_data, expected_status=200):

        return self.send_request(
            method="POST",
            endpoint=ENDPOINT_LOGIN,
            data=login_data,
            expected_status=expected_status
        )

    def create_user(self, create_user_data, expected_status=201):

        return self.send_request(
            method="POST",
            endpoint=ENDPOINT_USER,
            data=create_user_data,
            expected_status=expected_status
        )
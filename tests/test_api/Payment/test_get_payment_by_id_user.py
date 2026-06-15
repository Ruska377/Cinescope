from config.hosts import BASE_URL_PAYMENT
from helpers.get_payment import assert_get_payment
import pytest

pytestmark = pytest.mark.skip(reason="Тесты надо рефакторить")

class TestPositive:
    def test_get_payments_by_user_id(self, movie_auth_session):
        user_id = 'd71554a6-f70b-4931-872d-19d897f50b23'
        response = movie_auth_session.get(url=f"{BASE_URL_PAYMENT}/user/{user_id}")
        assert response.status_code == 200, \
            f"Ожидали статус код 200, получили статус код {response.status_code}"

        payments = response.json()
        assert isinstance(payments, list)
        assert payments, "Payments list is empty"

        payment = payments[0]
        assert_get_payment(payment)

class TestNegative:
    def test_get_payments_by_user_id_not_found(self, movie_auth_session):
        user_id = 3
        response = movie_auth_session.get(url=f"{BASE_URL_PAYMENT}/user/{user_id}")
        assert response.status_code == 404, \
            f"Ожидали статус код 404, получили статус код {response.status_code}"
        response_data = response.json()
        assert response_data['message'] == "Пользователь не найден"
        assert response_data['error'] == "Not Found"

    def test_get_payments_by_user_id_forbidden(self, auth_session_test_user):
        user_id = 'd71554a6-f70b-4931-872d-19d897f50b23'
        response = auth_session_test_user.get(url=f"{BASE_URL_PAYMENT}/user/{user_id}")
        assert response.status_code == 403, \
            f"Ожидали статус код 403, получили статус код {response.status_code}"
        response_data = response.json()
        assert response_data['message'] == "Forbidden resource"
        assert response_data['error'] == "Forbidden"
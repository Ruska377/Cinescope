from config.hosts import BASE_URL_PAYMENT
from data.payment import PaymentData
import requests

class TestPositive:
    def test_create_payment(self, auth_session_test_user):
        data = PaymentData.payment_success_data()
        response = auth_session_test_user.post(url=f"{BASE_URL_PAYMENT}/create", json=data)
        assert response.status_code == 201, \
            f"Ожидали статус код 201, получили статус код {response.status_code}"
        response_data = response.json()
        assert response_data['status'] == "SUCCESS"


class TestNegative:
    def test_create_payment_invalid_card(self, auth_session_test_user):
        data = PaymentData.payment_data_invalid_card()
        response = auth_session_test_user.post(url=f"{BASE_URL_PAYMENT}/create", json=data)
        assert response.status_code == 400, \
            f"Ожидали статус код 400, получили статус код {response.status_code}"
        assert  response.json()["message"] == "Неверная карта"
        assert response.json()['error']['status'] == "INVALID_CARD"

    def test_create_payment_unauthorized(self):
        data = PaymentData.payment_success_data()
        response = requests.post(url=f"{BASE_URL_PAYMENT}/create", json=data)
        assert response.status_code == 401, \
            f"Ожидали статус код 401, получили статус код {response.status_code}"
        assert response.json()["message"] == "Unauthorized"

    def test_create_payment_movie_not_found(self, auth_session_test_user):
        data = PaymentData.payment_data_movie_not_found()
        response = auth_session_test_user.post(url=f"{BASE_URL_PAYMENT}/create", json=data)
        assert response.status_code == 404, \
            f"Ожидали статус код 404, получили статус код {response.status_code}"
        assert response.json()["message"] == "Фильм не найден"

    def test_create_payment_empty_body(self, auth_session_test_user):
        data = {}
        response = auth_session_test_user.post(url=f"{BASE_URL_PAYMENT}/create", json=data)
        assert response.status_code == 400, \
            f"Ожидали статус код 400, получили статус код {response.status_code}"
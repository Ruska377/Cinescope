from config.hosts import BASE_URL_PAYMENT
from helpers.get_payment import assert_get_payment
import requests
import pytest

pytestmark = pytest.mark.skip(reason="Тесты надо рефакторить")

def test_get_payments(auth_session_test_user):
    response = auth_session_test_user.get(url=f"{BASE_URL_PAYMENT}/user")
    assert response.status_code == 200, \
        f"Ожидали статус код 200, получили статус код {response.status_code}"

    payments = response.json()
    assert isinstance(payments, list)
    assert payments, "Payments list is empty"

    payment = payments[0]
    assert_get_payment(payment)


def test_get_payments_unauthorized():
    response = requests.get(url=f"{BASE_URL_PAYMENT}/user")
    assert response.status_code == 401, \
        f"Ожидали статус код 401, получили статус код {response.status_code}"
    assert response.json()['message'] == "Unauthorized"



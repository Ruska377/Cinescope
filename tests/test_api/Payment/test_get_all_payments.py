from config.hosts import BASE_URL_PAYMENT
from data.payment import PaymentData
import pytest

pytestmark = pytest.mark.skip(reason="Тесты надо рефакторить")

class TestPositive:
    def test_find_all_payments(self, movie_auth_session):
        data = PaymentData.find_all_user_payment_data()
        response = movie_auth_session.get(url=f"{BASE_URL_PAYMENT}/find-all", params=data)

        assert response.status_code == 200, \
            f"Ожидали статус-код 200, а получили статус код {response.status_code}"

        response_data = response.json()
        assert isinstance(response_data["payments"], list)
        assert isinstance(response_data['count'], int)
        assert isinstance(response_data['page'], int)
        assert response_data["page"] == data["page"]
        assert isinstance(response_data['pageSize'], int)
        assert response_data["pageSize"] == data["pageSize"]
        assert isinstance(response_data['pageCount'], int)

        for payment in response_data["payments"]:
            assert payment['status'] in ["SUCCESS", "INVALID_CARD", "ERROR"]

        payments = response_data["payments"]
        dates = [payment["createdAt"] for payment in payments]
        assert dates == sorted(dates)
        assert response_data["count"] >= len(payments)

    def test_find_all_payments_filter_by_status_success(self, movie_auth_session):
        data = PaymentData.find_all_user_payment_data()
        data['status'] = 'SUCCESS'
        response = movie_auth_session.get(url=f"{BASE_URL_PAYMENT}/find-all", params=data)
        response_data = response.json()
        payments = response_data['payments']
        for payment in payments:
            assert payment['status'] == data['status'], \
                f"Ожидали статус {data['status']}, получили статус {payment['status']}"

    def test_find_all_payments_filter_by_status_error(self, movie_auth_session):
        data = PaymentData.find_all_user_payment_data()
        data['status'] = 'ERROR'
        response = movie_auth_session.get(url=f"{BASE_URL_PAYMENT}/find-all", params=data)
        response_data = response.json()
        payments = response_data['payments']
        for payment in payments:
            assert payment['status'] == data['status'], \
                f"Ожидали статус {data['status']}, получили статус {payment['status']}"

    def test_find_all_payments_filter_by_status_invalid_card(self, movie_auth_session):
        data = PaymentData.find_all_user_payment_data()
        data['status'] = 'INVALID_CARD'
        response = movie_auth_session.get(url=f"{BASE_URL_PAYMENT}/find-all", params=data)
        response_data = response.json()
        payments = response_data['payments']
        for payment in payments:
            assert payment['status'] == data['status'], \
                f"Ожидали статус {data['status']}, получили статус {payment['status']}"


class TestNegative:
    def test_find_all_payments_with_empty_data(self, movie_auth_session):
        data = PaymentData.find_all_user_payment_with_invalid_data()
        response = movie_auth_session.get(url=f"{BASE_URL_PAYMENT}/find-all", params=data)

        assert response.status_code == 400, \
            f"Ожидали статус-код 400, а получили статус код {response.status_code}"
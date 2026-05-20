class PaymentData:
    @staticmethod
    def payment_success_data():
        return {
            "movieId": 4,
            "amount": 1,
            "card": {
                "cardNumber": "4242424242424242",
                "cardHolder": "John Doe",
                "expirationDate": "12/25",
                "securityCode": 123
            }
        }

    @staticmethod
    def payment_data_invalid_card():
        return {
            "movieId": 4,
            "amount": 1,
            "card": {
                "cardNumber": "1111111111111111",
                "cardHolder": "John Doe",
                "expirationDate": "12/25",
                "securityCode": 123
            }
        }

    @staticmethod
    def payment_data_movie_not_found():
        return {
            "movieId": 4122222222222222,
            "amount": 1,
            "card": {
                "cardNumber": "1111111111111111",
                "cardHolder": "John Doe",
                "expirationDate": "12/25",
                "securityCode": 123
            }
        }

    @staticmethod
    def find_all_user_payment_data():
        return {
            "page": 1,
            "pageSize": 10,
            "status":  "SUCCESS",
            "createdAt": "asc"
        }

    @staticmethod
    def find_all_user_payment_with_invalid_data():
        return {
            "page": '222',
            "pageSize": '222',
            "status":  True,
            "createdAt": "asc"
        }
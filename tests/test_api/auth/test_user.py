from models.base_models import RegisterUserResponse


class TestUser:
    def test_create_user(self, super_admin, creation_user_data_for_pydentic):
        response = super_admin.api.user_api.create_user(creation_user_data_for_pydentic)
        created_user_response = RegisterUserResponse(**response.json())
        assert created_user_response.email == creation_user_data_for_pydentic.email
        assert created_user_response.fullName == creation_user_data_for_pydentic.fullName
        assert created_user_response.roles == creation_user_data_for_pydentic.roles



    def test_get_user_by_locator(self, super_admin, creation_user_data_for_pydentic):
        response = super_admin.api.user_api.create_user(creation_user_data_for_pydentic)
        created_user = RegisterUserResponse(**response.json())
        response_by_id = super_admin.api.user_api.get_user(created_user.id).json()
        response_by_email = super_admin.api.user_api.get_user(creation_user_data_for_pydentic.email).json()

        assert response_by_id == response_by_email, "Содержание ответов должно быть идентичным"


    def test_get_user_by_id_common_user(self, common_user):
        common_user.api.user_api.get_user(common_user.email, expected_status=403)



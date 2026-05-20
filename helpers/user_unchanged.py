def assert_user_unchanged(old_data, new_data):
    assert old_data["email"] == new_data["email"]
    assert old_data["fullName"] == new_data["fullName"]
    assert old_data["createdAt"] == new_data["createdAt"]


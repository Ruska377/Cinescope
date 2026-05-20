def assert_get_payment(payment):
    assert isinstance(payment["id"], int)
    assert isinstance(payment["userId"], str)
    assert isinstance(payment["movieId"], int)
    assert isinstance(payment["total"], int)
    assert isinstance(payment["amount"], int)
    assert isinstance(payment["createdAt"], str)
    assert isinstance(payment["status"], str)
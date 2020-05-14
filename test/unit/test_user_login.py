# test/unit/test_user_login.py


def test_login_endpoint_dont_accept_get_calls(test_client, db_init):
    response = test_client.get("/login")
    assert response.status_code == 405
    assert b"The method is not allowed for the requested URL." in response.data
